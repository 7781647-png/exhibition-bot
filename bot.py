import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте!\n"
        "Я бот «Форма обратной связи».\n\n"
        "Здесь Вы можете поделиться мыслями и идеями о выставке.\n\n"
        "Выберите формат сообщения: текст, голосовое или видео-кружочек."
    )
    await update.message.reply_text(text)

# получение сообщений
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # сообщение админу
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Новое сообщение от @{user.username} (id: {user.id})"
    )
    await update.message.forward(ADMIN_CHAT_ID)

    # ответ пользователю
    await update.message.reply_text(
        "Спасибо за участие!\n"
        "Приглашаем вас 11 января в 16:00 ❤️"
    )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, feedback))

    # Render даёт переменную PORT
    port = int(os.environ.get("PORT", 8443))

    # Webhook режим
    await app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}",
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

