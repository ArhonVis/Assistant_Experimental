# api for telegram lib
from typing import Dict, Callable, List, AnyStr, Tuple
import re
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

from Assistant_Experimental.api.ApiException import ApiException, UserException

CmdNotFound = UserException(code=404, message='Command not found')
_ApiException = ApiException()

Answer = List[AnyStr] or str
Handler = Callable[[Update, CallbackContext], Answer]
Format = Callable[[Answer], Answer]
Routing = Dict[str, Tuple[Handler, Format] or Handler]


class TeleBot:

    def __init__(self, token: str, routing: Routing) -> None:
        self.updater = Updater(token)
        self.routing = routing
        self.updater.dispatcher.add_handler(MessageHandler(Filters.all, self.router))

    @_ApiException.exc_handler
    def router(self, update: Update, context: CallbackContext) -> None:
        handler = self.routing.get(self.get_cmd(update.message.text))
        if not handler:
            update.message.reply_text(CmdNotFound.get_message())
            assert CmdNotFound
        handler, formatter = handler if isinstance(handler, tuple) else handler, self.format_default
        res = handler(update, context)
        update.message.reply_text(res)

    @staticmethod
    def format_default(data: Answer) -> Answer:
        if isinstance(data, list):
            return '\n'.join(data)
        else:
            return data

    @staticmethod
    def get_cmd(data: str) -> str:
        res = re.match(r'/\w+', data)
        if res:
            return res.group()[1:]
        else:
            return data

    @_ApiException.exc_handler
    def start(self):
        self.updater.start_polling()
        self.updater.idle()

# A small example
# from Assistant_Experimental.api import ApiConfig
#
#
# def hello(update: Update, context: CallbackContext) -> Answer:
#     return f'Hello {update.effective_user.first_name}'
#
#
# bot = TeleBot(ApiConfig.Libraries['tele_bot']['token'], {'hello': hello})
# bot.start()
