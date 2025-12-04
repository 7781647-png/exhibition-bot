import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


# ========= ВСТАВЬ СВОИ ДАННЫЕ ==========
TOKEN = "8004861374:AAE4aSX_IfEd_l6ljYbqC3BetlRqxCcDqsE"
ADMIN_ID = 684872569
# ========================================


# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте!\n"
        "Я бот «Форма обратной связи».\n"
        "Здесь вы можете поделиться вашими мыслями, ассоциациями,\n"
        "образами и идеями о выставке.\n\n"
        "Вы можете отправить:\n"
        "• текст\n"
        "• голосовое сообщение\n"
        "• видео-кружок\n\n"
        "Мы будем рады получить вашу обратную связь ❤️"
    )
    await update.message.reply_text(text)


# Определение типа сообщения
def get_message_type(update: Update) -> str:
    msg = update.message
    if msg.text:
        return "text"
    if msg.voice:
        return "voice"
    if msg.video_note:
        return "video_note"
    if msg.photo:
        return "photo"
    if msg.document:
        return "document"
    return "unknown"


# Обработка сообщений
async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg_type = get_message_type(update)

    caption = (
        f"Новое сообщение от пользователя:\n"
        f"Имя: {user.first_name}\n"
        f"ID: {user.id}\n"
        f"Тип: {msg_type}"
    )

    # Пересылка админу
    if msg_type == "text":
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"{caption}\n\nТекст:\n{update.message.text}"
        )

    elif msg_type == "voice":
        await context.bot.send_voice(
            chat_id=ADMIN_ID,
            voice=update.message.voice.file_id,
            caption=caption
        )

    elif msg_type == "video_note":
        await context.bot.send_video_note(
            chat_id=ADMIN_ID,
            video_note=update.message.video_note.file_id
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=caption)

    elif msg_type == "photo":
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption
        )

    elif msg_type == "document":
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=caption
        )

    else:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"{caption}\n\n(Тип сообщения не распознан)"
        )

    # Ответ пользователю
    await update.message.reply_text(
        "Спасибо за участие! "
        "Приглашаем вас на финисаж выставки 28 декабря в 19:00, как учатника проекта ❤️"
	"До встречи!"
    )


# ======== ПРАВИЛЬНЫЙ ЗАПУСК ДЛЯ WINDOWS + PYTHON 3.14 ==========
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_feedback))

    print("Бот запущен...")

    # Создать event loop вручную — критично для Python 3.14
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Запустить polling без закрытия loop
    loop.run_until_complete(
        app.run_polling(stop_signals=None)
    )


if __name__ == "__main__":
    main()