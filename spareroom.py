from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


message = """Hey,

I'm looking for someone to replace me in my current house in Maida Vale ASAP.
This is my ad: www.spareroom.co.uk/flatshare/ london/maida_vale/14904769

Please let me know if you have any questions.

Many thanks
Sebastian
"""

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)


driver.get("https://www.spareroom.co.uk/flatshare/logon.pl")

driver.find_element_by_id("loginemail").send_keys("voneuwdel@gmail.com")
driver.find_element_by_id("loginpass").send_keys("5RM&MBzawbs5")
driver.find_element_by_id("sign-in-button").click()


url = "https://www.spareroom.co.uk/flatmate/flatmates.pl?flatshare_type=wanted&=&search_id=956693413&offset={}&sort_by=days_since_placed"


listings = []

for page in range(0, 651, 10):
    time.sleep(1)
    print(page, len(listings))
    driver.get(url.format(page))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all("li", {"class": "listing-result"})
    for result in results:
        current = {}
        current['title'] = result.find('header').find('a').find('h1').get_text().strip()
        current['url'] = result.find('header').find('a')['href']
        current['status'] = result.find('footer').find('span').get_text().strip()
        current['status2'] = result.find('footer').find('span', {'class': 'tooltip_text'}).get_text().strip()
        listings.append(current)

# df = pd.DataFrame(listings)

count=0
for i, l in enumerate(listings):
    if 'couple' in l['title'].lower():
        continue
    if l['status2'] == 'You have contacted this ad. Click the link to change its status.':
        continue
    print(count, l['title'])

    driver.get("https://www.spareroom.co.uk"+l['url']+'&mode=contact&submode=byemail')
    driver.find_element_by_id('message').send_keys(message)
    driver.find_element_by_class_name('contact-form__submit').click()
    count += 1
    time.sleep(3)


