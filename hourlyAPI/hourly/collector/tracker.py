#import cryptocompare as cc
import numpy as np
import json as json
import math as m
import datetime as datetime
import pandas as pd
import csv as csv
import os
import requests as r

#file_tracker="coins_tracked"
#file_to_track="coins_to_track.json"
#file_json='../json'

def add_price(df,price,time):
    """
    df : pd.Series (base de données de prix)
    price: float (prix à ajouter)
    time : Timestamp (temps à ajouter)
    Ajoute le prix price au pd.Dataframe df
    """
    df.loc[time]=[price]


def get_current_prices(coins):
    """
    coins : list (liste de coins sous forme de chaine de caractère. Exemple : ['BTC','ETH','BNB'])
    Prend en entrée les Tickers d'une liste de coins (list) et retourne leurs prix instantanés (float)
    Exemple : get_current_prices(['BTC','ETH'])
    Output: {'BTC': {'USD': 42203.58}, 'ETH': {'USD': 2864.44}}
    """
    currency="USDT"
    adress='https://api.binance.com/api/v3/ticker/price?symbol='
    res={}
    for coin in coins:
        request= r.get(adress+coin+currency)
        dic=eval(request.text)
        res[coin]={'USD':float(dic["price"])}
    return res
        
   

def track(coin,file_tracker,price,time):
    """
    coin : str (cryptomonnaie sous forme de chaine de caractères. Exemple : 'BTC')
    file_tracker : str (Dossier dans lequel enregistrer le prix du coin. Exemple: "coins_tracked")
    price : float (Prix du coin)
    time : Timestamp (Temps correspondant au prix du coin)

    Ecrit dans le fichier correspondant à l'année en cours dans le dossier file_tracker, le prix de coin à l'instant time
    Créer les dossiers et fichiers nécessaires si ceux-ci n'existent pas
    """
    #file_name=file_tracker+'/'+coin+'/'+time[:4]+'.csv'
    file_name=time[:4]+'.csv'
    file_path=file_tracker+'/'+coin
    fields=[time,price]
    flag=False
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if not(os.path.isfile(file_path+'/'+file_name)):
        flag=True
    with open(file_path+'/'+file_name, 'a') as f:
        writer = csv.writer(f)
        if flag:
            writer.writerow(['Time','Price'])
        writer.writerow(fields)
 
def track_coins(file_to_track,file_tracker):
    """
    file_to_track : str (Fichier JSON indiquant les coins à tracker. Exemple: "coins_to_track.json")
    file_tracker : str  (Dossier dans lequel enregistrer le prix du coin. Exemple: "coins_tracked")

    Ecrit les prix instantanés des coins présents dans le fichier json file_to_track dans le dossier file_tracker
    """
    with open(file_to_track,'r') as f:
        coins=json.load(f)
        f.close()
    coins=eval(coins["coins"])
    time=str(datetime.datetime.now())
    prices=get_current_prices(coins)
    for coin in coins:
        price=prices[coin]["USD"]
        track(coin,file_tracker,price,time)
    
def tracking(file_to_track,file_tracker,file_json,time_delta):
    """
    file_to_track : str (Fichier JSON indiquant les coins à tracker. Exemple: "coins_to_track.json")
    file_tracker : str  (Dossier dans lequel enregistrer le prix du coin. Exemple: "coins_tracked")
    file_json : str (Adresse du dossier dans lequel se trouve l'intrégalité des fichiers JSON à utiliser. Exemple : '../json')
    time_delta: int (Temps entre les captures de prix. time_delta est exprimée en secondes)

    Collecte les prix des coins dans file_to_track toutes les time_delta secondes

    Exemple: tracking("coins_to_track.json","coins_tracked",'../json',10)
    """
    flag=True
    old_time=datetime.datetime.now()
    #while old_time.second!=0:
        #old_time=datetime.datetime.now()
    while flag:
        try:
            time=datetime.datetime.now()
            if (time-old_time).seconds>=time_delta:
                old_time=time
                old_time=old_time.replace(microsecond=0)
                track_coins(file_json+'/'+file_to_track,file_tracker)
        except:
            pass
        
        
#tracking("coins_to_track.json","coins_tracked",'../../config/coins',10)
            
