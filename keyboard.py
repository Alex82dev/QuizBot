from telegram import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для ввода пароля
password_keyboard = ReplyKeyboardMarkup([[KeyboardButton('Отмена')]], one_time_keyboard=True)
