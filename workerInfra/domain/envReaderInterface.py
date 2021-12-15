from typing import List
from abc import ABC, abstractclassmethod
from os import getenv


class EnvReaderInterface(ABC):
    @abstractclassmethod
    def read(self) -> List:
        pass

    @staticmethod
    def __splitDiscordLinks__(raw: str) -> List[str]:
        res = list()
        if raw == "" or raw is None:
            return list()
        else:
            for i in raw.split(","):
                i = i.lstrip()
                i = i.rstrip()
                res.append(i)
        return res

    @staticmethod
    def __parseBool__(envFlag: str) -> bool:
        try:
            value: str = getenv(envFlag).lower()
            if value == 'false':
                return False
            elif value == 'true':
                return True
            else:
                raise Exception(f"Unknown value type for '{envFlag}'.  Expected True or False.")
        except Exception as e:
            print(f"EnvReader was unable to parse a bool, could be a null value. {e}")
            return False
