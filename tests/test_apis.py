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

    # Test of get_orders API
    def test_get_orders(self):
        with app.test_client() as c:
            res = c.get('/orders?email=praveen.thakur@sjsu.edu')

            # Passing the mock object
            response = []
            data = json.loads(res.get_data(as_text=True))
            # Assert response
            print(data)
            self.assertEqual(data, response)

    # Test of get_products API
    def test_get_products(self):
        with app.test_client() as c:
            res = c.get('/products?email=praveen.thakur@sjsu.edu')

            # Passing the mock object
            response = []
            data = json.loads(res.get_data(as_text=True))
            # Assert response
            print(data)
            self.assertEqual(data, response)

if __name__ == '__main__':
    unittest.main()