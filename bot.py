import telebot
import mysql.connector

bot = telebot.TeleBot("")

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  port="3307",
  database="youtube"
)

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


user_data = {}

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