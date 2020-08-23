import requests
from pprint import pprint
from base64 import b64decode

class Pinboard:
    def __init__(self, api_token):
        self.api_url = 'https://api.pinboard.in/v1'
        self.api_params = {
            'auth_token': b64decode(api_token).decode('utf-8'),
            'format': 'json'
        }
    
    def get_bookmark(self, bm_url):
        api_params = self.api_params
        api_params.update({'url':bm_url})
        
        req = requests.get(
            url=self.api_url+'/posts/get',
            params=api_params
        )
        
        if req.status_code == 200:
            return(req.json())
        else:
            print(req.text)
            print(req.status_code)
            print("*** REQUESTS Error ***")
    
    def add_post(self, bookmark):
        api_params = self.api_params
        api_params.update({
            'url': bookmark['url'],
            'description': bookmark['title'],
            'extended': bookmark['summary'],
            'tags': 'rss_star',
            'replace': 'no'
        })
        resp = requests.get(
            url=self.api_url+'/posts/add',
            params=api_params
        )
        
        if resp.status_code == 200:
            resp_data = resp.json()
            if resp_data['result_code'] != 'done':
                pprint(resp_data)
        else:
            pprint(resp.text)
            print(resp.status_code)
            pprint(resp.headers)


if '__main__' == __name__:
    data = {
        'url': 'https://daringfireball.net/linked/2020/07/08/brain-disorders-covid19',
        'title': 'Warning of Serious Brain Disorders in People With Mild Coronavirus Symptoms',
        'summary': 'Ian Sample, reporting for The Guardian: Neurologists are on Wednesday publishing details of more than 40 UK Covid-19 patients whose complications ranged from brain inflammation and delirium to nerve damage and stroke. In some cases, the neurological'
    }
    pb = Pinboard()
    pprint(pb.get_bookmark(data['url']))
    # pb.add_post(data)


