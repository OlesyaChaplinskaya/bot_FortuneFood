from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import openpyxl
import sqlite3
import random
import os


# Функция для создания таблицы пользователей
def create_users_table():
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE
    )
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

# Функция для добавления user_id в таблицу пользователей
def add_user_to_database(user_id):
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


# Создание таблиц базы данных

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Recipes(Recipe_id INTEGER PRIMARY KEY, Category_id INTEGER, FOREIGN KEY (Category_id) REFERENCES Category(Category_id))'
    cursor.execute(query)

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Category(Category_id INTEGER PRIMARY KEY, Category_name TEXT)'
    cursor.execute(query)

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Lunch(Recipe_id INTEGER UNIQUE, Name_L TEXT, Ingredients_L TEXT, Instruction_L TEXT, FOREIGN KEY (Recipe_id) REFERENCES Recipes(Recipe_id))'
    cursor.execute(query)

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Dinner(Recipe_id INTEGER UNIQUE, Name_D TEXT, Ingredients_D TEXT, Instruction_D TEXT, FOREIGN KEY (Recipe_id) REFERENCES Recipes(Recipe_id))'
    cursor.execute(query)

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Immunity(Id INTEGER PRIMARY KEY, Name TEXT, Description TEXT)'
    cursor.execute(query)

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Energy(Id INTEGER PRIMARY KEY, Name TEXT, Description TEXT)'
    cursor.execute(query)

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Weight(Id INTEGER PRIMARY KEY, Name TEXT, Description TEXT)'
    cursor.execute(query)

