"""Alembic environment shared by the three ETEMAD databases (S01-024).

The target database is chosen by the ``etemad_role`` option in the ini file
(``central`` by default) and its URL comes from ``ROLE_ENV``. No URL is stored
in the repository; a migration without an explicit target refuses to run.
"""

from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None

_ROLE_ENV = {
    "central": "ETEMAD_DB_CENTRAL_URL",
    "domestic": "ETEMAD_DB_DOMESTIC_URL",
    "foreign": "ETEMAD_DB_FOREIGN_URL",
}


def _url() -> str:
    role = (config.get_main_option("etemad_role") or "central").strip()
    env_name = _ROLE_ENV.get(role)
    if env_name is None:
        raise SystemExit(f"unknown etemad_role {role!r}; expected one of {sorted(_ROLE_ENV)}")
    url = os.getenv(env_name, "").strip()
    if not url:
        raise SystemExit(
            f"{env_name} is not set; refusing to run a migration without an explicit target"
        )
    return url


def run_migrations_offline() -> None:
    context.configure(
        url=_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_url(), poolclass=pool.NullPool, future=True)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
