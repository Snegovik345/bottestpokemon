import telebot
from config import token

bot = telebot.TeleBot(token)

def is_admin(chat_id, user_id):
    """Проверяет, является ли пользователь администратором"""
    try:
        return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Я автоматически баню за ссылки!")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        
        if is_admin(chat_id, user_id):
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эту команду нужно использовать в ответ на сообщение нарушителя.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(func=lambda message: True)
def ban_links(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Если это не админ и сообщение содержит ссылку
    if not is_admin(chat_id, user_id) and ('http://' in message.text or 'https://' in message.text or 'www.' in message.text):
        try:
            bot.delete_message(chat_id, message.message_id)  # Удаляем сообщение со ссылкой
            bot.ban_chat_member(chat_id, user_id)  # Баним пользователя
            bot.send_message(chat_id, f"Пользователь @{message.from_user.username} был забанен за отправку ссылки.")
        except Exception as e:
            print(f"Ошибка при бане: {e}")

bot.infinity_polling(none_stop=True)