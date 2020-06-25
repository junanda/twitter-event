from event import Event
from pprint import pprint as pr


if __name__ == "__main__":

    keywords = "kubernetes webinars"

    event = Event(keywords)
    data = event.start()

    pr(data)
