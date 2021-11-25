from urllib.parse import quote
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver

url = "https://service.tp-link.com.cn"
first_url = "https://service.tp-link.com.cn/download?classtip=software&p=1&o=0"
driver_path = r'D:\chromedriver2\chromedriver.exe'
options = webdriver.ChromeOptions()
out_path = r'D:\firmware\TPLINK'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.get(first_url)
while 1 == 1:
    button = driver.find_element_by_xpath("//*[@class='dreadMore']")
    # 找出标签中的文本内容
    name = button.get_attribute('textContent')
    if name == "查看更多 ∨ ":
        driver.find_element_by_xpath("//*[@class='dreadMore']").click()
    else:
        break
bs4 = BeautifulSoup(driver.page_source, "lxml")
download_list = bs4.find_all(class_="col1")
for url1 in download_list:
    try:
        down_url = urllib.parse.urljoin(url, url1.select("a:nth-of-type(1)")[0]["href"])
        # print(down_url)
        driver.get(down_url)
        driver.find_element_by_xpath("//*[@class='download-link']").click()
    except IndexError:
        pass

print("Done.")
