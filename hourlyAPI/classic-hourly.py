#!/usr/bin/env python3
# -*- coding: utf 8 -*-
"""Launch the flask server

Attributes:
    migrate (Migrate): Flask object to deal with migration scripts

    manager (Manager): FLask object to apply migration script
"""

from flask_script import Manager

from hourly import app

manager = Manager(app)


# ============================================================================
# Main module
# ============================================================================
if __name__ == '__main__':
    # launch the application
    manager.run()