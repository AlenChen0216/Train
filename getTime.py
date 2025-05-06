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
        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response.status_code} {response.text}")
        return response.json()['access_token']
    def get_response(self, url):
        headers={'authorization': f'Bearer {self.get_token()}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get data: {response.status_code} {response.text}")
        return response.json()

if __name__ == '__main__':
    tdx = TDX(client_id, client_secret)
    star = '3360'
    end = '3300'
    base_url = "https://tdx.transportdata.tw/api/basic/"
    endpoint = f"v3/Rail/TRA/DailyTrainTimetable/OD/{star}/to/{end}/{datetime.datetime.now().strftime('%Y-%m-%d')}"
    filter = f"?$filter=StopTimes/any(st: st/ArrivalTime gt '{datetime.datetime.now().strftime('%H:%M')}' and st/ArrivalTime lt '{(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%H:%M')}')"
    state = "&$format=JSON"
    url = base_url + endpoint + filter + state
    response = tdx.get_response(url)
    #print("URL:", url)
    #print(response)
    if response:
        for data in response['TrainTimetables']:
            info = data['TrainInfo']
            times = data['StopTimes']
            if(info['TrainTypeName']['En'].find('Express(3000)') != -1 or info['TrainTypeName']['En'].find('Puyuma') != -1):
                continue
            # print(info)
            # print(times)
            print(f"Train Number: {info['TrainNo']}")
            print(f"Train Type: {info['TrainTypeName']['Zh_tw']}")
            print(f"Start Time: {times[0]['ArrivalTime']}")
            print(f"End Time: {times[1]['ArrivalTime']}")
            print("=========================================")
    else:
        print("No data found")
