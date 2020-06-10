import re
import requests
import tweepy
from bs4 import BeautifulSoup
from tweepy import OAuthHandler
from config import *


class Twitter:
    def __init__(self):
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(token_key, token_secret)
        self.API = tweepy.API(self.auth)

    def getTweet(self, text_src):
        src_twt = self.API.search(text_src)
        return src_twt

    def ektrakTweetUrl(self, text_seacrh):
        data_ektraksi = []
        data_twt = self.getTweet(text_seacrh)
        for dt in data_twt:
            for u in dt.entities["urls"]:
                if "https://twitter.com/" in u["expanded_url"]:
                    data_ektraksi.append({'id': dt.id, 'name': dt.user.name, 'text': dt.text, 'url': u["expanded_url"]})

        return data_ektraksi

    def agent_get_link_on_screen(self, request_text):
        header = {'User-Agent': user_agent_old_phone}
        urlx = [x['url'] for x in self.ektrakTweetUrl(request_text)]
        url_ext = []
        for url in urlx:
            page = requests.get(url, headers=header)
            if page.status_code == 200:
                link = self.extract_link_web(page.content)
                if len(link) > 0 and link not in url_ext:
                    url_ext.append(link)

        return list(dict.fromkeys(url_ext))

    def extract_link_web(self, request):
        soupb = BeautifulSoup(request, 'lxml')
        links = soupb.find_all("a", {"href": True, "title": True})
        for l in links:
            us = re.findall('https://t.co/[^\s]+', l['href'])
            if us:
                return us[0]
        return None