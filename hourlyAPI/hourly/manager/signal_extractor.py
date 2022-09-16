import sys
import os
path=os.path.abspath(os.getcwd())
sys.path.insert(1, path+"\\..\\strategy")
sys.path.insert(1, path+"\\..\\simulator")
from cryptotrader_simulator import Simulator
import datetime as datetime
import Strategy as Strat
import portfolio_management as pm
import portfolio_function as pf


def ExtractSignal(cache,families,index,cashDict,stocksDict,ratioDict,fees,params):
    backlog={"flag":False}
    coreRatioDict={}
    tradeCountDict={}
    i=0
    oldRatioDict=ratioDict.copy()
    for coins in families:
        for coin in families[coins]:
            coreRatioDict[coin]=0
            tradeCountDict[coin]=0
            i+=1
    tradeCountDict,cashDict,stocksDict,ratioDict,backlog,families=function(cache,families,index,tradeCountDict,cashDict,stocksDict,ratioDict,coreRatioDict,fees,params,backlog)
    return GetSignal(oldRatioDict,ratioDict)     

def GetSignal(oldRatioDict,ratioDict):
    resDict=ratioDict.copy()
    for coin in resDict:
        resDict[coin]-=oldRatioDict[coin]
    return resDict


"""
#Coins
coins=["BTC","ETH","BNB"]
families={"coins":coins}

#Parameters
fees={"percent":0.025,"fixed":0}
totcoins=[]
for obj in families.values():
    totcoins+=obj
lag=500
managementParameters={"fun":pf.optimalWeights,"core":0,"lag":500,"risk":0.2,"addCash":True,"arbitrage":False,"autoFamilies":False}
function=pm.ModernManagement

#Dates
#now=datetime.datetime.today()
#index=datetime.datetime(now.year,now.month,now.day,now.hour)
index = datetime.datetime(2021, 8, 1, 0, 0, 0, 0)
start=index-datetime.timedelta(hours=lag)


#Initializing
simulator=Simulator()
simulator.data_processing(totcoins,start,index,step=1)

n=sum([len(obj) for obj in families.values()])

cache=simulator.cache
params=managementParameters

stocksDict={}
ratioDict={}
cashDict={}

i=0
for coins in families:
    cashDict[coins]=1
    for coin in families[coins]:
        ratioDict[coin]=0
        stocksDict[coin]=0
        i+=1

signal=ExtractSignal(cache,families,index,cashDict,stocksDict,ratioDict,fees,params)
"""
