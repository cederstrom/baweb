from datetime import datetime
from app import app


def is_submit_open():
    print("Anmälan öppnar %r" % app.config['FLUMRIDE']['SUBMIT_OPEN'])
    return app.config['FLUMRIDE']['SUBMIT_OPEN'] < datetime.now()
