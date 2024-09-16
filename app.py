import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
from uuid import uuid4
from collections import defaultdict
from credentials import BOT_TOKEN, WEBAPP_URL, BOT_USERNAME

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Словарь для хранения чатов, куда пользователь переслал сообщение
user_forwarded_chats = defaultdict(set)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    # Запуск веб-приложения с кнопками
    keyboard = [
        [InlineKeyboardButton("Open webapp", web_app=WebAppInfo(WEBAPP_URL))],
        [InlineKeyboardButton("Share", switch_inline_query="https://t.me/dvachannel/143325 ")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Hi! Use @{BOT_USERNAME} in inline mode or share link in webapp.",
        reply_markup=reply_markup
    )

# Обработчик inline-запросов
async def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    user = update.inline_query.from_user

    # Кнопка подтверждения
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Confirm", callback_data="confirm")]]
    )
    
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Share link",
            input_message_content=InputTextMessageContent(f"{query} https://t.me/dvachannel/143325 "),
            reply_markup=keyboard
        )
    ]

    await update.inline_query.answer(results)

# Обработчик callback-запросов
async def handle_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    
    print(query)

    if query.message:
        chat_id = query.message.chat_id
        logger.info(f"Callback query received from {user.username} (user_id: {user.id}) in chat {chat_id}: {query.data}")
    elif query.inline_message_id:
        logger.info(f"Callback query received from {user.username} (user_id: {user.id}) in chat {query.chat_instance} with inline_message_id: {query.inline_message_id}")
    else:
        logger.info(f"Callback query received from {user.username} (user_id: {user.id}), но не удалось найти информацию о сообщении или чате.")

    # Снижаем счетчик и обновляем в веб-приложении (если бы это было связано с веб-сервером)
    # await update_counter(user.id)

    await query.edit_message_reply_markup(reply_markup=None)

    await query.answer("Message confirmed!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    logging.info("Bot started!")
    application.run_polling()
