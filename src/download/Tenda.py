import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver

driver_path = r'D:\chromedriver2\chromedriver.exe'
options = webdriver.ChromeOptions()
out_path = r'D:\firmware\Tenda'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=driver_path, options=options)

first_url="https://www.tenda.com.cn/download/default.html"
html = requests.get(first_url).text
bs41 = BeautifulSoup(html,"html.parser")
url_list = bs41.find_all(class_="t3")

for url in url_list:
    url_str = str(url['href'])
    down = urllib.parse.urljoin("http:", url_str)
    html1 = requests.get(down).text
    soup = BeautifulSoup(html1,"html.parser")
    download_list = soup.find_all(class_="btn-download ga-data")
    for download in download_list:
        download_str = str(download['href'])
        download_url = urllib.parse.urljoin("http:", download_str)
        driver.get(download_url)
        driver.find_element_by_xpath("//*[@class='btnxz btndown downhits']").click()

driver.quit()
print("Done.")
