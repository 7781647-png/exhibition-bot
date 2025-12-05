import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import asyncio

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Данные окружения из Render
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте!\n\n"
        "Я бот «Форма обратной связи».\n"
        "Отправьте сообщение, голосовое или видео-кружочек.\n"
        "Мы будем рады получить вашу обратную связь!"
    )

# Обработка любого сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Пересылка админу
    if ADMIN_ID:
        try:
            await context.bot.send_message(
                ADMIN_ID,
                text=f"Новое сообщение от @{user.username or user.id}:"
            )
            await update.message.forward(ADMIN_ID)
        except Exception as e:
            logger.error(f"Ошибка пересылки админу: {e}")

    # Ответ пользователю
    await update.message.reply_text(
        "Спасибо за участие!\n"
        "Приглашаем вас на финисаж выставки 11 января в 16:00!"
    )

import asyncio
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Бот запущен...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())


