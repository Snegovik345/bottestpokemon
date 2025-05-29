import telebot
import random
import config
bot = telebot.TeleBot(config.token)

class House:
    def __init__(self, size, material, country):
        self.size = size
        self.material = material
        self.country = country
    
    def open(self):
        return "🚪 Дом открыт!"
    
    def closed(self):
        return "🔒 Дом закрыт!"
    
    def info(self):
        return (
            f"🏠 Информация о доме:\n\n"
            f"▫️ Размер: {self.size}\n"
            f"▫️ Материал: {self.material}\n"
            f"▫️ Страна: {self.country}"
        )


quiz_questions = [
    "1. Сколько лет разлагается пластиковая бутылка? (20/100/450/1000)",
    "2. Какой материал наиболее экологичен? (Стекло/Пластик/Алюминий)",
    "3. Что экономит больше воды? (Душ/Выкл.воду при чистке зубов/Посудомойка)",
    "4. Какой % пластика перерабатывается в мире? (9%/25%/50%)",
    "5. Что разлагается быстрее? (Стекло/Бан.кожура/Пакет)"
]

correct_answers = ["450", "Стекло", "Посудомойка", "9", "Бан.кожура"]

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@bot.message_handler(commands=['house'])
def house_command(message):
    try:
        # Разбиваем сообщение на части
        parts = message.text.split(maxsplit=3)
        
        # Создаем экземпляр дома
        house = House(
            size=parts[1],
            material=parts[2],
            country=parts[3] if len(parts) > 3 else "Не указана"
        )
        
        # Отправляем красиво оформленное сообщение
        bot.send_message(message.chat.id, house.info())
        bot.send_message(message.chat.id, house.open())
        bot.send_message(message.chat.id, house.closed())
    except:
        bot.send_message(message.chat.id, "⚠️ Используйте: /house [размер] [материал] [страна]")

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    bot.send_message(message.chat.id, "🌍 Эко-викторина (5 вопросов):")
    msg = bot.send_message(message.chat.id, quiz_questions[0])
    bot.register_next_step_handler(msg, process_answer1)


def process_answer1(message):
    check_answer(message, 0, quiz_questions[1], process_answer2)

def process_answer2(message):
    check_answer(message, 1, quiz_questions[2], process_answer3)

def process_answer3(message):
    check_answer(message, 2, quiz_questions[3], process_answer4)

def process_answer4(message):
    check_answer(message, 3, quiz_questions[4], process_answer5)

def process_answer5(message):
    if message.text.lower() == correct_answers[4].lower():
        bot.send_message(message.chat.id, "✅ Верно!\n\nВикторина завершена!")
    else:
        bot.send_message(message.chat.id, f"❌ Неверно! Правильно: {correct_answers[4]}\n\nВикторина завершена!")


def check_answer(message, answer_index, next_question, next_handler):
    if message.text.lower() == correct_answers[answer_index].lower():
        bot.send_message(message.chat.id, "✅ Верно!")
    else:
        bot.send_message(message.chat.id, f"❌ Неверно! Правильно: {correct_answers[answer_index]}")
    
    msg = bot.send_message(message.chat.id, next_question)
    bot.register_next_step_handler(msg, next_handler)


@bot.message_handler(commands=["info"])  
def info_text(message):
    bot.reply_to(message, "Привет! Я Echobot! Я думаю ты по названию понимаешь, что я делаю, приятного пользования!")



@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"Получил твоё фото! ID: {file_id}")



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)



bot.infinity_polling()