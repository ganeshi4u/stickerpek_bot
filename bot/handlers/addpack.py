import logging

from telegram import ChatAction
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.error import BadRequest
from telegram.error import TelegramError

from bot import u
from bot import db
from bot import strings as s
from bot.overrides import Filters

logger = logging.getLogger(__name__)

@u.action(ChatAction.TYPING)
@u.restricted
@u.failwithmessage
def on_addpack_command(bot, update, user_data):
    logger.info('%d: /addpack', update.effective_user.id)

    update.message.reply_text(s.PACK_ADD_WAITING_NAME)
    user_data['status'] = 'waiting_addpack_name'

@u.action(ChatAction.TYPING)
@u.failwithmessage
def on_addpack_name_receive(bot, update, user_data):
    logger.info('%d: received possible addpack name', update.effective_user.id)

    addpack_name = update.message.text
    if "https://t.me/addstickers/" in addpack_name:
        addpack_name = addpack_name.split("https://t.me/addstickers/", 1)[1]
        if "_by_" + bot.username not in addpack_name:
            update.message.reply_text(s.PACK_NAME_NOT_OURS_ERROR)
            user_data['status'] = 'waiting_addpack_name'
            return
    elif addpack_name is not None:
        addpack_name = addpack_name + '_by_' + bot.username
    else:
        update.message.reply_text(s.PACK_NAME_NOT_OURS_ERROR)
        user_data['status'] = 'waiting_addpack_name'
        return

    if len(addpack_name) > 64:
        logger.info('Not a valid pack name too long: %s', addpack_name)
        update.message.reply_text(s.PACK_TITLE_TOO_LONG)
        # do not change the user status and let him send another title
        return

    if '\n' in addpack_name:
        logger.info('pack title contains newline character')
        update.message.reply_text(s.PACK_TITLE_CONTAINS_NEWLINES)
        # do not change the user status and let him send another title
        return

    logger.info('pack title is valid')
    # get sticker set
    try:
        addpack_name_stickerset = bot.getStickerSet(addpack_name)
    except (BadRequest, TelegramError) as e:
        logger.error('Telegram error while trying to get the sticker set: %s', e.message)
        error_code = u.get_exception_code(e.message)

        if error_code == 13:
            update.message.reply_text(s.PACK_CREATION_ERROR_INVALID_NAME)
            user_data['status'] = 'waiting_addpack_name'
        else:
            update.message.reply_html(s.PACK_CREATION_ERROR_GENERIC.format(e.message))

        return  # do not continue

    db.save_pack(update.effective_user.id, addpack_name_stickerset.name, addpack_name_stickerset.title)
    pack_link = u.name2link(addpack_name_stickerset.name)
    update.message.reply_html(s.PACK_ADDED.format(pack_link))

    user_data['status'] = ''

HANDLERS = (
    CommandHandler(['addpack', 'ap'], on_addpack_command, filters=Filters.status(''), pass_user_data=True),
    MessageHandler(Filters.status('waiting_addpack_name'), on_addpack_name_receive, pass_user_data=True)
)

    