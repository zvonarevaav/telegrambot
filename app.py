import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = ('Чтобы начать работу, отправьте сообщение боту в следующем формате:\n'
            '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n'
            'Например: доллар рубль 10\n'
            'Используйте команду /values, чтобы увидеть список всех доступных валют.')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = 'Доступные валюты:'
    for key in CurrencyConverter.get_available_currencies():
        text += f'\n{key}'
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def handle_convert(message):
    try:
        base, quote, amount = message.text.split(' ')
        total = CurrencyConverter.get_price(base, quote, amount)
        text = f'Цена {amount} {base} в {quote} - {total}'
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя: {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, text)

if __name__ == '__main__':
    bot.polling(none_stop=True)