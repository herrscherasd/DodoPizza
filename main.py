from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import logging
import os

from buttons import button, loc_button, num_button
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
        cursor.execute(f"INSERT INTO customers VALUES ('{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.from_user.id}', 'None');")
    connect.commit()

@dp.callback_query_handler(lambda call : call)
async def inline(call):
    if call.data == 'send_number':
        await get_number(call.message)
    elif call.data == 'send_location':
        await get_location(call.message)

@dp.message_handler(commands='number')
async def get_number(message:types.Message):
    await message.answer('Подтвердите отправку своего номера.', reply_markup=num_button)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def add_number(message:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"UPDATE customers SET phone_number = '{message.contact['phone_number']}' WHERE user_id = {message.from_user.id};")
    connect.commit()
    await message.answer("Ваш номер успешно добавлен.")

@dp.message_handler(commands='location')
async def get_location(message:types.Message):
    await message.answer("Подтвердите отправку местоположения.", reply_markup=loc_button)

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def add_location(message:types.Message):
    await message.answer("Ваш адрес записан.")
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO address VALUES ('{message.from_user.id}', '{message.location.longitude}', '{message.location.latitude}');")
    connect.commit()



executor.start_polling(dp)