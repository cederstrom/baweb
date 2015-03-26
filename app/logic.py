from datetime import datetime, timezone
from app import app
from app.models import TeamMember


def is_submit_open():
    anmalan_open_at = app.config['FLUMRIDE']['SUBMIT_OPEN']
    is_open = anmalan_open_at < datetime.now(timezone.utc)
    return is_open


def get_milliseconds_until_submit_opens():
    submit_open = app.config['FLUMRIDE']['SUBMIT_OPEN']
    now = datetime.now(timezone.utc)
    delta_milliseconds = (submit_open - now).total_seconds() * 1000
    return int(round(delta_milliseconds))


def are_there_beds_left():
    max_nr_of_beds = app.config['FLUMRIDE']['MAX_NR_OF_NEED_BED']
    return TeamMember.need_bed_count() < max_nr_of_beds


def are_there_sittning_left():
    max_nr_of_sitting = app.config['FLUMRIDE']['MAX_NR_OF_SITTNING']
    return TeamMember.sitting_count() < max_nr_of_sitting


def get_number_of_non_sfs_left():
    max_nr_of_not_sfs = app.config['FLUMRIDE']['MAX_NR_OF_NOT_SFS']
    nr_of_not_sfs = TeamMember.not_sfs_count()
    return max_nr_of_not_sfs - nr_of_not_sfs
