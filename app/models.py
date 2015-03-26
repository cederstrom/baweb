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

    def is_authenticated(self):
        return self.is_admin

    def is_active(self):
        return self.is_admin

    def is_anonymous(self):
        return not self.is_admin

    def get_id(self):
        return str(self.id)

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

    def __repr__(self):
        return '<Team %r>' % (self.name)

    @property
    def price(self):
        price = 0
        for member in self.members:
            price += member.price
        return price


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

    def __repr__(self):
        return '<TeamMember %r, person_number=%r>' % (self.name_of_member,
                                                      self.person_number)

    @property
    def price(self):
        if self.need_bed:
            return app.config['FLUMRIDE']['TICKET_PRICE_WITH_SOVSAL']
        return app.config['FLUMRIDE']['TICKET_PRICE']

    @staticmethod
    def get(id):
        return db.session.query(TeamMember).get(id)

    @staticmethod
    def need_bed_count():
        return TeamMember.query.filter_by(need_bed=True).count()

    @staticmethod
    def sitting_count():
        return TeamMember.query.filter_by(sittning=True).count()

    @staticmethod
    def not_sfs_count():
        return TeamMember.query.filter_by(sfs=False).count()
