import logging
import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8004861374:AAE4aSX_IfEd_l6ljYbqC3BetlRqxCcDqsE"
ADMIN_ID = 684872569

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте!\n"
        "Я бот «Форма обратной связи».\n\n"
        "Здесь Вы можете поделиться мыслями и идеями о выставке.\n\n"
        "Выберите формат сообщения: текст, голосовое или видео-кружочек."
    )
    await update.message.reply_text(text)

# Ответы пользователей
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Пересылаем админу
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Новое сообщение от @{user.username} (id: {user.id})"
    )
    await update.message.forward(ADMIN_CHAT_ID)

    # Ответ пользователю
    await update.message.reply_text(
        "Спасибо за участие!\n"
        "Приглашаем вас на финальный день выставки 11 января в 16:00 ❤️"
    )

# Запуск бота
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, feedback))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
