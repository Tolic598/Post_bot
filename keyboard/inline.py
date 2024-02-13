from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# start
button1 = InlineKeyboardButton(text="Выбрать канал для поста", callback_data="add_post")
button2 = InlineKeyboardButton(text="Добавить канал", callback_data="add")

menu = InlineKeyboardMarkup(inline_keyboard=[
                                            [button1],
                                            [button2]
                                            ],row_width=2)

# добавления кнопки
button1 = InlineKeyboardButton(text="Добавить кнопки", callback_data="add_buttons")
button2 = InlineKeyboardButton(text="Предварительный просмотр", callback_data="look")

add_text = InlineKeyboardMarkup(inline_keyboard=[
                                            [button1],
                                            [button2]
                                            ],row_width=2)

# добавления кнопки ещё
button1 = InlineKeyboardButton(text="Добавить ещё", callback_data="add_buttons")
button2 = InlineKeyboardButton(text="Предварительный просмотр", callback_data="look")

add_but = InlineKeyboardMarkup(inline_keyboard=[
                                            [button1],
                                            [button2]
                                            ],row_width=2)

# не добавлять фото
button1 = InlineKeyboardButton(text="Не добавлять", callback_data="del_ph_vi")

del_ph = InlineKeyboardMarkup(inline_keyboard = [[button1]],row_width=2)

# готово
button1 = InlineKeyboardButton(text="Отправить", callback_data="ok")
button2 = InlineKeyboardButton(text="Главное меню", callback_data="menu")

menu_gotov = InlineKeyboardMarkup(inline_keyboard=[
                                            [button1],
                                            [button2]
                                            ],row_width=2)

# меню
button2 = InlineKeyboardButton(text="Главное меню", callback_data="menu")

menu_menu = InlineKeyboardMarkup(inline_keyboard=[[button2]],row_width=2)