import requests
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import json

ticker = input('\nENTER THE TICKER SYMBOL FOR AUTOANALYSIS - ')

class RDPanalysis ():

    headers = None
    balancesheet = None

    def __init__(self,ticker):
        self.loadapikey()
        self.ticker = ticker

    def loadapikey(self):
        with open('./APIKEY.json') as f:
            data = json.load(f) #HAVE YOUR OWN KEY AND SAVE THAT AS A JSON IN THE SAME FOLDER

        headers = {
        'x-rapidapi-key': data['x-rapidapi-key'],
        'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
        }
        self.headers = headers
    
    def getquote(self):
        
        url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{}".format(self.ticker)
        response = requests.request("GET", url, headers=self.headers)
        quotes = response.json()
        return quotes

    def getassetinfo(self):
        
        url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{}".format(ticker) + "/asset-profile"
        response = requests.request("GET", url, headers=self.headers)
        assetprofile = response.json()
        return assetprofile

    def getbalancesheet(self):
        
        url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{}".format(ticker) + "/balance-sheet"
        response = requests.request("GET", url, headers=self.headers)
        self.balancesheet = response.json()

    def balancesheet_analyzer(self):
        self.getbalancesheet()
        total_assets = self.balancesheet['balanceSheetHistory']['balanceSheetStatements'][0]['totalAssets']['fmt']
        total_lia = self.balancesheet['balanceSheetHistory']['balanceSheetStatements'][0]['totalLiab']['fmt']
        total_assets_raw = self.balancesheet['balanceSheetHistory']['balanceSheetStatements'][0]['totalAssets']['raw']
        total_lia_raw = self.balancesheet['balanceSheetHistory']['balanceSheetStatements'][0]['totalLiab']['raw']
        date = self.balancesheet['balanceSheetHistory']['balanceSheetStatements'][0]['endDate']['fmt']
        percent = (total_lia_raw/total_assets_raw)*100
        return '\nAs of {} {} has {} dollars of assets and {} dollars of total liability. \nThis is {} percent of the total assets.\n'.format(date,self.ticker,total_assets,total_lia,percent)


STOCK = RDPanalysis(ticker=ticker)
result = STOCK.balancesheet_analyzer()
print(result)
