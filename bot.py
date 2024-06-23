from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackQueryHandler

from data import tg_token
from util import *


async def start(update, context):
    text = load_message('main')
    await send_photo(update, context, name='main')
    await send_text(update, context, text)


async def hello(update, context):
    await send_text(update, context, text='*Hi!*')
    await send_text(update, context, text='_How are you?_')
    await send_text(update, context, text=f"You wrote '{update.message.text}'")
    await send_photo(update, context, name='avatar_main')
    await send_text_buttons(update, context, text='Run?', buttons={
        'start': 'Start',
        'stop': 'Stop'
    })


async def hello_button(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, text='Started')
    else:
        await send_text(update, context, text='Stopped')


app = ApplicationBuilder().token(tg_token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
