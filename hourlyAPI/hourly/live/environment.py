import sys
import os
path=os.path.abspath(os.getcwd())
sys.path.insert(1, path+"/../manager")
from extractor import Extractor
from datetime import timedelta
class Environment:
    def __init__(self,cache={},volumes={},index=None,extractor=Extractor(),fees={"percent":0}):
        self.cache=cache
        self.volumes=volumes
        self.index=index
        self.extractor=extractor
        self.fees=fees

    def loadAll(self,start,end,step=1,path="../collector/coins_tracked"):
        files=os.listdir(path)
        coins=[]
        for file in files:
            coins.append(file[:-4])
        self.dataProcessing(coins,start,end,step)
                    
    def dataProcessing(self,coins,start,end,step):
        """
        Description :
        A method to extract and change the step of given coins data. The step is in second.
        It can for example transform data from 1 minute step to 4 hours step.

        Inputs :
        coins : list
        start,end : Datetime
        step : int (seconds)
        Outputs:
        None

        Example:
        >>> coins=['BTC','ETH']
        >>> start = datetime.datetime(2018, 1, 10, 0, 0, 0, 0)
        >>> end = datetime.datetime(2021, 9, 30, 0, 0, 0, 0)
        >>> step = 1
        >>> environment=Environment()
        >>> environment.dataProcessing(coins,start,end,step=step)
        """
        for coin in coins:
            df=self.extractor.extract_data(coin,start,end)
            if step!=3600:
                df=self.extractor.change_step(df,step*3600)
            self.cache[coin]=df["Price"]
            

    def assetValue(self,coin):
        """
        Description:
        Returns the value (in USD) of a given asset
        
        Inputs:
        coin: str
        
        Outputs :
        float
        """
        if self.index>=self.cache[coin].index[0]:
            return self.cache[coin].loc[self.index]
        else:
            return 0
    def getCache(self,lag,whiteList):
        """
        Description:
        Returns the lagged values at index for the coins in whiteList
        
        Inputs:
        index: datetime
        lag : int
        whiteList : set
        
        Outputs :
        cache : dict
        """
        cache={}
        delta=timedelta(hours=lag)
        for coin in whiteList:
            cache[coin]=self.cache[coin].loc[self.index-delta:self.index]
        return cache
         
