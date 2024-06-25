from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackQueryHandler

from testdata import tg_token, gpt_token
from util import *
from gpt import *


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, name="main")
    await send_text(update, context, text)
    await show_main_menu(update, context, commands={
        "start": "Самое главное меню бота",
        "profile": "Генерация Tinder-профиля 🔥",
        "new": "Сообщение для знакомства ❤️",
        "message": "Переписка от вашего имени 💌",
        "news": "Переписка со звездой ⭐",
        "gpt": "Задать вопрос чату GPT 💬"
    })


async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, name="gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    prompt = load_prompt("gpt")
    text = update.message.text
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, text="*Привет*")
        await send_text(update, context, text="_Как дела?_")
        await send_text(update, context, text=f"Вы написали '{update.message.text}'")
        await send_photo(update, context, name="avatar_main")
        await send_text_buttons(update, context, text="Запустить процесс?", buttons={
            "start": "Запустить",
            "stop": "Остановить"
        })


async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, text="Процесс запущен")
    else:
        await send_text(update, context, text="Процесс остановлен")

dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token=gpt_token)
app = ApplicationBuilder().token(tg_token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
