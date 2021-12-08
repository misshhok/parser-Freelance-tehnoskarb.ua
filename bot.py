import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from parser import main
import os
import asyncio

bot = Bot(token='5070639816:AAG1YkTnFe0t161-CisoRyMN1kEt7GQ7nWs', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Проверить обновления товаров', 'Фильтры']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Выберите действие', reply_markup=keyboard)
    

@dp.message_handler(Text(equals='Проверить обновления товаров'))
async def get_discount_knives(message: types.Message):
    await message.answer('Please waiting...')
    
    main()
    conn = sqlite3.connect('techno-scrab.db')
    cur = conn.cursor()

    products = cur.execute('SELECT * FROM products ORDER BY productPRICE')
    
    for index,item in enumerate(products):
        card = f'{hlink(item[2])}\n' \
            f'{hbold("Название: ")}{item[1]}%\n' \
            f'{hbold("Цена: ")}${item[3]}🔥'
        
    # for index, item in enumerate():
    #     card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
    #         f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
    #         f'{hbold("Цена: ")}${item.get("item_price")}🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
        if index%20 == 0:
            break 
        await message.answer(card)
        
        
# @dp.message_handler(Text(equals=''))
# async def get_discount_guns(message: types.Message):
#     await message.answer('Please waiting...')
    
    
    
    
        
#     for index, item in enumerate(data):
#         card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
#             f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
#             f'{hbold("Цена: ")}${item.get("item_price")}🔥'
    
    
#         if index%5 == 0:
#             asyncio.sleep(1)
            
#         await message.answer(card)

    
def main():
    executor.start_polling(dp)
    
    
if __name__ == '__main__':
    main()
