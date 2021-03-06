from typing import List
from json import loads
from os import getenv
from workerInfra.exceptions import MissingApiUrl
from workerInfra.domain import DbApiTableInterface


class RestSql(DbApiTableInterface):
    def __getApiUri__(self) -> str:
        try:
            res = getenv("NEWSBOT_API_URI")
            if res is None:
                raise MissingApiUrl
            return res
        except MissingApiUrl:
            print("Was unable to find a value against 'NEWSBOT_API_URI'.  Please make sure it has been added and try again.")
            exit(1)

    def __singleFromApi__(self, raw: str) -> object:
        d = loads(raw)
        return self.__fromApi__(d)

    def __listFromApi__(self, raw: str) -> List[object]:
        d: List[dict] = loads(raw)
        _l = list()
        for i in d:
            _l.append(self.__fromApi__(i))
        return _l

    def validateStatusCode(self, statusCode: int, text: str) -> bool:
        """
        This is validates the status code and text given to see how to respond.

        """
        if statusCode == 404:
            return False
        elif statusCode == 200:
            if text == 'null' or text == '[]':
                return False
            else:
                return True

    def convertListResults(self, statusCode: int, text: str) -> List[object]:
        isGood = self.validateStatusCode(statusCode, text)
        if isGood is True:
            return self.__listFromApi__(text)
        else:
            _l = list()
            _l.append(self.__generateBlank__())
            return _l

    def convertSingleResult(self, statusCode: int, text: str) -> object:
        isGood = self.validateStatusCode(statusCode, text)
        if isGood is True:
            return self.__singleFromApi__(text)
        else:
            return self.__generateBlank__()
