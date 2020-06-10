import requests
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
from config import user_agent_old_phone


class Web:
    def __init__(self):
        self.urls = []

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'nav', 'footer', 'header']:
            return False
        if isinstance(element, Comment):
            return False
        if re.match(r"[\n]+", str(element)): return False
        return True

    def ektraksiData(self, request):
        clean_text = ''
        bs_soup = BeautifulSoup(request.text, 'lxml')
        texts = bs_soup.findAll(text=True)
        # check form ready or not
        # if form true extract from from web page_source
        form = bs_soup.find('form')
        if form:
            if form.get('method') == 'POST':
                fields = form.findAll(('input', 'button', 'select', 'textarea'))
                action = form.get('action')
                print(action)
                formdata = dict((field.get('name'), field.get('value')) for field in fields)
                print(formdata)

        # filter data head, footer, 'style', 'script', 'head', 'title', 'meta', '[document]'
        # get all text in web page_source
        visible_text = filter(self.tag_visible, texts)

        text = [t.strip() for t in visible_text]
        for sen in text:
            if sen:
                sen = sen.rstrip().lstrip()
                clean_text += sen+' '

        # return data
        return clean_text

    @property
    def start_get(self):
        dat_extra = []
        for url in self.urls:
            try:
                print("Start request link: {}".format(url))
                re = requests.get(url, headers={'User-Agent': user_agent_old_phone})
                print("Ekstraksi text from webpage.....")
                dat_extra.append(self.ektraksiData(re))
            except Exception as e:
                print(e)

        print("Finish ....")

        return dat_extra
