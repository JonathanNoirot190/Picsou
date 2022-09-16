#!/usr/bin/env python3
# -*- coding: utf 8 -*-
"""Implement the resolutionAPI shell context 

"""


from hourly import app

@app.shell_context_processor
def make_shell_context() -> dict:
    """Wrap the application context into the shell context

    Returns:
        dict: a dictionnary with a key-value pairs where the key is the name of
            the object within the shell context and the value the instance of
            the object
    """
    # return collected object accessible to the shell context
    return {}