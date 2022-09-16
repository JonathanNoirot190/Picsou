import math as m
import numpy as np
import pandas as pd
from scipy import signal
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.stattools import adfuller

def regulizer(x):
    return (np.exp(x**2) - np.exp(0))/(np.exp(1)-np.exp(0))

def MDD(df):
    maxs=DropMultiple(df.cummax())
    mins=DropMultiple(df.iloc[::-1].cummin()).iloc[::-1]
    mdd=0
    for i in range(len(maxs)):
        indexMax=maxs.index[i]
        indexMin=mins.loc[indexMax:].index[0]
        temp=(mins.loc[indexMin]/maxs.loc[indexMax])-1
        if temp<mdd:
            mdd=temp
    return -mdd

def DropMultiple(df):
    data=[]
    index=[]
    for i in range(len(df)):
        if not(df[i] in data):
            data.append(df[i])
            index.append(df.index[i])
    return pd.Series(data=data,index=index)

def variationVector(df,log):
    res=[]
    for i in range(1,len(df)):
        if log:
            res.append(np.log(df[i]/df[i-1]))
        else:
            res.append((df[i]/df[i-1])-1)
    return res

def ComputeReturns(df,log=True):
    df=df[1:]/df[0]
    #if log:
        #df.apply(np.log)
    if log:
        df=[np.log(i) for i in df]
    return df

def EVMatrix(X,log=True):
    X=variationVector(np.transpose(X),log)
    return np.transpose(np.dot(np.transpose(X),np.ones((len(X),1)))/len(X))[0]

def LassoEstimator(X):
    y=np.asarray(X)
    n=len(y)
    alpha= abs((y.mean()-1)*5)
    clf = Lasso(alpha=alpha)
    x=np.asarray([i for i in range(n)]).reshape(n,1)
    clf.fit(x,y)
    return float(clf.coef_),float(clf.intercept_)

def LinearEstimator(df):
    y=np.asarray(df)
    n=len(y)
    x=np.asarray([i for i in range(n)]).reshape(n,1)
    reg=LinearRegression().fit(x,y)
    return float(reg.coef_),float(reg.intercept_)

def NaiveEstimator(df):
    return (df[-1]-df[0])/len(df),0


def ButterEstimator(y):
    res=ButterFilter(y)
    return (res[-1]-res[0])/len(res),0

def ButterFilter(sig,fc=0.1,fe=60):
    f_nyq = fe / 2
    b, a = signal.butter(4, fc/f_nyq, 'low', analog=False)
    s_but = signal.filtfilt(b, a, sig)
    return s_but    
    
def RegressionEstimator(X,fun,i):
    coeff,intercept=fun(X)
    return coeff*i + intercept

def CovarianceMatrix(X,log=True):
    X=variationVector(np.transpose(X),log)
    return np.cov(np.transpose(X),ddof=0)

def CorrelationMatrix(X,log=True):
    X=variationVector(np.transpose(X),log)
    return np.corrcoef(np.transpose(X),ddof=0)

def StartEndMonth(df):
    start=[df.index[0]]
    end=[]
    for i in range(1,len(df.index)):
        if df.index[i].day==1 and df.index[i].hour==0:
            if not(df.index[i] in start):
                start.append(df.index[i])
            if not(df.index[i-1] in end):
                end.append(df.index[i-1])
    if not(df.index[-1] in end):
        end.append(df.index[-1])
    return start,end

def MinMaxMonth(df):
    start,end=StartEndMonth(df)
    maxMonth=-1
    minMonth=10000
    for i in range(len(start)):
        perf=(df.loc[end[i]]/df.loc[start[i]])-1
        if perf>maxMonth:
            maxMonth=perf
        if perf<minMonth:
            minMonth=perf
    return minMonth,maxMonth
        
def DSD(X):
    res=0
    for obj in X:
        if obj<0:
            res+=obj**2
    return m.sqrt(res/len(X))

def ExcessEquilibriumReturn(alpha,Sigma,w):
    return alpha*np.dot(Sigma,w)

def MakeTradeDf(tradeMatrix):
    index=[]
    data={}
    ini=tradeMatrix[0][0]
    for key in ini:
        data[key]=[]
    for obj in tradeMatrix:
        for key in obj[0]:
            data[key].append(obj[0][key])
        index.append(obj[1])
    return pd.DataFrame(data=data,index=index)

def stationaryArea(data,treshold=0.1,minStep=0.05):
    index=0
    result=adfuller(data[index:])[1]
    n=len(data)
    while result>treshold and (n-index)>minStep*n:
        index+=int(minStep*n)
        result=adfuller(data[index:])[1]
    if (n-index)<minStep*n:
        return None,False
    return index,True

def stationaryEV(data,lag,treshold=0.1,minStep=0.05):
    res=[]
    for i in range(lag,len(data)):
        index,flag=stationaryArea(data[i-lag:i],treshold,minStep)
        if flag:
            res.append(np.asarray(variationVector(data[i-lag:i][index:],True)).mean())
        else:
            res.append(res[-1])
        
    return pd.Series(data=res,index=data.index[lag:])
    
    




 
