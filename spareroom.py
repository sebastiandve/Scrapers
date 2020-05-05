from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

def get_contact_status(item):
    try:
        return item.find('footer').find('a', {'class': 'tooltip savedAd'}).find('span').get_text().strip()
    except:
        return "Not contacted"

def is_contactable(item):
    try:
        item.find('footer').find('span', {'class': 'freeContact status'}).get_text().strip()
    except:
        return "Early Bird"

message = """Hey,

I'm looking for someone to replace me in my current house in Maida Vale and can move in June at the latest.
This is my ad: www.spareroom.co.uk/flatshare/london/maida_vale/14904769

Please let me know if you have any questions.

PS: A second room in the house is also available

Cheers
Sebastian
"""

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)


driver.get("https://www.spareroom.co.uk/flatshare/logon.pl")

driver.find_element_by_id("loginemail").send_keys("voneuwdel@gmail.com")
driver.find_element_by_id("loginpass").send_keys("5RM&MBzawbs5")
driver.find_element_by_id("sign-in-button").click()


url = "https://www.spareroom.co.uk/flatmate/flatmates.pl?flatshare_type=wanted&=&search_id=959113513&offset={}&sort_by=days_since_placed"


listings = []

for page in range(0, 991, 10):
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
        current['contactable'] = is_contactable(result)
        current['status'] = get_contact_status(result)
        listings.append(current)

df = pd.DataFrame(listings)
print(len(listings))
print(df.status.value_counts())

count=0
for i, l in enumerate(listings):
    if 'couple' in l['title'].lower():
        count+=1
        continue
    elif l['status'].strip() == 'Contacted':
        count += 1
        continue
    elif l['contactable'] == 'Early Bird':
        count += 1
        continue
    else:
        print(count, l['title'], l['status'])

        driver.get("https://www.spareroom.co.uk"+l['url']+'&mode=contact&submode=byemail')
        driver.find_element_by_id('message').send_keys(message)
        driver.find_element_by_class_name('contact-form__submit').click()
        count += 1
        time.sleep(1)


