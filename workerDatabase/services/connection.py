from os import getenv
from enum import Enum


class ConnectionStringTypes(Enum):
    SQLITE = 'sqlite'
    POSTGRES = 'postgres'


class ConnectionStringModes(Enum):
    """
    Used to determin what mode the application is running in for the database connection string.
    This helps to determin part of the database name.
    """
    DEV = 'dev'     # Used for local development
    TEST = 'test'   # Used for unit tests
    PROD = 'prod'   # Used for production databases


class ConnectionString():
    """
    This builds the connection string for SQL Alchemy.
    You do not need to interact with this object, just call it and collect the value.

    Example
        value: str = ConnectionString().getConnectionString()

    Env Values:
        NEWSBOT_DATABASE_NAME = 'newsbot'
        NEWSBOT_DATABASE_TYPE = 'sqlite'
        NEWSBOT_DATABASE_PATH = ''
        NEWSBOT_ENV = 'prod'
    """
    __defaultType__: ConnectionStringTypes = ConnectionStringTypes.SQLITE
    __defaultName__: str = 'newsbot'
    __defaultPath__: str = "/mounts/database"

    __dbEnv__: str = ''
    __dbMode__: str = ''

    # Used with SQLite
    __dbName__: str = ''
    __dbPath__: str = ''

    # Used for Postgres
    __dbUsername__: str = ''
    __dbPassword__: str = ''
    __dbHost__: str = ''

    def __init__(self) -> None:
        self.__dbName__ = self.readEnvName()
        self.__dbEnv__ = self.readEnvMode()
        self.__dbType__ = self.readEnvType()
        if self.__dbType__ == ConnectionStringTypes.POSTGRES:
            # Read the extra values
            self.__dbUsername__ = str(getenv("NEWSBOT_DATABASE_USERNAME"))
            self.__dbPassword__ = str(getenv("NEWSBOT_DATABASE_PASSWORD"))
            self.__dbHost__ = str(getenv("NEWSBOT_DATABASE_HOST"))
            pass

        if self.__dbType__ == ConnectionStringTypes.SQLITE:
            self.__dbPath__ = self.readEnvDbPath()

        self.value: str = self.getConnectionString()

    def readEnvName(self) -> str:
        name = str(getenv("NEWSBOT_DATABASE_NAME")).lower()
        if name == "none":
            return self.__defaultName__
        else:
            return name

    def readEnvMode(self) -> str:
        mode = str(getenv("NEWSBOT_ENV")).lower()
        if mode == 'none':
            return ConnectionStringModes.PROD.value
        elif mode == 'dev':
            return ConnectionStringModes.DEV.value
        elif mode == 'test':
            return ConnectionStringModes.TEST.value

    def readEnvType(self) -> ConnectionStringTypes:
        res = str(getenv("NEWSBOT_DATABASE_TYPE")).lower()
        if res == "sqlite":
            return ConnectionStringTypes.SQLITE
        elif res == 'none':
            return ConnectionStringTypes.SQLITE
        elif res == "postgres":
            return ConnectionStringTypes.POSTGRES
        else:
            raise Exception("Invalid database type given.")

    def readEnvDbPath(self) -> str:
        res = str(getenv("NEWSBOT_SQLITE_PATH"))
        if res == "None":
            return self.__defaultPath__
        else:
            return res

    def getConnectionString(self) -> str:
        if self.__dbType__ == ConnectionStringTypes.SQLITE:
            res = "sqlite://ReplacePath"
            path = f"{self.__dbPath__}/{self.__dbName__}.db"
            res = res.replace("ReplacePath", path)
            # print(f"Setting connection string to: {res}")
            return res

        elif self.__dbType__ == ConnectionStringTypes.POSTGRES:
            res = "postgresql+psycopg2://username:password@host/databaseName"
            res = res.replace("username", self.__dbUsername__)
            res = res.replace("password", self.__dbPassword__)
            res = res.replace("host", self.__dbHost__)
            res = res.replace("databaseName", self.__dbName__)
            return res
        else:
            raise Exception("Invalid database type given.")
