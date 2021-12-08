from bs4 import BeautifulSoup, element
import requests
import sqlite3   # импорты необходимых бибилиотек



URL  = 'https://tehnoskarb.ua/katalog-komissionnojj-tekhniki/c-all/filter/new=1'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
    }
HOST = 'https://tehnoskarb.ua' # инициализация конгстант URL HEADERS и HOST

urls = {
    'Smartphones': 'https://tehnoskarb.ua/telefony-smartfony-aksessuary/c66/filter/new=1',
    'Instruments': 'https://tehnoskarb.ua/instrumenty-i-oborudovanie/c49/filter/new=1',
    'TV/Photo': 'https://tehnoskarb.ua/televizory-foto-audio-video/c2/filter/new=1',
    'Notebooks': 'https://tehnoskarb.ua/noutbuki-planshety-kompjutery/c33/filter/new=1',
    'Appliances': 'https://tehnoskarb.ua/bytovaja-tekhnika/c141/filter/new=1',
    'Clocks': 'https://tehnoskarb.ua/chasy-naruchnye/c39/filter/new=1',
    'Sport': 'https://tehnoskarb.ua/sport-i-otdykh/c122/filter/new=1',
    'House': 'https://tehnoskarb.ua/dom-sad-i-remont/c761/filter/new=1',
    'Auto' : 'https://tehnoskarb.ua/avtotovary/c112/filter/new=1'
}

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



def main():  # извлечение небходимой информации из html-кода 
    print('Выберите категроию - ')
    print('Доступные категории:')
    print('Smartphones - 1 \n' 
    'Instruments - 2 \n'
    'TV/Photo - 3 \n'
    'Notebooks - 4 \n'
    'Appliances - 5 \n'
    'Clocks - 6 \n'
    'Sport - 7 \n'
    'House - 8 \n'
    'Auto - 9 \n')
    category = int(input())
    if category == 1:
        url = urls['Smartphones']
    elif category == 2:
            url = urls['Instruments']
    elif category == 3:
            url = urls['TV/Photo']
    elif category == 4:
            url = urls['Notebooks']
    elif category == 5:
            url = urls['Appliances']
    elif category == 6:
            url = urls['Clocks']
    elif category == 7:
            url = urls['Sport']
    elif category == 8:
            url = urls['House']
    elif category == 9:
            url = urls['Auto']
    else:
        print('none')
    r = requests.get(url, headers=HEADERS, params='')

    soup = BeautifulSoup(r.text, 'html.parser')
    pages = soup.find_all('div', class_ = 'tc-el-pagination c-pagination tc-is-background')

    for page in pages:
        number = int(page.find_all('li')[-1].get_text()) # пагинация
    
    
    number = int(number / 2)
    i = 1
    count = 0
    for i in range(number, 0, -1):
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
                itemPRICERR = item.find('div', class_ = 'c-model-content d-f fl-d-c').find('div', class_ = 'c-model-price text-truncate c-model-price--sale')
                itemPRICE = itemPRICERR.get_text().replace(' ', '')[:-3].split('-')
                if len(itemPRICE) == 2:
                    del itemPRICE[1]
                    itemPRICE = int(itemPRICE[0])
                else:
                    itemPRICE = int(itemPRICE[0])
            # Создание кортежа для последущей передачи в БД
            # так-как sqlite3 при передаче VALUES требует кортеж
            el = (
                None,
                itemNAME,
                itemURL,
                itemPRICE
            )
            info = cur.execute('SELECT * FROM products WHERE ID=? OR productNAME=? AND productURL=? AND productPRICE=? ', (el))
            if info.fetchone() is None: 
                cur.execute("INSERT INTO products VALUES (?, ?, ?, ?);", (el))
                conn.commit()
                print("запись добавлена в таблицу")
                count +=1
            else:
                print("запись есть в таблице")
    print(f'{count} - добавлено в таблицу')
            
            # выполнение SQL-запроса

    #         print('запись добавлена')
    # print('Все записи были добавлены!')   


    
    
if __name__ == '__main__':
    main()