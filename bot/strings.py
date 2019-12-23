START_MESSAGE = """Hello mokafaka,
I've been made to create custom sticker peks by kanging existing stickers or from PNG files.

Main commands:
/create to create a new pek
/add to add stickers to an existing pek
/help for more commands and info (take a look at these commands!)"""

HELP_MESSAGE = """<b>Full commands list</b>:
- /create: create a new pek
- /add: add a sticker to a pek
- /remove: remove a sticker from its pek
- send me a sticker and I will send you its png back
- /list: list your peks (max 100 entries)
- /export: export a sticker pek as a zip of png files
- /forgetme: delete yourself from my database. The peks you created will <b>not</b> be deleted from Telegram
- /status: debug command, shows your current status
- /transparency: makes background transparent for images/stickers that have a white background (wip)
- /addpack: add an existing pack to your database

<b>Other operations</b>
You can delete a pek, change stickers' emojis/order and see stickers/peks stats from @stickers

<b>Tips</b>:
- when adding a sticker or creating a pek, you can either pass a sticker or a png file
- when adding a sticker as png, you can pass its emojis in the caption

<b>Other info</b>
All the peks you create with me have their links ending by "_by_{}". This is not made on purpose, \
but something forced by Telegram"""

PACK_ADD_WAITING_NAME = """Please send me the name or link of the sticker pek you want to add\n
(Only peks made by using this bot are supported) """

PACK_ADDED = """<a href="{}"> pek</a> has been added to your database. It should now be available in your pek /list to add stickers."""

PACK_NAME_NOT_OURS_ERROR = """ The provided pek name is not created by me. Please give me the link or name of the peks created by me. """

PACK_CREATION_WAITING_TITLE = """Please send me the pek title (must not exceed 64 characters).
Use /cancel to cancel"""

PACK_TITLE_TOO_LONG = """I'm sorry, the title must be at max 64 characters long. Try with another title"""

PACK_TITLE_CONTAINS_NEWLINES = """I'm sorry, the title must be a single line (no newline characters)"""

PACK_CREATION_WAITING_NAME = """Good, this is going to be the pek title: <i>{}</i>

Please send the what will be the pek link (must be at max {} characters long)"""

PACK_NAME_TOO_LONG = """I'm sorry, this link is too long ({}/{}). Try again with another link"""

PACK_NAME_INVALID = """<b>Invalid link</b>. A link must:
• start with a letter
• consist exclusively of letters, digits or underscores
• not contain two consecutive underscores
• not end with an underscore

Please try again"""

PACK_NAME_DUPLICATE = """I'm sorry, you already have a pek with this link saved. try with another link"""

PACK_CREATION_WAITING_FIRST_STICKER = """got it, we are almost done. Now send me the first sticker of the pek"""

PACK_CREATION_FIRST_STICKER_PACK_DATA_MISSING = """Ooops, something went wrong.
Please repeat the creation process with /create"""

PACK_CREATION_ERROR_DUPLICATE_NAME = """I'm sorry, there's already a pek with <a href="{}">this link</a>.
Please send me a new link, or /cancel"""

PACK_CREATION_ERROR_INVALID_NAME = """I'm sorry, Telegram rejected the link you provided saying it's not valid.
Please send a me new link, or /cancel"""

PACK_CREATION_ERROR_GENERIC = """Error while trying to create the pek: <code>{}</code>.
Please try again, or /cancel"""

PACK_CREATION_PACK_CREATED = """Your pek has been created, add it through <a href="{}">this link</a>
Continue to send me stickers to add more, or /done"""

ADD_STICKER_SELECT_PACK = """Select the pek you want to add stickers to, or /cancel"""

ADD_STICKER_NO_PACKS = """You don't have any pek yet. Use /create to start creating a new pek"""

ADD_STICKER_SELECTED_TITLE_DOESNT_EXIST = """It seems like the pek "{}" doesn't exist.
Please select a valid pek from the keyboard"""

