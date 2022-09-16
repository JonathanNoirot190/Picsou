import numpy as np
import cvxpy as cvx
from scipy import optimize
from scipy.linalg import norm

#Optimal Portfolio
def minimizeVariance(Sigma,alpha,params):
    #ratio=params["risk"]
    #alpha0=max(alpha)*ratio
    n=len(alpha)
    SigmaInv=np.linalg.inv(Sigma)
    a=float(np.dot(np.dot(alpha,SigmaInv),alpha))
    b=float(np.dot(np.dot(alpha,SigmaInv),np.ones((n,1))))
    c=float(np.dot(np.dot(np.ones((1,n)),SigmaInv),np.ones((n,1))))
    alpha0=a/b
    temp=np.dot(np.linalg.inv(np.array([[a,b],[b,c]])),np.array([alpha0,1]))
    lambda1=temp[0]
    lambda2=temp[1]
    omega0=lambda1*np.dot(SigmaInv,alpha) + lambda2*np.transpose(np.dot(SigmaInv,np.ones((n,1))))[0]
    #sigma2_0=((c*(alpha0**2))-(2*b*alpha0)+a)/((a*c)-(b**2))
    return omega0 

def optimalWeights(Sigma,mu,params,wprime,fees):
    ratio=params["risk"]
    n=len(mu)
    w=cvx.Variable(n)
    ret = mu@w
    risk= cvx.quad_form(w,Sigma)
    beta=2*(10**2)
    #beta=2*(10**3)
    #beta=1
    
    if type(wprime)==type(None):
        objective = cvx.Minimize(risk-(ratio*ret))
    else:
        objective = cvx.Minimize(risk-(ratio*ret)+(cvx.abs(w-wprime)@np.ones((n,1)))*(1/beta)*fees)
    
    #objective = cvx.Minimize(risk-(ratio*ret))
    constraints=[np.ones((1,n))@w==1,w>=0]
    
    prob=cvx.Problem(objective,constraints)
    prob.solve(verbose=False)
    output=[]
    
    for i in range(len(w.value)):
        output.append(round(w[i].value,4))
    return output

def GMVWeights(Sigma,mu,params,wprime,fees):
    ratio=params["risk"]
    tau=params["tau"]
    n=len(mu)
    w=cvx.Variable(n)
    risk= cvx.quad_form(w,Sigma)

    objective = cvx.Minimize(risk+(tau*w@w))
    constraints=[np.ones((1,n))@w==1,w>=0]
    
    prob=cvx.Problem(objective,constraints)
    prob.solve(verbose=False)
    output=[]
    
    for i in range(len(w.value)):
        output.append(round(w[i].value,4))
    return output

"""
def optimalSRWeights(Sigma,mu,params,wprime,fees):
    ratio=params["risk"]
    n=len(mu)
    w=cvx.Variable(n)
    ret = mu@w
    risk= cvx.quad_form(w,Sigma)

    objective=cvx.Minimize(risk)
    constraints=[ret==1,w>=0]
    
    prob=cvx.Problem(objective,constraints)
    prob.solve(verbose=False)
    output=[]
    if type(w.value)==type(None):
        objective = cvx.Minimize(risk-(ratio*ret))
        constraints=[np.ones((1,n))@w==1,w>=0]
        prob=cvx.Problem(objective,constraints)
        prob.solve(verbose=False)
        output=[]
        for i in range(len(w.value)):
            output.append(round(w[i].value,4))
        return output
    
    for i in range(len(w.value)):
        output.append(round(w[i].value,4))
    return output/sum(output)

"""

def constantWeights(Sigma,mu,params):
    n=len(mu)
    output=[]
    for i in range(n):
        output.append(1/n)
    return output


def func(w,mu,Sigma):
    funcDenomr = np.sqrt(np.matmul(np.matmul(w.T,Sigma),w))
    funcNumer= np.matmul(np.array(mu),w)
    func=(funcNumer/funcDenomr)
    return func

def constraintEq(w):
    A=np.ones(w.shape)
    b=1
    constraintVal= np.matmul(A,w)-b
    return constraintVal

def optimalSRWeights(Sigma,mu,params,wprime,fees):
    n=len(mu)
    winit=np.repeat(1/n,n)
    cons=({'type':'eq','fun':constraintEq})
    lb=0.0
    ub=1.0
    bnds=tuple([(lb,ub) for w in winit])
    opt = optimize.minimize(func,x0=winit,args=(mu,Sigma),bounds=bnds,constraints=cons,tol=1.e-16)
    return opt['x']

"""
import statistical_analysis as sa
import sys
sys.path.insert(1, "/Users/NANCY/Documents/Algo_Trading/trading/hourly/manager")
import extractor as ext
import datetime as datetime
import pandas as pd


coins=["ADA","ATOM","BAT","BNB","BTC","BTT","CRO","DASH","DOGE","ENJ","EOS","ETH","FTM"]
coins+=["LINK","LRC","LTC","MANA","NEO","NULS","OMG","THETA","TRX","VET"]
coins+=["XEM","XLM","XMR","XRP","XTZ","ZEC"]
start=datetime.datetime(2021, 8, 15, 5, 36, 25, 445941)
end=datetime.datetime(2021, 8, 25, 23, 36, 25, 445941)
extractor=ext.Extractor()
temp=[]

for coin in coins:
    df=extractor.extract_data(coin,start,end)
    df=df["Price"]
    temp.append(df)


#coins+=["USDT"]
#temp.append(df*0 + 1)

X=np.asarray(temp)

df=pd.DataFrame(np.transpose(X),columns=coins)



mu=sa.EVMatrix(X)
Sigma=sa.CovarianceMatrix(X)
"""
