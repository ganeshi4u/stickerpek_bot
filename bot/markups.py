from telegram import InlineKeyboardButton
from telegram import KeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

HIDE = ReplyKeyboardRemove()


def get_markup_from_list(titles, add_back_button=False):
    if add_back_button:
        cancel_btn = [
            KeyboardButton('/cancel')
        ]

    return ReplyKeyboardMarkup(build_menu(titles, n_cols=2, footer_buttons=cancel_btn), resize_keyboard=True)

def get_start_menu_markup(titles, add_back_button=False):
    if add_back_button:
        cancel_btn = [
            KeyboardButton('/cancel')
        ]

    return ReplyKeyboardMarkup(build_menu(titles, n_cols=2, footer_buttons=cancel_btn), resize_keyboard=True)

# Create a button menu to show in Telegram messages
def build_menu(buttons, n_cols=1, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)

    return menu
