#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from user import User
from cart import Cart
from product import Product
from cartitem import CartItem


class TestCart(unittest.TestCase):
    def setUp(self):
        # Bob doesn't get a loyalty discount, Alice does
        self.user1 = User('Bob Test', 'bobtest@example.com', False)
        self.user2 = User('Alice Test', 'alicetest@example.com', True)

        self.cart1 = Cart(self.user1)
        self.cart2 = Cart(self.user2)

        self.product1 = Product('123456', 'Product 1', 9.99)
        self.product2 = Product('555555', 'Product 2', 30)

    def test_cart_add_item(self):
        # Add a single item
        self.cart1.add_item(self.product1)

        # Ensure that there's only one item, and quantity = 1
        self.assertEqual(len(self.cart1.items), 1)
        self.assertEqual(self.cart1.items[0].quantity, 1)

    def test_cart_add_item_twice(self):
        # Add the item twice - ensure there's only on item in self.cart1.items
        # (And that the quantity is now 2)
        self.cart1.add_item(self.product1)
        self.cart1.add_item(self.product1)
        self.assertEqual(len(self.cart1.items), 1)
        self.assertEqual(self.cart1.items[0].quantity, 2)

    def test_add_no_quantity_throws_error(self):
        # Adding a product with less than one quantity should throw an error
        with self.assertRaises(Exception) as context:
            self.cart1.add_item(self.product1, 0)

    def test_remove_item(self):
        # Add an item, remove it, make sure cart is empty
        self.cart1.add_item(self.product1)
        self.cart1.remove_item(self.product1)

        self.assertEqual(len(self.cart1.items), 0)

    def test_empty(self):
        # Add an item, empty the cart, make sure that self.cart1.items is empty
        self.cart1.add_item(self.product1)
        self.cart1.empty()

        self.assertEqual(len(self.cart1.items), 0)
        self.assertEqual(len(self.cart1.discounts), 0)

    def test_total(self):
        #  No discount - should be 9.99
        self.cart1.add_item(self.product1)
        self.assertEqual(self.cart1.get_total(), 9.99)

        self.cart1.empty()

        # Two items, no discount - should be 19.98
        self.cart1.add_item(self.product1, 2)
        self.assertEqual(self.cart1.get_total(), 19.98)

    def test_total_bogof(self):
        # check BOGOF functionality - should be (2 * 9.99) - 9.99
        self.cart1.add_item(self.product1, 2)
        self.cart1.add_discount('bogof_discount')
        self.assertEqual(self.cart1.get_total(), 9.99)

    def test_total_bogof_odd_quantity(self):
        # Check that carts with BOGOF charge for the correct number of items
        # e.g. Quantity 3: charge for 2. Quantity 4 > charge for 2 etc.
        # Should be (3 * 9.99) - 9.99
        self.cart1.add_item(self.product1, 3)
        self.cart1.add_discount('bogof_discount')
        self.assertEqual(self.cart1.get_total(), 19.98)

    def test_total_bogof_multiple_items(self):
        # Ensure BOGOF applies more than once where appropriate
        # Should be ((2 * 9.99) - 9.99) + ((2 * 30) - 30) = 39.99
        self.cart1.add_item(self.product1, 2)
        self.cart1.add_item(self.product2, 2)
        self.cart1.add_discount('bogof_discount')
        self.assertEqual(self.cart1.get_total(), 39.99)

    def test_total_bogof_other_items(self):
        # Check that BOGOF applies properly to a single item
        # with other items in the cart
        # Should be ((2 * 9.99) - 9.99) + 30
        self.cart1.add_item(self.product1, 2)
        self.cart1.add_item(self.product2, 1)
        self.cart1.add_discount('bogof_discount')
        self.assertEqual(self.cart1.get_total(), 39.99)

    def test_remove_discount(self):
        # Check removing a discount has the desired effect
        # Should be full price - 2 * 9.99
        self.cart1.add_item(self.product1, 2)
        self.cart1.add_discount('bogof_discount')
        self.cart1.remove_discount('bogof_discount')
        self.assertEqual(self.cart1.get_total(), 19.98)

    def test_bulk_discount(self):
        # Check bulk discount - should be (9.99 + 30) * 0.9
        self.cart1.add_item(self.product1)
        self.cart1.add_item(self.product2)
        self.cart1.add_discount('bulk_discount')
        self.assertEqual(self.cart1.get_total(), 35.99)

    def test_bogof_bulk(self):
        # Check BOGOF + bulk together - should be (9.99 + 9.99 - 9.99 + 30) * 0.9
        self.cart1.add_item(self.product1, 2)
        self.cart1.add_item(self.product2)
        self.cart1.add_discount('bulk_discount')
        self.cart1.add_discount('bogof_discount')
        self.assertEqual(self.cart1.get_total(), 35.99)

    def test_loyalty_discount(self):
        # Check loyalty discount - 9.99 * 0.98
        self.cart2.add_item(self.product1)
        self.cart2.add_discount('loyalty_discount')
        self.assertEqual(self.cart2.get_total(), 9.79)

    def test_bogof_and_loyalty(self):
        # Check BOGOF + loyalty. (9.99 + 9.99 - 9.99) * 0.98
        self.cart2.add_item(self.product1, 2)
        self.cart2.add_discount('loyalty_discount')
        self.cart2.add_discount('bogof_discount')
        self.assertEqual(self.cart2.get_total(), 9.79)

    def test_all_discounts(self):
        # Check BOGOF + bulk + loyalty. (((30 + 9.99 + 9.99 - 9.99) - 10%) - 2%)
        self.cart2.add_item(self.product2)
        self.cart2.add_item(self.product1, 2)
        self.cart2.add_discount('bogof_discount')
        self.cart2.add_discount('bulk_discount')
        self.cart2.add_discount('loyalty_discount')
        self.assertEqual(self.cart2.get_total(), 35.27)

    def test_item_in_cart(self):
        item = self.cart1.get_item_in_cart(self.product1.sku)
        self.assertIsNone(item)

        self.cart1.add_item(self.product1)
        item = self.cart1.get_item_in_cart(self.product1)
        self.assertIsInstance(item, CartItem)

if __name__ == '__main__':
    unittest.main()
