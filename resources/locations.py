from flask_restful import fields, Resource, reqparse, marshal
from models.location import Location


def add_arguments(request_arguments, parser, required=True):
    for key, value in request_arguments.items():
        if value.get('location'):
            parser.add_argument(
                key,
                type=value.get('type'),
                location=value.get('location'),
                help=value.get('help'),
                required=required
            )
            continue
        parser.add_argument(
            key,
            type=value.get('type'),
            help=value.get('help'),
            required=required
        )


def replace_arguments(request_arguments, parser, required=True):
    for key, value in request_arguments.items():
        if value.get('location'):
            parser.replace_argument(
                key,
                type=value.get('type'),
                location=value.get('location'),
                help=value.get('help'),
                required=required
            )
            continue
        parser.replace_argument(
            key,
            type=value.get('type'),
            help=value.get('help'),
            required=required
        )


request_arguments = {
    'name': {
        'type': str,
        'help': 'Location\'s name',
    },
    'email': {
        'type': str,
        'help': 'Location\'s email',
    },
    'phone': {
        'type': str,
        'help': 'Location\'s phone',
    },
    'business_hour': {
        'type': list,
        'location': 'json',
        'help': 'Location\'s business hour',
    },
    'street': {
        'type': str,
        'help': 'Location\'s street',
    },
    'number': {
        'type': str,
        'help': 'Location\'s address number',
    },
    'zip_code': {
        'type': str,
        'help': 'Location\'s zip code',
    },
    'neighborhood': {
        'type': str,
        'help': 'Location\'s neighborhood',
    },
    'city': {
        'type': str,
        'help': 'Location\'s city',
    },
    'state': {
        'type': str,
        'help': 'Location\'s state',
    },
    'country': {
        'type': str,
        'help': 'Location\'s country',
    },
}

parser = reqparse.RequestParser()
add_arguments(request_arguments, parser)

parser_put = parser.copy()
replace_arguments(request_arguments, parser_put, False)

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
        args = parser_put.parse_args()
        location = Location.query.filter_by(id=location_id).first_or_404()
        for key, value in args.items():
            if value:
                if key == 'business_hour':
                    value = ', '.join(value)
                setattr(location, key, value)
        db.session.commit()
        location = Location.query.filter_by(id=location_id).first()
        return marshal_location(location)

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
