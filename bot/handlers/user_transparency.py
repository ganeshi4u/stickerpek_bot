import logging

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram import ChatAction
from telegram import KeyboardButton

from bot import strings as s
from bot.overrides import Filters
from bot import u
from bot import db
from bot import markups as rm

logger = logging.getLogger(__name__)

transparency_btns = [
    KeyboardButton('on'),
    KeyboardButton('off')
]

@u.action(ChatAction.TYPING)
@u.restricted
@u.failwithmessage
def on_transparency_command(bot, update, user_data):
    logger.info('%d: /transparency', update.effective_user.id)

    transparency_state = db.get_transparency_state(update.effective_user.id)

    update.message.reply_html(s.CURRENT_USER_TRANSPARENCY_STATE.format(transparency_state[0]))
    transparency_menu_markup = rm.get_menu_markup(transparency_btns, add_back_button=True)
    update.message.reply_html('<b>{}</b>'.format('Set a value!'), reply_markup=transparency_menu_markup)

    user_data['status'] = 'waiting_user_transparency'

@u.action(ChatAction.TYPING)
@u.restricted
@u.failwithmessage
def on_transparency_state_receive(bot, update, user_data):
    logger.info('%d: received possible transparency state', update.effective_user.id)

    if 'on' not in update.message.text and 'off' not in update.message.text:
        logger.info('unknown transparency state value')
        update.message.reply_html(s.UNKNOWN_CURRENT_USER_TRANSPARENCY_STATE.format(update.message.text))
        return

    logger.info('passed transparency state value')

    db.update_transparency_state(update.effective_user.id, update.message.text)
    update.message.reply_html(s.CURRENT_USER_TRANSPARENCY_STATE_UPDATE.format(update.message.text))
    return


HANDLERS = (
    CommandHandler(['transparency', 'tr'], on_transparency_command, filters=Filters.status(''), pass_user_data=True),
    MessageHandler(Filters.status('waiting_user_transparency'), on_transparency_state_receive, pass_user_data=True)
)
