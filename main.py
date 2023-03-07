from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import logging
import time
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
    await message.answer(f'Здравствуйте, {message.from_user.full_name}')
    await message.answer("В этом боте вы можете оставить свой заказ на пиццу.\n\nНо не забывайте оставить ваш адрес и контактный номер!!!", reply_markup=button)
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
    elif call.data == 'take_order':
        await get_order(call.message)

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

@dp.message_handler(commands='order')
async def get_order(message:types.Message):
    await message.reply("Прошу, меню:")

    with open('pizza1.webp', 'rb') as photo1:
        await message.answer_photo(photo1, caption='1. Пицца-сказка\n\n25 см, традиционное тесто, 360 г\n\nМоцарелла, смесь сыров чеддер и пармезан, цыпленок, пепперони, соус альфредо\n\nЦена: 399 сом')

    with open('pizza2.webp', 'rb')as photo2:
        await message.answer_photo(photo2, caption='2. Пепперони-сердце\n\n30 см, тонкое тесто, 380 г\n\nПепперони из говядины, моцарелла, томатный соус\n\nЦена: 649 сом')

    with open('pizza3.webp', 'rb')as photo3:
        await message.answer_photo(photo3, caption='3. Четыре сыра\n\n30 см, традиционное тесто, 550 г\n\nМоцарелла, сыры чеддер и пармезан, сыр блю чиз, соус альфредо\n\nЦена: 695 сом')

    with open('pizza4.webp', 'rb')as photo4:
        await message.answer_photo(photo4, caption='4. Додоко\n\n30 см, традиционное тесто, 720 г\n\nВетчина из цыпленка, пепперони из цыпленка, моцарелла, шампиньоны, сладкий перец, красный лук, чеснок, томатный соус, томаты, фарш из говядины\n\nЦена: 695 сом')

    with open('pizza5.webp', 'rb')as photo5:
        await message.answer_photo(photo5, caption='5. Четыре сезона\n\n30 см, традиционное тесто\n\nМоцарелла, ветчина из цыпленка, пепперони из цыпленка, кубики брынзы, томаты, шампиньоны, томатный соус, итальянские травы\n\nЦена: 695 сом')

    await message.answer("Введите номер из меню и мы запишем ваш заказ.")

@dp.message_handler(text=[1,2,3,4,5])
async def add_order(message:types.Message):
    cursor = connect.cursor()
    if message.text == '1':
        cursor.execute(f"INSERT INTO orders VALUES('Пицца-сказка', 'None', '{time.ctime()}');")
    if message.text == '2':
        cursor.execute(f"INSERT INTO orders VALUES('Пепперони-сердце', 'None', '{time.ctime()}');")
    if message.text == '3':
        cursor.execute(f"INSERT INTO orders VALUES('Четыре сыра', 'None', '{time.ctime()}');")
    if message.text == '4':
        cursor.execute(f"INSERT INTO orders VALUES('Додоко', 'None', '{time.ctime()}');")
    if message.text == '5':
        cursor.execute(f"INSERT INTO orders VALUES('Четыре сезона', 'None', '{time.ctime()}');")
    connect.commit()
    await message.reply("Ваш заказ записан")

executor.start_polling(dp)