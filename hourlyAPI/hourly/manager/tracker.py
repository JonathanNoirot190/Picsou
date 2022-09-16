import sys
import os
path=os.path.abspath(os.getcwd())
sys.path.insert(1, path+"/../simulator")
from cache import Cache

class Tracker:
    def __init__(self,tradeCountDict={},tradeMatrix=[],backlog={},cache=Cache()):
        self.tradeCountDict=tradeCountDict
        self.tradeMatrix=tradeMatrix
        self.backlog=backlog
        self.cache=cache
        self.save=False
        self.tracking=False
        
    def getTradeCount(self):
        tradeCount=0
        for count in self.tradeCountDict.values():
            tradeCount+=count
        return tradeCount

    
        
