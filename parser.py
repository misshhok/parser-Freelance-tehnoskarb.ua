from bs4 import BeautifulSoup, element
import requests
import sqlite3   # импорты необходимых бибилиотек



URL  = 'https://tehnoskarb.ua/katalog-komissionnojj-tekhniki/c-all/filter/new=1'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
    }
HOST = 'https://tehnoskarb.ua' # инициализация конгстант URL HEADERS и HOST


 # -----------------------------------------------------
conn = sqlite3.connect('techno-scrab.db') # создание и подключение базы данных SQLite3
cur = conn.cursor()
                          # создание таблцы
cur.execute("""CREATE TABLE IF NOT EXISTS products(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
productNAME TEXT,                                           
productURl TEXT,
productPRICE INTEGER);
""")                      # создание полей таблцы
conn.commit()
# -------------------------------------------------------

def get_html(url, params=''): # функция для получения html кода страницы передаваемой через парметр url
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def main(html):  # извлечение небходимой информации из html-кода 
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('div', class_ = 'tc-el-pagination c-pagination tc-is-background')

    for page in pages:
        number = int(page.find_all('li')[-1].get_text()) # пагинация
    
    

    i = 1

    while i <= number:
        url = 'https://tehnoskarb.ua/katalog-komissionnojj-tekhniki/c-all/filter/new=1?page={}' # после того как получили url страницы из пагинации посылаем get-запрос для получения html-кода
        r = requests.get(url.format(i), headers=HEADERS, params='')
        
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('div', class_ = 'c-model__item')  # получение карточек товаров
        
        for item in items:

            # получение из карточки 
            # 1) наименования товара
            # 2) url товара
            # 3) цены товара
            
            itemNAME = item.find('div', class_ = 'c-model-content d-f fl-d-c').find('h2').find('a').get_text().strip()
            itemURL = HOST + item.find('div', class_ = 'c-model-content d-f fl-d-c').find('h2').find('a').get('href')
            itemPRICERR = item.find('div', class_ = 'c-model-content d-f fl-d-c').find('div', class_ = 'c-model-price text-truncate')
            # так как не во всех карточках присутствует цена приходится проверять ее наличие в карточке перед тем как ее заносить в БД
            # после получения цены с помощью get_text() необходимо разбить цену по разделителю "-"
            # itemPRICE - список, его первый элемент нужно превратить в int
            # если в списке 2 элемента то мы берем только 1 первый как минимальную цену
            if not(itemPRICERR is None):
                
                itemPRICE = itemPRICERR.get_text().replace(' ', '')[:-3].split('-')
                if len(itemPRICE) == 2:
                    del itemPRICE[1]
                    itemPRICE = int(itemPRICE[0])
                else:
                    itemPRICE = int(itemPRICE[0])
            else:
                itemPRICE = None
            # Создание кортежа для последущей передачи в БД
            # так-как sqlite3 при передаче VALUES требует кортеж
            el = (
                None,
                itemNAME,
                itemURL,
                itemPRICE
            )
            cur.execute("INSERT INTO products VALUES (?, ?, ?, ?);", (el))
            conn.commit()
            # выполнение SQL-запроса

    #         print('запись добавлена')
    # print('Все записи были добавлены!')   


    
    
if __name__ == '__main__':
    html = get_html(URL)
    result = main(html.text)