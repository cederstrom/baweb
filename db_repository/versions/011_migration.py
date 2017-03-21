from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('team_id', INTEGER),
    Column('name_of_member', VARCHAR(length=140), nullable=False),
    Column('person_number', VARCHAR(length=13), nullable=False),
    Column('allergies', VARCHAR(length=140)),
    Column('ticket_type', INTEGER, nullable=False),
    Column('sfs', BOOLEAN, nullable=False),
)

team_member = Table('team_member', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('team_id', Integer),
    Column('name_of_member', String(length=140), nullable=False),
    Column('person_number', String(length=13), nullable=False),
    Column('allergies', String(length=140)),
    Column('ticket_type', Integer, nullable=False, default=ColumnDefault(False)),
    Column('sfs', Boolean, nullable=False, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['team_member'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['team_member'].drop()
