from tweet import Twitter
from gensim.summarization import summarize
from web import Web
import re
from pprint import pprint as pr

class Event:
    def __init__(self, tag_search):
        self.tw = Twitter()
        self.web = Web()
        self.tag_search = tag_search

    @staticmethod
    def summarization(doc):
        pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        doc = re.sub(pattern, '', str(doc))
        return summarize(doc)

    @staticmethod
    def get_date_event(doc):
        date_format = re.compile(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}|[ADFJMNOS]\w* [\d]{1,2} [\d]{4}")
        date_event = date_format.findall(str(doc))
        if date_event:
            return date_event[0]
        else:
            return None

    def start(self):
        out_text = []
        link_from_tweet = self.tw.agent_get_link_on_screen(self.tag_search)
        self.web.urls = link_from_tweet

        text_clean_format, detail = self.web.start_get()

        for index, doc in enumerate(text_clean_format):
            try:
                out_text.append({'date': self.get_date_event(doc), 'summarize': self.summarization(doc),'detail': detail[index]})
            except Exception as e:
                print(e)

        print("Finish.........\n")
        pr(out_text)
        # yield out_text


if __name__ == '__main__':

    ev = Event("mongodb webinars")
    ev.start()
