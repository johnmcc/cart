#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Handles discounts for cart objects """

import math
from DiscountTypes import DiscountTypes

class DiscountManager:
    def __init__(self, cart):
        """ Apply discounts to a cart. Parameter:
            - cart - class Cart - cart.py
        """
        self.cart = cart

    def apply_discounts(self):
        """ Applies the relevant discounts for each cart order,
            in the order specified in self.discounts
        """
        # for each valid discount...
        for discount in list(DiscountTypes):
            # only apply the discount if it is set in the cart
            if(discount in self.cart.discounts):
                getattr(self, discount.value)()

    def bogof_discount(self):
        """ Buy one, get one free.
            If there are multiples - e.g. 4 items, BOGOF should apply to each item
        """
        bogof_discount = 0
        for item in self.cart.items:
            if item.quantity > 1:
                bogof_discount += (math.floor(item.quantity / 2) * item.product.price)

        self.cart._total -= bogof_discount

    def bulk_discount(self):
        """ 10% off when the total > £20 after BOGOF """
        if self.cart._total > 20:
            self.cart._total *= 0.9

    def loyalty_discount(self):
        """ 2% off when the user has a loyalty card """
        if self.cart.user.is_loyal:
            self.cart._total *= 0.98
