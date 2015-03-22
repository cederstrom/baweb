from datetime import datetime, timezone
from app import app, db
from app.models import TeamMember


def is_submit_open():
    anmalan_open_at = app.config['FLUMRIDE']['SUBMIT_OPEN']
    print("Anmälan öppnar %r" % anmalan_open_at)
    return anmalan_open_at < datetime.now(timezone.utc)


def get_milliseconds_until_submit_opens():
    submit_open = app.config['FLUMRIDE']['SUBMIT_OPEN']
    now = datetime.now(timezone.utc)
    delta_milliseconds = (submit_open - now).total_seconds() * 1000
    return int(round(delta_milliseconds))


def get_members_non_sfs_count():
    return db.session.query(TeamMember)\
        .filter(TeamMember.sfs.is_(False)).count()


def get_members_need_bed_count():
    return db.session.query(TeamMember)\
        .filter(TeamMember.need_bed.is_(True)).count()


def get_members_sitting_count():
    return db.session.query(TeamMember)\
        .filter(TeamMember.sittning.is_(True)).count()
