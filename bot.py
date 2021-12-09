import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from parser import main
import os
import asyncio

bot = Bot(token='', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = [
    'Смартфоны и Аксессуары', 
    'Инструменты',
    'TV/Фото',
    'Ноутбуки и Компьютеры',
    'Бытовая техника',
    'Часы',
    'Спорт',
    'Для дома',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Выберите категорию', reply_markup=keyboard)
    

@dp.message_handler(Text(equals='Смартфоны и Аксессуары'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(1)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)
        
@dp.message_handler(Text(equals='Инструменты'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(2)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)
    
@dp.message_handler(Text(equals='TV/Фото'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(3)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)

@dp.message_handler(Text(equals='Ноутбуки и Компьютеры'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(4)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)

@dp.message_handler(Text(equals='Бытовая техника'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(5)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)


@dp.message_handler(Text(equals='Часы'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(6)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)

@dp.message_handler(Text(equals='Спорт'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(7)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)

@dp.message_handler(Text(equals='Для дома'))
async def get_smart(message: types.Message):
    await message.answer('Please waiting...')
    
    main(8)
    
    with open('result.json') as file:
        data = json.load(file)
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("url"), item.get("name"))}\n' \
            f'{hbold("Цена: ")}{item.get("price")} грн🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)

    
def start():
    executor.start_polling(dp)
    
    
if __name__ == '__main__':
    start()
