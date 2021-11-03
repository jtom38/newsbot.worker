from workerInfra.enum import LogLevels
from workerInfra.models import EnvLogger
from workerInfra.domain import LoggerInterface
from datetime import datetime
from inspect import getframeinfo, stack
from os.path import exists
from os import getenv

class LoggerCommon():
    def getLevelWithPadding(self, level: str) -> str:
        level = level.lower()
        if level == "debug":
            return "debug    "
        elif level == "info":
            return "info     "
        elif level == "warning":
            return "warning  "
        elif level == "error":
            return "error    "
        elif level == 'critical':
            return "critical "

    def getTimeStamp(self) -> str:
        dt = datetime.now()
        month = self.getPaddedDateTimeValue(dt.month)
        day = self.getPaddedDateTimeValue(dt.day)
        date=f"{dt.year}-{month}-{day}"

        hour = self.getPaddedDateTimeValue(dt.hour)
        minute = self.getPaddedDateTimeValue(dt.minute)
        second = self.getPaddedDateTimeValue(dt.second)
        #time=f"{dt.hour}:{dt.minute}:{dt.second}:{dt.microsecond}"
        time=f"{hour}:{minute}:{second}"
        return f"{date} {time}"

    def getPaddedDateTimeValue(self, value:int) -> str:
        if len(str(value)) == 1:
            return f"0{value}"
        else:
            return value

    def cleanCallerClass(self) -> str:
        remove = "<", '>', "'", "class "
        if self.callerClass != "":
            cc: str = self.callerClass
            for r in remove:
                cc = cc.replace(r, '')
            return cc
        else:
            return "CallerClassMissing"

    def setCallerDetails(self, stack) -> None:
        caller = getframeinfo(stack[1][0])
        self.callerMethod: str = caller.function
        self.callerLine: int = caller.lineno

class LoggerStdOut(LoggerCommon):
    def sendToStdout(self, level: str, message: str) -> str:
        dt = self.getTimeStamp()
        level = self.getLevelWithPadding(level)
        callerClass = self.cleanCallerClass()
        line: str = self.getStdoutLineNumber()
        if self.config.isSimple.lower() == 'true':
            t = callerClass.split('.')
            l = len(t)
            start = l - 1
            callerClass = f"{t[start]}"
            pass
        line: str = f"{dt} | {level.upper()} | {callerClass}.{self.callerMethod}:{line} | {message}"
        print(line)
        return line

    def getStdoutLineNumber(self) -> str:
        l = str(self.callerLine)
        if len(l) == 1:
            return f"{l}   "
        elif len(l) == 2:
            return f"{l}  "
        elif len(l) == 3:
            return f"{l} "
        else:
            return l

class LoggerFile(LoggerCommon):
    def sendToFile(self, msg: str) -> None:
        if exists(self.logFile) == False:
            with open(self.logFile, 'w') as l:
                l.write(f"{msg}\n")
        else:
            with open(self.logFile, 'a') as l:
                l.write(f"{msg}\n")

class Logger(LoggerInterface, LoggerStdOut, LoggerFile):
    def __init__(self, callerClass: str = "") -> None:
        """
        This class generates the logger used in NewsBot.
        When you call it, call it like this Logger(__class__).
        Doing this will let the logger know the source class

        Examples:
        logger = Logger(__class__)
        Logger(__class__).debug("hello world")
        """
        self.callerClass: str = str(callerClass)
        self.logFile: str = './mounts/logs/newsbot.log'
        self.file = LoggerFile()
        self.config = EnvLogger(
            isSimple=getenv("NEWSBOT_LOGGER_MODE_SIMPLE")
        )
        pass

    def debug(self, message: str) -> None:
        level: str = LogLevels.DEBUG.value
        self.setCallerDetails(stack())
        msg = self.sendToStdout(level, message)
        self.sendToFile(msg)

    def info(self, message: str) -> None:
        level: str = LogLevels.INFO.value
        self.setCallerDetails(stack())
        msg = self.sendToStdout(level, message)
        self.sendToFile(msg)

    def warning(self, message: str) -> None:
        level: str = LogLevels.WARNING.value
        self.setCallerDetails(stack())
        #m = f"{message} - Error: {exception}"
        msg = self.sendToStdout(level, message)
        self.sendToFile(msg)

    def error(self, message: str) -> None:
        level: str = LogLevels.ERROR.value
        self.setCallerDetails(stack())
        msg = self.sendToStdout(level, message)
        self.sendToFile(msg)

    def critical(self, message: str) -> None:
        level: str = LogLevels.CRITICAL.value
        self.setCallerDetails(stack())
        msg = self.sendToStdout(level, message)
        self.sendToFile(msg)