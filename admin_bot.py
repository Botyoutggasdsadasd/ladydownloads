import logging

from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

import config
import db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in config.ADMIN_IDS:
            if update.message:
                await update.message.reply_text("⛔ You're not authorized to use this bot.")
            return
        return await func(update, context)
    return wrapper


@admin_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Admin panel\n\n"
        "/pending — list payment requests awaiting approval\n"
        "/setqr — reply to a QR photo with this command to set the payment QR\n"
        "/setcookies — reply to a cookies.txt file with this command to fix YouTube blocks\n"
        "/stats — usage stats\n"
        "/find <id or @username> — look up a user\n"
        "/extend <id> <free|premium2|premium5> <days> — set/extend a plan manually\n"
        "/ban <id> — restrict a user\n"
        "/unban <id> — remove restriction\n"
        "/broadcast <message> — message every user"
    )


@admin_only
async def pending_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reqs = db.list_pending_requests()
    if not reqs:
        await update.message.reply_text("No pending requests.")
        return
    lines = []
    for r in reqs:
        info = config.TIERS[r["tier_requested"]]
        lines.append(
            f"#{r['id']} — @{r['username'] or r['telegram_id']} → {info['label']} "
            f"(${info['price']}) — {r['created_at'][:16]}"
        )
    await update.message.reply_text(
        "Pending requests (approve/reject from the photo notification, or use "
        "/find <id> for details):\n\n" + "\n".join(lines)
    )


@admin_only
async def setqr_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    photo = None
    if msg.photo:
        photo = msg.photo[-1]
    elif msg.reply_to_message and msg.reply_to_message.photo:
        photo = msg.reply_to_message.photo[-1]

    if not photo:
        await msg.reply_text(
            "Send a QR code photo with the caption /setqr, or reply to a QR photo with /setqr."
        )
        return

    file = await context.bot.get_file(photo.file_id)
    import os
    path = os.path.join(config.QR_DIR, "qr.jpg")
    await file.download_to_drive(path)
    await msg.reply_text("✅ Payment QR code updated.")


@admin_only
async def setcookies_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    document = None
    if msg.document:
        document = msg.document
    elif msg.reply_to_message and msg.reply_to_message.document:
        document = msg.reply_to_message.document

    if not document:
        await msg.reply_text(
            "Send your exported cookies.txt as a file (document, not photo) with the "
            "caption /setcookies, or reply to that file with /setcookies.\n\n"
            "How to export: log into YouTube in a normal browser window, install a "
            "'cookies.txt' export extension (e.g. 'Get cookies.txt LOCALLY' for Chrome), "
            "click it while on youtube.com, and send the downloaded file here."
        )
        return

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(config.COOKIES_PATH)
    await msg.reply_text(
        "✅ Cookies updated — YouTube downloads should work again. "
        "If YouTube signs that account out, re-export and resend when needed."
    )


@admin_only
async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = db.get_stats()
    lines = [f"Total users: {s['total_users']}", f"Pending requests: {s['pending_requests']}", ""]
    for tier_key, info in config.TIERS.items():
        lines.append(f"{info['label']}: {s['by_tier'].get(tier_key, 0)}")
    await update.message.reply_text("\n".join(lines))


@admin_only
async def find_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /find <telegram_id or @username>")
        return
    row = db.find_user(context.args[0])
    if not row:
        await update.message.reply_text("No such user.")
        return
    await update.message.reply_text(
        f"ID: {row['telegram_id']}\nUsername: @{row['username']}\nTier: {row['tier']}\n"
        f"Expiry: {row['expiry_date']}\nToday's downloads: {row['daily_count']}\n"
        f"Banned: {bool(row['banned'])}"
    )


