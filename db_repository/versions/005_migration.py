from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
team_member = Table('team_member', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('person_number', VARCHAR(length=13)),
    Column('allergies', VARCHAR(length=140)),
    Column('sfs', BOOLEAN),
    Column('sittning', BOOLEAN),
    Column('team_id', INTEGER),
    Column('need_bed', BOOLEAN),
    Column('ticket_type', VARCHAR(length=12)),
    Column('name_of_member', VARCHAR(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['team_member'].columns['ticket_type'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['team_member'].columns['ticket_type'].create()
