# Small api for database lib

from montydb import set_storage, MontyClient
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0].absolute()))

from api_config import DB
from api_exception import ApiException, UserException

exc_handler = ApiException().exc_handler
DatabaseIsBlock = UserException(4040, "Something went wrong, the error was accepted for processing")


class Client:

    @exc_handler
    def __init__(self):
        print(MontyClient)
        set_storage(DB['path'])
        db_client = MontyClient(DB["path"])
        self.__main = db_client
        self.__client = self.__main.db
        self.__block = False

    @exc_handler
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Client, cls).__new__(cls)
        return cls.instance

    @exc_handler
    def get_connect(self):
        if not self.__block:
            return self.__client
        else:
            try_count = 1
            while try_count <= 5:
                if not self.__block:
                    return self.__client
                else:
                    try_count += 1
                    time.sleep(1)

    def set_block(self):
        self.__block = False if self.__block else True

    @exc_handler
    def drop_coll(self, coll):
        if self.__block:
            self.__client.drop_collection(coll)
