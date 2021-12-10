"""0.1.0 Changes

Revision ID: c77ad08fa772
Revises: 1e72dcb284c9
Create Date: 2021-04-04 15:48:07.364376

"""
from alembic.op import create_table
from sqlalchemy import Column, String, Boolean, Integer

# revision identifiers, used by Alembic.
revision = "c77ad08fa772"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    create_table(
        'articles',
        Column("id", String, primary_key=True),
        Column('sourceId', String),
        Column("tags", String),
        Column("title", String),
        Column("url", String),
        Column("pubDate", String),
        Column("video", String),
        Column("videoHeight", Integer),
        Column("videoWidth", Integer),
        Column("thumbnail", String),
        Column("description", String),
        Column("authorName", String),
        Column("authorImage", String)
    )

    create_table(
        'discordQueue',
        Column("id", String, primary_key=True),
        Column('articleId', String)
    )

    create_table(
        "discordwebhooks",
        Column("id", String, primary_key=True),
        Column("name", String),
        Column("key", String),
        Column("url", String),
        Column("server", String),
        Column("channel", String),
        Column("enabled", Boolean),
        Column("fromEnv", Boolean)
    )

    create_table(
        "icons",
        Column("id", String, primary_key=True),
        Column("filename", String),
        Column("site", String),
    )

    create_table(
        "settings",
        Column("id", String, primary_key=True),
        Column("key", String),
        Column("value", String),
        Column("options", String),
        Column("notes", String)
    )

    create_table(
        "sources",
        Column("id", String, primary_key=True),
        Column('site', String),
        Column('name', String),
        Column("source", String),
        Column("type", String),
        Column("value", String),
        Column("enabled", Boolean),
        Column("url", String),
        Column("tags", String),
        Column("fromEnv", Boolean)
    )

    create_table(
        "sourcelinks",
        Column("id", String, primary_key=True),
        Column("sourceID", String),
        Column("sourceType", String),
        Column("sourceName", String),
        Column("discordID", String),
        Column('discordName', String),
    )


def downgrade():
    pass
