from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv  # Добавлено для удобства работы с .env

# Загрузка переменных окружения из .env файла
load_dotenv()

# Приветственное сообщение
WELCOME_MESSAGE = """
💼 <b>Dollar by Dollar</b> — доступ к выжимке из трёх культовых книг по стоимостному инвестированию.
Создан для тех, кто хочет разобраться в инвестициях без воды и лишних трат времени.

📘 <b>Внутри ты получишь:</b>

— Сжатые выжимки по Баффетту, Линчу и Грэму — только главное, никаких теорий ради теорий
— Мою авторскую стратегию на 2025+ — как я применяю принципы стоимостного инвестирования в текущих реалиях
— Бонус — моя личная консультация после прочтения

⏳ <b>Экономия времени</b> — вместо 100+ часов чтения
💸 <b>Экономия денег</b> — знания, которые вживую стоили бы тебе от $250–1000
📂 <b>Файлы останутся у тебя навсегда</b>

🔒 <b>Гарантия возврата:</b>
Если после прочтения всех материалов и консультации ты посчитаешь, что они тебе не помогли — я верну деньги, без вопросов.

🎯 <b>Получить доступ к основам стоимостного инвестирования — 4888₽ или 50 USDT</b>
"""

TG_LINK = "https://t.me/invest_er"  # Обязательно замени на реальную ссылку

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [[InlineKeyboardButton("👉 Получить доступ", url=TG_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Добавлена проверка на наличие сообщения
    if update.message:
        await update.message.reply_text(
            WELCOME_MESSAGE, 
            reply_markup=reply_markup, 
            parse_mode='HTML',
            disable_web_page_preview=True  # Отключаем превью ссылки
        )

if __name__ == '__main__':
    # Добавлена проверка наличия токена
    if not os.getenv("BOT_TOKEN"):
        raise ValueError("Токен бота не найден! Проверьте переменную окружения BOT_TOKEN")
    
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Бот запущен...")
    app.run_polling()
