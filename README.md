# baweb

## Requirements

Python 3.x

## Setup

```bash
$ git clone https://github.com/cederstrom/baweb.git
$ cd baweb
$ mkvirtualenv --python=/usr/bin/python3 baweb
$ pip install -r requirements.txt
$ python db_create.py
```

## Run

```bash
$ python run.py
```

## Datebase cheatsheet

```bash
workon baweb-prod
```
```python
from app.models import Team, TeamMember, User
from app import db


### Flytta medlem mellan lag ###
m = TeamMember.query.get(21)
fromTeam = Team.query.get(2)
toTeam = Team.query.get(4)

m in fromTeam.members => True
m in toTeam.members => False

toTeam.members.append(m)
fromTeam.members.remove(m)

m in fromTeam.members => False
m in toTeam.members => True
db.session.commit()


### Ta bort medlem ###
TeamMember.query.filter_by(id=21).delete()
db.session.commit()


### Ta ort alla lag och medlemmar ###
TeamMember.query.delete()
Team.query.delete()
db.session.commit()


### Lägga till admin ###
u = User(nickname='nick name', email='nick@domian.topdomain', is_admin=True, generation=20, favorite_sport='', best_dekk='')
db.session.add(u)
db.session.commit()
```
