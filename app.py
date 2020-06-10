from tweet import Twitter

if __name__ == "__main__":
    twt = Twitter()
    textTw = twt.ektrakTweetUrl("")
    for t in textTw:
        print(t)
    data = twt.agent_get_link_on_screen("")
    for l in data:
        print(l)

    ex_url = ["https://t.co/hVN8TPXDKg", "https://t.co/ZaZ0jc6YhI", "https://t.co/G34WBJWmAC",
              "https://t.co/StaofNzTYi"]
    #
    # ob_web = Web(data)
    # ob_web.start_get()
