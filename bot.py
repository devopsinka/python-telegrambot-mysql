import sys
import telebot
import mysql.connector
from mysql.connector import errorcode

bot = telebot.TeleBot("")

try:
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="root",
      port="3307",
      database="youtube"
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    sys.exit()
  else:
    print(err)
    sys.exit()



cursor = db.cursor()

# cursor.execute("CREATE DATABASE youtube")

# cursor.execute("SHOW DATABASES")

# for x in cursor:
#   print(x)


# cursor.execute("CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255))")

# cursor.execute("SHOW TABLES")

# for x in cursor:
#   print(x)


# cursor.execute("ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE)")

# sql = "INSERT INTO users (first_name, last_name, user_id) VALUES (%s, %s, %s)"
# val = ("Vlad", "Неверов", 1)
# cursor.execute(sql, val)
# db.commit()

# print(cursor.rowcount, "запись добавлена.")

# sql = "INSERT INTO users (first_name, last_name, user_id) VALUES (%s, %s, %s)"
# val = [
#   ('Peter', 'Lowstreet 4', 2),
#   ('Amy', 'Apple st 652', 3),
#   ('Hannah', 'Mountain 21', 4),
# ]

# cursor.executemany(sql, val)
# db.commit()

# print(cursor.rowcount, "записи были добавлены.")

####################################################################
# cursor.execute("CREATE TABLE categories (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description VARCHAR(255))")
# sql = "INSERT INTO categories (title, description) VALUES (%s, %s)"
# val = [
#   ('Телефоны', 'Описание телефонов'),
#   ('Ноутбуки', 'Описание ноутбуков'),
#   ('Ноутбуки другие', 'Описание других ноутбуков'),
# ]

# cursor.executemany(sql, val)
# db.commit()


# SELECT
# cursor.execute("SELECT * FROM categories")
# categories = cursor.fetchall()

# for category in categories:
#     print(category[1])

# SELECT COLUMN
# cursor.execute("SELECT title FROM categories")
# categories = cursor.fetchall()

# for nameCategory in categories:
#     print(nameCategory)

# SELECT ONE RECORD
# cursor.execute("SELECT * FROM categories")
# category = cursor.fetchone()
# print(category)

# user_data = {}

# FILTER
# cursor.execute("SELECT * FROM categories WHERE title = 'Ноутбуки'")
# categories = cursor.fetchall()

# for category in categories:
#     print(category)

# FILTER 2
# cursor.execute("SELECT * FROM categories WHERE title LIKE '%Ноутбуки%'")
# categories = cursor.fetchall()

# for category in categories:
#     print(category)

# FILTER 1 SQL защита
# sql = "SELECT * FROM categories WHERE title = %s"
# val = ("Ноутбуки", )

# cursor.execute(sql, val)
# categories = cursor.fetchall()

# for category in categories:
#     print(category)


# FILTER 2 SQL защита
# sql = "SELECT * FROM categories WHERE title LIKE %s"
# val = ("%Ноутбуки%", )

# cursor.execute(sql, val)
# categories = cursor.fetchall()

# for category in categories:
#     print(category)


# ORDER ASC
# cursor.execute("SELECT * FROM categories ORDER BY title")
# categories = cursor.fetchall()

# for category in categories:
#     print(category)

# ORDER DESC
# cursor.execute("SELECT * FROM categories ORDER BY title DESC")
# categories = cursor.fetchall()

# for category in categories:
#     print(category)

###############################################################

# DELETE RECORD
# cursor.execute("DELETE FROM categories WHERE title = 'Ноутбуки'")
# db.commit()
# print('Запись удалена!')

# DELETE ALL RECORDS
# cursor.execute("DELETE FROM categories")
# db.commit()
# print('Записи удалены!')

# DELETE RECORD защита SQL
# sql = "DELETE FROM categories WHERE title = %s"
# val = ("Ноутбуки", )
# cursor.execute(sql, val)

# db.commit()
# print('Запись удалена!')

# DROP TABLE
# cursor.execute("DROP TABLE categories")
# print('Таблица удалена!')

# DROP TABLE если существует
# cursor.execute("DROP TABLE IF EXISTS categories")
# print('Таблица удалена!')

# UPDATE RECORD
# cursor.execute("UPDATE users SET first_name = 'Андрей' \
#                 WHERE user_id = 2 ")
# db.commit()
# print('Запись обновлена!')

# UPDATE RECORD защита SQL
# sql = "UPDATE users SET first_name = %s \
#                 WHERE user_id = %s"
# val = ("Влад", 2)

# cursor.execute(sql, val)
# db.commit()
# print('Запись обновлена!')

# LIMIT
# cursor.execute("SELECT * FROM users LIMIT 2")
# users = cursor.fetchall()

# for user in users:
#     print(user)

# LIMIT OFFSET
# cursor.execute("SELECT * FROM users LIMIT 2 OFFSET 1")
# users = cursor.fetchall()

# for user in users:
#     print(user)

######### JOIN ############################
# cursor.execute("CREATE TABLE user_groups (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))")
# sql = "INSERT INTO user_groups (title) VALUES (%s)"
# val = [('Администратор', ), ('Модератор', ), ('Пользователь', )]

# cursor.executemany(sql, val)
# db.commit()

# cursor.execute("ALTER TABLE users ADD COLUMN (user_group_id INT)")


# sql = "SELECT \
#     users.first_name AS user, \
#     user_groups.title AS user_group \
#     FROM users \
#     JOIN user_groups ON users.user_group_id = user_groups.id"

# cursor.execute(sql)
# users = cursor.fetchall()

# for user in users:
#     print(user)

###### LEFT JOIN #############
# sql = "SELECT \
#     users.first_name AS user, \
#     user_groups.title AS user_group \
#     FROM users \
#     LEFT JOIN user_groups ON users.user_group_id = user_groups.id"

# cursor.execute(sql)
# users = cursor.fetchall()

# for user in users:
#     print(user)

##### RIGHT JOIN #############
# sql = "SELECT \
#     users.first_name AS user, \
#     user_groups.title AS user_group \
#     FROM users \
#     RIGHT JOIN user_groups ON users.user_group_id = user_groups.id"

# cursor.execute(sql)
# users = cursor.fetchall()

# for user in users:
#     print(user)



class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Введите имя")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id, "Введите фамилию")
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        sql = "INSERT INTO users (first_name, last_name, user_id) \
                                  VALUES (%s, %s, %s)"
        val = (user.first_name, user.last_name, user_id)
        cursor.execute(sql, val)
        db.commit()

        bot.send_message(message.chat.id, "Вы успешно зарегистрированны!")
    except Exception as e:
        bot.reply_to(message, 'Ошибка, или вы уже зарегистрированны!')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)