from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

inline_button1 = [ 
    InlineKeyboardButton('Отправить номер', callback_data='send_number')
]

inline_button2 = [
    InlineKeyboardButton('Отправить местоположение', callback_data='send_location')
]

inline_button3 = [
    InlineKeyboardButton('Заказать еду', callback_data='take_order')
]

inline_button1 = InlineKeyboardMarkup().add(*inline_button1)
inline_button2 = InlineKeyboardMarkup().add(*inline_button2)
inline_button3 = InlineKeyboardMarkup().add(*inline_button3)

number_button = [
    KeyboardButton('Подтвердить отправку номера.', request_contact=True, )
]

location_button = [
    KeyboardButton('Подтвердить отправку местоположения.', request_location=True)
]

num_button = ReplyKeyboardMarkup(resize_keyboard=True).add(*number_button)
loc_button = ReplyKeyboardMarkup(resize_keyboard=True).add(*location_button)