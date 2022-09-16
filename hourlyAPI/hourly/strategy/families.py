import math as m
import numpy as np
import pandas as pd
import random as rand

class Families:
    def __init__(self,coins=[],nCoins=0):
        self.portfolios=[]
        self.coins=coins
        self.nCoins=nCoins
        
    def giveRandomFamilies(self,k):
        n=len(self.coins)
        nFamilies=max(round(n/self.nCoins),1)
        target=self.splitNumber(n,nFamilies)
        for j in range(k):
            temp=self.coins.copy()
            rand.shuffle(temp)
            portfolios=self.giveFamilies(self.initDict(temp),target)
            self.portfolios.append(portfolios)

    def initDict(self,coins):
        portfolio={}
        for coin in coins:
            portfolio[coin]=0
        return portfolio
            
    def reshape(self,nCoins,k):
        self.clean()
        self.nCoins=nCoins
        self.giveRandomFamilies(k)

    def clean(self):
        self.portfolios=[]

    def addCoins(self,newCoins):
        n=len(self.coins)
        m=len(newCoins)
        nFamilies=max(round(n/self.nCoins),1)
        newNFamilies=max(round((n+m)/self.nCoins),1)
        k=len(self.portfolios)
        targets=self.splitNumber(n+m,newNFamilies)
        for i in range(k):
            temp=newCoins.copy()
            rand.shuffle(temp)
            tempPortfolios=self.initDict(temp)
            jmax=len(self.portfolios[i])
            for j in range(jmax):
                tempPortfolios=self.modify(tempPortfolios,targets[j],i,j)
            if jmax<len(targets):
                portfolios=self.giveFamilies(tempPortfolios,targets[jmax:])
                self.portfolios[i]+=portfolios
        self.coins+=newCoins

    def modify(self,newPortfolios,target,i,j):
        current=len(self.portfolios[i][j])
        diff=target-current
        if diff>0:
            for _ in range(diff):
                coin=list(newPortfolios.keys())[-1]
                self.portfolios[i][j][coin]=newPortfolios.pop(coin)
        else:
            for _ in range(abs(diff)):
                coin=list(self.portfolios[i][j])[-1]
                newPortfolios[coin]=self.portfolios[i][j].pop(coin)
        return newPortfolios
        
    def fillFamilies(self,newPortfolios,nCoins,i):
        for j in range(len(self.portfolios[i])):
            while len(self.portfolios[i][j])!=nCoins and len(newPortfolios)>0:
                newCoin=list(newPortfolios.keys())[-1]
                self.portfolios[i][j][newCoin]=newPortfolios.pop(newCoin)
        return newPortfolios

    def dropFamilies(self,nCoins,i):
        newCoins=[]
        newPortfolios={}
        for j in range(len(self.portfolios[i])):
            while len(self.portfolios[i][j])!=nCoins and len(self.portfolios[i][j])>0:
                coin=list(self.portfolios[i][j].keys())[-1]
                newPortfolios[coin]=self.portfolios[i][j].pop(coin)
        return newPortfolios

    def giveFamilies(self,portfolios,targets):
        newPortfolios=[]
        coins=list(portfolios.keys())
        for target in targets:
            portfolio={}
            for _ in range(target):
                coin=coins.pop()
                portfolio[coin]=portfolios[coin]
            newPortfolios.append(portfolio)
        return newPortfolios

    def update(self,assetDict):
        newCoins=[]
        for coin in assetDict:
            if not(coin in self.coins):
                newCoins.append(coin)
        
        if newCoins!=[]:
            self.addCoins(newCoins)
        assetMap=self.mergePortfolios()  
        for batch in self.portfolios:
            for coins in batch:
                for coin in coins:
                    if assetMap[coin]>0:
                        coins[coin]=coins[coin]*(assetDict[coin]/assetMap[coin])

    def mapAssets(self):
        assetMap={}
        for batch in self.portfolios:
            for coins in batch:
                for coin in coins:
                    if not(coin in assetMap.keys()):
                        assetMap[coin]=coins[coin]
                    else:
                        assetMap[coin]+=coins[coin]
        return assetMap
    
    def mergePortfolios(self):
        totPortfolio=self.mapAssets()
        k=len(self.portfolios)
        dividedPortfolio={}
        for coin in totPortfolio:
            dividedPortfolio[coin]=totPortfolio[coin]/k
        return dividedPortfolio

    def splitNumber(self,n,k):
        res=[]
        res=[n//k]*k
        residual=n%k
        for i in range(residual):
            res[i]+=1
        return res

"""
coins=["ADA","ATOM","BAT","BNB","BTC","BTT","CRO","DASH","DOGE","ENJ","EOS","ETH","FTM"]
coins+=["LINK","LRC","LTC","MANA","NEO","NULS","OMG","THETA","TRX","VET"]
#coins+=["XEM","XLM","XMR","XRP","XTZ","ZEC"]
newCoins=["XEM","XLM","XMR","XRP","XTZ","ZEC"]
#newCoins+=["LINK","LRC","LTC","MANA","NEO","NULS","OMG","THETA","TRX","VET"]
families=Families(coins,8)
families.giveRandomFamilies(3)
     
#(nFamilies,target),(newNFamilies,newTarget)

for batch in families.portfolios:
    for coins in batch:
        for coin in coins:
            coins[coin]=rand.random()
       
"""
"""       
families=Families()    
families.nCoins=20
families.coins=['LRC', 'LTC', 'XTZ', 'MANA', 'MKR', 'LINK',
                'ENJ', 'TRX', 'BNB', 'STMX', 'XEM', 'BCH',
                'ANT', 'XLM', 'XRP', 'RLC', 'STORJ', 'ZRX',
                'BAT', 'BTC', 'ADA', 'DOGE', 'ETH', 'EOS',
                'ZIL', 'FTM', 'CRO', 'ATOM', 'SNX']

families.portfolios=[[{'BAT': -0.0, 'BTC': -0.0, 'XRP': -0.0, 'ZRX': -0.0, 'LINK': -0.0,
                       'MANA': -0.0, 'LRC': -0.0, 'DOGE': -0.0, 'XEM': -0.0,
                       'STMX': -0.0, 'ADA': -0.0, 'BNB': -0.0, 'STORJ': -0.0,
                       'BCH': -0.0, 'MKR': -0.0, 'XLM': -0.0, 'EOS': -0.0, 'ZIL': -0.0, 'LTC': -0.0,
                       'ENJ': -0.0, 'TRX': -0.0, 'RLC': -0.0, 'ANT': -0.0, 'ETH': -0.0, 'XTZ': -0.0,
                       'FTM': -0.0, 'CRO': -0.0, 'ATOM': -0.0, 'SNX': -0.0}],
                     [{'XTZ': -0.0, 'ETH': -0.0, 'XEM': -0.0, 'RLC': -0.0, 'BCH': -0.0, 'LRC': -0.0,
                       'ANT': -0.0, 'BTC': -0.0, 'MKR': -0.0, 'ADA': -0.0, 'STORJ': -0.0, 'MANA': 0.0,
                       'BNB': -0.0, 'ENJ': -0.0, 'DOGE': -0.0, 'XRP': -0.0, 'STMX': -0.0, 'LTC': -0.0,
                       'TRX': -0.0, 'ZIL': -0.0, 'XLM': -0.0, 'EOS': -0.0, 'ZRX': -0.0, 'BAT': -0.0,
                       'LINK': -0.0, 'FTM': -0.0, 'CRO': -0.0, 'ATOM': -0.0, 'SNX': -0.0}],
                     [{'ANT': -0.0, 'TRX': -0.0, 'ENJ': -0.0, 'MANA': 0.0, 'STORJ': -0.0, 'DOGE': -0.0,
                       'ETH': -0.0, 'BCH': -0.0, 'ZRX': -0.0, 'XRP': -0.0, 'RLC': -0.0, 'XEM': -0.0,
                       'XTZ': -0.0, 'BAT': -0.0, 'LRC': -0.0, 'ZIL': -0.0, 'STMX': -0.0, 'LINK': -0.0,
                       'XLM': -0.0, 'EOS': -0.0, 'BNB': -0.0, 'MKR': -0.0, 'LTC': -0.0, 'BTC': -0.0,
                       'ADA': -0.0, 'FTM': -0.0, 'CRO': -0.0, 'ATOM': -0.0, 'SNX': -0.0}],
                     [{'XLM': -0.0, 'ANT': -0.0, 'TRX': -0.0, 'BCH': -0.0, 'DOGE': -0.0, 'BNB': -0.0,
                       'LRC': -0.0, 'ZRX': -0.0, 'LINK': -0.0, 'STMX': -0.0, 'ZIL': -0.0, 'BAT': -0.0,
                       'XEM': -0.0, 'XRP': -0.0, 'ENJ': -0.0, 'EOS': -0.0, 'MKR': -0.0, 'BTC': -0.0,
                       'MANA': -0.0, 'ADA': -0.0, 'RLC': -0.0, 'STORJ': -0.0, 'XTZ': -0.0, 'LTC': -0.0,
                       'ETH': -0.0, 'FTM': -0.0, 'CRO': -0.0, 'ATOM': -0.0, 'SNX': -0.0}],
                     [{'LTC': -0.0, 'STMX': -0.0, 'LRC': -0.0, 'STORJ': -0.0, 'BNB': -0.0,
                       'BCH': -0.0, 'XTZ': -0.0, 'MANA': 0.0, 'BAT': -0.0, 'ANT': -0.0, 'ZIL': -0.0,
                       'XRP': -0.0, 'ENJ': -0.0, 'DOGE': -0.0, 'ADA': -0.0, 'LINK': -0.0, 'BTC': -0.0,
                       'RLC': -0.0, 'TRX': -0.0, 'MKR': -0.0, 'ETH': -0.0, 'EOS': -0.0, 'XEM': -0.0,
                       'XLM': -0.0, 'ZRX': -0.0, 'FTM': -0.0, 'CRO': -0.0, 'ATOM': -0.0, 'SNX': -0.0}]]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
current=families.mergePortfolios()
current["KAVA"]=0
#families.update(current)
"""
