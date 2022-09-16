#!/usr/bin/env python3
# -*- coding: utf 8 -*-
"""Environment Script

Adapt environnement variable according to the execution environment (development,
staging or production)

Attributes:
    FLASK_ENV (str): Execution environment code among 'dev', 'stag' or 'prod'
    APP_CONFIG_FILE (str): Name of the config file to be loaded in the instance
        directory
"""

import os
from hourly import app

# ============================================================================
# Script 
# ============================================================================

# get the execution environment and choose the appropriate
# config file that is loaded from the instance directory
FLASK_ENV               = os.environ.get('FLASK_ENV') or 'prod'
os.environ['FLASK_ENV'] = FLASK_ENV
APP_CONFIG_FILE         = 'config.py'

# Overwrite the SERVICE_ENV to expose in the service description in which
# environment the service is running
if FLASK_ENV == 'dev':
    app.config.from_object('config.development')
    app.config['SERVICE_ENV'] = 'DEV'
    APP_CONFIG_FILE           = 'config_dev.py'
else:
    if FLASK_ENV == 'stag':
        app.config.from_object('config.staging')
        app.config['SERVICE_ENV'] = 'STAG'
        APP_CONFIG_FILE           = 'config_stag.py'
    else:
        app.config.from_object('config.production')
        app.config['SERVICE_ENV'] = 'PROD'
        APP_CONFIG_FILE           = 'config_prod.py'
        
app.config['APP_CONFIG_FILE'] = APP_CONFIG_FILE