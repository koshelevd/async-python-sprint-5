import sys

from migration_tool.composite import alembic_runner

alembic_runner(*sys.argv[1:])
