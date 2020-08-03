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
        elif response.find("meta", property="og:title"):
            title = response.find('meta', property="og:title")
            title = title['content']
        elif response.find('meta', {"name": "og:title"}):
            title = response.find('meta', {"name": "og:title"})
            title = title['content']
        else:
            title = None

        return title

    @staticmethod
    def get_description(response):
        if response.find('meta', {"name": "description"}):
            desc = response.find('meta', {"name": "description"})
            if desc.get('content'):
                desc = desc['content']
            else:
                desc = None
        elif response.find("meta", property="og:description"):
            desc = response.find('meta', property="og:description")
            desc = desc['content']
        elif response.find('meta', {"name": "og:description"}):
            desc = response.find('meta', {"name": "og:description"})
            desc = desc['content']
        else:
            desc = None

        return desc

    @staticmethod
    def selection_content(response):
        if response.find_all('article'):
            return response.find_all('article')
        elif response.find_all('section'):
            return response.find_all('section')
        elif response.find_all(class_="content"):
            return response.find_all(class_="content")
        elif response.find_all(id="content"):
            return response.find_all(id="content")
        else:
            return response.find_all("main")

    @staticmethod
    def selection_content_url(response):
        list_element = response.find_all()
        el_find = ['article', 'section', 'div.content']

        for tag in list_element:
            if tag.name in el_find:
                return response.find_all(tag.name)

    def ektraksiData(self, request):
        clean_text = ''
        bs_soup = BeautifulSoup(request.content, 'lxml')
        # texts = bs_soup.findAll(text=True)
        # article = bs_soup.find_all(re.compile(r"article|section|div#content"))
        article = self.selection_content(bs_soup)
        frame = bs_soup.find_all(re.compile(r"iframe|iFrame"))
        if frame:
            print(frame)
        # find element tag for title
        title = self.get_title(bs_soup)

        # find element tag for description
        desc = self.get_description(bs_soup)

        link_extend = request.url

        # check form ready or not
        # if form ready extract form from web page_source
        forms = bs_soup.find_all("form")
        if forms:
            for i, form in enumerate(forms, start=1):
                forms_detail = self.get_form_details(form)
                # print("="*10, f"form#{i}", "="*10)
                # print(forms_detail)
        else:
            forms_detail = None

        if article:
            # remove javascript code in document
            article = re.sub(r'<script.+?</script>', '', str(article), flags=re.DOTALL)
            # remove image tag
            pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            doc = re.sub(pattern, '', str(article))
            clean_text = ' '.join(doc.split())
        else:
            print("Text")
            # filter data head, footer, 'style', 'script', 'head', 'title', 'meta', '[document]'
            # visible_text = filter(self.tag_visible, texts)
            #
            # text = [t.strip() for t in visible_text]
            # for sen in text:
            #     if sen:
            #         sen = sen.rstrip().lstrip()
            #         clean_text += sen + ' '

        # return data
        return clean_text, {'title': title, 'description': desc, 'link': link_extend, 'form': forms_detail}

    def start_get(self):
        dat_extra = []
        data_detail = []
        for url in self.urls:

            print("request url <GET> {} ....".format(url))
            response = requests.get(url)
            # print("Check request history")
            for rr in response.history:
                print("status response: {} from request <GET> {} ".format(rr.status_code, rr.url))

            print("status response: {} from request <GET> {}".format(response.status_code, response.url))
            # html = requests.get(response.url, headers={'User-Agent': user_agent_old_phone})
            html = requests.get(response.url)
            if html.status_code == 200:
                txt_dat, detail_info = self.ektraksiData(html)
            else:
                txt_dat, detail_info = self.ektraksiData(response)

            dat_extra.append(txt_dat)
            data_detail.append(detail_info)

            print("\n")

        return dat_extra, data_detail
