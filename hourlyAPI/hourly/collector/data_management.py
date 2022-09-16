import pandas as pd
import os

import process as pro


def merge_df(df1,df2):
    """
    df1,df2 : pd.Dataframe

    Fusionne df1 et df2
    """
    time=[]
    price=[]
    time1=df1["Time"]
    price1=df1["Price"]
    time2=df2["Time"]
    price2=df2["Price"]
    i1=0
    i2=0
    while i1!=len(df1) and i2!=len(df2):
        if time1[i1]==time2[i2]:
            time.append(time1[i1])
            price.append(price1[i1])
            i1+=1
            i2+=1
        elif time1[i1]<time2[i2]:
            time.append(time1[i1])
            price.append(price1[i1])
            i1+=1
        else:
            time.append(time2[i2])
            price.append(price2[i2])
            i2+=1
    if i1!=len(df1):
        time+=list(time1[i1:])
        price+=list(price1[i1:])
    elif i2!=len(df2):
        time+=list(time2[i2:])
        price+=list(price2[i2:])
            
    df=pd.DataFrame(data={'Time': time, 'Price': price})
    df=df.set_index('Time')
    return df

def merge_data(path_start,path_end):
    """
    path_start: str (Chemin vers les nouvelles données)
    path_end: str (Chemin vers les anciennes données)

    Fusionne les données dans le dossier indiquer par path_start dans celui
    indiqué par path_end
    """
    files=os.listdir(path_start)
    for file in files:
        df1=pd.read_csv(path_start+'/'+file)
        if os.path.exists(path_end+'/'+file):
            df2=pd.read_csv(path_end+'/'+file)
            df=merge_df(df2,df1)
            df.to_csv(path_end+'/'+file)
        else:
            df1=df1.set_index('Time')
            df1.to_csv(path_end+'/'+file)

def preprocessing(path):
    files=os.listdir(path)
    for file in files:
        df=pd.read_csv(path+'/'+file)
        index=pro.process_df_index(df["Time"])
        values=df["Price"]
        res=pd.DataFrame(data={'Time': index, 'Price': values})
        res=res.set_index("Time")
        res.to_csv(path+'/'+file)
        
        
        
#2019-09-08 17:57:00
