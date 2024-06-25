from gpt import *
from util import *
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from testdata import gpt_token, tg_token, date_partners, start_menu, message_buttons


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)
    await show_main_menu(update, context, start_menu)


async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    prompt = load_prompt("gpt")
    text = update.message.text
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, date_partners)


async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "_Собеседник набирает текст..._")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    await send_photo(update, context, query)
    await send_text(update, context, "Отличный выбор! Пригласите вашего партнера на свидание за 5 сообщений :)")
    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mode = 'message'
    text = load_message('message')
    await send_photo(update, context, "message")
    await send_text_buttons(update, context, text, message_buttons)
    dialog.list.clear()


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "_ChatGPT думает над ответом..._")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


async def profile(update, context):
    dialog.mode = 'profile'
    text = load_message('profile')
    await send_photo(update, context, "profile")
    await send_text(update, context, text)
    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, 'Сколько вам лет?')


async def profile_dialog(update, context):
    text = update.message.text
    dialog.count += 1
    if dialog.count == 1:
        dialog.user["age"] = text
        await send_text(update, context, 'Кем вы работаете?')
    elif dialog.count == 2:
        dialog.user["occupation"] = text
        await send_text(update, context, 'Чем вы увлекаетесь?')
    elif dialog.count == 3:
        dialog.user["hobby"] = text
        await send_text(update, context, 'Что вам НЕ нравится в людях?')
    elif dialog.count == 4:
        dialog.user["annoys"] = text
        await send_text(update, context, 'Цели знакомства?')
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt('profile')
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "_🧠 ChatGPT генерирует ваш профиль..._")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)


async def opener(update, context):
    dialog.mode = 'opener'
    text = load_message('opener')
    await send_photo(update, context, "opener")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, 'Как зовут вашего собеседника?')


async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] = text
        await send_text(update, context, 'Возраст вашего собеседника?')
    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, context, 'На сколько баллов от 1 до 10 выглядит ваш собеседник?')
    elif dialog.count == 3:
        dialog.user["handsome"] = text
        await send_text(update, context, 'Кем работает ваш собеседник?')
    elif dialog.count == 4:
        dialog.user["occupation"] = text
        await send_text(update, context, 'Цели знакомства?')
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt('opener')
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "_🧠 ChatGPT генерирует для вас сообщение..._")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)


async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    elif dialog.mode == 'date':
        await date_dialog(update, context)
    elif dialog.mode == 'message':
        await message_dialog(update, context)
    elif dialog.mode == 'profile':
        await profile_dialog(update, context)
    elif dialog.mode == 'opener':
        await opener_dialog(update, context)
    else:
        await send_text(update, context, "*Привет*")
        await send_text(update, context, "_Как дела?_")
        await send_text(update, context, "Вы написали " + update.message.text)
        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Запустить процесс?", {
            "start": "Запустить",
            "stop": "Остановить"
        })


async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "Процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")


dialog = Dialog()
dialog.mode = None
dialog.list = []
dialog.count = 0
dialog.user = {}

chatgpt = ChatGptService(token=gpt_token)
app = ApplicationBuilder().token(tg_token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('date', date))
app.add_handler(CommandHandler('message', message))
app.add_handler(CommandHandler('profile', profile))
app.add_handler(CommandHandler('opener', opener))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
