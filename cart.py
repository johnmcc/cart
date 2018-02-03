#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Representation of a cart object """

from cartitem import CartItem
from discounts import DiscountManager


class Cart:
    def __init__(self, user):
        """ Initialize a cart object. Parameter:
            - user - class User - user.py
        """
        self.items = []
        self.discounts = []
        self.user = user

        # Private
        self._total = 0

    @property
    def total(self):
        self._total = sum(item.product.price * item.quantity for item in self.items)
        DiscountManager(self).apply_discounts()
        return round(self._total, 2)

    def add_discount(self, discount):
        """ Adds a discount to the cart. Parameter:
            - discount - String

            Valid values for discount are:
            - bogof_discount
            - bulk_discount
            - loyalty_discount
        """
        if (discount not in self.discounts):
            self.discounts.append(discount)

    def remove_discount(self, discount):
        """ Removes a discount from the cart. Parameter:
            - discount - String

            Valid values for discount are
            - bogof_discount
            - bulk_discount
            - loyalty_discount
        """
        self.discounts.remove(discount)

    def add_item(self, product, quantity = 1):
        """ Add an item to the cart. Parameters:
            - product - Class Product - product.py
            - quantity - Integer - default 1
        """
        if (quantity <= 0):
            raise ValueError('You can only add one or more products to the cart')

        # First, check if the cart item exists (assuming the SKU is unique)
        cart_item = self.get_item_in_cart(product)

        if cart_item is None:
            # Create a new cart item and add it to the cart
            cart_item = CartItem(product, quantity)
            self.items.append(cart_item)
        else:
            cart_item.quantity += quantity

    def remove_item(self, product, quantity = 1):
        """ Remove an item from the cart. Parameters
            - product - Class Product - product.py
            - quantity - Integer - default 1
        """
        if(quantity <= 0):
            raise ValueError('You can only remove one or more products from the cart')

        cart_item = self.get_item_in_cart(product)

        if cart_item is not None:
            cart_item.quantity -= quantity

            # Delete the cart_item if quantity < 1
            if cart_item.quantity < 1:
                self.items.remove(cart_item)

    def get_item_in_cart(self, product):
        """ Return an item in the cart by sku. (e.g. for editing or deletion).
            Parameter:
            - product - Class Product - product.py
        """
        try:
            matches = [x for x in self.items if x.product.sku == product.sku].pop()
            return matches
        except IndexError:
            return None

    def empty(self):
        """ Deletes all items and discounts from the cart """
        self.items = []
        self.discounts = []
