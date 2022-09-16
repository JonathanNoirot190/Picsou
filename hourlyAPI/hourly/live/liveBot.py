import sys
import os
path=os.path.abspath(os.getcwd())
sys.path.insert(1, path+"/../manager")
sys.path.insert(1, path+"/../strategy")
from trader import Trader
from liveTracker import Tracker
from portfolio import Portfolio
from families import Families
import statistical_analysis as sa
import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
import datetime
import json

class LiveBot:
    def __init__(self,environment,manager,tracker=Tracker(),parameters={}):
        self.environment=environment
        self.manager=manager
        self.tracker=tracker
        self.parameters=parameters
        self.fileAllow="trade.json"
        self.folder="flag"

    def trade(self):
        print("Trade !")
        self.manager.PortfolioManagement(self.tracker,self.environment)
        
    def trading(self):
        self.manager.families.nCoins=self.manager.parameters["nCoins"]
        flag=self.control(self.fileAllow)
        old_time=datetime.datetime.now()
        while flag:
            time=datetime.datetime.now()-datetime.timedelta(days=160)
            flag=self.control(self.fileAllow)
            condition=True
            if (time-old_time).seconds>=self.manager.timeDelta and condition:
                old_time=time
                old_time=old_time.replace(microsecond=0)
                self.environment.index=time
                self.environment.dataProcessing(self.manager.assets,time-datetime.timedelta(seconds=self.parameters["lag"]),time,self.parameters["step"])
                self.trade()
                self.tracker.savePortfolio(self.manager.botApi.getPortfolio(),old_time)
    
                
    def control(self,file):
        with open(self.folder+'/'+file,'r') as f:
            res=eval(json.load(f)["value"])
        return res
    
    
