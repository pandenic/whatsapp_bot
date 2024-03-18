"""Add selector and repeat interval


Revision ID: 36385f28ad45
Revises: 9080a8a4fb60
Create Date: 2024-03-18 00:32:06.939121

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic_postgresql_enum import TableReference
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "36385f28ad45"
down_revision: Union[str, None] = "9080a8a4fb60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum(
        "GREETING",
        "CREATE_REMINDER",
        "SHOW_ACTIVE_REMINDERS",
        "DELETE_REMINDER",
        "CREATE_REPEATABLE_REMINDER",
        name="selector",
    ).create(op.get_bind())
    op.add_column(
        "botuser",
        sa.Column(
            "selector_status",
            postgresql.ENUM(
                "GREETING",
                "CREATE_REMINDER",
                "SHOW_ACTIVE_REMINDERS",
                "DELETE_REMINDER",
                "CREATE_REPEATABLE_REMINDER",
                name="selector",
                create_type=False,
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "reminder",
        sa.Column(
            "repeat_interval",
            postgresql.ENUM(
                "NON_REPEAT",
                "EVERYDAY",
                "EVERY_WEEK",
                "EVERY_MONTH",
                "EVERY_YEAR",
                name="repeatinterval",
                create_type=False,
            ),
            nullable=False,
        ),
    )
    op.sync_enum_values(
        "public",
        "repeatinterval",
        ["NON_REPEAT", "EVERYDAY", "EVERY_WEEK", "EVERY_MONTH", "EVERY_YEAR"],
        [
            TableReference(
                table_schema="public",
                table_name="reminder",
                column_name="repeat_interval",
            )
        ],
        enum_values_to_rename=[],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values(
        "public",
        "repeatinterval",
        ["everyday", "every_week", "every_month", "every_year"],
        [
            TableReference(
                table_schema="public",
                table_name="reminder",
                column_name="repeat_interval",
            )
        ],
        enum_values_to_rename=[],
    )
    op.drop_column("reminder", "repeat_interval")
    op.drop_column("botuser", "selector_status")
    sa.Enum(
        "GREETING",
        "CREATE_REMINDER",
        "SHOW_ACTIVE_REMINDERS",
        "DELETE_REMINDER",
        "CREATE_REPEATABLE_REMINDER",
        name="selector",
    ).drop(op.get_bind())
    # ### end Alembic commands ###
