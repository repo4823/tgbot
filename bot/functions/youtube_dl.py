async def func_add_download_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    url = re_msg.text if re_msg else " ".join(context.args)

    if chat.type != "private":
        _bot_info = await bot.get_me()
        btn_name = ["Start me in private"]
        btn_url = [f"http://t.me/{_bot_info.username}?start=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.reply_msg(update, f"Coming Soon...\nYou can use this feature in bot private chat!", btn)
        return
    
    if not url:
        await Message.reply_msg(update, "Use <code>/ytdl youtube_url</code> to download a video!")
        return
    
    youtube_domains = ["youtube.com", "youtu.be"]
    domain = await RE_LINK.get_domain(url)
    if domain not in youtube_domains:
        await Message.reply_msg(update, "Please send a valid youtube video link!")
        return
    
    btn_name_row1 = ["Video (mp4)", "Audio (mp3)"]
    btn_data_row1 = ["mp4", "mp3"]

    btn_name_row2 = ["Cancel"]
    btn_data_row2 = ["close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2)

    btn = row1 + row2

    del_msg = await Message.reply_msg(update, f"\nSelect <a href='{url}'>Content</a> Quality/Format", btn, disable_web_preview=False)

    timeout = 0

    while timeout < 15:
        content_format = context.user_data.get("content_format")
        timeout += 1
        await asyncio.sleep(1)
        if content_format:
            context.user_data["content_format"] = None
            break
    
    await Message.del_msg(chat.id, del_msg)

    if not content_format:
        await Message.reply_msg(update, "Timeout!")
        return
    
    asyncio.create_task(_func_ytdl(update, url, content_format))


async def _func_ytdl(update: Update, url, content_format):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message

    sent_msg = await Message.reply_msg(update, "📥 Downloading...")
    res = await YouTubeDownload.ytdl(url, content_format)

    if res[0] == 0:
        await Message.edit_msg(update, res[1], sent_msg)
        return
    
    await Message.edit_msg(update, "📤 Uploading...", sent_msg)

    try:
        if content_format == "mp4":
            title, file_path, thumbnail = res
            await Message.send_vid(chat.id, file_path, thumbnail, title, e_msg.id)
        elif content_format == "mp3":
            title, file_path = res
            await Message.send_audio(chat.id, file_path, title, title, e_msg.id)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error Uploading: {e}", sent_msg)

    try:
        if len(res) == 3:
            rem_files = [res[1], res[2]]
        else:
            rem_files = [res[1]]
        for rem in rem_files:
            os.remove(rem)
            logger.info(f"{rem} Removed...")
        await Message.del_msg(chat.id, sent_msg)
    except Exception as e:
        logger.error(e)