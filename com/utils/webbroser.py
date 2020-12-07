def get_news():
    from selenium import webdriver
    import sys
    sys.path.append("/home/wangwen/PycharmProjects/BTC/com/utils/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    chrome = webdriver.Chrome(executable_path="/home/wangwen/PycharmProjects/BTC/com/utils/chromedriver",
                              )
    chrome.get("https://www.binancezh.com/cn/support/announcement/")

    elem = chrome.find_element_by_class_name("css-6f91y1")

    return elem




if __name__ == '__main__':
    news = get_news()
    print(news.text)









