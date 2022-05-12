from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from main import get_app, db
from src.config import config as our_config
get_app()
target_metadata = db

config = context.config
fileConfig(config.config_file_name)

user = our_config['postgres']['db_user']
password = our_config['postgres']['db_password']
host = our_config['postgres']['db_host']
database = our_config['postgres']['db_database']

config.set_main_option('sqlalchemy.url', f'postgres://{user}:{password}@{host}/{database}')


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
