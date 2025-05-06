import requests
import json
import datetime
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['API']['client_id']
client_secret = config['API']['client_secret']


class TDX():
    def __init__(self,client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    def get_token(self):
        token_url = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
        headers = {'content-type':'application/x-www-form-urlencoded'}
        data = {
            'grant_type':'client_credentials',
            'client_id':self.client_id,
            'client_secret':self.client_secret
        }
        response = requests.post(token_url, headers=headers, data=data)
        return response.json()['access_token']
    def get_response(self, url):
        headers={'authorization': f'Bearer {self.get_token()}'}
        response = requests.get(url, headers=headers)
        return response.json()

if __name__ == '__main__':
    print(client_id," ", client_secret)
    #tdx = TDX(client_id, client_secret)