ADD_STICKER_SELECTED_TITLE_MULTIPLE = """It seems like you have multiple peks that match the title "{}".
Please select the Pek you want to choose from the keyboard below. Peks reference:
• {}"""

ADD_STICKER_PACK_SELECTED = """Good, we are going to add stickers to <a href="{}">this pek</a>.
Send me a sticker or a png file"""

ADD_STICKER_SELECTED_NAME_DOESNT_EXIST = """It seems like the pek "{}" doesn't exist.
Please select a valid pek from the keyboard"""

ADD_STICKER_PACK_DATA_MISSING = """Ooops, something went wrong.
Please repeat the process with /add"""

ADD_STICKER_PACK_NOT_VALID = """Ooops, it looks like <a href="{}">this pek</a> doesn't exist.
Please select another pek"""

ADD_STICKER_PACK_NOT_VALID_NO_PACKS = """Ooops, it looks like <a href="{}">this pek</a> doesn't exist.
Please create a new pek with /create"""

ADD_STICKER_SUCCESS = """Sticker added to <a href="{}">this pek</a>.
Continue to send me stickers to add more, use /done when you're done"""

ADD_STICKER_PACK_FULL = """I'm sorry, <a href="{}">this pek</a> is full (120 stickers), \
you can no longer add stickers to it. Use /remove to remove some stickers
Use /done when you've finished"""

ADD_STICKER_SIZE_ERROR = """Whoops, it looks like an error happened while resizing the sticker \
and now its dimensions are {}x{} px. I can't add this sticker to the pek due to wrong resizing logic.
Send me another sticker, or use /done when you're done"""

ADD_STICKER_GENERIC_ERROR = """An error occurred while adding this sticker to <a href="{}">this pek</a>: \
<code>{}</code>.
Try again, send me another sticker or use /done when you're done"""

REMOVE_STICKER_SELECT_STICKER = """Send me the sticker you want to remove from its pek, or /cancel"""

REMOVE_STICKER_SUCCESS = """Sticker removed from <a href="{}">its pek</a>.
Send me another sticker to remove, or /done when you're done"""

REMOVE_STICKER_FOREIGN_PACK = """This sticker is from a <a href="{}">pek</a> you didn't create through me. \
Try with a valid sticker, or /done"""

REMOVE_STICKER_ALREADY_DELETED = """This sticker is no longer part of <a href="{}">the pek</a>, \
try with another sticker"""

REMOVE_STICKER_GENERIC_ERROR = """An error occurred while removing this sticker from <a href="{}">this pek</a>: \
<code>{}</code>.
Try again, send me another sticker or use /done when you're done"""

FORGETME_SUCCESS = """Success, I've deleted all of your peks from my database"""

CANCEL = """Good, we're done with that"""

LIST_NO_PACKS = """You don't have any pek. Use /create to create one"""

EXPORT_PACK_SELECT = """Please send me a stciker from the pek you want to export, or /cancel"""

EXPORT_PACK_NO_PACK = """This sticker doesn't belong to any pek. Please send me a stciker from a pek, or /cancel"""

EXPORT_PACK_START = """Exporting stickers from <i>{}</i>... it may take some minutes. Please hold on"""

EXPORT_PACK_UPLOADING = """Zipping png files and uploading..."""

CURRENT_USER_TRANSPARENCY_STATE = """Current transparency state is: <b>{}</b> \n\nPossible values: on, off \n\n\
Send your preferred value to set transparency state.\n\n /cancel to leave it at current state."""

CURRENT_USER_TRANSPARENCY_STATE_UPDATE = """Transparency state is now set to: <b>{}</b> \n /done"""

UNKNOWN_CURRENT_USER_TRANSPARENCY_STATE = """Invalid value '<b>{}</b>' for transparency state. Please provide a valid value! \
\n or /cancel"""
