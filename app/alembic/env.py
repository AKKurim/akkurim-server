import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection, engine_from_config, pool, text
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

# Import all models so they are registered on SQLModel.metadata for
# Alembic autogenerate support.
import app.models  # noqa: F401
from app.core.config import settings
from app.core.database import db_settings

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
# target_metadata = None


target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    return db_settings.DATABASE_URL


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connectable):
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations_sync)

    asyncio.run(do_run_migrations(connectable))


def do_run_migrations_sync(connection: Connection):
    def run_for_schema(schema: str):
        print(f"--- Migrating Schema: {schema} ---")

        # Ensure the tenant schema exists, then set the Postgres search path
        # so 'CREATE TABLE x' happens inside 'schema.x'
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        connection.execute(text(f'GRANT USAGE ON SCHEMA "{schema}" TO "czmatejt"'))
        connection.commit()
        connection.execute(text(f'SET search_path TO "{schema}"'))

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="public",
            # We don't use 'include_schemas=True' here because we are
            # manually switching the search_path instead.
        )

        with context.begin_transaction():
            context.run_migrations()
        connection.commit()

    for tenant in db_settings.ACTIVE_TENANTS:
        run_for_schema(tenant)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