@admin_only
async def extend_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /extend <telegram_id> <free|premium2|premium5> <days>")
        return
    tg_id, tier, days = context.args
    if tier not in config.TIERS:
        await update.message.reply_text(f"Unknown tier. Choose from: {', '.join(config.TIERS)}")
        return
    expiry = db.set_user_tier(int(tg_id), tier, int(days))
    await update.message.reply_text(f"✅ User {tg_id} set to {tier}. Expiry: {expiry or 'N/A'}")

    try:
        bot = Bot(token=config.DOWNLOAD_BOT_TOKEN)
        info = config.TIERS[tier]
        note = f" until {expiry}" if expiry else ""
        await bot.send_message(
            chat_id=int(tg_id),
            text=f"🎉 Your plan is now {info['label']}{note}. Use /status to check details.",
        )
    except Exception:
        logger.exception("Could not notify user of manual extend")


@admin_only
async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ban <telegram_id>")
        return
    db.set_banned(int(context.args[0]), True)
    await update.message.reply_text("User banned.")


@admin_only
async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unban <telegram_id>")
        return
    db.set_banned(int(context.args[0]), False)
    await update.message.reply_text("User unbanned.")


@admin_only
async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    ids = db.list_all_user_ids()
    bot = Bot(token=config.DOWNLOAD_BOT_TOKEN)
    sent = 0
    for uid in ids:
        try:
            await bot.send_message(chat_id=uid, text=text)
            sent += 1
        except Exception:
            pass
    await update.message.reply_text(f"Broadcast sent to {sent}/{len(ids)} users.")


async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if update.effective_user.id not in config.ADMIN_IDS:
        await query.answer("Not authorized.", show_alert=True)
        return
    await query.answer()

    action, request_id = query.data.split("_")
    request_id = int(request_id)
    req = db.get_payment_request(request_id)
    if req is None or req["status"] != "pending":
        await query.edit_message_caption(caption=(query.message.caption or "") + "\n\n(Already handled)")
        return

    approve = action == "approve"
    db.resolve_payment_request(request_id, approve)

    bot = Bot(token=config.DOWNLOAD_BOT_TOKEN)
    if approve:
        expiry = db.set_user_tier(req["telegram_id"], req["tier_requested"])
        info = config.TIERS[req["tier_requested"]]
        try:
            await bot.send_message(
                chat_id=req["telegram_id"],
                text=(
                    f"🎉 Payment confirmed! You're now on {info['label']}.\n"
                    f"Valid until: {expiry}\nUse /status anytime to check."
                ),
            )
        except Exception:
            logger.exception("Could not notify user of approval")
        result_text = "✅ APPROVED"
    else:
        try:
            await bot.send_message(
                chat_id=req["telegram_id"],
                text="❌ Your payment could not be confirmed. Please contact support or try again.",
            )
        except Exception:
            logger.exception("Could not notify user of rejection")
        result_text = "❌ REJECTED"

    await query.edit_message_caption(caption=(query.message.caption or "") + f"\n\n{result_text}")


def main():
    db.init_db()
    if not config.ADMIN_BOT_TOKEN:
        raise SystemExit("Set the ADMIN_BOT_TOKEN env var first.")
    if not config.ADMIN_IDS:
        raise SystemExit("Set the ADMIN_IDS env var (your numeric Telegram id) first.")

    app = ApplicationBuilder().token(config.ADMIN_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pending", pending_cmd))
    app.add_handler(CommandHandler("setqr", setqr_cmd))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex(r"^/setqr"), setqr_cmd))
    app.add_handler(CommandHandler("setcookies", setcookies_cmd))
    app.add_handler(
        MessageHandler(filters.Document.ALL & filters.CaptionRegex(r"^/setcookies"), setcookies_cmd)
    )
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("find", find_cmd))
    app.add_handler(CommandHandler("extend", extend_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd))
    app.add_handler(CommandHandler("unban", unban_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    app.add_handler(CallbackQueryHandler(handle_approval, pattern=r"^(approve|reject)_\d+$"))

    logger.info("Admin bot starting...")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
