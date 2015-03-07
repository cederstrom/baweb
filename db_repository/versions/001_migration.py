from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
team = Table('team', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('teamName', String(length=140)),
    Column('submit_date', DateTime),
    Column('email', String(length=140)),
    Column('slogan', String(length=140)),
    Column('city', String(length=140)),
    Column('has_payed', Boolean, default=ColumnDefault(False)),
)

team_member = Table('team_member', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('person_number', String(length=13)),
    Column('allergies', String(length=140)),
    Column('needBed', Boolean),
    Column('sfs', Boolean),
    Column('sittning', Boolean),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=140)),
    Column('is_admin', Boolean, default=ColumnDefault(False)),
    Column('generation', Integer),
    Column('favorite_sport', String(length=128)),
    Column('best_dekk', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['team'].create()
    post_meta.tables['team_member'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['team'].drop()
    post_meta.tables['team_member'].drop()
    post_meta.tables['user'].drop()
