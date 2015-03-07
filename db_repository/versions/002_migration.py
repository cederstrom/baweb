from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
team_member = Table('team_member', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('team_id', Integer),
    Column('name', String(length=140)),
    Column('person_number', String(length=13)),
    Column('allergies', String(length=140)),
    Column('needBed', Boolean),
    Column('sfs', Boolean),
    Column('sittning', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['team_member'].columns['team_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['team_member'].columns['team_id'].drop()
