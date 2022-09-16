import sys
import os
path=os.path.abspath(os.getcwd())
sys.path.insert(1, path+"/../strategy")
from families import Families
from trader import Trader
from portfolio import Portfolio

class Manager:
    def __init__(self,function=None,trader=Trader(),families=Families(),botApi=None,parameters={},assets=set(),startCash=1,timeDelta=3600):
        self.function=function
        self.parameters=parameters
        self.assets=assets
        self.startCash=startCash
        self.timeDelta=timeDelta
        self.portfolio=Portfolio()
        self.trader=trader
        self.families=families
        self.botApi=botApi
  

    def PortfolioManagement(self,tracker,environment):
        """
        Description :
        Manage the portfolio through a given strategy.
        """
        whiteList=set()
        lag=self.parameters["lag"]
        for coin in environment.cache:
            if environment.index >= environment.cache[coin].index[lag]:
                whiteList.add(coin)
                if not(coin in self.portfolio.assetDict.keys()):
                    self.portfolio.assetDict[coin]=0
        if whiteList!=set():
            if self.families.portfolios==[]:
                k=self.parameters["k"]
                self.families.coins=list(whiteList)
                self.families.giveRandomFamilies(k)
            self.families.update(whiteListDict(self.portfolio.GetRatioDict(self.botApi),whiteList))
            tracker.backlog["flag"]=True
            ordersCondition=True
            if ordersCondition:
                temp=tracker.tradeCountDict.copy()
                targetPortfolio=self.computeOptimalPortfolio(environment,tracker,lag)
                tracker.tradeMatrix.append((DiffDict(temp,tracker.tradeCountDict),environment.index))
                self.botApi.rebalance(targetPortfolio)
                
            
    def computeOptimalPortfolio(self,environment,tracker,lag):
        for i in range(len(self.families.portfolios)):
            for j in range(len(self.families.portfolios[i])):
                self.families.portfolios[i][j]=self.function(self.families.portfolios[i][j],
                                                            environment.getCache(lag,list(self.families.portfolios[i][j].keys())),
                                                            self.parameters,
                                                            environment.fees["percent"],
                                                            tracker,
                                                            environment.index)
        return self.families.mergePortfolios()
    
     
def DiffDict(dict1,dict2):
    temp={}
    for key in dict1:
        temp[key]=abs(dict1[key]-dict2[key])
    return temp        

def IncreaseRf(cashDict,rfr):
    for key in cashDict:
        cashDict[key]=cashDict[key]*(1+rfr)
    return cashDict

def whiteListDict(assetDict,whiteList):
    whiteDict={}
    for coin in whiteList:
        if coin in assetDict.keys():
            whiteDict[coin]=assetDict[coin]
        else:
            whiteDict[coin]=0
    return whiteDict
