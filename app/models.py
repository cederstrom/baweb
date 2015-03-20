from app import app, db
from wtforms.validators import Email, Regexp


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(
        db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(140), index=True, unique=True, nullable=False,
                      info={'validators': Email()})
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    generation = db.Column(db.Integer, nullable=False)
    favorite_sport = db.Column(db.String(128), index=False, unique=False,
                               nullable=False)
    best_dekk = db.Column(db.String(140), index=False, unique=False,
                          nullable=False)

    def __repr__(self):
        return '<User %r, is_admin=%r>' % (self.nickname, self.is_admin)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True, nullable=False)
    submit_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    email = db.Column(db.String(140), index=True, unique=True, nullable=False,
                      info={'validators': Email()})
    slogan = db.Column(db.String(140), nullable=False)
    city = db.Column(db.String(140), nullable=False)
    has_payed = db.Column(db.Boolean, default=False, nullable=False)
    members = db.relationship('TeamMember', backref='team', lazy='dynamic')
    # price: get from each member

    def __repr__(self):
        return '<Team %r>' % (self.name)

    def get_price(self):
        team_price = 0
        for member in self.members:
            team_price += member.get_price()
        return team_price


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    name_of_member = db.Column(db.String(140), nullable=False)
    person_number = db.Column(
        db.String(13), unique=True, nullable=False,
        info={'validators': Regexp("^[12]{1}[90]{1}[0-9]{6}-[0-9]{4}$",
              message=u"Skriv personnummer på formatet ååååmmdd-xxxx")})
    allergies = db.Column(db.String(140))
    need_bed = db.Column(db.Boolean, default=False, nullable=False)
    sfs = db.Column(db.Boolean, default=False, nullable=False)
    sittning = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Integer()
    # ticket_type = db.Column(db.String(12))

    def __repr__(self):
        return '<TeamMember %r, person_number=%r>' % (self.name_of_member,
                                                      self.person_number)

    def get_price(self):
        return app.config['FLUMRIDE']['TICKET_PRICE']
