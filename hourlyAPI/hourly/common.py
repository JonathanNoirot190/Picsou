#!/usr/bin/env python3
# -*- coding: utf 8 -*-
"""Useful functions and classes

This module provides some function to deal with extended response both for function
and for flask response in an uniform way.

Attributes:
    utc_date_format (str): Define the UTC date format

Classes:
    Pagination: Class that help to paginate output data where they are huge
    pgStatus  : Internal class to provide an extended error code for Postgresql 
        requests

Methods:
    status_response(status: int = 200, message: str = 'OK', key: str = None, data: Any = None) -> dict:
        Return a detailed status code, message and data for functions
    
    route_response(
        status: int  = 200, 
        message: str = 'OK', 
        key: str     = None, 
        data: Any    = None
    ) -> Flask.response_class: Return an extended Flask responses with a status, 
        a message and additional data (optional)

     status_to_route_response(status_resp: dict, status: int = None) -> Flask.response_class:
        convert a status message for function into a status flask response

    status_is_success(response: dict) -> bool: Check if the status response if 
        successful

    route_is_success(response: Flask.response_class) -> bool: Check if the flask
        response is successful

    get_response_key(response:dict) -> str: Get the key of additional data in a
        response of function

    check_json_keys(keys: list, data: dict) -> dict: Check if all the keys of a 
        list are in the dictionnary

    pmex_log(level: str, msg: str) -> None: Default logging function
"""


import logging
from functools import wraps
from typing import Any

from flask import jsonify
from flask.app import Flask

from .errors import *
#from . import db

# ============================================================================
# Global variables 
# ============================================================================
# define the UTC date format
utc_date_format = "%Y-%m-%d %H:%M:%SZ"
"""str: Define the UTC date format

"""

# ============================================================================
# Class Pagination 
# ============================================================================
# Pagination class for data pagination
class Pagination(object):
    """Implementation of the Pagination class

    This class manage the way to provide data using a sliding windows, ie a page.
    Each page of data is linked to the next and the previous next.

    Args:
        page (int, optional)    : The number of the current page. 
                                  Defaults to 1.
        pages (int, optional)   : The number of pages. 
                                  Defaults to 1.
        per_page (int, optional): The number of records per page. 
                                  Defaults to 1.
        total (int, optional)   : The number of records. 
                                  Defaults to 1.
        prev_num (int, optional): The number of the previous page. 
                                  Defaults to 0.
        next_num (int, optional): The number of the next page. 
                                  Defaults to 0.
    Attributes:
        page (int)    : The number of the current page.
        pages (int)   : The number of pages.
        per_page (int): The number of records per pages.
        total (int)   : The number of records.
        prev_num (int): The number of the previous page.
        next_num (int): The number of the next page.

    Methods:
        __init__ (
            self, 
            page:int, 
            pages:int, 
            per_pages:int, 
            total:int, 
            prev_num:int,
            next_num
        ) -> Pagination ; Constructor of the Pagination class

        __repr__(self) -> str: A string that represents a Pagination instance

        to_dict(self) -> dict: A dictionnary which the keys are the Pagination
            attributes and the associated values, the values of the instance for
            each attribute.
        
        from_dict(data: dict) -> "Pagination": define a new instance of Pagination
            from a dictionnary which the keys are exactly the attributes and their
            values, the values associated to the keys in the dictionnary.
    """
    def __init__(
        self, 
        page    : int = 1, 
        pages   : int = 1, 
        per_page: int = 1, 
        total   : int = 1, 
        prev_num: int = 0, 
        next_num: int = 0
    ) -> "Pagination":
        """Constructor of the Pagination Class

        """
        self.page     = page
        self.pages    = pages
        self.per_page = per_page
        self.total    = total
        self.prev_num = prev_num
        self.next_num = next_num

    def __repr__(self) -> str:
        """Represent a Pagination instance

        Returns:
            str: Representation of a Pagination instance
        """
        return '<page {}:{}>'.format(self.page,self.pages)

    def to_dict(self) -> dict:
        """Convert a page into a dict

        Returns:
            dict: A dictionnary with all attributes of the class
        """
        return {
            'page'      : self.page,
            'pages'     : self.pages,
            'per_page'  : self.per_page,
            'total'     : self.total,
            'prev_num'  : self.prev_num,
            'next_num'  : self.next_num
        }

    @staticmethod
    def from_dict(data: dict) -> "Pagination":
        """Convert a dictionnary into a Pagination instance

        All the attributes of Pagination are keys of the data dict

        Args:
            data (dict): Dictionnary to be converted

        Returns:
            Pagination: A new instance of Pagination
        """

        if check_json_keys(('page','per_page','pages'), data) is False:
            return None

        p = Pagination(
            page        = data['page'],
            pages       = data['pages'],
            per_page    = data['per_page'],
            total       = data['total'],
            prev_num    = data['prev_num'],
            next_num    = data['next_num']
        )
        return p

