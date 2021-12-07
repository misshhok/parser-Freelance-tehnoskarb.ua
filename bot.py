import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from parser import main
import os
import asyncio

bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = []
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Выберите категорию', reply_markup=keyboard)
    

@dp.message_handler(Text(equals=''))
async def get_discount_knives(message: types.Message):
    await message.answer('Please waiting...')
    
    
    
    
        
    for index, item in enumerate():
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
            f'{hbold("Цена: ")}${item.get("item_price")}🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)
        
        
@dp.message_handler(Text(equals=''))
async def get_discount_guns(message: types.Message):
    await message.answer('Please waiting...')
    
    
    
    
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
            f'{hbold("Цена: ")}${item.get("item_price")}🔥'
    
    
        if index%5 == 0:
            asyncio.sleep(1)
            
        await message.answer(card)

    
def main():
    executor.start_polling(dp)
    
    
if __name__ == '__main__':
    main()
