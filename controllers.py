import datetime

from dateutil.parser import isoparse


def create_model(model):
    fields = {}
    for field, spec in model.fields.items():
        is_time_object = False
        print(f'Please enter your value for {field}, this should be of type: {spec["type"].__name__}')
        if spec.get('choices'):
            print(f'These are the possible choices: {spec["choices"]}')
        if spec.get('message'):
            print(spec['message'])
        if spec['type'] is datetime.datetime:
            print('Please enter your value in the format yyyy-mm-ddThh:mm:ss')
            is_time_object = True
        if spec['type'] is datetime.date:
            print('Please enter your value in the format yyyy-mm-dd')
            is_time_object = True
        if spec.get('default') is not None:
            print(f'(Leave blank to default to: {spec["default"]})')
        while True:
            value = input()
            try:
                if value == '' and spec.get('default') is not None:
                    value = spec['default']
                    if callable(value):
                        value = value()
                    fields[field] = value
                    break

                if is_time_object:
                    value = isoparse(value)
                else:
                    value = spec['type'](value)
                if spec.get('choices'):
                    if value not in spec['choices']:
                        raise ValueError('invalid choice')
                fields[field] = value
                break
            except ValueError:
                print('Invalid input, try again:')

    instance = model(**fields)
    return instance
