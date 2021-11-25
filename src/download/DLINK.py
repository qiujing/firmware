import urllib.request
from urllib.parse import quote

from bs4 import BeautifulSoup
from selenium import webdriver

driver_path = r'D:\chromedriver2\chromedriver.exe'
options = webdriver.ChromeOptions()
out_path = r'D:\firmware\DLINK'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=driver_path, options=options)
url = "http://support.dlink.com.cn:9000/AllPro.aspx"
down_url = "http://support.dlink.com.cn:9000/ProductInfo.aspx?m="
first_url = "http://support.dlink.com.cn:9000"
driver.get(url)
bs4 = BeautifulSoup(driver.page_source, "lxml")
namelist = bs4.find_all(class_="aRedirect")

unvisited = []
for name in namelist:
    text = name['alt']
    prourl = urllib.parse.urljoin(down_url, text)
    if prourl != "" and prourl not in unvisited:
        unvisited.insert(0, prourl)

while True:
    if len(unvisited) == 0:
        print("Done.")
        break
    visitedurl = unvisited.pop()

    driver.get(visitedurl)
    options = BeautifulSoup(driver.page_source, "lxml").find_all("option")
    if not options:
        continue
    down_urls = BeautifulSoup(driver.page_source, "lxml").find_all(class_="fileDownload")
    '''
    a = BeautifulSoup(driver.page_source,"lxml")#.find_all(id="litProductModelNo")
    b = str(a.select('#litProductModelNo'))
    name = re.findall(r'(?<=<span id="litProductModelNo" class="color1 font14em" style="line-height: 0px;">).*?(?=</span>)',b)
    print(name)
    '''

    for downurl in down_urls:
        if str(downurl['href']) == "javascript:void(0);":
            continue
        else:
            download = urllib.parse.urljoin(first_url, downurl['href'])
            print(download)
            driver.get(download)
driver.close()
print("Done.")

