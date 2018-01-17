#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Representation of a User object """


class User:
    """ Parameters:
        - name - String
        - email - String
        - is_loyal - Boolean
    """
    def __init__(self, name, email, is_loyal):
        self.name = name
        self.email = email
        self.is_loyal = is_loyal
    
    def __str__(self):
        return self.name
