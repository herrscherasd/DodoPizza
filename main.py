from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import logging
import os

from buttons import button
from databases import DataBaseCustomers

db = DataBaseCustomers()
connect = db.connect
db.connect_db()

load_dotenv('.env')

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}', reply_markup=button)
    cursor = connect.cursor()
    cursor.execute(f'SELECT user_id FROM customers WHERE user_id = {message.from_user.id};')
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"INSERT INTO customers VALUES ('{message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.username}, {message.from_user.id}');")
    connect.commit()

# @dp.callback_query_handler(lambda call : call)
# async def inline(call):
#     if call.data == 'send_number':
#         await add_number(call.message)
#     elif call.data == 'send_location':
#         await add_location(call.message)


executor.start_polling(dp)