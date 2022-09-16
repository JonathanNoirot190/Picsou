import sys
import os
path=os.path.abspath(os.getcwd())
sys.path.insert(1, path+"/../strategy")
sys.path.insert(1, path+"/../manager")
sys.path.insert(1, path+"/../botapi")
from manager import Manager
from environment import Environment
from liveBot import LiveBot
from bots_api import Bot
import datetime as datetime
import portfolio_management as pm
import portfolio_function as pf


coins=["BTC","ETH","LTC"]
fees={"percent":0.0025,"fixed":0}
environment=Environment(fees=fees)
botApi=Bot("Eolus","FUNWUDMFC8BZ4PEL")
managementParameters={"fun":pf.optimalWeights,"lag":500,"risk":0.1,"rfr":0,"rf":0,"nCoins":20,"k":1}
manager=Manager(function=pm.ModernManagement,botApi=botApi,parameters=managementParameters,assets=set(coins),timeDelta=1)
liveBot=LiveBot(environment,manager,parameters={"lag":600*3600,"step":3600})
res=liveBot.trading()


