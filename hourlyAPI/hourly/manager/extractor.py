import numpy as np
import json as json
import math as m
import datetime as datetime
import pandas as pd
import csv as csv
import os

class Extractor:
    def __init__(self,file_tracker="../collector/coins_tracked",file_store="data"):
        self.file_tracker=file_tracker
        self.file_store=file_store
    
    def extract_data(self,coin,start,end):
        """
        Input:
        coin: str (Nom du coin à extraire. Exemple: 'BTC')
        file_tracker : str (Dossier dans lequel se trouve les coins. Exemple: "../collector/coins_tracked")
        start : Timestamp ( Date de début. Exemple: datetime.datetime(2021, 8, 15, 20, 36, 25, 445941) )
        end : Timestamp  ( Date de fin. Exemple: datetime.datetime(2021, 8, 25, 20, 36, 25, 445941) )

        Output:
        res: pd.DataFrame
        
        Retourne les données du coin(str) des fichiers csv présents dans les dossiers de file_tracker(str)
        de la date start(datetime.datetime) à end(datetime.datetime)

        Exemple: extract_data("BTC","coins_tracked",datetime.datetime(2021, 8, 15, 20, 36, 25, 445941),datetime.datetime(2021, 8, 25, 20, 36, 25, 445941))
        """
        year_start=start.year
        year_end=end.year
        res=pd.DataFrame({'Time' : [],'Price' : []})
        res=res.set_index('Time')
        for year in range(year_start,year_end+1):
            df=pd.read_csv(self.file_tracker+'/'+coin+'/'+str(year)+'.csv',index_col='Time')
            res=res.append(df.loc[str(start):str(end)])
        res.index=convert_index(res.index)
        return res[["Price"]]



    def store_data(self,coins,start,end,step,eps):
        """
        Input:
        coins: list (Liste des noms des coins. Exemple : ['BTC','ETH','BNB'])
        start : Timestamp ( Date de début. Exemple: datetime.datetime(2021, 8, 15, 20, 36, 25, 445941) )
        end : Timestamp  ( Date de fin. Exemple: datetime.datetime(2021, 8, 25, 20, 36, 25, 445941) )
        file_store : str (Dossier dans lequel stocker les données extraites. Exemple: "data")
        file_tracker : str (Dossier dans lequel se trouve les coins. Exemple: "coins_tracked")
        step : int  (Nouveau pas entre les prix exprimé en secondes)
        eps : float (L'erreur tolérée de step en pourcentage)

        Output:
        None
        
        Copie les données des coins de coins(list) des fichiers csv présents dans les dossiers de file_tracker(str)
        de la date start(datetime.datetime) à end(datetime.datetime) et les colles dans file_store dans un fichier
        csv du nom du coin

        Example :
        start=datetime.datetime(2021, 8, 15, 20, 36, 25, 445941)
        end=datetime.datetime(2021, 8, 25, 20, 36, 25, 445941)
        store_data(['BTC','ETH','BNB'],start,end,"data","../collector/coins_tracked",60,0.05)
        
        """
        if not os.path.exists(self.file_store):
            os.makedirs(self.file_store)
        for coin in coins:
            res=self.extract_data(coin,start,end)
            res=change_step(res,step,eps)
            file_name=self.file_store+'/'+coin+'.csv'
            res.to_csv(file_name)



def delta_time(time1,time2):
    """
    Input:
    time1,time2: str

    Output:
    int

    Retourne l'écart en secondes entre time1 et time2
    """
    delta=(time1-time2)
    return delta.seconds+(3600*24)*delta.days
    
    

def change_step(df,step):
    """
    Input:
    df : pd.Dataframe (Dataframe de prix à modifier)
    step : int  (Nouveau pas entre les prix exprimé en secondes)
    eps : float (L'erreur tolérée de step en pourcentage)

    Output:
    res : pd.DataFrame

    Change le pas de temps minimum de df par step secondes
    """
    index=df.index
    temp=index[0]
    new_index=[temp]
    df=df["Price"]
    values=[float(df.loc[temp])]
    for i in range(len(df)):
        if delta_time(index[i],temp)>=step:
            value=float(df.loc[index[i]])
            temp=index[i]
            new_index.append(index[i])
            values.append(value)
    res=pd.DataFrame(data={'Time': new_index, 'Price': values})
    res=res.set_index('Time')
    return res


def get_estimated_price(df,date1,date2,date):
    """
    Description :
    Linearely estimate the price values between two time step of a dataframe

    Inputs:
    df : pd.DateFrame
    date,date1,date2 : str

    Outputs:
    float

    Example:
    >>> extractor=Extractor()
    >>> start=datetime.datetime(2021, 1, 15, 10, 0, 0, 0)
    >>> end=datetime.datetime(2021, 1, 15, 20, 0, 0, 0)
    >>> target=datetime.datetime(2021, 1, 15, 0, 0, 0, 0)
    >>> df=extractor.extract_data('XLM',start,end)["Price"]
    >>> get_estimated_price(df,start,end,target)
    0.31559999999999994
    """
    a=delta_time(date,date1)
    x=delta_time(date2,date1)
    c=float(df.loc[date1])
    y=float(df.loc[date2])-c
    return c+(y*a/x)

def FillData(df):
    res={}
    index=[]
    keys=["Price"]
    df=df[keys]
    for i in range(len(df)-1):
        start=df.index[i]
        end=df.index[i+1]
        for key in keys:
            if key in res.keys():
                res[key].append(df.loc[df.index[i]][key])
            else:
                res[key]=[df.loc[df.index[i]][key]]
        if end!=start+datetime.timedelta(hours=1):
            target=start
            index.append(start)
            while target+datetime.timedelta(hours=1)!=end:
                target=target+datetime.timedelta(hours=1)
                for key in keys:
                    res[key].append(res[key][-1])
                index.append(target)
        else:
            index.append(df.index[i])
    index.append(df.index[-1])
    for key in keys:
        res[key].append(df.loc[df.index[-1]][key])
    res["Time"]=index
    return pd.DataFrame(data=res)
        
            
            
    
def convert_index(index):
    """
    Inputs :
    index : pandas.core.indexes.base.Index (Index d'un DataFrame)

    Outputs :
    res : pandas.core.indexes.base.Index (index dont les valeurs ont été converties en Timestamp)

    Description :
    Retourne un index contenant les valeurs de l'index index converti en Timestamp

    Exemple:
    index=convert_index(index)
    
    """
    res=[]
    for i in range(len(index)):
        res.append(datetime.datetime.strptime(index[i][:19], '%Y-%m-%d %H:%M:%S'))
    return res
  
"""
>>> extractor=Extractor()
>>> start=datetime.datetime(2021, 1, 15, 20, 36, 25, 445941)
>>> end=datetime.datetime(2021, 8, 15, 20, 36, 25, 445941)
>>> df=extractor.extract_data('XLM',start,end)
>>> get_estimated_price(df,'2021-01-15 20:39:00','2021-01-15 20:40:00','2021-01-15 20:40:30')
"""

