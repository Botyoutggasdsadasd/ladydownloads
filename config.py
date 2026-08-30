import os

# --- Bot tokens (create two bots with @BotFather) ---
# SECURITY: no hardcoded fallback values here on purpose. A fallback baked into
# the source means anyone who reads this public repo has your live token. Set
# these as real environment variables (Railway Variables tab, systemd
# EnvironmentFile, etc). The bot refuses to start if they're missing — see
# the checks in download_bot.py / admin_bot.py main().
DOWNLOAD_BOT_TOKEN = os.environ.get("DOWNLOAD_BOT_TOKEN", "")
ADMIN_BOT_TOKEN = os.environ.get("ADMIN_BOT_TOKEN", "")

# Your personal Telegram numeric ID(s) - the only people allowed to use the admin bot.
# Get your ID by messaging @userinfobot on Telegram. Comma-separate for multiple admins.
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip()]

# On Railway, set DB_PATH and QR_DIR to paths inside your mounted Volume
# (e.g. /data/bot.db and /data/qr_codes) so they survive redeploys.
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "bot.db"))
QR_DIR = os.environ.get("QR_DIR", os.path.join(os.path.dirname(__file__), "qr_codes"))
os.makedirs(QR_DIR, exist_ok=True)

# Path to a Netscape-format cookies.txt file, used so yt-dlp can pass YouTube's
# bot-check on server IPs. Set via the admin bot's /setcookies command, or
# point this at a path inside your Railway volume (e.g. /data/cookies.txt).
COOKIES_PATH = os.environ.get(
    "COOKIES_PATH", os.path.join(os.path.dirname(__file__), "cookies.txt")
)

MAX_FILE_MB = 49  # Telegram bot upload limit

# --- Scaling / reliability knobs ---
# Caps how many yt-dlp downloads can run at the same time across all users.
# yt-dlp + ffmpeg are CPU/bandwidth heavy; without a cap, a burst of users
# (e.g. a link going viral in a group) can pile up processes and take the
# whole VPS down. Tune based on your server's CPU cores / RAM.
MAX_CONCURRENT_DOWNLOADS = int(os.environ.get("MAX_CONCURRENT_DOWNLOADS", "4"))

# How long a single yt-dlp extraction+download is allowed to run before it's
# killed and reported to the user as failed, instead of hanging forever and
# holding a concurrency slot.
DOWNLOAD_TIMEOUT_SECONDS = int(os.environ.get("DOWNLOAD_TIMEOUT_SECONDS", "180"))

# How many download attempts (with a short backoff) before giving up. Helps
# with transient TikTok/YouTube throttling instead of failing on one hiccup.
DOWNLOAD_MAX_RETRIES = int(os.environ.get("DOWNLOAD_MAX_RETRIES", "2"))

# Telegram allows up to 10 items per media group (album).
MAX_MEDIA_GROUP_SIZE = 10

# Lightweight, non-AI photo enhancement (sharpen + mild upscale via Pillow).
# This is NOT AI super-resolution — see README for the real-ESRGAN note if
# you want true AI upscaling later (needs a GPU-capable server).
ENABLE_PHOTO_ENHANCE = os.environ.get("ENABLE_PHOTO_ENHANCE", "true").lower() == "true"
PHOTO_ENHANCE_SCALE = float(os.environ.get("PHOTO_ENHANCE_SCALE", "1.5"))  # upscale factor

# --- Subscription tiers ---
# max_height controls which video qualities a tier is allowed to pick.
# price is in USD/month, shown to the user during /upgrade.
TIERS = {
    "free": {
        "label": "Free",
        "daily_limit": 5,
        "max_height": 720,
        "price": 0,
    },
    "premium2": {
        "label": "Premium ($2/mo)",
        "daily_limit": 10,
        "max_height": 1080,
        "price": 2,
    },
    "premium5": {
        "label": "Premium+ ($5/mo, 4K)",
        "daily_limit": 30,
        "max_height": 2160,
        "price": 5,
    },
}

SUBSCRIPTION_DAYS = 30  # length of one paid period

# Quality buttons shown to users, ordered high -> low.
# (internal_key, height, display_label)
QUALITY_OPTIONS = [
    ("4k", 2160, "🎬 4K (2160p)"),
    ("1080", 1080, "🎬 1080p"),
    ("720", 720, "🎬 720p"),
    ("480", 480, "🎬 480p"),
]
