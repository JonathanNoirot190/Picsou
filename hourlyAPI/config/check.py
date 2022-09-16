#!/usr/bin/env python3
# -*- coding: utf 8 -*-
"""Checking script

This script aims to check the configuration before lanching the service and to
configure the db connection.

Attributes:
    basedir (str): Absolute path of the given file

Methods:
    get_env_variable(name:str): get environment variables
"""

__author__     = "Johann BARBIER"
__copyright__  = "Copyright 2021, PMEx plateform project"
__credits__    = ["Johann BARBIER", "Gilles MALARD"]
__license__    = "Proprietary"
__maintainer__ = "Johann BARBIER"
__email__      = "johann.barbier@pmex.io"

import logging
import os

from hourly import app

# ============================================================================
# Definition of global variables
# ============================================================================
basedir = os.path.abspath(os.path.dirname(__file__))

# ============================================================================
# Definition of fucntions
# ============================================================================
def get_env_variable(name:str):
    """Get an environment variable by its name to store it in app.conf context.

    Args:
        name (str): name of the variable

    Raises:
        Exception: when the variable is not set

    Returns:
        : The value of the variable
    """
    try:
        return os.environ[name]
    except KeyError:
        message = 'Expected environment variable {} not set.'.format(name)
        logger.log(level = logging.CRITICAL, msg = message)
        raise Exception(message)

# ============================================================================
# Script 
# ============================================================================

# the values of those depend on your setup
# complete with db connextion and other mandatory variables
MANDATORY_VA = ["POSTGRES_URL", "POSTGRES_USER", "POSTGRES_PW", "POSTGRES_DB"]
for va in MANDATORY_VA:
    if va not in app.config:
        app.config[va] = get_env_variable(va)

# alchemy configuration: Set up the database connection
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user = app.config['POSTGRES_USER'],
    pw   = app.config['POSTGRES_PW'],
    url  = app.config['POSTGRES_URL'],
    db   = app.config['POSTGRES_DB']
    )
SQLALCHEMY_DATABASE_URI        = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
