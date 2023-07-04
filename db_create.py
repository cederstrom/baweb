#Could not get the migrate stuff to work with sessions, another time perhaps.
#!/usr/bin/env python
from app import app, db

with app.app_context():
    db.create_all()
