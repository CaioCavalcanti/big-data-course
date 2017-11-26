schema = {
    'username': {
        'type': 'string',
        'required': True,
        'unique': True
    },
    'password': {
        'type': 'string',
        'required': True
    },
    'roles': {
        'type': 'list',
        'allowed': ['user', 'admin'],
        'required': True,
    },
    'token': {
        'type': 'string',
        'required': True,
    }
}