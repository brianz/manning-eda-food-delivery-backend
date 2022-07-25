import click
import requests

from foodie2ue.api import app    # noqa: W292, F401

SMALL = 'small'
MEDIUM = 'medium'
LARGE = 'large'

MENU_ITEMS = [
    {
        "name": "Hamburger",
        "description": "Delicious hamburger with one all-American beef patty",
        "price": "8.99",
    },
    {
        "name": "Cheeseburger",
        "description": "Delicious hamburger with one all-American beef patty with cheese",
        "price": "9.99",
    },
    {
        "name": "Bacon cheeseburger",
        "description": "Delicious hamburger with one all-American beef patty, cheese and bacon",
        "price": "11.99",
    },
    {
        "name": "Grilled cheese",
        "description": "A grilled cheese sandwich with cheddar cheese",
        "price": "7.99",
    },
    {
        "name": "French fries",
        "description": "Yummy freedom/french fries",
        "price": "1.99",
        "size": SMALL,
    },
    {
        "name": "French fries",
        "description": "Yummy freedom/french fries",
        "price": "2.99",
        "size": MEDIUM,
    },
    {
        "name": "French fries",
        "description": "Yummy freedom/french fries",
        "price": "4.99",
        "size": LARGE,
    },
]

ADD_ONS = [
    # NOTE:
    # make sure to keep this item, extra cheese, in position 0
    {
        "name": "Extra cheese", "description": "Add extra cheddar cheese", "price": 0.99
    },
    {
        "name": "Extra patty", "description": "An extra 1/3 lb all-beef patty", "price": 2.99
    },
    {
        "name": "Extra pickles", "price": 0.49
    },
    {
        "name": "Extra lettuce", "price": 0.99
    },
    {
        "name": "Extra mayo",
        "description": "Slather on some extra mayonaise goodness",
        "price": 0.99
    },
    {
        "name": "Extra ketchup", "description": "Add extra ketchup", "price": 0.99
    },
    {
        "name": "Extra tomatoes", "description": "Add extra tomatoes", "price": 0.99
    },
]
CUSTOMER_BRIAN = {
    "first_name": "Brian",
    "last_name": "Zambrano",
    "phone_number": "510-444-1234",
    "email": "brianz@gmail.com",
    "address": "123 main St.",
    "city": "Winter Park",
    "state": "CO",
    "zip": "80534"
}

CUSTOMER_MATT = {
    "first_name": "Matt",
    "last_name": "Diamond",
    "phone_number": "444-555-1212",
    "email": "matt.d.diamond@hotmail.com",
    "address": "123 main St.",
    "city": "Charlotte",
    "state": "NC",
    "zip": "23456"
}

ORDERS = [
    {
        "customer": CUSTOMER_BRIAN,
        "delivery_fee": "3.00",
        "items": [
            {
                "name": "Hamburger"
            },
            {
                "name": "Cheeseburger",
                "addons": [
                    {
                        "name": "Extra mayo",
                    },
                    {
                        "name": "Extra patty",
                    },
                ]
            },
            {
                "name": "Bacon cheeseburger", "addons": [
                    {
                        "name": "Extra mayo",
                    },
                ]
            },
            {
                "name": "French fries",
                "size": "large",
            },
        ]
    },
    {
        "customer": CUSTOMER_MATT,
        "delivery_fee": "5.00",
        "items": [
            {
                "name": "Cheeseburger"
            },
            {
                "name": "Cheeseburger"
            },
            {
                "name": "Cheeseburger"
            },
            {
                "name": "Bacon cheeseburger", "addons": [
                    {
                        "name": "Extra mayo"
                    },
                ]
            },
            {
                "name": "French fries", "size": LARGE
            },
            {
                "name": "French fries", "size": LARGE
            },
        ]
    },
    {
        "customer": CUSTOMER_MATT,
        "delivery_fee": "5.00",
        "items": [
            {
                "name": "Bacon cheeseburger"
            },
            {
                "name": "Grilled cheese"
            },
        ]
    },
]


def _fetch_burgers(menu_items):
    return (menu_items['Cheeseburger'], menu_items['Hamburger'], menu_items['Bacon cheeseburger'])


def _fetch_grilled_cheese(menu_items):
    return menu_items['Grilled cheese']


@app.cli.command("create-data")
@click.option("--host", default='http://127.0.0.1:5000')
def create_data(host):
    # Create menu items
    for item in MENU_ITEMS:
        response = requests.post(f"{host}/menuitems", json=item)

    # Get all of the menu item names
    all_menu_items = {item['name']: item for item in requests.get(f"{host}/menuitems").json()}

    # Create the addons for the burders
    for burger in _fetch_burgers(all_menu_items):
        for addon in ADD_ONS:
            response = requests.post(f"{host}/menuitems/{burger['id']}/addons", json=addon)
            print(response.json())

    # Create an addon for the grilled cheese
    grilled_cheese = _fetch_grilled_cheese(all_menu_items)
    response = requests.post(f"{host}/menuitems/{grilled_cheese['id']}/addons", json=ADD_ONS[0])
    print(response.json())

    # create some orders
    for order in ORDERS:
        response = requests.post(f"{host}/orders", json=order)
        print(response)
        print(response.json())
