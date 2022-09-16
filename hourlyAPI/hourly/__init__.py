#!/usr/bin/env python3
# -*- coding: utf 8 -*-
"""Initialize the resolution module

The initialization follows the steps:
* load the service variables
* load the default variables (secret key, environment and log level)
* configure the environment for dev, stag or prod and overwrite default files
* load the configuration by default in the instance directory
* overwrite the default configuration with the configuration file of the instance
    directory according with execution environment (config_dev.py, config_stag.py
    or config_prod.py)

NB : files in the instance directory should be adapted to your own environment
"""

import os
import logging

from flask import Flask


# ============================================================================
# Configure the Flask application
# ============================================================================
app = Flask(__name__, instance_relative_config = True)

# load service information
app.config.from_object('config.service')

# Load the default configuration
app.config.from_object('config.default')

# load from environnement
app.config.from_object('config.environment')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
# The configuration file is loaded from instance directory
app.config.from_pyfile(app.config['APP_CONFIG_FILE'])

# check the environnement variables and connect to the database
app.config.from_object('config.check')

# ============================================================================
# Module importation
# ============================================================================
from . import common, errors
from . import routes, manager