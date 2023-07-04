# baweb

## Requirements

Python 3.8

## Setup

```bash
$ git clone https://github.com/cederstrom/baweb.git
$ cd baweb
$ mkvirtualenv --python=/usr/bin/python3.8 baweb
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
cd baweb-prod
python
```

### Flytta medlem mellan lag
```python
from app.models import Team, TeamMember, User
from app import db

m = TeamMember.query.get(1)
Team.query.get(1).members.append(m)
Team.query.get(2).members.remove(m)

db.session.commit()
```

### Ta bort medlem
```python
from app.models import Team, TeamMember, User
from app import db

TeamMember.query.filter_by(id=1).delete()

db.session.commit()
```

### Ta bort alla lag och medlemmar
```python
from app.models import Team, TeamMember, User
from app import db

TeamMember.query.delete()
Team.query.delete()

db.session.commit()
```

### Lägga till admin ###
```python
from app.models import Team, TeamMember, User
from app import db

u = User(facebook_id=999999, nickname='nick name', email='name@example.com', is_admin=True, generation=99, favorite_sport='', best_dekk='')
db.session.add(u)

db.session.commit()
```
