from bs4 import BeautifulSoup
import requests




URL  = 'https://tehnoskarb.ua/katalog-komissionnojj-tekhniki/c-all/filter/new=1'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
    }
HOST = 'https://tehnoskarb.ua'

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def main(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('div', class_ = 'tc-el-pagination c-pagination tc-is-background')

    for page in pages:
        number = int(page.find_all('li')[-1].get_text())
    
    elements = []

    i = 1
    while i <= number:
        url = 'https://tehnoskarb.ua/katalog-komissionnojj-tekhniki/c-all/filter/new=1?page={}'
        r = requests.get(url.format(i), headers=HEADERS, params='')
        
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('div', class_ = 'c-model__item')
         
        for item in items:
            itemName = item.find('div', class_ = 'c-model-content d-f fl-d-c').find('h2').find('a').get_text()
            itemUrl = item.find('div', class_ = 'c-model-content d-f fl-d-c').find('h2').find('a').get('href')
            itemPriceR = item.find('div', class_ = 'c-model-content d-f fl-d-c').find('div', class_ = 'c-model-price text-truncate')
            if not(itemPriceR is None):
                itemPrice = itemPriceR.get_text()


            el = {
                'NAME' : itemName,
                'URL'  : HOST + itemUrl,
                'Price': itemPrice
            }

            elements.append(el)


        print(elements)


if __name__ == '__main__':
    html = get_html(URL)
    result = main(html.text)