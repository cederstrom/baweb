from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(140), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    generation = db.Column(db.Integer)
    favorite_sport = db.Column(db.String(128), index=False, unique=False)
    best_dekk = db.Column(db.String(140), index=False, unique=False)

    def __repr__(self):
        return '<User %r, is_admin=%r>' % (self.nickname, self.admin)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(140), index=True, unique=True)
    submit_date = db.Column(db.DateTime)
    email = db.Column(db.String(140), index=True, unique=True)
    slogan = db.Column(db.String(140))
    city = db.Column(db.String(140))
    has_payed = db.Column(db.Boolean, default=False)
    members = db.relationship('TeamMember', backref='team', lazy='dynamic')
    # price: get from each member

    def __repr__(self):
        return '<Team %r>' % (self.teamName)


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    name = db.Column(db.String(140))
    person_number = db.Column(db.String(13), unique=True)
    allergies = db.Column(db.String(140))
    need_bed = db.Column(db.Boolean)
    sfs = db.Column(db.Boolean)
    sittning = db.Column(db.Boolean)
    ticket_type = db.Column(db.String(12))

    def __repr__(self):
        return '<TeamMember %r, person_number=%r>' % (self.name, self.person_number)