# ============================================================================
# Class pgStatus
# ============================================================================
class pgStatus:
    """Postgresql error code convertion

    For internal use only. This returns an improved error code by adding a message 
    to it. Useful for return codes of PostgreSQL

    Args:
        pg_status_str (str, optional): [description]. Defaults to ''.
    """
    def __init__(self, pg_status_str = ''):
        self.status  = False
        self.message = 'Status undetermined'

        if pg_status_str != '':
            self.status  = pg_status_str[1] == 't'
            self.message = pg_status_str[4:len(pg_status_str) - 2]

    def __repr__(self):
        return '<status {}: {}>'.format(self.status, self.message)

    def to_dict(self) -> dict:
        """Convert a dictionnary into a pgStatus instance

        Returns:
            dict: [description]
        """
        return {
            'status' : self.status,
            'message': self.message
        }

# ============================================================================
# Functions 
# ============================================================================
def status_response(status: int = 200, message: str = 'OK', key: str = None, data: Any = None) -> dict:
    """Return  code for functions

    Return a status code, a message and data as a value of a given key.
    Data are added if only the key is not None.

    If status is not provided, then it returns the OK status.
    If message is not provided, then it returns the standard message associated
    to the status. The standard messages are defined in errors.py

    Args:
        status (int, optional) : Status code of the response. Defaults to 200.
        message (str, optional): Message of the response. Defaults to 'OK'.
        key (str, optional)    : Key associated to the data. Defaults to None.
        data (Any, optional)   : Data associated with the response. Defaults to None.

    Returns:
        dict: A detailed response for functions

        By default, the ok response is
        {
            'status': 200,
            'message': 'OK'
        }

        The status code is taken among the HTTP error codes.
        data could be of any type
    """
    out = {
        'status' : int(status), 
        'message': message
    }

    if key is not None:
        out[str(key)] = data
    
    return out

def route_response(
        status: int  = 200, 
        message: str = 'OK', 
        key: str     = None, 
        data: Any    = None
    ) -> Flask.response_class:
    """Return  code for HTTP routes

    Return a status code, a message and data as a value of a given key as the
    body of a given HTTP response. The HTTP response has the same message and
    the same status code as status and messages

    If status is not provided, then it returns the OK status.
    If message is not provided, then it returns the standard message associated
    to the status. The standard messages are defined in errors.py

    Args:
        status (int, optional) : Status code of the response. Defaults to 200.
        message (str, optional): Message of the response. Defaults to 'OK'.
        key (str, optional)    : Key associated to the data. Defaults to None.
        data (Any, optional)   : Data associated with the response. Defaults to None.

    Returns:
        Flask.response_class: an HTTP response. The body is composed of a json 
            message

        By default, the ok message response is
        {
            'status_code': 200,
            'message': 'OK'
        }

        The status code is taken among the HTTP error codes.
        data could be of any type.
    """
    resp = jsonify(
        status_response(
            status  = status,
            message = message,
            key     = key,
            data    = data
        )
    )
    resp.status_code = status

    return resp

