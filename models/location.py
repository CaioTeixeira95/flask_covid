from app import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(15))
    business_hour = db.Column(db.String(100))
    street = db.Column(db.String(100))
    number = db.Column(db.String(10))
    zip_code = db.Column(db.String(9))
    neighborhood = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))

    def __repr__(self):
        return '<Location {}>'.format(self.name)
