import math as m
import numpy as np
import pandas as pd
from scipy.stats import linregress
from statistical_analysis import regulizer
from statsmodels.tsa.stattools import coint

def MarketReturns(X):
    return np.transpose((np.dot(np.transpose(X),np.ones((len(X),1)))/len(X)))[0]

def MarketIndex(X):
    returns=MarketReturns(X)
    temp=1
    res=[]
    for ret in returns:
        temp+=ret
        res.append(temp)
    return np.asarray(res)

def TokensIndex(X):
    Y=X.copy()
    Y[:,0]+=1
    for i in range(1,Y.shape[1]):
        Y[:,i]+=Y[:,i-1]
    return Y
    
def CointMat(X):
    mat=TokensIndex(X)
    n=len(mat)
    res=np.ones((n,n))
    for i in range(n-1):
        for j in range(i+1,n):
            _,pvalue,_=coint(X[i],X[j])
            res[i][j]=1-pvalue
            res[j][i]=1-pvalue
    return res

def CointPairs(X):
    mat=TokensIndex(X)
    n=len(mat)
    res=np.ones((n,n))
    for i in range(n-1):
        for j in range(i+1,n):
            _,pvalue,_=coint(X[i],X[j])
            if pvalue<0.05:
                print(coins[i],coins[j])

def CointVector(X):
    mat=TokensIndex(X)
    market=MarketIndex(X)
    n=len(mat)
    res=np.zeros((1,n))[0]
    for i in range(len(mat)):
        _,pvalue,_=coint(mat[i],market)
        res[i]=1-pvalue
    return res
        

def CointTokens(X):
    mat=TokensIndex(X)
    market=MarketIndex(X)
    n=len(mat)
    for i in range(len(mat)):
        _,pvalue,_=coint(mat[i],market)
        if pvalue<0.05:
            print(coins[i])

def LinRegressVector(X):
    mat=TokensIndex(X)
    market=MarketIndex(X)
    n=len(mat)
    slopes=np.zeros((1,n))[0]
    rvalues=np.zeros((1,n))[0]
    for i in range(n):
        slope, _ , r_value, _, _ = linregress(market,mat[i])
        slopes[i]=slope
        rvalues[i]=regulizer(r_value)
    return slopes,rvalues


#MarketReturns(np.asarray([X[0]]))

#CointVector(X)
#mat=TokensIndex(X)
#market=MarketIndex(X)
#plt.scatter(mat[0],market)
#linregress(mat[0],market)
#plt.scatter(mat[-1],market)
#linregress(mat[-1],market)


    
coins=['XEM', 'ZRX', 'ETH', 'BNB', 'XRP', 'LTC', 'BCH', 'XLM', 'EOS', 'LRC', 'MKR', 'BAT', 'ZIL', 'RLC',"BTC"]
import sys
import os
path=os.path.abspath(os.getcwd())
sys.path.insert(1, path+"\\..\\simulator")
from environment import Environment
from simulator import Simulator
from statistical_analysis import CovarianceMatrix
import datetime
start = datetime.datetime(2019, 1, 1, 0, 0, 0, 0)
end = datetime.datetime(2019, 7, 12, 0, 0, 0, 0)
environment=Environment()
environment.dataProcessing(coins,start,end,step=1)
X=[]
for coin in coins:
    X.append(list(environment.cache[coin]))
