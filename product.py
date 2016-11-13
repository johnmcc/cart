#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Representation of a product object """


class Product:
    """ Parameters:
        - SKU - String
        - Title - String
        - Price - Float
    """
    def __init__(self, sku, title, price):
        self.sku = sku
        self.title = title
        self.price = price
        
        return None
    
    def __str__(self):
        return self.title