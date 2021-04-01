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
from Goodwin import parseGoodwin

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


def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    curr_text = update.effective_message.text
    chat_id = update.effective_message.chat_id
    if data == KinoMaxButton:
        query.message.reply_text(
            text="Пожалуйста подождите, мы уже загружаем все фильмы Киномакса"
        )
        # update.callback_query.message. тут надо отредачить фото
        myfilms = parse()
        myfilms.sort(key=lambda dictionary: dictionary['rating'], reverse=True)
        listoffilms = ""
        for i in range(len(myfilms)):
            if myfilms[i]['title'] is None or myfilms[i]['rating'] is None:
                continue
            if myfilms[i]['rating'] == "0":
                myfilms[i]['rating'] = "б/р"
            listoffilms += myfilms[i]['title'] + myfilms[i]['rating'] + "\n"
        query.message.reply_text(
            text=listoffilms
        )
    elif data == GoodwinButton:
        query.message.reply_text(
            text="Пожалуйста подождите, мы уже загружаем все фильмы Гудвина"
        )
        goodwinfilms = parseGoodwin()
        goodwinfilms.sort(key=lambda dictionary: dictionary['rating'], reverse=True)
        listforfoodwin = ""
        for i in range(len(goodwinfilms)):
            if goodwinfilms[i]['title'] is None or goodwinfilms[i]['rating'] is None:
                print(goodwinfilms[i]['title'])
                continue
            if goodwinfilms[i]['rating'] == "0":
                goodwinfilms[i]['rating'] = "б/р"
            listforfoodwin += goodwinfilms[i]['title'] + " " + goodwinfilms[i]['rating'] + "\n"

        query.message.reply_text(
            text=listforfoodwin
        )

    elif data == Exit:
        update.callback_query.edit_message_text(
            text=curr_text,
            parse_mode=ParseMode.MARKDOWN
        )
        query.message.reply_text(
            text="By, Send me some money to my number",
        )


def button_location_handler(update: Update, context: CallbackContext):
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


def start(update: Update, context: CallbackContext):
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

    # updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("helppls", greeting))
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)
    updater.dispatcher.add_handler(buttons_handler)
    # updater.dispatcher.add_handler(CommandHandler("help"))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()