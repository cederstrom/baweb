from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
team_member = Table('team_member', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=140)),
    Column('person_number', VARCHAR(length=13)),
    Column('allergies', VARCHAR(length=140)),
    Column('needBed', BOOLEAN),
    Column('sfs', BOOLEAN),
    Column('sittning', BOOLEAN),
    Column('team_id', INTEGER),
)

team_member = Table('team_member', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('team_id', Integer),
    Column('name', String(length=140)),
    Column('person_number', String(length=13)),
    Column('allergies', String(length=140)),
    Column('need_bed', Boolean),
    Column('sfs', Boolean),
    Column('sittning', Boolean),
    Column('ticket_type', String(length=12)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['team_member'].columns['needBed'].drop()
    post_meta.tables['team_member'].columns['need_bed'].create()
    post_meta.tables['team_member'].columns['ticket_type'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['team_member'].columns['needBed'].create()
    post_meta.tables['team_member'].columns['need_bed'].drop()
    post_meta.tables['team_member'].columns['ticket_type'].drop()
