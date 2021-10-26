from enum import Enum


class SourceTypeEnum(Enum):
    USER = 'user'
    TAG = 'tag'
    INVALID = ''

    #@staticmethod
    #def fromString(item: str):
    #    if item == 'user': return SourceTypeEnum.USER
    #    elif item == 'tag': return SourceTypeEnum.TAG
    #    else: return SourceTypeEnum.INVALID