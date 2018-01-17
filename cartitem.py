#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Representation of a CartItem """


class CartItem:
    def __init__(self, product, quantity):
        """ Parameters:
        - product - class Product - product.py
        - quantity - Int
        """
        self.product = product
        self.quantity = quantity

    def __str__(self):
        return self.product.title
