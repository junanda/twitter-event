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

    @staticmethod
    def summarization(doc):
        pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        doc = re.sub(pattern, '', str(doc))
        return summarize(doc)

    @staticmethod
    def get_date_event(doc):
        date_format = re.compile(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}|[ADFJMNOS]\w* [\d]{1,2} [\d]{4}")
        return date_format.findall(str(doc))[0]

    def start(self):
        out_text = []
        link_from_tweet = self.tw.agent_get_link_on_screen(self.tag_search)
        self.web.urls = link_from_tweet

        text_clean_format = self.web.start_get()

        for index, doc in enumerate(text_clean_format):
            try:
                out_text.append({'date': self.get_date_event(doc), 'summarize': self.summarization(doc),
                                 'link': link_from_tweet[index]})
                # out_text.append({'date': self.get_date_event(date[index]), 'summarize': self.summarization(date[index]), 'link': link_from_tweet[index]})
            except Exception as e:
                print(e)

        print("----------------------\n")
        print(out_text)
        # yield out_text


if __name__ == '__main__':
    ex_url = ["https://t.co/hVN8TPXDKg", "https://t.co/ZaZ0jc6YhI", "https://t.co/G34WBJWmAC",
              "https://t.co/StaofNzTYi"]

    ev = Event("Kubernetes webinars")
    ev.start()
