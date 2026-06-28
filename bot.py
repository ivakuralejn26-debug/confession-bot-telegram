import telebot
from telebot import types

BOT_TOKEN = ""
ADMINS = [ID USER]  

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    """Приветствие пользователя"""
    bot.send_message(
        message.chat.id,
        "Привет! Я анонимный бот.\n\n"
        "Напиши любое сообщение, и оно будет отправлено администраторам анонимно."
    )

@bot.message_handler(content_types=[
    'text', 'photo', 'video', 'document', 'audio', 
    'voice', 'sticker', 'video_note', 'animation'
])
def handle_all_messages(message):
    """
    Основной обработчик всех сообщений.
    Пересылает сообщение администраторам анонимно.
    """
    # Формируем текст для админов
    header = "📨 <b>Анонимное сообщение</b>\n\n"
    
    if message.text:
        content = message.text
    elif message.caption:
        content = f"Подпись: {message.caption}\n\n[Медиа]"
    else:
        content = "[Медиа-файл без подписи]"

    full_message = header + content

    # Отправляем каждому админу
    for admin_id in ADMINS:
        try:
            # Если это текст
            if message.text:
                bot.send_message(admin_id, full_message, parse_mode='HTML')
            
            # Если есть медиа — пересылаем вместе с шапкой
            elif message.photo:
                bot.send_photo(admin_id, message.photo[-1].file_id, 
                             caption=full_message, parse_mode='HTML')
            elif message.video:
                bot.send_video(admin_id, message.video.file_id, 
                             caption=full_message, parse_mode='HTML')
            elif message.document:
                bot.send_document(admin_id, message.document.file_id, 
                                caption=full_message, parse_mode='HTML')
            elif message.audio:
                bot.send_audio(admin_id, message.audio.file_id, 
                             caption=full_message, parse_mode='HTML')
            elif message.voice:
                bot.send_voice(admin_id, message.voice.file_id, 
                             caption=full_message, parse_mode='HTML')
            elif message.sticker:
                bot.send_message(admin_id, full_message, parse_mode='HTML')
                bot.send_sticker(admin_id, message.sticker.file_id)
            elif message.video_note:
                bot.send_message(admin_id, full_message, parse_mode='HTML')
                bot.send_video_note(admin_id, message.video_note.file_id)
            elif message.animation:
                bot.send_animation(admin_id, message.animation.file_id, 
                                 caption=full_message, parse_mode='HTML')
                
            
            bot.send_message(message.chat.id, "✅ Сообщение отправлено анонимно.")
            
        except Exception as e:
            print(f"Ошибка отправки админу {admin_id}: {e}")


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()