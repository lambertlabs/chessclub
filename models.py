import datetime


class Model:
    fields = {}

    def __init__(self, **kwargs):
        for field, spec in self.fields.items():
            try:
                value = kwargs[field]
            except KeyError:
                value = spec.get('default')
                if callable(value):
                    value = value()
                if value is None:
                    raise ValueError(f'{field} not provided and no default set')

            setattr(self, field, value)
        self.validate()

    def to_dict(self):
        return {
            field: getattr(self, field) for field in self.fields
        }

    def validate(self):
        for field, spec in self.fields.items():
            value = getattr(self, field)
            if not isinstance(value, spec['type']):
                raise ValueError(f'"{field}" must be of type: {spec["type"]}')
            if spec.get('choices') and value not in spec['choices']:
                raise ValueError(f'"{field}" must be one of: {spec["choices"]}')


class Player(Model):
    fields = {
        'first_name': {
            'type': str,
        },
        'last_name': {
            'type': str,
        },
        'date_of_birth': {
            'type': datetime.date,
        },
        'sex': {
            'type': str,
            'choices': ['male', 'female', 'other']
        },
        'rating': {
            'type': float,
            'default': 0.0
        },
    }


class Tournament(Model):
    fields = {
        'name': {
            'type': str,
        },
        'venue': {
            'type': str,
        },
        'start_date': {
            'type': datetime.date,
        },
        'end_date': {
            'type': datetime.date,
        },
        'number_of_rounds': {
            'type': int,
            'default': 4,
        },
        'time_control': {
            'type': str,
            'choices': ['bullet', 'blitz', 'rapid']
        },
        'description': {
            'type': str,
        },
        'status': {
            'type': str,
            'choices': ['created', 'in_progress', 'completed'],
            'default': 'created',
        },
        'players': {
            'type': list,
            'default': list,
            'message': 'Enter "[]" to leave empty and add later.'
        }
    }


class Round(Model):
    fields = {
        'tournament_id': {
            'type': int,
        },
        'round_number': {
            'type': int,
        },
        'pairings': {
            'type': list,
        },
        'timestamp': {
            'type': datetime.datetime
        },
        'status': {
            'type': str,
            'choices': ['created', 'completed'],
            'default': 'created'
        }
    }
