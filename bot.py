from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Первый экран после старта
ADVANTAGES_1 = """
📘 <b>Внутри ты получаешь:</b>

1️⃣ <b>Сжатые выжимки по Баффетту, Линчу и Грэму</b> — только главное, никаких теорий ради теорий. Удобно для новичков и полезно для опытных инвесторов.

2️⃣ <b>Мою авторскую стратегию на 2025+</b> — как я применяю принципы стоимостного инвестирования в текущей экономической ситуации (с примерами и выводами).

3️⃣ <b>Бонус — моя личная консультация после прочтения:</b> вместе разберём твои вопросы и подберём шаги под твой уровень и цели.
"""

# Второй экран — выгоды, гарантия, цена
ADVANTAGES_2 = """
⏳ <b>Экономия времени</b> — вместо 100+ часов чтения  
💸 <b>Экономия денег</b> — знания, которые вживую стоили бы тебе от $250–$1000  
📂 <b>Файлы останутся у тебя навсегда</b>

🔒 <b>Гарантия возврата</b>  
Если после прочтения всех материалов и консультации ты посчитаешь, что они тебе не помогли — я верну деньги, без вопросов.

🎯 <b>Получить доступ</b> — 4800₽ или 50 USDT
"""

TG_LINK = "https://t.me/invest_er"

async def initial_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start - первое сообщение с кнопкой"""
    keyboard = [[InlineKeyboardButton("👉 START", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await update.message.reply_text(
            text="💼 <b>Dollar by Dollar</b> — доступ к выжимке из трёх культовых книг по стоимостному инвестированию.\nСоздан для тех, кто хочет разобраться в инвестициях без воды и лишних трат времени.",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка при отправке начального сообщения: {e}")

# Первый шаг — после нажатия START
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        print(f"Ошибка при ответе на callback (start): {e}")
        return
    
    keyboard = [[InlineKeyboardButton("👉 Следующее", callback_data="next")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            text=ADVANTAGES_1,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка при редактировании сообщения (start): {e}")
        # Fallback: попробовать отправить новое сообщение
        try:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=ADVANTAGES_1,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Ошибка при отправке нового сообщения: {e}")

# Второй шаг — показываем преимущества + кнопку
async def next_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        print(f"Ошибка при ответе на callback (next): {e}")
        return
    
    keyboard = [[InlineKeyboardButton("👉 Получить доступ", url=TG_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            text=ADVANTAGES_2,
            reply_markup=reply_markup,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Ошибка при редактировании сообщения (next): {e}")
        # Fallback: попробовать отправить новое сообщение
        try:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=ADVANTAGES_2,
                reply_markup=reply_markup,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"Ошибка при отправке нового сообщения: {e}")

if __name__ == "__main__":
    if not os.getenv("BOT_TOKEN"):
        raise ValueError("Токен бота не найден! Проверь переменную окружения BOT_TOKEN")

    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    
    # Добавлен обработчик команды /start
    app.add_handler(CommandHandler("start", initial_start))
    app.add_handler(CallbackQueryHandler(start_handler, pattern="^start$"))
    app.add_handler(CallbackQueryHandler(next_handler, pattern="^next$"))

    print("Бот запущен...")
    app.run_polling()
