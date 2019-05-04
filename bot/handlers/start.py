import logging

from telegram.ext import CommandHandler
from telegram import ChatAction
from telegram import KeyboardButton

from bot import u
from bot import db
from bot import strings as s
from bot import markups as rm
from config import config

logger = logging.getLogger(__name__)

start_menu = [
    KeyboardButton('/create'),
    KeyboardButton('/add'),
    KeyboardButton('/remove'),
    KeyboardButton('/list'),
    KeyboardButton('/status'),
    KeyboardButton('/export'),
    KeyboardButton('/forgetme'),
    KeyboardButton('/help')
]


@u.action(ChatAction.TYPING)
@u.restricted
@u.failwithmessage
def on_help_command(bot, update):
    logger.info('%d: /help', update.effective_user.id)

    update.message.reply_html(s.HELP_MESSAGE.format(bot.username))


@u.action(ChatAction.TYPING)
@u.restricted
@u.failwithmessage
def on_start_command(bot, update, user_data):
    logger.info('%d: /start', update.effective_user.id)

    db.insert_user(update.effective_user.id)
    start_message = s.START_MESSAGE
    if config.bot.sourcecode:
        start_message = '{}\n\n<a href="{}">source code</a>'.format(start_message, config.bot.sourcecode)

    update.message.reply_html(start_message, disable_web_page_preview=True)

    start_menu_markup = ''
    start_menu_markup = rm.get_start_menu_markup(start_menu, add_back_button=True)
    update.message.reply_html('<b>{}</b>'.format('Choose an option!'), reply_markup=start_menu_markup)

    # reset user status
    user_data['status'] = ''


HANDLERS = (
    CommandHandler('help', on_help_command),
    CommandHandler('start', on_start_command, pass_user_data=True)
)
