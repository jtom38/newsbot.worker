from os import environ
from dotenv import load_dotenv
from workerInfra.enum import EnvEnum


class EnvBase():
    def __validateBool__(self, msg: str) -> bool:
        if msg.lower() == 'true':
            return True
        else: 
            return False

    def __isOptional__(self, isOptional: bool, value: str) -> None:
        if isOptional == True:
            return None

        if value == '' or value == None:
            raise Exception(f"'{self.getKey()}' was expected, but not found.  Enter a value and try again.")

    def __validateString__(self, value: str) -> str:
        return str(value)

    def __validateInt__(self, value: str) -> int:
        return int(value)

    def getValue(self) -> str:
        return environ[self.__key__]

    def setKey(self, key: str) -> None:
        self.__key__: str = key

    def getKey(self) -> str:
        return self.__key__


class EnvReaderService():
    def __init__(self) -> None:
        load_dotenv('.env')

    def getValue(self, key: EnvEnum, required: bool = False) -> str:
        try:
            res = environ[key.value]
        except:
            res = ''

        if required == True:
            if res == '':
                raise Exception("No value was returned from the env.")

        if res.isnumeric() == True:
            return int(res)
        if res.lower() == 'true':
            return True
        if res.lower() == 'false':
            return False
        return res