def status_to_route_response(status_resp: dict, status: int = None) -> Flask.response_class:
    """Convert a response to a function into an HTTP flask response

    The response is embedded in the body of the flask response and the status 
    code is given by status. If not defined, status code is exactly the same as
    the value of the key status in the status_resp.

    Args:
        status_resp (dict): Status response. Dictionnary with at least two keys:
            'status' and 'message'. Some additional data can be added as the value
            of a third key.
            The status_resp must contain at least the following keys:
                * 'status' (int)
                * 'message' (str)

        status (int, optional): Status of the HTTP response. If not None, overwrite
            the status code hold by the status_response. Defaults to None.

    Returns:
        Flask.response_class: HTTP flask response with the body contains the status
            response.
    """
    key  = None
    data = None
    if status is None:
        status = status_resp['status']

        key = get_response_key(status_resp)
        if key is not None:
            data = status_resp[key]

    return route_response(status  = status,
                          message = status_resp['message'],
                          key     = key,
                          data    = data
                        )

# 
def status_is_success(response: dict) -> bool:
    """Verify if a response is a success or not

    Args:
        response (dict): Response of a given function. The status_resp must 
            contain at least the following keys:
            * 'status' (int)
            * 'message' (str)

    Returns:
        bool: True is 'status' equals 200 False otherwise
    """
    if ('status' not in response) or (response['status'] != 200):
        return False
    
    return True

def route_is_success(response: Flask.response_class) -> bool:
    """Verify if an HTTP flask response is a success or not

    Args:
        response (Flask.response_class): HTTP flask response to be tested

    Returns:
        bool: True if response status code equals 200, Flase otherwise
    """
    if not response.status_code != 200:
        return False

    return status_is_success(response = (response.json() or {}))

def get_response_key(response:dict) -> str:
    """Get key of additional data

    In a response of a function, some data can be added using a given key chosen
    by the developer. In that case, the function has 'status' and 'message' as
    mandatory keys and an additional one that refers the data. This function
    returns that key.

    Args:
        response (dict): Response of a given function. The status_resp must 
            contain at least the following keys:
            * 'status' (int)
            * 'message' (str)

    Returns:
        str: The key that refers to additional data
    """
    if response is None:
        return None

    for key, values in response.items():
        if key != 'message' and key != 'status':
            return key

    return None

def check_json_keys(keys: list, data: dict) -> dict:
    """Check if keys are in a dict

    Args:
        keys (list of str) : List of key to check if they are in data or not
        data (dict)        : Dictionnary in which we are looking for keys

    Returns: 
        dict: The dictionnary is composed at least of 'status' and 'message' keys
        with 'status':
            * 200 for success
            * 400 status and the list of missing keys associated to the 'missing_keys' 
                key.
    """
    status  = 200
    message = 'OK'
    missing = []
    for k in keys:
        if k not in data:
            status  = 400
            message = error_codes['400']
            missing.append(k)
    
    return status_response(status = status, message = message,key = 'missing_keys', data = missing )


def db_health_check() -> dict:
    """Check the availability of the database

    Returns: A function response defined in common. The dictionnary is 
        composed of:\n
            * status (int, optional) : Status code of the response. Defaults to 200.
            * message (str, optional): Message of the response. Defaults to 'OK'.
            * key (str, optional)    : Key associated to the data. Defaults to None.
            * data (Any, optional)   : Data associated with the response. Defaults to None.
        The status: 
            * 200 for success
            * 408 when the database is not available
    """
    try:
        db.session.execute('SELECT 1;')
    except Exception:
        return status_response(status = 408, message ='DB Timeout')

    return status_response()

# ============================================================================
#  Decorators
# ============================================================================
def check_db_health(f):
    """Wrap API call to check if the db is available

    Args:
        f (function): Function to be decorated

    Returns:
        Flask.response: If the db is not available return a 408 response
            otherwise return the response of the called API
    """
    @wraps(f)
    def wrapped_db_check(*args, **kwargs):
        resp = db_health_check()
        if not status_is_success(resp):
            return status_to_route_response(resp)
        return f(*args, **kwargs)
    return wrapped_db_check