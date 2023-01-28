from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = "https://www.linkedin.com/jobs/search?keywords=Developer&location=Ireland&geoId=104738515&f_TPR=r7200&currentJobId=3453541841&position=1&pageNum=0"

# preparing driver to allow for js loading before parsing the page
options = Options()
options.add_argument('-headless')
browser = webdriver.Firefox(options=options)

browser.get(url)
soup = BeautifulSoup(browser.page_source,"lxml")

print(soup.prettify())