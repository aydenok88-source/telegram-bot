import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Читаем токен и ID из переменных окружения ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
# ------------------------------------------------

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = f"👤 От: {user.first_name}"
    if user.username:
        user_info += f" (@{user.username})"
    user_info += f"\n🆔 ID: {user.id}"
    
    if update.message.text:
        text = f"{user_info}\n\n📝 Текст:\n{update.message.text}"
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        await update.message.reply_text("✅ Отправлено в канал!")
    
    elif update.message.photo:
        photo = await update.message.photo[-1].get_file()
        caption = f"{user_info}\n\n📸 Фото"
        if update.message.caption:
            caption += f"\n\n📝 Подпись: {update.message.caption}"
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo.file_id, caption=caption)
        await update.message.reply_text("✅ Фото отправлено!")
    
    elif update.message.video:
        video = await update.message.video.get_file()
        caption = f"{user_info}\n\n🎥 Видео"
        if update.message.caption:
            caption += f"\n\n📝 Подпись: {update.message.caption}"
        await context.bot.send_video(chat_id=CHANNEL_ID, video=video.file_id, caption=caption)
        await update.message.reply_text("✅ Видео отправлено!")
    
    else:
        await update.message.reply_text("📎 Отправьте текст, фото или видео.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
