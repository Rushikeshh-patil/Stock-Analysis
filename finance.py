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
        balance = self.balancesheet['balanceSheetHistory']['balanceSheetStatements'][0]
        equity_list = []
        for i in range(4):
            equity_list.append(self.balancesheet['balanceSheetHistory']['balanceSheetStatements'][i]['totalStockholderEquity']['raw'])
        
        average_change = ((((equity_list[0] - equity_list[1])/equity_list[1])*100) + (((equity_list[1] - equity_list[2])/equity_list[2])*100) + (((equity_list[2] - equity_list[3])/equity_list[3])*100))/3


        
        total_assets = balance['totalAssets']['fmt']
        total_assets_raw = balance['totalAssets']['raw']
        
        total_lia = balance['totalLiab']['fmt']
        total_lia_raw = balance['totalLiab']['raw']

        current_assets = balance['totalCurrentAssets']['fmt']
        current_assets_raw = balance['totalCurrentAssets']['raw']

        current_lia = balance['totalCurrentLiabilities']['fmt']
        current_lia_raw = balance['totalCurrentLiabilities']['raw']

        totalstockholder_equity = balance['totalStockholderEquity']['fmt'] 
        totalstockholder_equity_raw = balance['totalStockholderEquity']['raw']

        netTangible_Assets = balance['netTangibleAssets']['fmt'] 
        netTangible_Assets_raw = balance['netTangibleAssets']['raw']

        date = balance['endDate']['fmt']
        percent = (total_lia_raw/total_assets_raw)*100
        
        print('\n WELCOME TO THE BALANCE SHEET ANALYZER -' )

        print ('\nAs of {} {} has {} dollars of assets and {} dollars of total liability. \nThis is {} percent of the total assets.\n'.format(date,self.ticker,total_assets,total_lia,percent))

        if percent <= 0  :
            print ('\nThis means that the company has a net debt. Be sure to research why that is.')

        else :
            print ('\nThis means that the company has a net positive worth. This is good.')

        if current_assets_raw > current_lia_raw : 
            print ('\n\nFrom a current assets and liability stanpoint {} is in a good shape'.format(self.ticker))

        else :
            print ('\n\nFrom a current assets and liability stanpoint {} is NOT in a good shape'.format(self.ticker))

        print ('\nThe current liabilities are {} while the current assets are {}.'.format(current_lia,current_assets))

        print ('the year over year average stockholders equity growth is {}\n'.format(average_change))

        

            

         




        
         


STOCK = RDPanalysis(ticker=ticker)
STOCK.balancesheet_analyzer()

