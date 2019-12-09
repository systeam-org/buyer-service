"""Tests for Basic Functions"""
import sys
import json
import unittest
import mysql.connector
sys.path.append("../..")
from app import *

## Connecting to the database

## importing 'mysql.connector' as mysql for convenient
import mysql.connector as mysql

class TestFunctions(unittest.TestCase):

    """Test case for the client methods."""
    # Test of get_hello API
    def test_hello(self):
        with app.test_client() as c:
            res = c.get('/hello')
            # Passing the mock object
            response = b'Hello world'

            # Assert response
            self.assertEqual(res.data, response)

    # Test of get_categories API
    def test_get_categories(self):
        with app.test_client() as c:
            res = c.get('/categories')

            # Passing the mock object
            response = ["Furniture"]
            data = json.loads(res.get_data(as_text=True))
            # Assert response
            print(data)
            self.assertEqual(data, response)

    # Test of get_orders API
    def test_get_orders(self):
        with app.test_client() as c:
            res = c.get('/orders?email=praveen.thakur@sjsu.edu')

            # Passing the mock object
            response = [
                {
                    "order_id": 1,
                    "total_amount": 57,
                    "created_on": "2019-12-04 00:13:26",
                    "status": "Ordered",
                    "products": [
                        {
                            "product_name": "Armoire",
                            "product_id": 3,
                            "quantity": 1,
                            "unit_cost": 57
                        }
                    ]
                }
            ]
            data = json.loads(res.get_data(as_text=True))
            # Assert response
            print(data)
            self.assertEqual(data, response)

    # Test of get_products API
    def test_get_products(self):
        with app.test_client() as c:
            res = c.get('/products?email=praveen.thakur@sjsu.edu')

            # Passing the mock object
            response = [
                {
                    "product_id": 3,
                    "category_name": "Furniture",
                    "product_name": "Armoire",
                    "description": "Bedroom Armoire 2-door 2-drawers wardrobe storage closet cabinet wood Home NEW",
                    "price": "57",
                    "image": "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"
                }

            ]
            data = json.loads(res.get_data(as_text=True))
            # Assert response
            print(data)
            self.assertEqual(data, response)

    # Test of get_user API
    def test_get_user(self):
        with app.test_client() as c:
            res = c.get('/user?email=praveen.thakur@sjsu.edu')

            # Passing the mock object
            response = {
                "role": "Buyer-Seller"
            }

            data = json.loads(res.get_data(as_text=True))
            # Assert response
            self.assertEqual(data, response)

if __name__ == '__main__':
    unittest.main()