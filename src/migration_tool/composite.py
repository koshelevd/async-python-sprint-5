import logging.config
import os

from alembic.config import CommandLine, Config

from migration_tool.config import alembic_settings
from settings.db import Settings as DbSettings
from utils.logger_config import make_logger_conf

if os.getenv('DEV_CONFIG'):
    db_settings = DbSettings(_env_file=os.getenv('DEV_CONFIG'))
else:
    db_settings = DbSettings()


def make_config():
    config = Config()
    config.set_main_option('script_location',
                            alembic_settings.ALEMBIC_SCRIPT_LOCATION)
    config.set_main_option('version_locations',
                           alembic_settings.ALEMBIC_VERSION_LOCATIONS)
    config.set_main_option('sqlalchemy.url', db_settings.get_db_url(True))
    config.set_main_option('file_template',
                           alembic_settings.ALEMBIC_MIGRATION_FILENAME_TEMPLATE)
    config.set_main_option('timezone', 'UTC')

    return config


def alembic_runner(*args):
    log_config = make_logger_conf(
        alembic_settings.log_config,
        log_level=alembic_settings.LOGGING_LEVEL,
        json_log=alembic_settings.LOGGING_JSON
    )
    logging.config.dictConfig(log_config)

    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))
