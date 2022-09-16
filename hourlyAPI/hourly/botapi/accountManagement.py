def returnSide(side):
    return 2*(side=="buy")-1

def convertSide(side):
    if side==1:
        return "buy"
    return "sell"


def getOrdersDict(orders):
    orderDict={}
    for order in orders["orders"]:
        if order["baseAsset"] in orderDict:
            orderDict[order["baseAsset"]]+=float(order["qtyPct"])
        else:
            orderDict[order["baseAsset"]]=float(order["qtyPct"])
    return orderDict
    
def notCloseEnough(currentDict,targetDict,whiteList,eps):
    newList=[]
    flag=False
    currentAssets=list(currentDict.keys())
    for asset in whiteList:
        if asset in currentAssets:
            if abs(currentDict[asset]-targetDict[asset])>eps:
                flag=True
                newList.append(asset)
        else:
            if asset in currentDict.keys():
                if currentDict[asset]>eps:
                    flag=True
                    newList.append(asset)
    return flag,newList

def sumDict(dict1,dict2):
    totDict={}
    keys=set(dict1.keys()).union(set(dict2.keys()))
    for key in keys:
        if not(key in dict1):
            totDict[key]=dict2[key]
        elif not(key in dict2):
            totDict[key]=dict1[key]
        else:
            totDict[key]=dict1[key]+dict2[key]
    return totDict
