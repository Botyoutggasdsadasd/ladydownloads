STRINGS = {
    "en": {
        "welcome": (
            "👋 Send me a link from TikTok, YouTube, Facebook, Instagram, etc.\n"
            "I'll download it without watermark — choose video quality or MP3.\n\n"
            "Commands:\n"
            "/status — your plan, downloads left today, expiry\n"
            "/upgrade — get more downloads/day + higher quality\n"
            "/quality — set a default quality so I skip the menu next time\n"
            "/language — switch between English and Khmer"
        ),
        "choose_language": "🌐 Choose your language:",
        "language_set": "✅ Language set to English.",
        "status_lines": (
            "Plan: {tier_label}\n"
            "Downloads today: {daily_count}/{daily_limit} (remaining {remaining})\n"
            "Max quality: {max_height}p"
        ),
        "status_expiry": "Expires: {expiry_date}",
        "upgrade_choose_plan": "Choose a plan to upgrade to:",
        "plan_button": "{label} — {daily_limit}/day",
        "payment_caption": (
            "💳 {label}\n"
            "Amount: ${price} / month\n\n"
            "Scan the QR code above to pay, then send a screenshot of your payment "
            "confirmation right here in this chat. An admin will review and approve it."
        ),
        "payment_no_qr": "\n\n(No QR code has been set up yet — contact the admin.)",
        "proof_received": (
            "✅ Got your payment screenshot. Your upgrade is pending admin approval — "
            "you'll get a message here once it's confirmed."
        ),
        "invalid_link": "Please send a valid link, or use /upgrade or /status.",
        "banned": "Your account has been restricted. Contact the admin.",
        "quota_exceeded": (
            "⏳ You've used all {daily_limit} downloads for today on the "
            "{tier_label} plan. Use /upgrade for more, or come back tomorrow."
        ),
        "choose_quality": "Choose format/quality ({remaining}/{daily_limit} downloads left today):",
        "locked_alert": "🔒 That quality needs a higher plan. Use /upgrade to unlock it.",
        "link_expired": "This link expired — please send it again.",
        "out_of_downloads": "You're out of downloads for today. Use /upgrade for more.",
        "downloading": "Downloading… ⏳",
        "file_too_large": (
            "⚠️ File is {size_mb:.1f}MB — over the {max_mb}MB bot limit. Try a lower quality."
        ),
        "done": "Done ✅ ({remaining}/{daily_limit} downloads left today)",
        "failed": "❌ Failed to download: {error}",
        "audio_label": "🎵 Audio only (MP3)",
        "choose_default_quality": (
            "⚡ Pick a default quality. I'll skip the menu and download instantly with this "
            "choice next time. You can change it anytime with /quality."
        ),
        "default_quality_set": "✅ Default set to {label}. Just send a link and it'll download right away.",
        "default_always_ask": "✅ I'll show the quality menu every time again.",
        "always_ask_button": "🔁 Always ask me",
        "photo_post_detected": "🖼 This is a photo post ({count} photo{plural}). Downloading all of them…",
        "photo_ask_enhance": "Want me to sharpen/upscale these photos a bit before sending?",
        "enhance_yes": "✨ Yes, enhance",
        "enhance_no": "➡️ No, send as-is",
        "photo_sending": "📤 Sending {count} photo{plural}…",
        "photo_done": "Done ✅ — sent {count} photo{plural} ({remaining}/{daily_limit} downloads left today)",
        "too_many_requests": "⏳ Lots of downloads running right now — yours is queued, hang tight…",
        "download_timeout": "⏱️ That took too long and timed out. The source may be slow or blocking us — try again in a bit.",
    },
    "km": {
        "welcome": (
            "👋 ផ្ញើតំណវីដេអូពី TikTok, YouTube, Facebook, Instagram ជាដើមមកខ្ញុំ\n"
            "ខ្ញុំនឹងទាញយកជូនអ្នកដោយគ្មានស្លាកសញ្ញា (watermark) — អ្នកអាចជ្រើសរើសគុណភាព ឬ MP3។\n\n"
            "ពាក្យបញ្ជា៖\n"
            "/status — គម្រោង, ចំនួនទាញយកនៅសល់ថ្ងៃនេះ, ថ្ងៃផុតកំណត់\n"
            "/upgrade — ចង់ទាញយកបានច្រើនជាងមុន និងគុណភាពខ្ពស់ជាងមុន\n"
            "/quality — កំណត់គុណភាពលំនាំដើម ដើម្បីរំលងម៉ឺនុយលើកក្រោយ\n"
            "/language — ប្តូរភាសារវាងអង់គ្លេស និងខ្មែរ"
        ),
        "choose_language": "🌐 សូមជ្រើសរើសភាសា៖",
        "language_set": "✅ ភាសាត្រូវបានប្តូរទៅជាភាសាខ្មែរ។",
        "status_lines": (
            "គម្រោង៖ {tier_label}\n"
            "ទាញយកថ្ងៃនេះ៖ {daily_count}/{daily_limit} (នៅសល់ {remaining})\n"
            "គុណភាពខ្ពស់បំផុត៖ {max_height}p"
        ),
        "status_expiry": "ផុតកំណត់៖ {expiry_date}",
        "upgrade_choose_plan": "សូមជ្រើសរើសគម្រោងដែលចង់អាប់ដេត៖",
        "plan_button": "{label} — {daily_limit}/ថ្ងៃ",
        "payment_caption": (
            "💳 {label}\n"
            "តម្លៃ៖ ${price} / ខែ\n\n"
            "សូមស្កេន QR ខាងលើដើម្បីទូទាត់ បន្ទាប់មកផ្ញើរូបថតបញ្ជាក់ការទូទាត់មកកាន់ជជែកនេះ។ "
            "អ្នកគ្រប់គ្រងនឹងពិនិត្យ និងអនុម័តឲ្យអ្នក។"
        ),
        "payment_no_qr": "\n\n(មិនទាន់មាន QR កំណត់ទេ — សូមទាក់ទងអ្នកគ្រប់គ្រង។)",
        "proof_received": (
            "✅ ទទួលបានរូបថតបញ្ជាក់ការទូទាត់របស់អ្នកហើយ។ ការអាប់ដេតរបស់អ្នកកំពុងរង់ចាំការអនុម័តពីអ្នកគ្រប់គ្រង — "
            "អ្នកនឹងទទួលបានសារនៅទីនេះនៅពេលវាត្រូវបានបញ្ជាក់។"
        ),
        "invalid_link": "សូមផ្ញើតំណដែលត្រឹមត្រូវ ឬប្រើ /upgrade ឬ /status។",
        "banned": "គណនីរបស់អ្នកត្រូវបានដាក់កម្រិត។ សូមទាក់ទងអ្នកគ្រប់គ្រង។",
        "quota_exceeded": (
            "⏳ អ្នកបានប្រើអស់ចំនួន {daily_limit} ដងសម្រាប់ថ្ងៃនេះលើគម្រោង {tier_label} ។ "
            "ប្រើ /upgrade ដើម្បីទទួលបានច្រើនជាងនេះ ឬត្រឡប់មកវិញនៅថ្ងៃស្អែក។"
        ),
        "choose_quality": "សូមជ្រើសរើសទម្រង់/គុណភាព (នៅសល់ {remaining}/{daily_limit} ដងសម្រាប់ថ្ងៃនេះ)៖",
        "locked_alert": "🔒 គុណភាពនេះត្រូវការគម្រោងកម្រិតខ្ពស់ជាងនេះ។ ប្រើ /upgrade ដើម្បីដោះសោ។",
        "link_expired": "តំណនេះបានផុតកំណត់ — សូមផ្ញើម្តងទៀត។",
        "out_of_downloads": "អ្នកបានប្រើអស់ចំនួនទាញយកសម្រាប់ថ្ងៃនេះ។ ប្រើ /upgrade ដើម្បីទទួលបានច្រើនជាងនេះ។",
        "downloading": "កំពុងទាញយក… ⏳",
        "file_too_large": (
            "⚠️ ឯកសារមានទំហំ {size_mb:.1f}MB — លើសកម្រិត {max_mb}MB របស់ Bot។ សូមសាកល្បងគុណភាពទាបជាងនេះ។"
        ),
        "done": "ធ្វើរួចរាល់ ✅ (នៅសល់ {remaining}/{daily_limit} ដងសម្រាប់ថ្ងៃនេះ)",
        "failed": "❌ ទាញយកបរាជ័យ៖ {error}",
        "audio_label": "🎵 សំឡេងតែប៉ុណ្ណោះ (MP3)",
        "choose_default_quality": (
            "⚡ សូមជ្រើសរើសគុណភាពលំនាំដើម។ ខ្ញុំនឹងរំលងម៉ឺនុយ ហើយទាញយកភ្លាមៗជាមួយជម្រើសនេះនៅពេលក្រោយ។ "
            "អ្នកអាចប្តូរបានគ្រប់ពេលដោយប្រើ /quality។"
        ),
        "default_quality_set": "✅ កំណត់លំនាំដើមទៅជា {label}។ គ្រាន់តែផ្ញើតំណ វានឹងទាញយកភ្លាមៗ។",
        "default_always_ask": "✅ ខ្ញុំនឹងបង្ហាញម៉ឺនុយគុណភាពគ្រប់ពេលដដែល។",
        "always_ask_button": "🔁 សួរខ្ញុំរាល់ពេល",
        "photo_post_detected": "🖼 នេះជាការបង្ហោះរូបភាព ({count} រូប)។ កំពុងទាញយកទាំងអស់…",
        "photo_ask_enhance": "តើអ្នកចង់ឲ្យខ្ញុំធ្វើឲ្យរូបភាពច្បាស់/ធំជាងមុនបន្តិចមុននឹងផ្ញើទេ?",
        "enhance_yes": "✨ បាទ/ចាស៎ ធ្វើឲ្យប្រសើរ",
        "enhance_no": "➡️ ទេ ផ្ញើដូចដើម",
        "photo_sending": "📤 កំពុងផ្ញើរូបភាព {count}…",
        "photo_done": "ធ្វើរួចរាល់ ✅ — បានផ្ញើរូបភាព {count} (នៅសល់ {remaining}/{daily_limit} ដងសម្រាប់ថ្ងៃនេះ)",
        "too_many_requests": "⏳ ការទាញយកកំពុងដំណើរការច្រើនក្នុងពេលនេះ — សំណើររបស់អ្នកកំពុងរង់ចាំ…",
        "download_timeout": "⏱️ ការទាញយកនេះយូរពេក ហើយត្រូវបានផ្អាក។ សូមសាកល្បងម្តងទៀតក្រោយមួយសន្ទុះ។",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    lang = lang if lang in STRINGS else "en"
    template = STRINGS[lang].get(key) or STRINGS["en"].get(key, key)
    if kwargs:
        return template.format(**kwargs)
    return template
