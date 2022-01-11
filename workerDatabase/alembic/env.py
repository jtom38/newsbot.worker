from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from os import environ

from dotenv import load_dotenv

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

load_dotenv()

DB_USER = environ.get("NEWSBOT_DATABASE_USERNAME")
if DB_USER is None:
    raise Exception("Did not find a value from env 'NEWSBOT_DATABASE_USERNAME'.")

DB_PASS = environ.get("NEWSBOT_DATABASE_PASSWORD")
if DB_PASS is None:
    raise Exception("Did not find a value from env 'NEWSBOT_DATABASE_PASSWORD'.")

DB_HOST = environ.get("NEWSBOT_DATABASE_HOST")
if DB_HOST is None:
    raise Exception("Did not find a value from env 'NEWSBOT_DATABASE_HOST'.")

DB_NAME = environ.get("NEWSBOT_DATABASE_NAME")
if DB_NAME is None:
    raise Exception("Did not find a value from env 'NEWSBOT_DATABASE_NAME'.")


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    section = config.get_section(config.config_ini_section)
    url = section["sqlalchemy.url"]
    url = url.replace("USER", DB_USER)
    url = url.replace("PASS", DB_PASS)
    url = url.replace("HOST", DB_HOST)
    url = url.replace("DBNAME", DB_NAME)
    print(url)
    # url = section["sqlalchemy.url"].format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
    # print(f"alembic url: {url}")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    section = config.get_section(config.config_ini_section)
    url = section["sqlalchemy.url"]
    url = url.replace("USER", DB_USER)
    url = url.replace("PASS", DB_PASS)
    url = url.replace("HOST", DB_HOST)
    url = url.replace("DBNAME", DB_NAME)

    section["sqlalchemy.url"] = url
    connectable = engine_from_config(
        # config.get_section(config.config_ini_section),
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
