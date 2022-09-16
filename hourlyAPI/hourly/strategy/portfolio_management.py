import numpy as np
from statistical_analysis import EVMatrix
from statistical_analysis import CovarianceMatrix

def ModernManagement(ratioDict,cache,parameters,fees,tracker,index):
    assets=[]
    previousWeights=[]
    for coin in cache:
        previousWeights.append(ratioDict[coin])#*(1/(1-core)))
        assets.append(coin)

    X=[]
    for coin in assets:
        X.append(cache[coin])
    X=np.asarray(X)
    sigma=[]
    matrix=CovarianceMatrix(X[:,len(X)//2:])
    for vect in matrix:
        sigma.append(list(vect)+[0])
    sigma.append([0]*(len(assets)+1))
    sigma=np.asarray(sigma)
    mu=np.asarray(list(EVMatrix(X))+[((1+parameters["rfr"])**(1/(365*24)))-1])
    previousWeights.append(1-sum(previousWeights))
    previousWeights=np.asarray(previousWeights)
    try:
    
        if len(previousWeights)==len(mu) and sum(previousWeights[:-1]>0.1):
            weights=parameters["fun"](sigma,mu,parameters,previousWeights,fees)
        else:
            weights=parameters["fun"](sigma,mu,parameters,None,fees)
            """
                    core=parameters["rf"]/GetTotValue(cache,families,index,cashDict,stocksDict,whiteList)
                    weights=[i*(1-core) for i in weights]
                    weights[-1]+=core
            """
        res=ratioDict.copy()
        i=0
        for coin in cache:
            res[coin]=weights[i]
            i+=1
        return res
    except:
        return ratioDict.copy()
    


