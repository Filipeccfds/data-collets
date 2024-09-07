# %%

import requests
import datetime
import json

class Collector:

    def __init__(self, url):
        self.url = url
        self.instance = url.strip("/").split("/")[-1]
    
    def get_endpoint(self, **kwargs):
        resp = requests.get(self.url, params=kwargs)
        return resp
    
    def save_data(self, data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        data['ingestion_date'] = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename= f'"/Pokemon/data/{self.instance}/{now}.json"'
        with open (filename, 'w') as open_file:
            json.dump(data, open_file)

    def save_data(self, **kwargs):
        resp = self.get_endpoint(**kwargs)
        if resp.status_code == 200:
            data = resp.json()
            self.save_data(data)
            return data
        else:
            return{}

 # %%   
url = 'https://pokeapi.co/api/v2/pokemon/'

collector = Collector(url)    

collector.save_data()