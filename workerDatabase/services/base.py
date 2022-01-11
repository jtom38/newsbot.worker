# from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from .connection import ConnectionString

# SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN")
# engine = create_engine(ConnectionString().value)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
