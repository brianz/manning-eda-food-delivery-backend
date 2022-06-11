from pprint import pprint as pp

from foodie2ue.domain import model


def test_foo():
    data = {
        'name': 'hamburger',
        'description': 'juicy hamburger',
        'size': 'regular',
        'price': 7.99,
    }

    result = model.MenuItem.load(data)

    pp(result)
