import requests
import json
import accountManagement as am
import numpy as np
import marketInfo as mi

class Bot:
    def __init__(self,name,key,baseAsset="USDT",exchange="binance",url="https://signal.revenyou.io/paper/api/signal/v2/",extIdPath="extId.json"):
        self.name=name
        self.key=key
        self.url=url
        self.baseAsset=baseAsset
        self.exchange=exchange
        self.extIdPath=extIdPath
        
    def getPositions(self):
        signal=requests.get(self.url+"getBotAssetsPct?"+"signalProvider="+self.name+"&signalProviderKey="+self.key+"&exchange="+self.exchange+"&baseAsset="+self.baseAsset)
        return signal.json()

    def getOrders(self):
        signal=requests.get(self.url+"getOrders?"+"signalProvider="+self.name+"&signalProviderKey="+self.key)
        return signal.json()
    
    def cleanOrders(self):
        orders=self.getOrders()
        for order in orders["orders"]:
            extId=order["extId"]
            data={"signalProvider":self.name,"signalProviderKey":self.key,"extId":extId,}
            _=requests.post(self.url+"cancelOrder",json=data,headers={"content-type": "application/json"})
        
    def placeOrder(self,asset,price,qty,side):
        data={"signalProvider":self.name,
              "signalProviderKey":self.key,
              "extId":self.getNewId(),
              "exchange":self.exchange,
              "baseAsset":asset,
              "quoteAsset":self.baseAsset,
              "limitPrice":str(price),
              "qtyPct":str(qty),
              "side":side,
              "ttlType":"gtc",
              "type":"limit",
              "responseType":"FULL"}
                   
        signal=requests.post(self.url+"placeOrder",json=data,headers={"content-type": "application/json"})
        return signal.json()
    
    def getNewId(self):
        file=self.extIdPath
        with open(file) as json_file:
            data = json.load(json_file)
        res=data["extId"]
        newData={"extId":"a"+hex(int(res[1:],16)-1)}
        with open(file, 'w') as outfile:
            json.dump(newData, outfile)
        return res
    
    def getCurrentPortfolio(self,positions):
        currentDict={}
        baseAsset=0
        baseTotal=float(positions["baseTotal"])
        for position in positions["amounts"]:
            if position["orderId"]=='' and position["signalId"]=='':
                if position["asset"] == self.baseAsset:
                    baseAsset=float(position["amount"])/baseTotal
                else:
                    currentDict[position["asset"]]=float(position["amount"])/baseTotal
        return currentDict,baseAsset
	
    def getPortfolio(self):
        return self.getCurrentPortfolio(self.getPositions())[0]

    def rebalance(self,targetDict,eps=0.005):
        self.cleanOrders()
        positions=self.getPositions()
        baseTotal=float(positions["baseTotal"])
        currentDict,baseAsset=self.getCurrentPortfolio(positions)
        for coin in targetDict:
            if not(coin in currentDict):
                currentDict[coin]=0
        whiteList=list(targetDict.keys())
        flag,whiteList=am.notCloseEnough(currentDict,targetDict,whiteList,eps)
        flagBis=flag
        whiteListBis=whiteList.copy()
        while flag:
            positions=self.getPositions()
            currentDict,baseAsset=self.getCurrentPortfolio(positions)
            for coin in targetDict:
                if not(coin in currentDict):
                    currentDict[coin]=0
            flag,whiteList=am.notCloseEnough(currentDict,targetDict,whiteList,eps)
            orders=self.getOrders()
            ordersDict=am.getOrdersDict(orders)
            totalDict=am.sumDict(ordersDict,currentDict)
            flagBis,whiteListBis=am.notCloseEnough(totalDict,targetDict,whiteListBis,eps)
            while flagBis:
                self.multipleOrders(currentDict,targetDict,whiteList,baseAsset,baseTotal)
                orders=self.getOrders()
                ordersDict=am.getOrdersDict(orders)
                positions=self.getPositions()
                currentDict,baseAsset=self.getCurrentPortfolio(positions)
                for coin in targetDict:
                    if not(coin in currentDict):
                        currentDict[coin]=0
                totalDict=am.sumDict(ordersDict,currentDict)
                flagBis,whiteListBis=am.notCloseEnough(totalDict,targetDict,whiteListBis,eps)
                flag,whiteList=am.notCloseEnough(currentDict,targetDict,whiteList,eps)
        self.cleanOrders()

    def multipleOrders(self,currentDict,targetDict,whiteList,baseAsset,baseTot):
        for key in whiteList:
            if not(key in currentDict):
                qtyPct=targetDict[key]
                side=1
            else:
                diff=targetDict[key]-currentDict[key]
                qtyPct=abs(diff)
                side=np.sign(diff)
            if side==1:
                qty=qtyPct/baseAsset
            else:
                qty=qtyPct/currentDict[key]
            price=mi.getPrice(key,self.baseAsset)
            treshold=0.05
            order=self.placeOrder(key,price*(1+(treshold*side)),qty*baseTot,am.convertSide(side))

    def liquidate(self):
        positions=self.getPositions()
        currentDict,baseAsset=self.getCurrentPortfolio(positions)
        for key in currentDict:
            price=mi.getPrice(key,self.baseAsset)
            treshold=0.05
            self.placeOrder(key,price*(1-treshold),100,"sell")
                

#response = requests.get("http://api.open-notify.org/astros.json")
#signal="https://signal.revenyou.io/paper/api/signal/v2/getBotAssetsPct?signalProvider="+bot.name+"&signalProviderKey="+bot.key+"&exchange=binance&baseAsset=BTC"

#response = requests.post('https://httpbin.org/post', data = {'key':'value'})

#bot=Bot("Eolus","FUNWUDMFC8BZ4PEL")
