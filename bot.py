from work_with_csv_sheet import query_find
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

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


#
# message = input("Введите что-нибудь, чтобы проверить это: \n")
# output = finder_csv(message)
# print(output)
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
API_TOKEN = '1823284420:AAEViu87LzrPenHUj7z531RIvnG6q_LUmAY'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
result = []
inline_kb_full = InlineKeyboardMarkup(row_width=1)
inline_kb_full.insert(InlineKeyboardButton('Смотреть ещё', callback_data='смотреть ещё'))
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.reply("Привет!\nЯ помогу найти нужный курс!")


@dp.message_handler(content_types=types.ContentType.TEXT )
async def finder(message: types.Message):
    global result


    await message.answer('<b>Начинаю искать...</b>', parse_mode=types.ParseMode.HTML)
    await message.bot.send_chat_action(message.from_user.id, 'typing')

    result = query_find(message.text)
    if result:
        for i in range(len(result)):
            if i < 5:
                await message.answer(result.pop())
                await asyncio.sleep(0.4)

            else:
                await message.answer(result.pop(), reply_markup=inline_kb_full)
                break
        await message.answer('<strong>Для уточнения цены и покупки пишите: @coolcourse</strong>', parse_mode=types.ParseMode.HTML)
    else:
        await message.answer('<strong>По данному запросу ничего не найдено</strong>',
                             parse_mode=types.ParseMode.HTML)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global result
    for i in range(len(result)):
        if i < 5:
            await callback_query.message.answer(result.pop())
            await asyncio.sleep(0.4)
        else:
            await callback_query.message.answer(result.pop(), reply_markup=inline_kb_full)
            break

    await callback_query.message.answer('<strong>Для уточнения цены и покупки пишите: @coolcourse</strong>', parse_mode=types.ParseMode.HTML)

dp.register_callback_query_handler(process_callback_kb1btn1, lambda c: c.data and c.data.startswith('смотреть ещё'))

if __name__ == '__main__':    executor.start_polling(dp, skip_updates=True)