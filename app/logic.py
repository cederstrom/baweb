from datetime import datetime, timezone
from app import app
from app.models import TeamMember


def is_submit_open():
    anmalan_open_at = app.config['FLUMRIDE']['SUBMIT_OPEN']
    is_open = anmalan_open_at < datetime.now(timezone.utc)
    return is_open

def has_submit_closed():
    anmalan_closes_at = app.config['FLUMRIDE']['SUBMIT_CLOSE']
    is_closed = anmalan_closes_at < datetime.now(timezone.utc)
    return is_closed

def get_milliseconds_until_submit_opens():
    submit_open = app.config['FLUMRIDE']['SUBMIT_OPEN']
    now = datetime.now(timezone.utc)
    delta_milliseconds = (submit_open - now).total_seconds() * 1000
    return int(round(delta_milliseconds))

def get_number_of_tickets_for_this_type_left(ticket_type):
    max_number_of_tickets = app.config['FLUMRIDE']['ticket_types'][ticket_type]['max_nr']
    return max_number_of_tickets - TeamMember.ticket_count_by_type(ticket_type)

def get_number_of_non_sfs_left():
    max_nr_of_not_sfs = app.config['FLUMRIDE']['MAX_NR_OF_NOT_SFS']
    nr_of_not_sfs = TeamMember.not_sfs_count()
    return max_nr_of_not_sfs - nr_of_not_sfs
