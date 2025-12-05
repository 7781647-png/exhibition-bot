import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем данные окружения от Render
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте!\n\n"
        "Я бот «Форма обратной связи».\n"
        "Здесь вы можете поделиться своими мыслями, ассоциациями и идеями о выставке.\n\n"
        "Отправьте сообщение, голосовое или видео-кружочек.\n"
        "Мы будем рады получить вашу обратную связь!"
    )

# Обработка любого сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Пересылаем админу
    if ADMIN_ID != 0:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Новое сообщение от @{user.username or user.id}:"
            )
            await update.message.forward(chat_id=ADMIN_ID)
        except Exception as e:
            logger.error(f"Ошибка пересылки админу: {e}")

    # Ответ пользователю
    await update.message.reply_text(
        "Спасибо за участие!\n"
        "Приглашаем вас на финисаж выставки 28 декабря в 19:00, как участника проекта.\n"
        "До встречи!"
    )

# Асинхронный запуск
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start))

    # Любые сообщения
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Бот запущен...")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
