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

    def ektraksiData(self, request):
        clean_text = ''
        bs_soup = BeautifulSoup(request.content, 'lxml')

        texts = bs_soup.findAll(text=True)

        # find title and meta data title
        if bs_soup.find('title'):
            title = bs_soup.find('title')
            title = title.string
            print("Title: {}".format(title))
        elif bs_soup.find("meta", property="og:title"):
            title = bs_soup.find('meta', property="og:title")
            title = title['content']
            print("Title: {}".format(title))
        else:
            title = bs_soup.find('meta', {"name": "og:title"})
            title = title['content']
            print("Title: {}".format(title))

        # find meta data with property description
        if bs_soup.find('meta', {"name": "description"}):
            desc = bs_soup.find('meta', {"name": "description"})
            desc = desc['content']
            print("Description: {}".format(desc))
        elif bs_soup.find("meta", property="og:description"):
            desc = bs_soup.find('meta', property="og:description")
            desc = desc['content']
            print("Description: {}".format(desc))
        else:
            desc = bs_soup.find('meta', {"name":"og:description"})
            desc = desc['content']
            print("Description: {}".format(desc))

        # link_extend = bs_soup.find('meta', property="og:link")
        link_extend = request.url
        print("Link website: {}".format(link_extend))

        #texts = bs_soup.find_all('span')
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
        return clean_text , {'title': title, 'description': desc, 'link': link_extend}

    def start_get(self):
        dat_extra = []
        data_detail = []
        for url in self.urls:
            try:
                # print("Start request link: {}".format(url))
                # response = requests.get(url, headers={'User-Agent': user_agent_old_phone})
                #
                # print("Check history request ... ")
                # if response.history:
                #     print("request was redirected")
                #     for n in response.history:
                #         print(n.status_code, n.url)
                #
                #     print("final destination")
                #     print("Status: {} Url: {}".format(response.status_code, response.url))
                # else:
                #     print("request was not redirected")
                #
                # dat_extra.append(self.ektraksiData(response))
                print("request....")
                re = requests.get(url, headers={'User-Agent': user_agent_old_phone})
                print("Check request history")
                for rr in re.history:
                    print(rr.status_code, rr.url)

                print(re.status_code, re.url)
                html = requests.get(re.url, headers={'User-Agent': user_agent_old_phone})
                if html.status_code != 200:
                    txt_dat, detail_info = self.ektraksiData(re)
                    # dat_extra.append(self.ektraksiData(re))
                txt_dat, detail_info = self.ektraksiData(html)
                # dat_extra.append(self.ektraksiData(html))

                dat_extra.append(txt_dat)
                data_detail.append(detail_info)
                # if re.status_code == 200:
                #     print("Ekstraksi text from webpage.....")
                #     dat_extra.append(self.ektraksiData(re))

                # else:
                #     for resp in re.history:
                #         print(resp.status_code, resp.url)
                #
                #     response = requests.get(re.url)
                #     print("Ekstraksi text from webpage.....")
                #     dat_extra.append(self.ektraksiData(response))
                print("\n")
            except Exception as e:
                print(e)

        return dat_extra, data_detail
