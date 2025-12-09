import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import asyncio

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # ID администратора

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! \n" 
        " Я бот выставки Форма обратной связи. \n\n"
        "Здесь вы можете поделиться своими мылями и идеями о выставке. \n\n" 
        " Выберите формат сообщения: текст, голосовое или видое-кружочек."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    admin_text = f"Новое сообщение от {user.full_name} (@{user.username}):\n\n{text}"

    # пересылаем админу
    await context.bot.send_message(chat_id=int(ADMIN_ID), text=admin_text)

    # отвечаем пользователю
    await update.message.reply_text("Спасибо за участие! Приглашаем вас на финисаж выставки 11 января в 16:00, как участиника выставки!")


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
