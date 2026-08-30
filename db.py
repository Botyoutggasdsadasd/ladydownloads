import sqlite3
import datetime
import threading

from config import DB_PATH, TIERS, SUBSCRIPTION_DAYS

_lock = threading.Lock()


def _connect():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _lock, _connect() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                tier TEXT DEFAULT 'free',
                expiry_date TEXT,
                daily_count INTEGER DEFAULT 0,
                daily_date TEXT,
                banned INTEGER DEFAULT 0,
                language TEXT DEFAULT 'en',
                default_quality TEXT,
                created_at TEXT
            )"""
        )
        # Add columns for databases created before these features existed.
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
        if "language" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
        if "default_quality" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN default_quality TEXT")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS payment_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                username TEXT,
                tier_requested TEXT,
                amount REAL,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                resolved_at TEXT
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )"""
        )


def _today() -> str:
    return datetime.date.today().isoformat()


def get_or_create_user(telegram_id: int, username: str = "") -> sqlite3.Row:
    with _lock, _connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE telegram_id=?", (telegram_id,)
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO users (telegram_id, username, tier, daily_count, daily_date, created_at) "
                "VALUES (?, ?, 'free', 0, ?, ?)",
                (telegram_id, username, _today(), datetime.datetime.utcnow().isoformat()),
            )
            row = conn.execute(
                "SELECT * FROM users WHERE telegram_id=?", (telegram_id,)
            ).fetchone()
        elif username and row["username"] != username:
            conn.execute(
                "UPDATE users SET username=? WHERE telegram_id=?", (username, telegram_id)
            )
        return row


def _downgrade_if_expired(conn, user_row):
    """If a premium user's subscription has passed its expiry date, revert to free."""
    if user_row["tier"] != "free" and user_row["expiry_date"]:
        expiry = datetime.date.fromisoformat(user_row["expiry_date"])
        if expiry < datetime.date.today():
            conn.execute(
                "UPDATE users SET tier='free', expiry_date=NULL WHERE telegram_id=?",
                (user_row["telegram_id"],),
            )
            return True
    return False


def set_language(telegram_id: int, language: str):
    with _lock, _connect() as conn:
        conn.execute(
            "UPDATE users SET language=? WHERE telegram_id=?", (language, telegram_id)
        )


def set_default_quality(telegram_id: int, choice: str):
    with _lock, _connect() as conn:
        conn.execute(
            "UPDATE users SET default_quality=? WHERE telegram_id=?",
            (None if choice == "ask" else choice, telegram_id),
        )


def get_user_status(telegram_id: int) -> dict:
    """Refreshes daily counters/expiry, and returns a plain dict of current status."""
    with _lock, _connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE telegram_id=?", (telegram_id,)
        ).fetchone()
        if row is None:
            return None

        if _downgrade_if_expired(conn, row):
            row = conn.execute(
                "SELECT * FROM users WHERE telegram_id=?", (telegram_id,)
            ).fetchone()

        if row["daily_date"] != _today():
            conn.execute(
                "UPDATE users SET daily_count=0, daily_date=? WHERE telegram_id=?",
                (_today(), telegram_id),
            )
            row = conn.execute(
                "SELECT * FROM users WHERE telegram_id=?", (telegram_id,)
            ).fetchone()

        tier_info = TIERS[row["tier"]]
        return {
            "telegram_id": row["telegram_id"],
            "username": row["username"],
            "tier": row["tier"],
            "tier_label": tier_info["label"],
            "daily_limit": tier_info["daily_limit"],
            "max_height": tier_info["max_height"],
            "daily_count": row["daily_count"],
            "remaining": max(0, tier_info["daily_limit"] - row["daily_count"]),
            "expiry_date": row["expiry_date"],
            "banned": bool(row["banned"]),
            "language": row["language"] or "en",
            "default_quality": row["default_quality"],
        }


def increment_download_count(telegram_id: int):
    with _lock, _connect() as conn:
        conn.execute(
            "UPDATE users SET daily_count = daily_count + 1 WHERE telegram_id=?",
            (telegram_id,),
        )


def set_user_tier(telegram_id: int, tier: str, days: int = SUBSCRIPTION_DAYS):
    expiry = None
    if tier != "free":
        expiry = (datetime.date.today() + datetime.timedelta(days=days)).isoformat()
    with _lock, _connect() as conn:
        conn.execute(
            "UPDATE users SET tier=?, expiry_date=? WHERE telegram_id=?",
            (tier, expiry, telegram_id),
        )
    return expiry


def set_banned(telegram_id: int, banned: bool):
    with _lock, _connect() as conn:
        conn.execute(
            "UPDATE users SET banned=? WHERE telegram_id=?", (1 if banned else 0, telegram_id)
        )


def create_payment_request(telegram_id: int, username: str, tier_requested: str) -> int:
    amount = TIERS[tier_requested]["price"]
    with _lock, _connect() as conn:
        cur = conn.execute(
            "INSERT INTO payment_requests (telegram_id, username, tier_requested, amount, status, created_at) "
            "VALUES (?, ?, ?, ?, 'pending', ?)",
            (telegram_id, username, tier_requested, amount, datetime.datetime.utcnow().isoformat()),
        )
        return cur.lastrowid


def get_payment_request(request_id: int):
    with _lock, _connect() as conn:
        return conn.execute(
            "SELECT * FROM payment_requests WHERE id=?", (request_id,)
        ).fetchone()


def resolve_payment_request(request_id: int, approve: bool):
    status = "approved" if approve else "rejected"
    with _lock, _connect() as conn:
        conn.execute(
            "UPDATE payment_requests SET status=?, resolved_at=? WHERE id=?",
            (status, datetime.datetime.utcnow().isoformat(), request_id),
        )


def list_pending_requests():
    with _lock, _connect() as conn:
        return conn.execute(
            "SELECT * FROM payment_requests WHERE status='pending' ORDER BY created_at ASC"
        ).fetchall()


def get_stats():
    with _lock, _connect() as conn:
        total = conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]
        by_tier = conn.execute(
            "SELECT tier, COUNT(*) c FROM users GROUP BY tier"
        ).fetchall()
        pending = conn.execute(
            "SELECT COUNT(*) c FROM payment_requests WHERE status='pending'"
        ).fetchone()["c"]
        return {
            "total_users": total,
            "by_tier": {r["tier"]: r["c"] for r in by_tier},
            "pending_requests": pending,
        }


def find_user(identifier: str):
    """identifier can be a numeric telegram_id or a @username."""
    with _lock, _connect() as conn:
        if identifier.lstrip("-").isdigit():
            return conn.execute(
                "SELECT * FROM users WHERE telegram_id=?", (int(identifier),)
            ).fetchone()
        uname = identifier.lstrip("@")
        return conn.execute(
            "SELECT * FROM users WHERE username=?", (uname,)
        ).fetchone()


def list_all_user_ids():
    with _lock, _connect() as conn:
        rows = conn.execute("SELECT telegram_id FROM users WHERE banned=0").fetchall()
        return [r["telegram_id"] for r in rows]


def set_setting(key: str, value: str):
    with _lock, _connect() as conn:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )


def get_setting(key: str):
    with _lock, _connect() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row["value"] if row else None
