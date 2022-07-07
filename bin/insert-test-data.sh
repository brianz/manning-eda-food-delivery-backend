#!/bin/bash

HOST='http://localhost:5150'

curl --location --request POST "$HOST/menuitems" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "French fries",
        "description": "Yummy freedom/french fries",
        "price": "7.99",
        "size": "large"
    }'

curl --location --request POST "$HOST/menuitems" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "French fries",
        "description": "Yummy freedom/french fries",
        "price": "3.99",
        "size": "small"
    }'

curl --location --request POST "$HOST/menuitems" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Hamburger",
        "description": "A single-patty all-american burger",
        "price": "8.99"
    }'

curl --location --request POST "$HOST/menuitems" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Double Hamburger",
        "description": "A double-patty all-american burger",
        "price": "11.99"
    }'

curl --location --request POST "$HOST/menuitems" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Cheeseburger",
        "description": "A single-patty all-american burger with cheese",
        "price": "9.99"
    }'

curl --location --request POST "$HOST/menuitems" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Double Cheeseburger",
        "description": "A double-patty all-american burger with cheese",
        "price": "14.99"
    }'