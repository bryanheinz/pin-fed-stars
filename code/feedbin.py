import os
import getpass
import requests
from pprint import pprint
from base64 import b64decode
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


class Feedbin:
    def __init__(self, email, password):
        user = getpass.getuser()
        self.cache_path = f'/Users/{user}/Library/Application Support/feedbin'
        self.cache_file = os.path.join(self.cache_path, 'processed_stars.txt')
        
        self.fb_api_url = 'https://api.feedbin.com/v2/'
        self.fb_auth = auth=HTTPBasicAuth(
            email,
            b64decode(password).decode('utf-8')
        )
        self.fb_headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        self.to_boomark = []
        
        self.read_cache_data()
    
    def read_cache_data(self):
        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                cache_stars = file.read()
                self.cache_stars = cache_stars.split(',')
        else:
            self.cache_stars = []
    
    def write_cache_data(self):
        cache_stars = ','.join(map(str, self.cache_stars))
        with open(self.cache_file, 'w') as file:
            file.write(cache_stars)
    
    def get_req(self, route, params):
        req = requests.get(
            url=self.fb_api_url+route,
            headers=self.fb_headers,
            auth=self.fb_auth,
            params=params
        )
        if req.status_code == 200:
            return(req.json())
        else:
            print(req.text)
            print(req.status_code)
            print("*** REQUESTS Error ***")
    
    def df_links(self, data):
        title = data['title']
        summary = data['summary']
        soup = BeautifulSoup(data['content'], 'html.parser')
        df_link = None
        for link in soup.find_all('a'):
            if 'daringfireball.net/linked/' in link.get('href'):
                df_link = link.get('href')
        if not df_link:
            df_link = data['url']
        return([title, summary, df_link])
    
    def parse_redirects(self, data):
        if 'feedpress.it' in data['url']:
            resp = requests.get(data['url'], allow_redirects=False)
            url = resp.headers['Location']
        else:
            url = data['url']
        return(url)
    
    def parse_stars(self):
        new_star_ids = []
        
        # get all star entries
        star_ids = self.get_req('starred_entries.json', {})
        
        # loop through the stars and pull out any cached stars
        cache_stars = self.cache_stars
        for i in star_ids:
            if str(i) not in cache_stars:
                new_star_ids.append(i)
                self.cache_stars.append(i)
        
        # map star entry list ([int,]) to a comma separated string
        stars = ','.join(map(str, new_star_ids))
        # get stars entries
        star_entries = self.get_req('entries.json', {'ids':stars})
        
        # loop through stared entries
        for _ in star_entries:
            if _['author']:
                # special Daring Fireball check since he does linked lists
                # which link directly to the source, Feedbin will star that
                # URL. so, this grabs the actual DF URL.
                if 'john gruber' in _['author'].lower():
                    # parse out the correct DF URL
                    bm_title, bm_sum, bm_url = self.df_links(_)
                    # append this star to be bookmarked
                    self.to_boomark.append({
                        'url': bm_url,
                        'title': bm_title,
                        'summary': bm_sum
                    })
                    continue
            
            # parse any weird redirect URLs out and get the canonical URL
            bm_url = self.parse_redirects(_)
            
            # append this star to be bookmarked
            self.to_boomark.append({
                'url': bm_url,
                'title': _['title'],
                'summary': _['summary']
            })


if '__main__' == __name__:
    fb = Feedbin()
    fb.parse_stars()
    print(fb.to_boomark)
