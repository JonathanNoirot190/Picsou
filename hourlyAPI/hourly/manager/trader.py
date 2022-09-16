from numpy import sign
from order import Order

class Trader:
    def __init__(self):
        self.orders=set()
    
    def makeOrders(self,portfolio,targetPortfolio,environment):
        totValue=portfolio.GetValue(environment)
        ratioDict=portfolio.GetRatioDict(environment)
        for coin in ratioDict:
            value = targetPortfolio[coin]-ratioDict[coin]
            side = sign(value)
            if side!=0:
                target = abs(value)
                amount=target*totValue/environment.assetValue(coin)
                self.orders.add(Order(coin,amount,side))
               
    
    
    def SplitOrders(self):
        buyOrders=set()
        sellOrders=set()
        for order in self.orders:
            if order.side+1:
                buyOrders.add(order)
            else:
                sellOrders.add(order)
            
        return buyOrders,sellOrders

    def executeOrders(self,portfolio,tracker,environment):
        """
        Description :
        Rebalance the portfolio according to it weights
        """
        buyOrders,sellOrders=self.SplitOrders()
        
        totValue=portfolio.GetValue(environment)
        for order in sellOrders:
            portfolio.assetDict[order.coin]-=order.amount
            portfolio.cash+=order.amount*environment.assetValue(order.coin)*(1-environment.fees["percent"])
            tracker.tradeCountDict[order.coin]+=order.amount*environment.assetValue(order.coin)/totValue
        newTotValue=portfolio.GetValue(environment)
        delta=newTotValue/totValue
        for order in buyOrders:
            portfolio.cash-=order.amount*environment.assetValue(order.coin)*delta
            portfolio.assetDict[order.coin]+=order.amount*delta*(1-environment.fees["percent"])
            tracker.tradeCountDict[order.coin]+=order.amount*environment.assetValue(order.coin)*delta/newTotValue

        self.orders=set()




    
    
