# An error handler that can be called as a decorator avoiding the eternal try except

import traceback


class EcxHandler:

    @staticmethod
    def exc_handler(function):
        def wrapped(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return function(*args, **kwargs)
            except Exception:
                traceback.print_exc()

        return wrapped
