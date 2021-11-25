import re
import urllib
from urllib.parse import quote
import requests
from selenium import webdriver


def spider_page(url):
    kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
    r = requests.get(url, headers=kv, timeout=1)
    r.recoding = r.apparent_encoding
    page_text = r.text
    page_links = re.findall(r'(?<=<a href=\").*?(?=\")|(?<=<a href=\').*?(?=\')', page_text)
    return page_links


def url_filtrate(page_links):
    same_target_url = []
    for link in page_links:
        if re.findall(r'(http://www.hiwifi.com.*?)', link):
            same_target_url.append(link)
        elif re.findall(r'/.*?', link):
            url = 'http://www.hiwifi.com'
            down_url = urllib.parse.urljoin(url, link)
            same_target_url.append(down_url)

    unique_url = []
    for link in same_target_url:
        if link not in unique_url:
            unique_url.append(link)
    return unique_url


class LinkQueue:
    def __init__(self):
        self.visited = []
        self.unvisited = []
        self.download_urls = []

    def get_visited_url(self):
        return self.visited

    def get_unvisited_url(self):
        return self.unvisited

    def get_download_url(self):
        return self.download_urls

    def add_visited_url(self, url):
        return self.visited.append(url)

    def remove_visited_url(self, url):
        return self.visited.remove(url)

    def unvisited_url_dequeue(self):
        try:
            return self.unvisited.pop()
        except:
            return None

    def add_unvisited_url(self, url):
        if url != "" and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0, url)

    def add_download_url(self, url):
        if url != "" and url not in self.download_urls:
            return self.download_urls.insert(0, url)

    def get_unvisited_url_count(self):
        return len(self.unvisited)

    def get_visited_url_count(self):
        return len(self.visited)

    def get_download_url_count(self):
        return len(self.download_urls)

    def is_unvisited_urls_empty(self):
        return len(self.unvisited) == 0


class Spider:
    def __init__(self, url):
        self.queue = LinkQueue()
        self.queue.add_unvisited_url(url)

    def crawler(self, url_count):
        x = 1
        while x <= url_count:
            if self.queue.is_unvisited_urls_empty():
                break
            if x > 1:
                print("Start ", x - 1, "/", url_count, " url")
            try:
                visited_url = self.queue.unvisited_url_dequeue()
                print("Processing ", visited_url)
                if re.findall(r'(.*?.jd.com.*?)|(.*?.qq.com.*?)', visited_url):
                    continue
                if visited_url is None or visited_url == '':
                    continue
                initial_links = spider_page(visited_url)
                if initial_links is None:
                    pass
                right_links = url_filtrate(initial_links)
                self.queue.add_unvisited_url(right_links)
                for link in right_links:
                    if re.findall(r'(http://.*?\.bin)|(.*?\.zip)', link):
                        self.queue.add_download_url(link)
                    else:
                        self.queue.add_unvisited_url(link)
                x += 1
            except:
                pass
        print("Total: ", x - 2)
        return self.queue.download_urls


def download_firmware(url_list):
    driver_path = r'D:\chromedriver2\chromedriver.exe'
    options = webdriver.ChromeOptions()
    out_path = r'D:\firmware\HiWiFi'
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    for url in url_list:
        driver.get(url)
    driver.close()
    print("All Done.")


def task():
    url = "http://www.hiwifi.com/j3pro-view"
    spider = Spider(url)
    url_list = spider.crawler(50)
    download_firmware(url_list)


task()
