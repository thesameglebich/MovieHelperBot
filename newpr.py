from telegram import Update, ParseMode, Bot
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram import ReplyKeyboardRemove
from telegram.ext import MessageHandler
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from Kinmomax_parser import parse

button_help = 'help'
button_location = 'location'

# Кнопки под смс CallBack
KinoMaxButton = "KinoMax"
GoodwinButton = "Goodwin"
Exit = "Exit"

# dictionary for Titles for inline button

Titles = {
    KinoMaxButton: "Киномакс",
    GoodwinButton: "Goodwin",
    Exit: "Exit",
}

def get_inline_keyboard_cinema():
    keyboard = [
        [
            InlineKeyboardButton(Titles[KinoMaxButton], callback_data=KinoMaxButton),
            InlineKeyboardButton(Titles[GoodwinButton], callback_data=GoodwinButton),
        ],
        [
            InlineKeyboardButton(Titles[Exit], callback_data=Exit),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def keyboard_callback_handler(update: Update, context:CallbackContext):
    query = update.callback_query
    data = query.data
    curr_text = update.effective_message.text
    chat_id = update.effective_message.chat_id
    if data == KinoMaxButton:
        #update.callback_query.message. тут надо отредачить фото
        myfilms = parse()
        listoffilms = ""
        for i in range(len(myfilms)):
            listoffilms += myfilms[i]['title'] + myfilms[i]['rating'] + "\n"
        query.message.reply_text(
            text=listoffilms
        )
    elif data == GoodwinButton:
        update.callback_query.edit_message_text(
            text=curr_text,
            parse_mode=ParseMode.MARKDOWN,
        )
        query.message.reply_text(
            text="Empty List of Goodwin",
        )

    elif data == Exit:
        update.callback_query.edit_message_text(
            text=curr_text,
            parse_mode=ParseMode.MARKDOWN
        )
        query.message.reply_text(
            text="By, Send me some money to my number",
        )



def button_location_handler(update:Update, context:CallbackContext):
    update.message.reply_text(
        text=update.message.location.longitude
    )


def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Press Help',
        reply_markup=ReplyKeyboardRemove(),
    )


def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_help:
        return button_help_handler(update=update, context=context)
    if text.lower() == button_location:
        return button_location_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help, request_location=True)
            ],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text="Hello",
        reply_markup=reply_markup
    )


def greeting(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f"""
        Привет,{update.message.from_user.name}!
        Данный телеграм бот, поможет тебе с выбором фильма.
        Пиши /start - если готов или /help - если нужна доп информация
        """
    )

def start(update:Update, context:CallbackContext):
    update.message.reply_photo(
        photo="https://kinomax.tomsk.ru/upload/gallery/image_orig_89_1845.jpg",
        caption="Выберите кинотеатр",
        reply_markup=get_inline_keyboard_cinema(),
    )



def main():

    updater = Updater(
        token='1673692535:AAHtigUE_yZ8xI39LhnGcreyjrurXFchNkM',
        use_context=True,
    )

    #updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("helppls", greeting))
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)
    updater.dispatcher.add_handler(buttons_handler)
    #updater.dispatcher.add_handler(CommandHandler("help"))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
