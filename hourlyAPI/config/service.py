#!/usr/bin/env python3
# -*- coding: utf 8 -*-
"""Service configuration

  This script aims to configure all variables related to the service.
  Standard fields are the following ones:\n

  SERVICE_NAME: Name of the service

  SERVICE_CAT : Its category among:
    RS:  for Referential Service
    BS:  for Business Service
    AS:  for Application Service
    TS:  for Technical Service
    BFF: for Backend-for-Front-end Service

  SERVICE_FUNC: Its functional family

  SERVICE_ID: Unique ID given by platform administrator respecting the following rules:
    TS:  from 1 000
    RS:  from 2 000
    BS:  from 3 000
    AS:  from 4 000
    BFF: from 5 000
    All the services are registered in a Service Book

  SERVICE_STATUS: Public when a service is exposed outside the platform, Private otherwise

  SERVICE_ENV: Current execution environnement (DEV, STAG, PROD).
    Will be overwritten by the effective execution context

  SERVICE_DESCR: The plain text description of the service

  SERVICE_VERSION: Its version expressed in MAJ.MIN.PACT with each expressed with 2 digits

  SERVICE_AUTHORS: List of the authors

  Additional and specific fields:

  SERVICE_SUPPORTED_ALGORITHM: Provide the implemented algorithms

  SERVICE_SUPPORTED_MATCHING: Provide the name of the implemented matching strategies

  SERVICE_SUPPORTED_NEGOTIATION: Provice the name of the implemented negotiation strategies
"""

SERVICE_NAME    = 'CryptoBot Hourly'
SERVICE_CAT     = 'BS'
SERVICE_FUNC    = 'Algorithm Service'
SERVICE_ID      = '3OO1'
SERVICE_STATUS  = 'Private'
SERVICE_ENV     = 'Production'
SERVICE_DESCR   = 'To Be Completed Later'
SERVICE_VERSION = '00.01.00b'
