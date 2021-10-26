# api for telegram lib
import re
from typing import Dict, Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

from Assistant_Experimental.api.ApiException import ApiException, UserException

CmdNotFound = UserException(code=404, message='Command not found')
_ApiException = ApiException()

Answer = Dict[str, Any]


class BaseHandler:
    SAMPLE = 0
    DIALOG = 1

    def __init__(self, type_handler: int = SAMPLE, have_but: bool = False):
        self.type_handler = type_handler
        self.have_but = have_but

    def go(self, **kwargs) -> Answer:
        """
        This method will be call for handling
        :return: {'text' : answer, 'reply_markup' = keyboard}
        """
        pass


Handler = Any  # BaseHandler subclass
Routing = Dict[str, Handler]


class TeleBot:

    def __init__(self, token: str, routing: Routing) -> None:
        self.updater = Updater(token)
        self.routing = routing
        self.have_def_but = False
        self.__def_keyboards = None
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.router))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.all, self.router))

    @_ApiException.exc_handler
    def router(self, update: Update, context: CallbackContext) -> None:
        callback = update.callback_query
        if callback:
            cmd = callback.data
            callback.answer()
            method = callback.edit_message_text
        else:
            cmd = update.message.text
            method = update.message.reply_text
        cmd = self.get_cmd(cmd)
        handler = self.routing.get(cmd)
        if not handler:
            method(CmdNotFound.get_message())
            raise CmdNotFound
        else:
            params = {
                'cmd': cmd}
            res = handler.go(**params)
        if not res.get('reply_markup') and self.have_def_but:
            res.update({'reply_markup': self.__def_keyboards})
        method(**res)

    @_ApiException.exc_handler
    def set_default_button(self, buttons_list: list):
        def create_keyboard(buttons: list):
            res = []
            for but in buttons:
                if isinstance(but, list):
                    but_obj = create_keyboard(but)
                else:
                    name, value = but
                    but_obj = InlineKeyboardButton(name, callback_data=value)
                res += [but_obj]
            return res

        self.__def_keyboards = InlineKeyboardMarkup(create_keyboard(buttons_list))
        self.have_def_but = True
        return self.__def_keyboards

    @staticmethod
    def get_cmd(data: str) -> str:
        res = re.match(r'/\w+', data)
        if res:
            return res.group()[1:]
        else:
            return data

    @_ApiException.exc_handler
    def run(self):
        self.updater.start_polling()
        self.updater.idle()
