import asyncio
import logging

import db
import download_bot
import admin_bot
import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def run():
    db.init_db()

    dl_app = download_bot.ApplicationBuilder().token(config.DOWNLOAD_BOT_TOKEN).build()
    dl_app.add_handler(download_bot.CommandHandler("start", download_bot.start))
    dl_app.add_handler(download_bot.CommandHandler("status", download_bot.status_cmd))
    dl_app.add_handler(download_bot.CommandHandler("upgrade", download_bot.upgrade_cmd))
    dl_app.add_handler(download_bot.CommandHandler("quality", download_bot.quality_cmd))
    dl_app.add_handler(download_bot.CommandHandler("language", download_bot.language_cmd))
    dl_app.add_handler(download_bot.CallbackQueryHandler(download_bot.language_choice, pattern=r"^lang_"))
    dl_app.add_handler(download_bot.CallbackQueryHandler(download_bot.plan_choice, pattern=r"^plan_"))
    dl_app.add_handler(
        download_bot.CallbackQueryHandler(download_bot.set_default_choice, pattern=r"^setdefault_")
    )
    dl_app.add_handler(
        download_bot.CallbackQueryHandler(
            download_bot.handle_quality_choice, pattern=r"^(video_|audio_mp3|locked_)"
        )
    )
    dl_app.add_handler(download_bot.MessageHandler(download_bot.filters.PHOTO, download_bot.handle_photo))
    dl_app.add_handler(
        download_bot.MessageHandler(
            download_bot.filters.TEXT & ~download_bot.filters.COMMAND, download_bot.handle_link
        )
    )

    ad_app = admin_bot.ApplicationBuilder().token(config.ADMIN_BOT_TOKEN).build()
    ad_app.add_handler(admin_bot.CommandHandler("start", admin_bot.start))
    ad_app.add_handler(admin_bot.CommandHandler("pending", admin_bot.pending_cmd))
    ad_app.add_handler(admin_bot.CommandHandler("setqr", admin_bot.setqr_cmd))
    ad_app.add_handler(
        admin_bot.MessageHandler(admin_bot.filters.PHOTO & admin_bot.filters.CaptionRegex(r"^/setqr"), admin_bot.setqr_cmd)
    )
    ad_app.add_handler(admin_bot.CommandHandler("setcookies", admin_bot.setcookies_cmd))
    ad_app.add_handler(
        admin_bot.MessageHandler(
            admin_bot.filters.Document.ALL & admin_bot.filters.CaptionRegex(r"^/setcookies"),
            admin_bot.setcookies_cmd,
        )
    )
    ad_app.add_handler(admin_bot.CommandHandler("stats", admin_bot.stats_cmd))
    ad_app.add_handler(admin_bot.CommandHandler("find", admin_bot.find_cmd))
    ad_app.add_handler(admin_bot.CommandHandler("extend", admin_bot.extend_cmd))
    ad_app.add_handler(admin_bot.CommandHandler("ban", admin_bot.ban_cmd))
    ad_app.add_handler(admin_bot.CommandHandler("unban", admin_bot.unban_cmd))
    ad_app.add_handler(admin_bot.CommandHandler("broadcast", admin_bot.broadcast_cmd))
    ad_app.add_handler(
        admin_bot.CallbackQueryHandler(admin_bot.handle_approval, pattern=r"^(approve|reject)_\d+$")
    )

    async with dl_app, ad_app:
        await dl_app.start()
        await dl_app.updater.start_polling()
        await ad_app.start()
        await ad_app.updater.start_polling()
        print("Both bots are running. Press Ctrl+C to stop.")
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(run())
