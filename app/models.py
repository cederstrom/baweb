# -*- coding: utf-8 -*-
from app import app, db
from flask_login import UserMixin
from wtforms.validators import Email, Regexp

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(
        db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(140), index=True, unique=True, nullable=False,
                      info={'validators': Email()})
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    generation = db.Column(db.Integer, nullable=False)
    favorite_sport = db.Column(db.String(128), index=False, unique=False, nullable=False)
    best_dekk = db.Column(db.String(140), index=False, unique=False, nullable=False)
    google_id = db.Column(db.String(255), index=True, unique=True, nullable=True)

    @staticmethod
    def get_from_email(email):
        if not email:
            return None

        return User.query.filter(
            db.func.lower(User.email) == email.strip().lower()
        ).first()

    @staticmethod
    def get_from_google_id(google_id):
        if not google_id:
            return None

        return User.query.filter_by(google_id=google_id).first()

    def __repr__(self):
        return '<User %r, is_admin=%r, email=%r, google_id=%r>' % (
            self.nickname,
            self.is_admin,
            self.email,
            self.google_id
        )

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True, nullable=False)
    submit_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    email = db.Column(db.String(140), nullable=False, info={'validators': Email()})
    slogan = db.Column(db.String(140), nullable=False)
    city = db.Column(db.String(140), nullable=False)
    has_payed = db.Column(db.Boolean, default=False, nullable=False)
    members = db.relationship('TeamMember', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team %r>' % (self.name)

    @property
    def price(self):
        price = 0
        for member in self.members:
            price += member.price
        return price

    @staticmethod
    def get(id):
        return db.session.query(Team).get(id)

class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    nickname = db.Column(db.String(140))
    person_number = db.Column(db.String(13), unique=True, nullable=False,
    info={'validators': Regexp("^[12]{1}[90]{1}[0-9]{6}-[0-9]{4}$",
          message=u"Skriv personnummer på formatet ååååmmdd-xxxx")})
    email = db.Column(db.String(140), nullable=False, info={'validators': Email()})
    mobile_number = db.Column(db.String(13))
    ticket_type = db.Column(db.Integer, default=False, nullable=False)
    has_payed = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Integer()

    @property
    def price(self):
        return app.config['ÖHLREISE']['ticket_types'][self.ticket_type]['price']

    @staticmethod
    def get(id):
        return db.session.query(Beer).get(id)

    @staticmethod
    def ticket_count_by_type_beer(ticket_type):
        return Beer.query.filter_by(ticket_type=ticket_type).count()


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    name_of_member = db.Column(db.String(140), nullable=False)
    person_number = db.Column(
        db.String(13), unique=True, nullable=False,
        info={'validators': Regexp("^[12]{1}[90]{1}[0-9]{6}-[0-9]{4}$",
              message=u"Skriv personnummer på formatet ååååmmdd-xxxx")})
    allergies = db.Column(db.String(140))
    drink_option = db.Column(db.Integer, default=False, nullable=True)
    ticket_type = db.Column(db.Integer, default=False, nullable=False)
    sfs = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Integer()

    def __repr__(self):
        return '<TeamMember %r, person_number=%r>' % (self.name_of_member,
                                                      self.person_number)

    @property
    def price(self):
        return app.config['FLUMRIDE']['ticket_types'][self.ticket_type]['price']

    @staticmethod
    def get(id):
        return db.session.query(TeamMember).get(id)

    @staticmethod
    def ticket_count_by_type(ticket_type):
        return TeamMember.query.filter_by(ticket_type=ticket_type).count()

    @staticmethod
    def not_sfs_count():
        return TeamMember.query.filter_by(sfs=False).count()
