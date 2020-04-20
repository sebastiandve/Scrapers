from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlunparse
import requests
import pandas as pd
import time


def get_price(listing, type='any'):
    price_node = listing.find('a', class_='text-price')
    price = price_node.get_text()

    price = (price.strip())
    if type == 'any':
        return price
    elif type == 'monthly':
        try:
            price = int(get_price(listing).replace(',', '').split(' ')[0][1:].replace(',', ''))
            return price
        except:
            return None

    elif type == 'weekly':
        try:
            int(get_price(listing).split('(')[1].split(' ')[0][1:].replace(',',''))
            return price
        except:
            return None


def beds(listing):
    try:
        return int(
            listing
            .find('span', class_='num-beds')
            .get_text()
            .strip()
        )
    except:
        return None

def parse_listing(listing):
    return {
        'listing_id' : int(listing.attrs['data-listing-id']),
        'price'      : get_price(listing, 'any'),
        'clean_price': get_price(listing, 'monthly'),
        # 'weekly_price': get_price(listing, 'weekly'),
        'address': listing.find('a', {'class':'listing-results-address'}).get_text(),
        'beds': beds(listing),
        'propertyURL': listing.find('a', {'class': 'listing-results-price text-price'})['href'],
        # 'latitude'   : listing.find('meta', itemprop='latitude').attrs['content'],
        # 'longitude'  : listing.find('meta', itemprop='longitude').attrs['content'],
        'Brandtradingname': listing.find('p', {'class': 'top-half listing-results-marketed'}).find('span').get_text(),
        'Propertytypefulldescription': listing.find('div', {'class': 'listing-results-right clearfix'}).find_all('p')[-1].get_text().strip(),
        'Summary': listing.find('h2', {'class': 'listing-results-attr'}).find('a').get_text().strip()
    }

def parse_listings(listings):
    return map(parse_listing, listings)



# """https://www.zoopla.co.uk/for-sale/property/west-yorkshire/leeds/?is_auction=false&is_retirement_home=false&is_shared_ownership=false&new_homes=exclude&q=Leeds&radius=10&results_sort=newest_listings&search_source=refine"""

# """https://www.zoopla.co.uk/for-sale/property/devon/exeter/?is_auction=false&is_retirement_home=false&is_shared_ownership=false&new_homes=exclude&q=Exeter&radius=10&results_sort=newest_listings&search_source=home"""


results = []
s = time.time()
for i in range(1, 9 + 1):
    params = {
        'q': 'Exeter',
        'is_auction': 'false',
        'is_retirement_home': 'false',
        'is_shared_ownership': 'false',
        'new_homes': 'exclude',
        # 'identifier': 'west-yorkshire%2Fleeds',
        # 'search_source': 'refine',
        # 'new_homes': 'include',
        'results_sort': 'newest_listings',
        'search_source': 'refine',
        # 'include_retirement_homes': 'true',
        # 'include_shared_ownership': 'true',
        # 'price_frequency': 'per_month',
        'radius': 10,
        'page_size': 100,
        'pn': i
    }

    url = urlunparse([
        'http',
        'www.zoopla.co.uk',
        'for-sale/property/devon/exeter',
        '',
        urlencode(params),
        ''
    ])

    soup = BeautifulSoup(requests.get(url).content, 'html5lib')

    soups = soup.find_all('li', attrs={'data-listing-id': True})
    listings = parse_listings(soups)

    results = results + list(map(dict,listings))

df = pd.DataFrame(results)

df.to_excel('sales_Exeter.xlsx')
print(time.time() - s)
print('\007')
