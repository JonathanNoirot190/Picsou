#!/usr/bin/env python3
# -*- coding: utf 8 -*-
from flask import Flask, request
from . import app
from .common import *
from .collector.tracker import tracking
from .manager.management import trading

import os

@app.route('/hello', methods = ['GET'])
def blank() -> Flask.response_class:
    infos_var = ['SERVICE_NAME']
    descr = {}
    for info in infos_var:
        descr[info] = app.config[info]
    return route_response(key='service', data = descr)

@app.route('/data-collect', methods = ['POST'])
def collect() -> Flask.response_class:
    infos_var = ['SERVICE_NAME']
    descr = {}
    for info in infos_var:
        descr[info] = app.config[info]

    print(os.getcwd())

    # Dev
    tracking("coins_to_track.json","../prices",'config/coins',10)

    # Prod
    # tracking("coins_to_track.json","/hourly/prices",'config/coins',10)
    
    return route_response(key='service', data = descr)

@app.route('/trade', methods = ['POST'])
def simulate() -> Flask.response_class:
    infos_var = ['SERVICE_NAME']
    descr = {}
    for info in infos_var:
        descr[info] = app.config[info]

    print(os.getcwd())

    files={"file_tracker":"../prices","file_data":"data",'path_users':'config/users/','path_coins':'config/coins/'}
    params={'long_window':48,'short_window':24,'super_short_window':4,'isplot':False}

    trading(files,params,time_delta = 20, coeff = 115)


    return route_response(key = 'service', data = descr)