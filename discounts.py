#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Handles discounts for cart objects """

import math


class DiscountManager:
    def __init__(self, cart):
        """ Apply discounts to a cart. Parameter:
            - cart - class Cart - cart.py
        """
        self.discounts = ('bogof_discount', 'bulk_discount', 'loyalty_discount')
        self.cart = cart

        return None

    def apply(self):
        """ Applies the relevant discounts for each cart order,
            in the order specified in self.discounts
        """
        # for each valid discount...
        for discount in self.discounts:
            # only apply the discount if it is set in the cart
            if(discount in self.cart.discounts):
                getattr(self, discount)()

        return None

    def bogof_discount(self):
        """ Buy one, get one free.
            If there multiples - e.g. 4 items, BOGOF should apply to each item
        """
        for item in self.cart.items:
            if item.quantity > 1:
                free_quantity = item.quantity - math.ceil(float(item.quantity) / 2)
                discount = free_quantity * item.product.price
                self.cart.set_total(self.cart.get_total() - discount)

        return None

    def bulk_discount(self):
        """ 10% off when the total > £20 after BOGOF """
        if self.cart.get_total() > 20:
            self.cart.set_total(self.cart.get_total() * 0.9)

        return None

    def loyalty_discount(self):
        """ 2% off when the user has a loyalty card """
        if self.cart.user.is_loyal:
            self.cart.set_total(self.cart.get_total() * 0.98)

        return None
