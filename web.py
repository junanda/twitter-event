import requests
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
from config import user_agent_old_phone


class Web:
    def __init__(self):
        self.urls = []

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'title', '[document]', 'nav', 'footer']:
            return False
        if isinstance(element, Comment):
            return False
        if re.match(r"[\n]+", str(element)): return False
        return True

    @staticmethod
    def get_form_details(form):
        """return html details of a form, include action, method and list of controls (inputs, etc)"""
        details = {}
        action = form.attrs.get("action")
        method = form.attrs.get("method", "post")

        # get all forms input
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            # add to that list
            inputs.append({'type': input_type, 'name': input_name, 'value': input_value})

        # put everything to the resulting dictionary
        details["action"] = action
        details["methods"] = method
        details["inputs"] = inputs

        return details

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
        elif response.find('meta', {"name": "og:title"}):
            title = response.find('meta', {"name": "og:title"})
            title = title['content']
            print("Title: {}".format(title))
        else:
            title = None

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
        elif response.find('meta', {"name": "og:description"}):
            desc = response.find('meta', {"name": "og:description"})
            desc = desc['content']
            print("Description: {}".format(desc))
        else:
            desc = None

        return desc

    def ektraksiData(self, request):
        clean_text = ''
        bs_soup = BeautifulSoup(request.content, 'lxml')
        texts = bs_soup.findAll(text=True)
        article = bs_soup.find_all('article')

        # find title and meta data title
        title = self.get_title(bs_soup)

        # find meta data with property description
        desc = self.get_description(bs_soup)

        # link_extend = bs_soup.find('meta', property="og:link")
        link_extend = request.url
        print("Link website: {}".format(link_extend))

        # check form ready or not
        # if form ready extract from from web page_source
        forms = bs_soup.find_all("form")
        if forms:
            for i, form in enumerate(forms, start=1):
                forms_detail = self.get_form_details(form)
                print("="*10, f"form#{i}", "="*10)
                print(forms_detail)
        else:
            forms_detail = None

        if article:
            # remove javascript code in html parser
            article = re.sub(r'<script.+?</script>', '', str(article[0]), flags=re.DOTALL)
            # remove image
            pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            doc = re.sub(pattern, '', str(article))
            clean_text = ' '.join(doc.split())
        else:
            # filter data head, footer, 'style', 'script', 'head', 'title', 'meta', '[document]'
            visible_text = filter(self.tag_visible, texts)

            text = [t.strip() for t in visible_text]
            for sen in text:
                if sen:
                    sen = sen.rstrip().lstrip()
                    clean_text += sen + ' '

        # return data
        return clean_text, {'title': title, 'description': desc, 'link': link_extend, 'form': forms_detail}

    def start_get(self):
        dat_extra = []
        data_detail = []
        for url in self.urls:
            try:
                print("request url <GET> {} ....".format(url))
                response = requests.get(url, headers={'User-Agent': user_agent_old_phone})
                # print("Check request history")
                for rr in response.history:
                    print("status response: {} from request <GET> {} ".format(rr.status_code, rr.url))

                print("status response: {} from request <GET> {}".format(response.status_code, response.url))
                html = requests.get(response.url, headers={'User-Agent': user_agent_old_phone})
                if html.status_code != 200:
                    txt_dat, detail_info = self.ektraksiData(response)
                else:
                    txt_dat, detail_info = self.ektraksiData(html)

                dat_extra.append(txt_dat)
                data_detail.append(detail_info)

                print("\n")
            except Exception as e:
                print("Error : {}".format(e))

        return dat_extra, data_detail
