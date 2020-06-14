import requests
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
from config import user_agent_old_phone


class Web:
    def __init__(self):
        self.urls = []

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', '[document]', 'nav', 'footer']:
            return False
        if isinstance(element, Comment):
            return False
        if re.match(r"[\n]+", str(element)): return False
        return True

    @staticmethod
    def get_title(response):
        if response.find('title'):
            title = response.find('title')
            title = title.string
            print("Title: {}".format(title))
        elif response.find("meta", property="og:title"):
            title = response.find('meta', property="og:title")
            title = title['content']
            print("Title: {}".format(title))
        else:
            title = response.find('meta', {"name": "og:title"})
            title = title['content']
            print("Title: {}".format(title))

        return title

    @staticmethod
    def get_description(response):
        if response.find('meta', {"name": "description"}):
            desc = response.find('meta', {"name": "description"})
            desc = desc['content']
            print("Description: {}".format(desc))
        elif response.find("meta", property="og:description"):
            desc = response.find('meta', property="og:description")
            desc = desc['content']
            print("Description: {}".format(desc))
        else:
            desc = response.find('meta', {"name":"og:description"})
            desc = desc['content']
            print("Description: {}".format(desc))

        return desc

    def ektraksiData(self, request):
        clean_text = ''
        bs_soup = BeautifulSoup(request.content, 'lxml')

        texts = bs_soup.findAll(text=True)

        # find title and meta data title
        title = self.get_title(bs_soup)

        # find meta data with property description
        desc = self.get_description(bs_soup)

        # link_extend = bs_soup.find('meta', property="og:link")
        link_extend = request.url
        print("Link website: {}".format(link_extend))

        # check form ready or not
        # if form true extract from from web page_source
        form = bs_soup.find("form")
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
        return clean_text , {'title': title, 'description': desc, 'link': link_extend}

    def start_get(self):
        dat_extra = []
        data_detail = []
        for url in self.urls:
            try:

                print("request....")
                response = requests.get(url, headers={'User-Agent': user_agent_old_phone})
                print("Check request history")
                for rr in response.history:
                    print(rr.status_code, rr.url)

                print(response.status_code, response.url)
                html = requests.get(response.url, headers={'User-Agent': user_agent_old_phone})
                if html.status_code != 200:
                    txt_dat, detail_info = self.ektraksiData(response)
                txt_dat, detail_info = self.ektraksiData(html)

                dat_extra.append(txt_dat)
                data_detail.append(detail_info)

                print("\n")
            except Exception as e:
                print(e)

        return dat_extra, data_detail
