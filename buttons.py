from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons = [ 
    InlineKeyboardButton('Отправить номер', callback_data='send_number'),
    InlineKeyboardButton('Отправить местоположение', callback_data='send_location'),
    InlineKeyboardButton('Заказать еду', callback_data='take_order')
]
button = InlineKeyboardMarkup().add(*inline_buttons)