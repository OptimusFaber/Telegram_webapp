from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters
from credentials import BOT_TOKEN, BOT_USERNAME, WEBAPP_URL
import json


async def launch_web_ui(update: Update, context: CallbackContext):
    # Отображаем веб-приложение
    kb = [
        [KeyboardButton(
            "Показать веб-приложение!",
            web_app=WebAppInfo(WEBAPP_URL)
        )]
    ]
    await update.message.reply_text("Давайте начнем...", reply_markup=ReplyKeyboardMarkup(kb))


async def web_app_data(update: Update, context: CallbackContext):
    data = json.loads(update.message.web_app_data.data)
    await update.message.reply_text("Ваши данные:")
    for result in data:
        await update.message.reply_text(f"{result['name']}: {result['value']}")


if __name__ == '__main__':
    # Создаем бот из токена
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Устанавливаем слушатель для команды /start для запуска веб-приложения
    application.add_handler(CommandHandler('start', launch_web_ui))

    # Слушатель для данных веб-приложения
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Запуск бота
    print(f"Ваш бот работает! Перейдите на http://t.me/{BOT_USERNAME}, чтобы взаимодействовать с ним!")
    application.run_polling()
