from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Первое сообщение (до нажатия START)
INITIAL_MESSAGE = """
💼 <b>Dollar by Dollar</b> — доступ к выжимке из трёх культовых книг по стоимостному инвестированию.
Создан для тех, кто хочет разобраться в инвестициях без воды и лишних трат времени.
"""

# Основное сообщение (после нажатия START)
WELCOME_MESSAGE = """
📘 <b>Внутри ты получишь:</b>

— Сжатые выжимки по Баффетту, Линчу и Грэму — только главное, никаких теорий ради теорий
— Мою авторскую стратегию на 2025+ — как я применяю принципы стоимостного инвестирования в текущих реалиях
— Бонус — моя личная консультация после прочтения

⏳ <b>Экономия времени</b> — вместо 100+ часов чтения
💸 <b>Экономия денег</b> — знания, которые вживую стоили бы тебе от $250–$1000
📂 <b>Файлы останутся у тебя навсегда</b>

🔒 <b>Гарантия возврата:</b>
Если после прочтения всех материалов и консультации ты посчитаешь, что они тебе не помогли — я верну деньги, без вопросов.

🎯 <b>Получить доступ к основам стоимостного инвестирования — 4800₽ или 50 USDT</b>
"""

TG_LINK = "https://t.me/invest_er"

async def send_initial_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляем первое сообщение при любом взаимодействии"""
    keyboard = [[InlineKeyboardButton("👉 START", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            INITIAL_MESSAGE,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатия кнопки"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("👉 Получить доступ", url=TG_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        INITIAL_MESSAGE + "\n\n" + WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

if __name__ == '__main__':
    if not os.getenv("BOT_TOKEN"):
        raise ValueError("Токен бота не найден! Проверьте переменную окружения BOT_TOKEN")
    
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    
    # Обработчик любого сообщения (покажет первое приветствие)
    app.add_handler(MessageHandler(filters.ALL, send_initial_message))
    
    # Обработчик кнопки START
    app.add_handler(CallbackQueryHandler(button_handler, pattern='^start$'))
    
    print("Бот запущен...")
    app.run_polling()
