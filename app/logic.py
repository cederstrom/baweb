from datetime import datetime, timezone
from app import app, db
from app.models import TeamMember


def is_submit_open():
    flumride_config = app.config['FLUMRIDE']
    max_nr_of_not_sms_members = flumride_config['MAX_NR_OF_NOT_SFS']
    return (
        is_submit_open_date_passed() and
        get_members_non_sfs_count() < max_nr_of_not_sms_members)


def is_submit_open_date_passed():
    anmalan_open_at = app.config['FLUMRIDE']['SUBMIT_OPEN']
    print("Anmälan öppnar %r" % anmalan_open_at)
    return anmalan_open_at < datetime.now(timezone.utc)


def get_members_non_sfs_count():
    return db.session.query(TeamMember)\
        .filter(TeamMember.sfs.is_(False)).count()


def get_members_need_bed_count():
    return db.session.query(TeamMember)\
        .filter(TeamMember.need_bed.is_(True)).count()


def get_members_sitting_count():
    return db.session.query(TeamMember)\
        .filter(TeamMember.sittning.is_(True)).count()
