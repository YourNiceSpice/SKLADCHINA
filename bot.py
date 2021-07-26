from work_with_csv_sheet import query_find
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import re
# def finder(message):
#     """
#     find all entries
#     """
#     find = SheetsHandler()
#
#     result = find.query_find(message)
#     q = 1
#     return result

def finder_csv(message):
    """
    find all entries
    """

    result = query_find(message)
    return result



import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
API_TOKEN = '1823284420:AAEViu87LzrPenHUj7z531RIvnG6q_LUmAY'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


inline_kb_full = InlineKeyboardMarkup(row_width=1)
inline_kb_full.insert(InlineKeyboardButton('Ещё результаты', callback_data='смотреть ещё'))
storage = {}

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.reply("Привет!\nЯ помогу найти нужный курс!")


async def process(id):
    result = storage[id]
    for i in range(len(result)):
        if i < 5:
            await bot.send_message(id, result.pop())
            await asyncio.sleep(0.4)
        else:
            await bot.send_message(id,result.pop(), reply_markup=inline_kb_full)
            break
    await bot.send_message(id,'<strong>Для уточнения цены и покупки пишите: @coolcourse</strong>',
                         parse_mode=types.ParseMode.HTML)
    if not result:
        del storage[id]

@dp.message_handler(content_types=types.ContentType.TEXT )
async def finder(message: types.Message):

    if re.findall(r"^[A-Za-zА-Яа-я0-9_-]*$", message.text):

        await message.answer('<b>Начинаю искать...</b>', parse_mode=types.ParseMode.HTML)
        await message.bot.send_chat_action(message.from_user.id, 'typing')

        global storage
        result = query_find(message.text)

        if result:
            storage[message.from_user.id] = result
            await process(message.from_user.id)
        else:
            await message.answer('<strong>По данному запросу ничего не найдено</strong>',
                                 parse_mode=types.ParseMode.HTML)
    else:
        await message.answer('Не указывайте в поиске символы')

async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await process(callback_query.from_user.id)

dp.register_callback_query_handler(process_callback_kb1btn1, lambda c: c.data and c.data.startswith('смотреть ещё'))

if __name__ == '__main__':    executor.start_polling(dp, skip_updates=True)