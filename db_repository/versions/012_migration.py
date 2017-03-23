from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64), nullable=False),
    Column('email', String(length=140), nullable=False),
    Column('is_admin', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('generation', Integer, nullable=False),
    Column('favorite_sport', String(length=128), nullable=False),
    Column('best_dekk', String(length=140), nullable=False),
    Column('facebook_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['facebook_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['facebook_id'].drop()
