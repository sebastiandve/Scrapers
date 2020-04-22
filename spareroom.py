from bs4 import BeautifulSoup
from selenium import webdriver
import time


message = """Hey,

I'm looking for someone to replace me in my current house in Maida Vale ASAP.
This is my ad: www.spareroom.co.uk/flatshare/ london/maida_vale/14904769

Please let me know if you have any questions.

Many thanks
Sebastian
"""

driver = webdriver.Chrome()

driver.get("https://www.spareroom.co.uk/flatshare/logon.pl")

driver.find_element_by_id("loginemail").send_keys("voneuwdel@gmail.com")
driver.find_element_by_id("loginpass").send_keys("5RM&MBzawbs5")
driver.find_element_by_id("sign-in-button").click()

driver.get("https://www.spareroom.co.uk/flatmate/flatmates.pl?search_id=956693413&")

listings = []
page = 0
while True:
    time.sleep(1)
    print(page)
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

    try:
        driver.find_element_by_id("paginationNextPageLink").click()
        page += 1

    except:
        break

for i, l in enumerate(listings):

    print(i, l['title'])
    if 'couple' in l['title'].lower():
        continue
    if l['status2'] == 'You have contacted this ad. Click the link to change its status.':
        continue
    driver.get("https://www.spareroom.co.uk"+l['url']+'&mode=contact&submode=byemail')
    driver.find_element_by_id('message').send_keys(message)
    driver.find_element_by_class_name('contact-form__submit').click()
    time.sleep(1)