with sqlite3.connect('venv\db\Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Products(Id INTEGER PRIMARY KEY, Name TEXT, Description TEXT)'
    cursor.execute(query)

with sqlite3.connect('venv/db/Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = '''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE
        )
        '''
    cursor.execute(query)

with sqlite3.connect('venv/db/Blackberry_bot.db') as db:
    cursor = db.cursor()
    query = '''
        CREATE TABLE IF NOT EXISTS Notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        send_day INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        '''
    cursor.execute(query)


# Чтение данных
workbook = openpyxl.load_workbook('C:/Users/Олеся/Desktop/bot/Tilda/Tilda_Заказы.xlsx')
sheet = workbook.active

# Подключение к базе данных SQLite
conn = sqlite3.connect('venv/db/Blackberry_bot.db')
c = conn.cursor()

# Проверка наличия таблицы Orders в базе данных и создание ее, если отсутствует
columns = [cell.value for cell in sheet[1]]
c.execute('CREATE TABLE IF NOT EXISTS Orders ({})'.format(' TEXT, '.join(columns)))

# Получение всех существующих заказов
c.execute('SELECT * FROM Orders')
existing_orders = c.fetchall()
existing_orders_dict = {tuple(row): True for row in existing_orders}

# Вставка новых данных из файла в бд (если они отсутствуют в существующих заказах)
for row in sheet.iter_rows(min_row=2, values_only=True):
    if tuple(row) not in existing_orders_dict:
        values = ','.join(['"' + str(cell) + '"' for cell in row])
        c.execute('INSERT INTO Orders VALUES ({})'.format(values))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()


bot = Bot('6572549436:AAE_zESbxcZgSNwIAmpIfpfZjJKpSPBP8C0')
dp = Dispatcher(bot)

def add_user_to_database(user_id):
    with sqlite3.connect('venv/db/Blackberry_bot.db') as db:
        cursor = db.cursor()
        cursor.execute("INSERT OR IGNORE INTO Users (user_id) VALUES (?)", (user_id,))

# Функция для получения уведомлений для определенного дня
def get_notifications_for_day(day):
    with sqlite3.connect('venv/db/Blackberry_bot.db') as db:
        cursor = db.cursor()
        # Получение уведомлений для заданного дня
        query = 'SELECT user_id, title, message FROM Notifications WHERE send_day = ?'
        cursor.execute(query, (day,))
        return cursor.fetchall()

# Асинхронная функция для отправки уведомлений
async def send_notifications(day):
    notifications = get_notifications_for_day(day)
    for user_id, title, message in notifications:
        # Отправка уведомления каждому пользователю
        await bot.send_message(user_id, f'{title}\n\n{message}')

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.chat.id
    # Добавление пользователя в базу данных
    add_user_to_database(user_id)
    inline_markup = InlineKeyboardMarkup()
    inline_markup.add(InlineKeyboardButton('Следующий шаг', callback_data='dalee'))
    # Приветственное сообщение пользователю
    await bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.full_name}!')
    await bot.send_message(message.chat.id, 'Мы рады приветствовать Вас в telegram bot магазина “Ежевика”!', reply_markup=inline_markup)

# Инициализация планировщика задач
scheduler = AsyncIOScheduler()

# Планирование задач отправки уведомлений на 6, 15 и 25 числа каждого месяца в 12:00
scheduler.add_job(send_notifications, CronTrigger(day='6', hour=12, minute=0), args=[6])
scheduler.add_job(send_notifications, CronTrigger(day='15', hour=12, minute=0), args=[15])
scheduler.add_job(send_notifications, CronTrigger(day='25', hour=12, minute=0), args=[25])

# Запуск планировщика
scheduler.start()


@dp.callback_query_handler(text='dalee')
async def next_step(callback_query: types.CallbackQuery):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Каталог', web_app=WebAppInfo(url='https://blackberrycatalog.tilda.ws')))
    markup.add(types.KeyboardButton('Рецепты', callback_data='recipes'))
    markup.add(types.KeyboardButton('Рекомендации', callback_data='advice'))
    await callback_query.message.answer('Воспользуйтесь кнопками в меню для выбора необходимого раздела.', reply_markup=markup)


user_sent_recipes = {}  # Инициализируем словарь для отслеживания отправленных рецептов

MAX_CAPTION_LENGTH = 1024

def create_caption(recipe_name, recipe_ingredients, recipe_instruction):
    full_caption = f'{recipe_name}\n\n{recipe_ingredients}\n\n{recipe_instruction}'
    if len(full_caption) > MAX_CAPTION_LENGTH:
        # Если длина подписи превышает допустимый лимит, сокращаем её
        truncated_caption = full_caption[:MAX_CAPTION_LENGTH - 3] + '...'
        return truncated_caption
    return full_caption

@dp.callback_query_handler(lambda call: call.data == 'breakfast')
async def send_breakfast_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Сброс отправленных рецептов при новом запросе
    user_sent_recipes[user_id] = {'breakfast': []}

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Breakfast')
    result = cursor.fetchall()

    if user_id not in user_sent_recipes:
        user_sent_recipes[user_id] = {'breakfast': []}

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recipes[user_id]['breakfast']]

    if not available_recipes:
        await call.message.answer("Все рецепты уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_ingredients = random_recipe[2]
    recipe_instruction = random_recipe[3]
    recipe_image = random_recipe[4]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление рецепта в список отправленных
    user_sent_recipes[user_id]['breakfast'].append(recipe_id)

    # Создание клавиатуры с кнопками "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_breakfast')
    keyboard.add(more_button)

    # Отправка случайного рецепта пользователю
    caption = create_caption(recipe_name, recipe_ingredients, recipe_instruction)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла (если необходимо)
    os.remove(image_path)


@dp.callback_query_handler(lambda call: call.data == 'more_breakfast')
async def send_more_breakfast_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Breakfast')
    result = cursor.fetchall()

    if user_id not in user_sent_recipes:
        user_sent_recipes[user_id] = {'breakfast': []}

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recipes[user_id]['breakfast']]

    if not available_recipes:
        await call.message.answer("Все рецепты уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_ingredients = random_recipe[2]
    recipe_instruction = random_recipe[3]
    recipe_image = random_recipe[4]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление рецепта в список отправленных
    user_sent_recipes[user_id]['breakfast'].append(recipe_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_breakfast')
    keyboard.add(more_button)

    # Отправка случайного рецепта пользователю
    caption = create_caption(recipe_name, recipe_ingredients, recipe_instruction)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла (если необходимо)
    os.remove(image_path)


# Хранение отправленных рецептов для каждого пользователя и каждого типа рецепта
user_sent_recipes = {}

MAX_CAPTION_LENGTH = 1024

def create_caption1(recipe_name, recipe_ingredients, recipe_instruction):
    full_caption = f'{recipe_name}\n\n{recipe_ingredients}\n\n{recipe_instruction}'
    if len(full_caption) > MAX_CAPTION_LENGTH:
        # Если длина подписи превышает допустимый лимит, сокращаем её
        truncated_caption = full_caption[:MAX_CAPTION_LENGTH - 3] + '...'
        return truncated_caption
    return full_caption

@dp.callback_query_handler(lambda call: call.data == 'lunch')
async def send_lunch_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Сброс отправленных рецептов при новом запросе
    if user_id in user_sent_recipes:
        user_sent_recipes[user_id]['lunch'] = []
    else:
        user_sent_recipes[user_id] = {'lunch': []}

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Lunch')
    result = cursor.fetchall()

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recipes[user_id]['lunch']]

    if not available_recipes:
        await call.message.answer("Все рецепты уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_ingredients = random_recipe[2]
    recipe_instruction = random_recipe[3]
    recipe_image = random_recipe[4]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление рецепта в список отправленных
    user_sent_recipes[user_id]['lunch'].append(recipe_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_lunch')
    keyboard.add(more_button)

    # Отправка случайного рецепта пользователю
    caption = create_caption1(recipe_name, recipe_ingredients, recipe_instruction)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла (если необходимо)
    os.remove(image_path)


@dp.callback_query_handler(lambda call: call.data == 'more_lunch')
async def send_more_lunch_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Lunch')
    result = cursor.fetchall()

    if user_id not in user_sent_recipes:
        user_sent_recipes[user_id] = {'lunch': []}

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recipes[user_id]['lunch']]

    if not available_recipes:
        await call.message.answer("Все рецепты уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_ingredients = random_recipe[2]
    recipe_instruction = random_recipe[3]
    recipe_image = random_recipe[4]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)
        # Добавление рецепта в список отправленных
        user_sent_recipes[user_id]['lunch'].append(recipe_id)

        # Создание клавиатуры с кнопкой "Еще"
        keyboard = types.InlineKeyboardMarkup()
        more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_lunch')
        keyboard.add(more_button)

        # Отправка случайного рецепта пользователю
        caption = create_caption1(recipe_name, recipe_ingredients, recipe_instruction)
        with open(image_path, 'rb') as photo:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=caption,
                reply_markup=keyboard
            )

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Удаление временного файла (если необходимо)
        os.remove(image_path)


# Хранение отправленных рецептов для каждого пользователя и каждого типа рецепта
user_sent_recipes = {}

MAX_CAPTION_LENGTH = 1024

def create_caption2(recipe_name, recipe_ingredients, recipe_instruction):
    full_caption = f'{recipe_name}\n\n{recipe_ingredients}\n\n{recipe_instruction}'
    if len(full_caption) > MAX_CAPTION_LENGTH:
        # Если длина подписи превышает допустимый лимит, сокращаем её
        truncated_caption = full_caption[:MAX_CAPTION_LENGTH - 3] + '...'
        return truncated_caption
    return full_caption

@dp.callback_query_handler(lambda call: call.data == 'dinner')
async def send_dinner_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Сброс отправленных рецептов при новом запросе
    if user_id in user_sent_recipes:
        user_sent_recipes[user_id]['dinner'] = []
    else:
        user_sent_recipes[user_id] = {'dinner': []}

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Dinner')
    result = cursor.fetchall()

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recipes[user_id]['dinner']]

    if not available_recipes:
        await call.message.answer("Все рецепты уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_ingredients = random_recipe[2]
    recipe_instruction = random_recipe[3]
    recipe_image = random_recipe[4]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление рецепта в список отправленных
    user_sent_recipes[user_id]['dinner'].append(recipe_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_dinner')
    keyboard.add(more_button)

    # Отправка случайного рецепта пользователю
    caption = create_caption2(recipe_name, recipe_ingredients, recipe_instruction)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


@dp.callback_query_handler(lambda call: call.data == 'more_dinner')
async def send_more_dinner_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Dinner')
    result = cursor.fetchall()

    if user_id not in user_sent_recipes:
        user_sent_recipes[user_id] = {'dinner': []}

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recipes[user_id]['dinner']]

    if not available_recipes:
        await call.message.answer("Все рецепты уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_ingredients = random_recipe[2]
    recipe_instruction = random_recipe[3]
    recipe_image = random_recipe[4]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)
        # Добавление рецепта в список отправленных
        user_sent_recipes[user_id]['dinner'].append(recipe_id)

        # Создание клавиатуры с кнопкой "Еще"
        keyboard = types.InlineKeyboardMarkup()
        more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_dinner')
        keyboard.add(more_button)

        # Отправка случайного рецепта пользователю
        caption = create_caption2(recipe_name, recipe_ingredients, recipe_instruction)
        with open(image_path, 'rb') as photo:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=caption,
                reply_markup=keyboard
            )

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Удаление временного файла
        os.remove(image_path)


# Хранение отправленных рекомендаций для каждого пользователя
user_sent_recommendations = {}

MAX_CAPTION_LENGTH = 1024

def create_caption3(recipe_name, recipe_description):
    full_caption = f'{recipe_name}\n\n{recipe_description}'
    if len(full_caption) > MAX_CAPTION_LENGTH:
        # Если длина подписи превышает допустимый лимит, сокращаем её
        truncated_caption = full_caption[:MAX_CAPTION_LENGTH - 3] + '...'
        return truncated_caption
    return full_caption

@dp.callback_query_handler(lambda call: call.data == 'immunity')
async def send_immunity_recommendation(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Сброс отправленных рекомендаций при новом запросе
    if user_id in user_sent_recommendations:
        user_sent_recommendations[user_id] = []
    else:
        user_sent_recommendations[user_id] = []

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Immunity')
    result = cursor.fetchall()

    # Фильтрация уже отправленных рекомендаций
    available_recommendations = [rec for rec in result if rec[0] not in user_sent_recommendations[user_id]]

    if not available_recommendations:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recommendation = random.choice(available_recommendations)
    recommendation_id = random_recommendation[0]
    recipe_name = random_recommendation[1]
    recipe_description = random_recommendation[2]
    recipe_image = random_recommendation[3]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление рекомендации в список отправленных
    user_sent_recommendations[user_id].append(recommendation_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_immunity')
    keyboard.add(more_button)

    # Отправка случайной рекомендации пользователю
    caption = create_caption3(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


@dp.callback_query_handler(lambda call: call.data == 'more_immunity')
async def send_more_immunity_recommendation(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Immunity')
    result = cursor.fetchall()

    if user_id not in user_sent_recommendations:
        user_sent_recommendations[user_id] = []

    # Фильтрация уже отправленных рекомендаций
    available_recommendations = [rec for rec in result if rec[0] not in user_sent_recommendations[user_id]]

    if not available_recommendations:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recommendation = random.choice(available_recommendations)
    recommendation_id = random_recommendation[0]
    recipe_name = random_recommendation[1]
    recipe_description = random_recommendation[2]
    recipe_image = random_recommendation[3]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление рекомендации в список отправленных
    user_sent_recommendations[user_id].append(recommendation_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_immunity')
    keyboard.add(more_button)

    # Отправка случайной рекомендации пользователю
    caption = create_caption3(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


# Хранение отправленных рекомендаций для каждого пользователя
user_sent_recommendations = {}

MAX_CAPTION_LENGTH = 1024

def create_caption4(recipe_name, recipe_description):
    full_caption = f'{recipe_name}\n\n{recipe_description}'
    if len(full_caption) > MAX_CAPTION_LENGTH:
        # Если длина подписи превышает допустимый лимит, сокращаем её
        truncated_caption = full_caption[:MAX_CAPTION_LENGTH - 3] + '...'
        return truncated_caption
    return full_caption

@dp.callback_query_handler(lambda call: call.data == 'energy')
async def send_energy_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Сброс отправленных при новом запросе
    if user_id in user_sent_recommendations:
        user_sent_recommendations[user_id] = []
    else:
        user_sent_recommendations[user_id] = []

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Energy')
    result = cursor.fetchall()

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recommendations[user_id]]

    if not available_recipes:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_description = random_recipe[2]
    recipe_image = random_recipe[3]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление в список отправленных
    user_sent_recommendations[user_id].append(recipe_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_energy')
    keyboard.add(more_button)

    # Отправка случайного рецепта пользователю
    caption = create_caption4(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


@dp.callback_query_handler(lambda call: call.data == 'more_energy')
async def send_more_energy_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Energy')
    result = cursor.fetchall()

    if user_id not in user_sent_recommendations:
        user_sent_recommendations[user_id] = []

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recommendations[user_id]]

    if not available_recipes:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_description = random_recipe[2]
    recipe_image = random_recipe[3]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление рецепта в список отправленных
    user_sent_recommendations[user_id].append(recipe_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_energy')
    keyboard.add(more_button)

    # Отправка случайного рецепта пользователю
    caption = create_caption4(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


# Хранение отправленных рекомендаций для каждого пользователя
user_sent_recommendations = {}

MAX_CAPTION_LENGTH = 1024

def create_caption5(recipe_name, recipe_description):
    full_caption = f'{recipe_name}\n\n{recipe_description}'
    if len(full_caption) > MAX_CAPTION_LENGTH:
        # Если длина подписи превышает допустимый лимит, сокращаем её
        truncated_caption = full_caption[:MAX_CAPTION_LENGTH - 3] + '...'
        return truncated_caption
    return full_caption

@dp.callback_query_handler(lambda call: call.data == 'weight')
async def send_weight_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Сброс отправленных при новом запросе
    if user_id in user_sent_recommendations:
        user_sent_recommendations[user_id] = []
    else:
        user_sent_recommendations[user_id] = []

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Weight')
    result = cursor.fetchall()

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recommendations[user_id]]

    if not available_recipes:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_description = random_recipe[2]
    recipe_image = random_recipe[3]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Добавление в список отправленных
    user_sent_recommendations[user_id].append(recipe_id)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_weight')
    keyboard.add(more_button)

    # Отправка случайного пользователю
    caption = create_caption5(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


@dp.callback_query_handler(lambda call: call.data == 'more_weight')
async def send_more_weight_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv/db/Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Weight')
    result = cursor.fetchall()

    if user_id not in user_sent_recommendations:
        user_sent_recommendations[user_id] = []

    # Получение списка уже отправленных рекомендаций
    sent_recipe_ids = user_sent_recommendations[user_id]

    # Фильтрация уже отправленных рекомендаций
    available_recipes = [recipe for recipe in result if recipe[0] not in sent_recipe_ids]

    if not available_recipes:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_description = random_recipe[2]
    recipe_image = random_recipe[3]

    # Сохранение изображения во временный файл
    image_path = 'temp_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_weight')
    keyboard.add(more_button)

    # Отправка случайного пользователю
    caption = create_caption5(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Добавление рекомендации в список отправленных
    user_sent_recommendations[user_id].append(recipe_id)

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


# Хранение отправленных рекомендаций для каждого пользователя
user_sent_recommendations = {}

MAX_CAPTION_LENGTH = 1024

def create_caption6(recipe_name, recipe_description):
    full_caption = f'{recipe_name}\n\n{recipe_description}'
    if len(full_caption) > MAX_CAPTION_LENGTH:
        # Если длина подписи превышает допустимый лимит, сокращаем её
        truncated_caption = full_caption[:MAX_CAPTION_LENGTH - 3] + '...'
        return truncated_caption
    return full_caption

@dp.callback_query_handler(lambda call: call.data == 'products')
async def send_breakfast_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Сброс отправленных при новом запросе
    if user_id in user_sent_recommendations:
        user_sent_recommendations[user_id] = []
    else:
        user_sent_recommendations[user_id] = []

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv\db\Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()

    # Фильтрация уже отправленных рецептов
    available_recipes = [recipe for recipe in result if recipe[0] not in user_sent_recommendations[user_id]]

    if not available_recipes:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_description = random_recipe[2]
    recipe_image = random_recipe[3]

    # Сохранение изображения во временный файл
    image_path = f'temp_image_{recipe_id}.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_products')
    keyboard.add(more_button)

    # Отправка случайной рекомендации пользователю с изображением
    caption = create_caption6(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Добавление рекомендации в список отправленных
    user_sent_recommendations[user_id].append(recipe_id)

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


@dp.callback_query_handler(lambda call: call.data == 'more_products')
async def send_more_products_recipe(call: types.CallbackQuery):
    user_id = call.message.chat.id

    # Установка соединения с базой данных
    conn = sqlite3.connect('venv\db\Blackberry_bot.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()

    if user_id not in user_sent_recommendations:
        user_sent_recommendations[user_id] = []

    # Получение списка уже отправленных рекомендаций
    sent_recipe_ids = user_sent_recommendations[user_id]

    # Фильтрация уже отправленных рекомендаций
    available_recipes = [recipe for recipe in result if recipe[0] not in sent_recipe_ids]

    if not available_recipes:
        await call.message.answer("Все рекомендации уже были отправлены.")
        return

    # Получение случайной записи
    random_recipe = random.choice(available_recipes)
    recipe_id = random_recipe[0]
    recipe_name = random_recipe[1]
    recipe_description = random_recipe[2]
    recipe_image = random_recipe[3]

    # Сохранение изображения во временный файл
    image_path = f'temp_image_{recipe_id}.jpg'
    with open(image_path, 'wb') as file:
        file.write(recipe_image)

    # Создание клавиатуры с кнопкой "Еще"
    keyboard = types.InlineKeyboardMarkup()
    more_button = types.InlineKeyboardButton(text='Еще', callback_data='more_products')
    keyboard.add(more_button)

    # Отправка случайной рекомендации пользователю с изображением
    caption = create_caption6(recipe_name, recipe_description)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard
        )

    # Добавление рекомендации в список отправленных
    user_sent_recommendations[user_id].append(recipe_id)

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Удаление временного файла
    os.remove(image_path)


@dp.message_handler(commands=['catalog'])
async def catalog(message: types.Message):
    mar = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Каталог", web_app=WebAppInfo(url='https://blackberrycatalog.tilda.ws'))
    mar.add(button1)
    await message.answer('Открыть каталог:', reply_markup=mar)


@dp.message_handler(commands=['recipes'])
async def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Завтрак', callback_data='breakfast'))
    markup.add(types.InlineKeyboardButton('Обед', callback_data='lunch'))
    markup.add(types.InlineKeyboardButton('Ужин', callback_data='dinner'))
    await message.answer('Выберете необходимый прием пищи:', reply_markup=markup)


@dp.message_handler(lambda message: message.text == 'Рецепты')
async def get_recipes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Завтрак', callback_data='breakfast'))
    markup.add(types.InlineKeyboardButton('Обед', callback_data='lunch'))
    markup.add(types.InlineKeyboardButton('Ужин', callback_data='dinner'))
    await message.answer('Выберете необходимый прием пищи:', reply_markup=markup)


@dp.message_handler(commands=['advice'])
async def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Укрепление иммунитета', callback_data='immunity'))
    markup.add(types.InlineKeyboardButton('Повышение энергии', callback_data='energy'))
    markup.add(types.InlineKeyboardButton('Снижение веса', callback_data='weight'))
    markup.add(types.InlineKeyboardButton('Хранение продуктов', callback_data='products'))
    await message.answer('Выберете необходимые рекомендации:', reply_markup=markup)


@dp.message_handler(lambda message: message.text == 'Рекомендации')
async def get_recipes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Укрепление иммунитета', callback_data='immunity'))
    markup.add(types.InlineKeyboardButton('Повышение энергии', callback_data='energy'))
    markup.add(types.InlineKeyboardButton('Снижение веса', callback_data='weight'))
    markup.add(types.InlineKeyboardButton('Хранение продуктов', callback_data='products'))
    await message.answer('Выберете необходимые рекомендации:', reply_markup=markup)


executor.start_polling(dp)