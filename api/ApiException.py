# An error handler that can be called as a decorator avoiding the eternal try except

import traceback

import ApiBase


class UserException(Exception):
    def get_message(self):
        pass


class ApiException(ApiBase):

    @staticmethod
    def exc_handler(function):
        def wrapped(*args, **kwargs) -> function:
            # noinspection PyBroadException
            try:
                return function(*args, **kwargs)
            except Exception:
                traceback.print_exc()

        return wrapped
