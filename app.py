from event import Event
from pprint import pprint as pr
from selenium import webdriver


# def sele_phantom():
#     url = "https://tanzu.vmware.com/content/webinars/jun-30-making-k8s-great-improving-the-kubernetes-developer-experience?utm_campaign=Global_BT_Q221_Improving-K8s-Developer-Experience&utm_source=twitter&utm_medium=social"
#     browser = webdriver.PhantomJS()
#     browser.get(url)
#
#     iframe = browser.find_element_by_tag_name("iframe")
#     print(iframe)
#     browser.switch_to.default_content()
#     browser.switch_to.frame(iframe)
#
#     iframe_source = browser.page_source
#
#     print(iframe_source)
#
#     print(browser.current_url)

if __name__ == "__main__":

    keywords = "kubernetes"

    event = Event(keywords)
    # start crawler
    data = event.start()

    pr(data)
    # sele_phantom()