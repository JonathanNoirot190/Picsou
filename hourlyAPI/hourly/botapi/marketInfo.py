import requests as r
def getPrice(asset,baseAsset):
    address='https://api.binance.com/api/v3/ticker/price?symbol='
    request= r.get(address+asset+baseAsset)
    dic=eval(request.text)
    return float(dic["price"])
