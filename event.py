from tweet import Twitter
from gensim.summarization import summarize
from web import Web
import re

class Event:
    def __init__(self, tag_search):
        self.tw = Twitter()
        self.web = Web()
        self.tag_search = tag_search

    def parse_data(self):
        pass

    def summarization(self, doc):
        return summarize(doc)

    def get_date_event(self, doc):
        date_format = re.compile(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}")
        return date_format.findall(doc)

    def start(self):
        link_from_tweet = self.tw.agent_get_link_on_screen(self.tag_search)
        self.web.urls = link_from_tweet

        text_clean_format = self.web.start_get()

        for date in text_clean_format:
            print(self.get_date_event(date))



if __name__ == '__main__':
    ex_url = ["https://t.co/hVN8TPXDKg", "https://t.co/ZaZ0jc6YhI", "https://t.co/G34WBJWmAC",
              "https://t.co/StaofNzTYi"]

    ev = Event("Kubernetes webinars")
    ev.start()