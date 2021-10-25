# An error handler that can be called as a decorator avoiding the eternal try except

import traceback
import functools
from pathlib import Path

from Assistant_Experimental.api import ApiConfig


class UserException(Exception):
    __code: int
    __message: str

    def get_message(self) -> str:
        return str(self.__code) + '\n' + self.__message

    def get_code(self):
        return self.__code

    def __init__(self, code: int, message: str) -> None:
        self.__message = message
        self.__code = code


class ApiException(UserException):

    def __init__(self):
        super().__init__(
            code=7020,
            message="Something went wrong, the error was accepted for processing"
        )

    @staticmethod
    def get_filename(log_name: str) -> Path:
        return Path(ApiConfig.System['log_dir'] / Path(log_name))

    def exc_handler(self, fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs) -> fn:
            # noinspection PyBroadException
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                message = e.get_message() if isinstance(e, UserException) else self.get_message()
                log_name = e.get_code() if isinstance(e, UserException) else self.get_code()
                with self.get_filename(str(log_name)).open(mode='a') as logfile:
                    traceback.print_exc(file=logfile)
                return message
        return wrapped
