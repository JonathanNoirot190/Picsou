import os
import csv
class Tracker:
    def __init__(self,tradeCountDict={},tradeMatrix=[],backlog={}):
        self.tradeCountDict=tradeCountDict
        self.tradeMatrix=tradeMatrix
        self.backlog=backlog
        self.save=False
        self.tracking=False
        
    def getTradeCount(self):
        tradeCount=0
        for count in self.tradeCountDict.values():
            tradeCount+=count
        return tradeCount

    def savePortfolio(self,portfolio,time,path="save"):
        year=str(time.year)
        month=str(time.month)
        day=str(time.day)
        file_name=day+'.csv'
        file_path=path+'/'+year+'/'+month
        flag=False
        fields=[time]+list(portfolio.values())
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        if not(os.path.isfile(file_path+'/'+file_name)):
            flag=True
        with open(file_path+'/'+file_name, 'a',newline='') as f:
            writer = csv.writer(f)
            if flag:
                writer.writerow(['Time']+list(portfolio.keys()))
            writer.writerow(fields)
