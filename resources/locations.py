from flask_restful import fields, Resource, reqparse, marshal
from models.location import Location


parser = reqparse.RequestParser()
parser.add_argument(
    'name',
    type=str,
    help='Location\'s name',
    required=True
)
parser.add_argument(
    'email',
    type=str,
    help='Location\'s e-mail',
    required=True
)
parser.add_argument(
    'phone',
    type=str,
    help='Location\'s phone',
    required=True
)
parser.add_argument(
    'business_hour',
    type=list,
    location='json',
    help='Location\'s business hour',
    required=True
)
parser.add_argument(
    'street',
    type=str,
    help='Location\'s street',
    required=True
)
parser.add_argument(
    'number',
    type=str,
    help='Location\'s address number',
    required=True
)
parser.add_argument(
    'zip_code',
    type=str,
    help='Location\'s zip code',
    required=True
)
parser.add_argument(
    'neighborhood',
    type=str,
    help='Location\'s neighborhood',
    required=True
)
parser.add_argument(
    'state',
    type=str,
    help='Location\'s state',
    required=True
)
parser.add_argument(
    'city',
    type=str,
    help='Location\'s city',
    required=True
)
parser.add_argument(
    'country',
    type=str,
    help='Location\'s country',
    required=True
)


location_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'business_hour': fields.List(fields.String),
    'address': {
        'street': fields.String(attribute='street'),
        'number': fields.String(attribute='number'),
        'zip_code': fields.String(attribute='zip_code'),
        'neighborhood': fields.String(attribute='neighborhood'),
        'state': fields.String(attribute='state'),
        'city': fields.String(attribute='city'),
        'country': fields.String(attribute='country'),
    }
}


def marshal_location(location, business_hour=None):
    location_dict = location.__dict__
    if not business_hour:
        business_hour = location_dict['business_hour']
    location_dict['business_hour'] = business_hour.split(', ')
    return marshal(location_dict, location_fields)


class LocationResource(Resource):
    def get(self, location_id):
        location = Location.query.filter_by(id=location_id).first_or_404()
        return marshal_location(location)

    def post(self):
        from app import db
        args = parser.parse_args()
        business_hour = ', '.join(args.pop('business_hour'))
        new_location = Location(**args, business_hour=business_hour)
        db.session.add(new_location)
        db.session.commit()
        return marshal_location(new_location, business_hour)

    def put(self, location_id):
        from app import db
        for arg in parser.args:
            arg.required = False
        args = parser.parse_args()
        location = Location.query.filter_by(id=location_id).first_or_404()
        for key, value in args.items():
            setattr(location, key, value)
        db.session.commit()
        return location

    def delete(self, location_id):
        from app import db
        location = Location.query.filter_by(id=location_id).first_or_404()
        db.session.delete(location)
        db.session.commit()
        return {}, 204


class LocationListResource(Resource):
    def get(self):
        locations = []
        for location in Location.query.all():
            locations.append(marshal_location(location))
        return locations
