from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
team = Table('team', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('teamName', VARCHAR(length=140)),
    Column('submit_date', DATETIME),
    Column('email', VARCHAR(length=140)),
    Column('slogan', VARCHAR(length=140)),
    Column('city', VARCHAR(length=140)),
    Column('has_payed', BOOLEAN),
)

team = Table('team', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('submit_date', DateTime),
    Column('email', String(length=140)),
    Column('slogan', String(length=140)),
    Column('city', String(length=140)),
    Column('has_payed', Boolean, default=ColumnDefault(False)),
)

team_member = Table('team_member', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=140)),
    Column('person_number', VARCHAR(length=13)),
    Column('allergies', VARCHAR(length=140)),
    Column('sfs', BOOLEAN),
    Column('sittning', BOOLEAN),
    Column('team_id', INTEGER),
    Column('need_bed', BOOLEAN),
    Column('ticket_type', VARCHAR(length=12)),
)

team_member = Table('team_member', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('team_id', Integer),
    Column('name_of_member', String(length=140)),
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
    pre_meta.tables['team'].columns['teamName'].drop()
    post_meta.tables['team'].columns['name'].create()
    pre_meta.tables['team_member'].columns['name'].drop()
    post_meta.tables['team_member'].columns['name_of_member'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['team'].columns['teamName'].create()
    post_meta.tables['team'].columns['name'].drop()
    pre_meta.tables['team_member'].columns['name'].create()
    post_meta.tables['team_member'].columns['name_of_member'].drop()
