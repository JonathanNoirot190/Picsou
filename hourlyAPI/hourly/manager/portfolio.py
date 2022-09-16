
class Portfolio:
    
    def __init__(self,cash=0,assetDict={}):
        self.cash=cash
        self.assetDict=assetDict
        
        
    def GetValue(self,environment):
        """
        Description :
        Return the value of the portfolio according to the number of coins hold in stocksDict and the money in moneyDict
        
        Outputs :
        res : float
        """
        res=self.cash
        for coin in self.assetDict:
            res+=self.assetDict[coin]*environment.assetValue(coin)       
        return res

    def GetRatioDict(self,botApi):
        """
        Description :
        Return the state of the portfolio in terms of percentage of allocation.
        
        Outputs :
        ratioDict : dict 
        """
        return botApi.getCurrentPortfolio(botApi.getPositions())[0]

    def GetAssets(self):
        return list(self.assetDict.keys())
