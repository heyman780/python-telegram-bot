from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "7921369567:AAFOS9TLa1B_H3CGbGPvDKwAgwjiZqBdLRY"

admins = {}

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"مرحباً {user.first_name}! أنا Heman، بوت الحماية للمجموعة.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "قائمة الأوامر:\n"
        "/start - بدء البوت\n"
        "/help - عرض هذه القائمة\n"
        "/admin - إضافة نفسك كمشرف\n"
        "/setrules - تعيين قوانين المجموعة\n"
        "/rules - عرض قوانين المجموعة\n"
        "/warn - تحذير عضو\n"
        "/ban - حظر عضو\n"
        "/unban - إلغاء حظر عضو\n"
        "/kick - طرد عضو\n"
        "/members - عرض عدد الأعضاء\n"
        "/id - الحصول على IDك أو ID المجموعة\n"
        "/ping - فحص سرعة البوت"
    )

def set_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.text == "/setrules":
        update.message.reply_text("يرجى إرسال قوانين المجموعة التي ترغب في تعيينها.")
        return
    rules = update.message.text
    admins[chat_id] = {"rules": rules}
    update.message.reply_text("لقد تم حفظ قوانين المجموعة!")

def get_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in admins and "rules" in admins[chat_id]:
        update.message.reply_text(f"قوانين المجموعة:\n{admins[chat_id]['rules']}")
    else:
        update.message.reply_text("لم يتم تعيين قوانين المجموعة بعد.")

def admin(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id not in admins.get(chat_id, []):
        update.message.reply_text("عذرًا، ليس لديك إذن لاستخدام هذا الأمر.")
        return
    update.message.reply_text(
        "لوحة تحكم المشرف:\n"
        "/setrules - تعيين قوانين المجموعة\n"
        "/warn - تحذير عضو\n"
        "/ban - حظر عضو\n"
        "/unban - إلغاء حظر عضو\n"
        "/kick - طرد عضو\n"
        "/members - عرض عدد الأعضاء\n"
        "/id - الحصول على IDك أو ID المجموعة"
    )

def warn(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id not in admins.get(chat_id, []):
        update.message.reply_text("عذرًا، ليس لديك إذن لاستخدام هذا الأمر.")
        return
    if not context.args:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في تحذيره.")
        return
    target_user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if not target_user:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في تحذيره.")
        return
    update.message.reply_text(f"{target_user.first_name} تم تحذيره.")

def ban(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id not in admins.get(chat_id, []):
        update.message.reply_text("عذرًا، ليس لديك إذن لاستخدام هذا الأمر.")
        return
    if not context.args:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في حظره.")
        return
    target_user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if not target_user:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في حظره.")
        return
    context.bot.ban_chat_member(chat_id, target_user.id)
    update.message.reply_text(f"{target_user.first_name} تم حظره.")

def unban(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id not in admins.get(chat_id, []):
        update.message.reply_text("عذرًا، ليس لديك إذن لاستخدام هذا الأمر.")
        return
    if not context.args:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في إلغاء حظره.")
        return
    target_user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if not target_user:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في إلغاء حظره.")
        return
    context.bot.unban_chat_member(chat_id, target_user.id)
    update.message.reply_text(f"{target_user.first_name} تم إلغاء حظره.")

def kick(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id not in admins.get(chat_id, []):
        update.message.reply_text("عذرًا، ليس لديك إذن لاستخدام هذا الأمر.")
        return
    if not context.args:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في طرده.")
        return
    target_user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if not target_user:
        update.message.reply_text("يرجى الإشارة إلى العضو الذي ترغب في طرده.")
        return
    context.bot.kick_chat_member(chat_id, target_user.id)
    update.message.reply_text(f"{target_user.first_name} تم طرده.")

def members(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id not in admins.get(chat_id, []):
        update.message.reply_text("عذرًا، ليس لديك إذن لاستخدام هذا الأمر.")
        return
    members = context.bot.get_chat_members_count(chat_id)
    update.message.reply_text(f"عدد الأعضاء في هذه المجموعة: {members}")

def get_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    update.message.reply_text(f"IDك: {user_id}\nID المجموعة: {chat_id}")

def ping(update: Update, context: CallbackContext):
    update.message.reply_text("Pong!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("admin", admin))
    dp.add_handler(CommandHandler("setrules", set_rules))
    dp.add_handler(CommandHandler("rules", get_rules))
    dp.add_handler(CommandHandler("warn", warn))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CommandHandler("unban", unban))
    dp.add_handler(CommandHandler("kick", kick))
    dp.add_handler(CommandHandler("members", members))
    dp.add_handler(CommandHandler("id", get_id))
    dp.add_handler(CommandHandler("ping", ping))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
