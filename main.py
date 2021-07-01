# Start2Impact: Python project
# Cryptocurrency reporting system

import json
import os
from password import COINMARKETCAP_API_KEY
import requests
import time


class CoinmarketcapHandler:
    """ Coinmarketcap APIs handler. Connect and fetch data from Coinmarketcap APIs """

    def __init__(self):
        self.url = ''
        self.parameters = {}
        self.headers = {}

    def fetch_currencies_data(self):
        # Get and return data via Coinmarketcap APIs
        response = requests.get(url=self.url, headers=self.headers, params=self.parameters).json()
        return response['data']


class CryptoReport(CoinmarketcapHandler):
    """ Cryptocurrencies reporting system.
    Generate 6 types of reports about cryptocurrencies using Coinmarketcap APIs """

    def __init__(self):
        super(CryptoReport, self).__init__()
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
        }
        self.reports = self.get_reports()

    def get_reports(self):
        # Return a dict with 6 types of reports about cryptocurrencies
        reports = {
            'most traded': self.most_traded_currency(),
            'best 10': self.best_ten_currencies(),
            'worst 10': self.worst_ten_currencies(),
            'amount top 20': self.amount_top_twenty_currencies(),
            'amount by volumes': self.amount_by_volumes_currencies(),
            'gain top 20': self.gain_top_twenty_currencies()
        }

        return reports

    def most_traded_currency(self):
        # Return the cryptocurrency with the largest volume (in $) of the last 24 hours
        self.parameters = {
            'start': 1,
            'limit': 1,
            'sort': 'volume_24h',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        return currencies[0]

    def best_ten_currencies(self):
        # Return the best 10 cryptocurrencies by percentage increase in the last 24 hours
        self.parameters = {
            'start': 1,
            'limit': 10,
            'sort': 'percent_change_24h',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        return currencies

    def worst_ten_currencies(self):
        # Return the worst 10 cryptocurrencies by percentage increase in the last 24 hours
        self.parameters = {
            'start': 1,
            'limit': 10,
            'sort': 'percent_change_24h',
            'sort_dir': 'asc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        return currencies

    def amount_top_twenty_currencies(self):
        # Return the amount of money required to purchase one unit of each of the top 20 cryptocurrencies in order of capitalization
        amount = 0
        self.parameters = {
            'start': 1,
            'limit': 20,
            'sort': 'market_cap',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        for currency in currencies:
            amount += currency['quote']['USD']['price']
        return round(amount, 2)

    def amount_by_volumes_currencies(self):
        # Return the amount of money required to purchase one unit of all cryptocurrencies whose last 24-hour volume exceeds $ 76,000,000
        amount = 0
        self.parameters = {
            'start': 1,
            'limit': 100,
            'volume_24h_min': 76000000,
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        for currency in currencies:
            amount += currency['quote']['USD']['price']
        return round(amount, 2)

    def gain_top_twenty_currencies(self):
        # Return the percentage of gain or loss you would have made if you had bought one unit of each of the top 20 cryptocurrencies the day before
        initial_amount = 0
        final_amount = 0
        self.parameters = {
            'start': 1,
            'limit': 20,
            'sort': 'market_cap',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        for currency in currencies:
            old_price = currency['quote']['USD']['price'] / (1 + (currency['quote']['USD']['percent_change_24h'] / 100))
            initial_amount += old_price
            final_amount += currency['quote']['USD']['price']
        gain = round((((final_amount - initial_amount) / initial_amount) * 100), 1)
        return gain


def make_json(report):
    # Create a json file named with the actual date into the 'Report' directory
    file_name = time.strftime('Report_%d_%m_%Y.json', time.localtime())
    script_dir = os.path.dirname(os.path.abspath(__file__))
    destination_dir = os.path.join(script_dir, 'report')
    path = os.path.join(destination_dir, file_name)

    # Create new directory if does not already exists
    try:
        os.mkdir(destination_dir)
    except OSError:
        pass  # Already exists
    with open(path, 'w') as f:
        json.dump(report, f)


def main():
    seconds = 60
    minutes = 60
    hours = 24

    while True:
        report = CryptoReport()

        # Display essential reports
        print('------------------------------------------------------------')
        print('Crypto currencies reports of ' + time.strftime('%d/%m/%Y', time.localtime()))
        print('Most traded: ' + str(report.reports['most traded']['symbol']))
        print('Best 10:', end=' ')
        for currency in report.reports['best 10']:
            print(str(currency['symbol']), end=' ')
        print('')
        print('Worst 10:', end=' ')
        for currency in report.reports['worst 10']:
            print(str(currency['symbol']), end=' ')
        print('')
        print('Amount top 20: ' + str(report.reports['amount top 20']) + '$')
        print('Amount by volumes: ' + str(report.reports['amount by volumes']) + '$')
        print('Gain top 20: ' + str(report.reports['gain top 20']) + '%')
        print('------------------------------------------------------------')

        make_json(report.reports)
        time.sleep(seconds * minutes * hours)


if __name__ == '__main__':
    main()
