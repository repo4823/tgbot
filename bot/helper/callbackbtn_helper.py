import asyncio
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.update_db import update_database
from bot.modules.github import GitHub
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_callbackbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query # always updates whenever clicked a button
    user = update.effective_user
    chat = update.effective_chat

























    if chat.type == "private":
        collection_name = "users"
    elif chat.type in ["group", "supergroup"]:
        collection_name = "groups"
    else:
        collection_name = None
    
    if not collection_name:
        logger.error(f"There is no Collection name...")
        return

    async def popup(msg):
        await query.answer(msg, True)
    
    async def _check_whois():
        user_id = context.chat_data.get("user_id")
        if not user_id:
            error_msg = "Error: user_id not found!"
            await popup(error_msg)
            try:
                await query.message.delete()
            except Exception as e:
                logger.error(e)
            return False
        if user.id != user_id:
            await popup("Access Denied!")
            return False
        return True
    
    async def _update_local_data(collection_name, db_find, db_vlaue):
        chat_data = await MongoDB.find_one(collection_name, db_find, db_vlaue)
        await LOCAL_DATABASE.insert_data(collection_name, chat.id, chat_data)

    # youtube ------------------------------------------------------------------------ Youtube
    if data == "mp4":
        context.user_data["content_format"] = data

    elif data == "mp3":
        context.user_data["content_format"] = data
    
    # -------------------------------------------------------------- Group management
    elif data == "unpin_all":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        try:
            await bot.unpin_all_chat_messages(chat_id)
            await Message.send_msg(chat_id, "All pinned messages has been unpinned successfully!")
            await query.message.delete()
        except Exception as e:
            logger.error(e)
    
    elif data == "filters":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
        if not find_group:
            find_group = await MongoDB.find_one("groups", "chat_id", chat_id)
            if find_group:
                await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        filters = find_group.get("filters")
        msg = f"Chat filters -\n"
        if filters:
            for keyword in filters:
                msg += f"- {keyword}\n"
        else:
            msg += "- No filters"

        btn_name = ["Close"]
        btn_data = ["close"]
        btn = await Button.cbutton(btn_name, btn_data)
        await Message.edit_msg(update, msg, sent_msg, btn)
    
    # Group management ----------------------------------------------------------------- help starts
    elif data == "group_management":
        msg = ()

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "ai":
        msg = (
            
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "misc_func":
        msg = (
            
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "owner_func":
        msg = (
            
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "help_menu":
        db = await MongoDB.info_db()
        for i in db:
            if i[0] == "users":
                total_users = i[1]
                break
            else:
                total_users = "❓"
        
        active_status = await MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        msg = (
            f
        )

        btn_name_row1 = ["Group Management", "Artificial intelligence"]
        btn_data_row1 = ["group_management", "ai"]

        btn_name_row2 = ["misc", "Bot owner"]
        btn_data_row2 = ["misc_func", "owner_func"]

        btn_name_row3 = ["GitHub", "Close"]
        btn_data_row3 = ["github_stats", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)
    # ---------------------------------------------------------------------------- help ends
    # bot settings ------------------------------------------------------------- bsettings starts
    elif data == "bot_pic":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        bot_pic = await MongoDB.get_data(collection_name, "bot_pic")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "bot_pic"

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "welcome_img":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        welcome_img = await MongoDB.get_data(collection_name, "welcome_img")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "welcome_img"
        
        msg = (
            
        )

        btn_name_row1 = ["Yes", "No"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "images":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        images = await MongoDB.get_data(collection_name, "images")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "images"

        if images:
            if len(images) > 20:
                storage, counter = "", 0
                for image in images:
                    storage += f"{image},"
                    counter += 1
                    if counter == 20:
                        await Message.send_msg(user.id, f"{storage}")
                        storage, counter = "", 0
                await Message.send_msg(user.id, f"{storage}")
                images = "Value sent below!"
            else:
                storage, counter = "", 0
                for i in images:
                    counter += 1
                    if counter == len(images):
                        storage += f"{i}"
                    else:
                        storage += f"{i}, "
                images = storage
        
        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "support_chat":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        support_chat = await MongoDB.get_data(collection_name, "support_chat")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "support_chat"

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "server_url":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        server_url = await MongoDB.get_data(collection_name, "server_url")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "server_url"

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "sudo_users":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        sudo_users = await MongoDB.get_data(collection_name, "sudo_users")
        if sudo_users:
            storage, counter = "", 0
            for i in sudo_users:
                counter += 1
                if counter == len(sudo_users):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            sudo_users = storage

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "sudo_users"

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "shrinkme_api":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        shrinkme_api = await MongoDB.get_data(collection_name, "shrinkme_api")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "shrinkme_api"

        msg = (
           
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "omdb_api":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        omdb_api = await MongoDB.get_data(collection_name, "omdb_api")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "omdb_api"

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "weather_api":
        collection_name = "bot_docs"
        db_find = "_id"
        db_vlaue = await MongoDB.find(collection_name, db_find)
        weather_api = await MongoDB.get_data(collection_name, "weather_api")

        context.chat_data["collection_name"] = collection_name
        context.chat_data["db_find"] = db_find
        context.chat_data["db_vlaue"] = db_vlaue[0]
        context.chat_data["edit_data_name"] = "weather_api"

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    

    
    elif data == "restore_db":
        msg = (
            
        )

        btn_name_row1 = ["⚠ Restore Database"]
        btn_data_row1 = ["confirm_restore_db"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "confirm_restore_db":
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return

        await MongoDB.delete_all_doc("bot_docs")

        res = await update_database()
        _id = await MongoDB.find("bot_docs", "_id")
        bot_docs = await MongoDB.find_one("bot_docs", "_id", _id[0])
        await LOCAL_DATABASE.insert_data_direct("bot_docs", bot_docs)

        msg = "Database data has been restored successfully from <code>config.env</code>!" if res else "Something went wrong!"
        await Message.send_msg(chat_id, msg)

    elif data == "b_setting_menu":
        btn_name_row1 = ["Bot pic", "Welcome img"]
        btn_data_row1 = ["bot_pic", "welcome_img"]

        btn_name_row2 = ["Images", "Support chat"]
        btn_data_row2 = ["images", "support_chat"]

        btn_name_row3 = ["GitHub", "Server url", "Sudo"]
        btn_data_row3 = ["github_repo", "server_url", "sudo_users"]

        btn_name_row4 = ["Shrinkme API", "OMDB API", "Weather API"]
        btn_data_row4 = ["shrinkme_api", "omdb_api", "weather_api"]

        btn_name_row5 = ["⚠ Restore Settings", "Close"]
        btn_data_row5 = ["restore_db", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
        row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

        btn = row1 + row2 + row3 + row4 + row5
        
        await Message.edit_msg(update, "<u><b>Bot Settings</b></u>", sent_msg, btn)
    # ---------------------------------------------------------------------------- bsettings ends
    # chat setting -------------------------------------------------------------- Chat settings starts
    elif data == "lang":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        find_chat = await LOCAL_DATABASE.find_one(collection_name, chat.id)
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                await LOCAL_DATABASE.insert_data(collection_name, chat.id, find_chat)
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        lang = find_chat.get("lang")
        context.chat_data["edit_data_name"] = "lang"

        msg = (
            
        )

        btn_name_row1 = ["Language code's"]
        btn_url_row1 = ["https://telegra.ph/Language-Code-12-24"]

        btn_name_row2 = ["Edit Value"]
        btn_data_row2 = ["edit_value"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["c_setting_menu", "close"]

        row1 = await Button.ubutton(btn_name_row1, btn_url_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "auto_tr":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        auto_tr = find_chat.get("auto_tr")

        context.chat_data["edit_data_name"] = "auto_tr"

        msg = (
            
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "set_echo":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        echo = find_chat.get("echo")

        context.chat_data["edit_data_name"] = "echo"

        msg = (
            
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "welcome_msg":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        welcome_msg = find_chat.get("welcome_msg")

        context.chat_data["edit_data_name"] = "welcome_msg"

        msg = (
            
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Set custom message"]
        btn_data_row2 = ["set_custom_msg"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "set_custom_msg":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        custom_welcome_msg = find_chat.get("custom_welcome_msg")

        context.chat_data["edit_data_name"] = "custom_welcome_msg"

        msg = (
            
        )

        btn_name_row1 = ["Set default message", "Set custom message"]
        btn_data_row1 = ["remove_value", "edit_value"]

        btn_name_row2 = ["Text formatting"]
        btn_data_row2 = ["text_formats"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["welcome_msg", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "text_formats":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        msg = (
            
        )

        btn_name = ["Close"]
        btn_data = ["close"]
        
        btn = await Button.cbutton(btn_name, btn_data)
        
        await Message.send_msg(chat_id, msg, btn)

    elif data == "goodbye_msg":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        goodbye_msg = find_chat.get("goodbye_msg")

        context.chat_data["edit_data_name"] = "goodbye_msg"

        msg = (
            
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "antibot":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        antibot = find_chat.get("antibot")

        context.chat_data["edit_data_name"] = "antibot"

        msg = (
            
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "del_cmd":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = await LOCAL_DATABASE.find_one(collection_name, chat.id)
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        del_cmd = find_chat.get("del_cmd")

        context.chat_data["edit_data_name"] = "del_cmd"

        msg = (
            
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "log_channel":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        context.chat_data["edit_data_name"] = "log_channel"

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        log_channel = find_chat.get("log_channel")

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "links_behave":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        all_links = find_chat.get("all_links")
        allowed_links = find_chat.get("allowed_links")
        if allowed_links:
            storage, counter = "", 0
            for i in allowed_links:
                counter += 1
                if counter == len(allowed_links):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            allowed_links = storage

        msg = (
            
        )

        btn_name_row1 = ["All links", "Allowed links"]
        btn_data_row1 = ["all_links", "allowed_links"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "all_links":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        context.chat_data["edit_data_name"] = "all_links"

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        all_links = find_chat.get("all_links")

        msg = (
            
        )

        btn_name_row1 = ["Delete", "Convert", "Nothing"]
        btn_data_row1 = ["d_links", "c_links", "none_links"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["links_behave", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "allowed_links":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        context.chat_data["edit_data_name"] = "allowed_links"

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        allowed_links = find_chat.get("allowed_links")
        if allowed_links:
            storage, counter = "", 0
            for i in allowed_links:
                counter += 1
                if counter == len(allowed_links):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            allowed_links = storage

        msg = (
            
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["links_behave", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "d_links":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        collection_name = context.chat_data.get("collection_name") # set from main.py
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find") # set from main.py
        db_vlaue = context.chat_data.get("db_vlaue") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = "delete"

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")
            await _update_local_data(collection_name, db_find, db_vlaue)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat_id, f"Error: {e}")
    
    elif data == "c_links":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        collection_name = context.chat_data.get("collection_name") # set from main.py
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find") # set from main.py
        db_vlaue = context.chat_data.get("db_vlaue") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = "convert"

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")
            await _update_local_data(collection_name, db_find, db_vlaue)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat_id, f"Error: {e}")
    
    elif data == "none_links":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        collection_name = context.chat_data.get("collection_name") # set from main.py
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find") # set from main.py
        db_vlaue = context.chat_data.get("db_vlaue") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = None

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")
            await _update_local_data(collection_name, db_find, db_vlaue)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat_id, f"Error: {e}")
    
    elif data == "ai_status":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")

        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        ai_status = find_chat.get("ai_status")

        context.chat_data["edit_data_name"] = "ai_status"

        msg = (
            
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "c_setting_menu":
        access = await _check_whois()
        if not access:
            return
        
        collection_name = context.chat_data.get("collection_name")
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find")
        db_vlaue = context.chat_data.get("db_vlaue")
        
        try:
            find_chat = context.chat_data[collection_name]
        except Exception as e:
            logger.error(e)
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
            if find_chat:
                context.chat_data[collection_name] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        if collection_name == "db_group_data":
            title = find_chat.get("title")
            lang = find_chat.get("lang")

            echo = find_chat.get("echo")
            auto_tr = find_chat.get("auto_tr")
            welcome_msg = find_chat.get("welcome_msg")
            goodbye_msg = find_chat.get("goodbye_msg")
            antibot = find_chat.get("antibot")
            ai_status = find_chat.get("ai_status")
            del_cmd = find_chat.get("del_cmd")
            all_links = find_chat.get("all_links")
            allowed_links = find_chat.get("allowed_links")
            if allowed_links:
                storage, counter = "", 0
                for i in allowed_links:
                    counter += 1
                    if counter == len(allowed_links):
                        storage += f"{i}"
                    else:
                        storage += f"{i}, "
                allowed_links = storage

            log_channel = find_chat.get("log_channel")

            msg = (
                
            )

            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["lang", "auto_tr"]

            btn_name_row2 = ["Echo", "Anti bot"]
            btn_data_row2 = ["set_echo", "antibot"]

            btn_name_row3 = ["Welcome", "Goodbye"]
            btn_data_row3 = ["welcome_msg", "goodbye_msg"]

            btn_name_row4 = ["Delete cmd", "Log channel"]
            btn_data_row4 = ["del_cmd", "log_channel"]

            btn_name_row5 = ["Links", "AI"]
            btn_data_row5 = ["links_behave", "ai_status"]

            btn_name_row6 = ["Close"]
            btn_data_row6 = ["close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
            row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
            row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
            row6 = await Button.cbutton(btn_name_row6, btn_data_row6)

            btn = row1 + row2 + row3 + row4 + row5 + row6

        elif collection_name == "db_user_data":
            user_mention = find_chat.get("mention")
            lang = find_chat.get("lang")
            echo = find_chat.get("echo")
            auto_tr = find_chat.get("auto_tr")

            msg = (
                f
            )

            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["lang", "auto_tr"]

            btn_name_row2 = ["Echo", "Close"]
            btn_data_row2 = ["set_echo", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

        else:
            await query.message.delete()
            return
        
        await Message.edit_msg(update, msg, sent_msg, btn)
    # ---------------------------------------------------------------------------- chat settings ends
    # global ----------------------------------------------------------------- Global
    elif data == "edit_value":
        """
        chat_id --> main
        collection_name --> main / query data
        db_find --> main / query data
        db_vlaue --> main / query data
        edit_data_name --> from query data
        new_value --> from user
        del_msg_pointer -- optional
        edit_value_del_msg -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        collection_name = context.chat_data.get("collection_name") # set from main.py
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find") # set from main.py
        db_vlaue = context.chat_data.get("db_vlaue") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return
        
        del_msg_1 = await Message.send_msg(chat_id, "Now send a value:")
        context.chat_data["status"] = "editing"
        await asyncio.sleep(2)

        attempt = 0

        while attempt < 10:
            new_value = context.chat_data.get("new_value")
            attempt += 1
            await asyncio.sleep(1)
            if new_value:
                break

        context.chat_data["new_value"] = None

        try:
            del_msg_2 = context.chat_data.get("edit_value_del_msg_pointer")
            del_msg = [del_msg_1, del_msg_2]
            for delete in del_msg:
                await Message.del_msg(chat_id, delete)
        except Exception as e:
            logger.error(e)
        
        if not new_value:
            await popup("Timeout!")
            return
        
        # ------------------------------------------------ some exceptions
        
        elif edit_data_name in ["images", "allowed_links", "sudo_users"]:
            if "," in str(new_value):
                storage = []
                for value in new_value.split(","):
                    if edit_data_name in ["sudo_users"]: # int value
                        storage.append(int(value))
                    else:
                        storage.append(value)
                new_value = storage
            else:
                if edit_data_name in ["sudo_users"]: # int value
                    new_value = [int(new_value)]
                else:
                    new_value = [new_value]
        
        try:
            await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_name, new_value)
            if edit_data_name in ["images", "allowed_links"]:
                new_value = f"{len(new_value)} items"
            elif edit_data_name == "custom_welcome_msg":
                new_value = "Check in message..."
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")
            await _update_local_data(collection_name, db_find, db_vlaue)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "remove_value":
        """
        chat_id --> main
        collection_name --> main / query data
        db_find --> main / query data
        db_vlaue --> main / query data
        edit_data_name --> from query data
        del_msg_pointer -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        collection_name = context.chat_data.get("collection_name") # set from main.py
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find") # set from main.py
        db_vlaue = context.chat_data.get("db_vlaue") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = None

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")
            await _update_local_data(collection_name, db_find, db_vlaue)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "true":
        """
        chat_id --> main
        collection_name --> main / query data
        db_find --> main / query data
        db_vlaue --> main / query data
        edit_data_name --> from query data
        del_msg_pointer -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        collection_name = context.chat_data.get("collection_name") # set from main.py
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find") # set from main.py
        db_vlaue = context.chat_data.get("db_vlaue") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = True

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")
            await _update_local_data(collection_name, db_find, db_vlaue)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat_id, f"Error: {e}")
    
    elif data == "false":
        """
        chat_id --> main
        collection_name --> main / query data
        db_find --> main / query data
        db_vlaue --> main / query data
        edit_data_name --> from query data
        del_msg_pointer -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        collection_name = context.chat_data.get("collection_name") # set from main.py
        if not collection_name:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        db_find = context.chat_data.get("db_find") # set from main.py
        db_vlaue = context.chat_data.get("db_vlaue") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = False

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")
            await _update_local_data(collection_name, db_find, db_vlaue)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "close":
        access = await _check_whois()
        if access:
            try:
                chat_id = context.chat_data.get("chat_id")
                del_msg_pointer = context.chat_data.get("del_msg_pointer")
                await query.message.delete()
                await Message.del_msg(chat_id, del_msg_pointer)
            except Exception as e:
                logger.error(e)
