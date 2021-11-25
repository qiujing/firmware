import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

list_url = "http://miwifi.com/miwifi_download.html"
driver_path = r'D:\chromedriver2\chromedriver.exe'
options = webdriver.ChromeOptions()
out_path = r'D:\firmware\MiWifi'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.get(list_url)
time.sleep(2)
driver.find_element_by_xpath("//*[@class='dlNav dlli_right']").click()
time.sleep(2)
bs4 = BeautifulSoup(driver.page_source, "lxml")
download_list = bs4.find_all(class_="link_download")
for download in download_list:
    download_url = str(download['href'])
    if re.findall(r'http.*?.bin',download_url):
        print(download_url)
        driver.get(download_url)
driver.close()
print("Done.")
