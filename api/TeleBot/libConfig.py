# Config data for lib

from typing import Tuple
import json

BaseOut = Tuple[bool, dict]


class Config:
    def get_token(self, filename: str = "token.json") -> BaseOut:
        try:
            with open(filename, 'r') as file:
                file.read()
        except Exception as e:
            return False, {'result': str(e)}

    def __init__(self):
        pass
