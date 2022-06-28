from extensions import *
from config import *


@bot.message_handler(commands=['start', 'help', ])
def instruction(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в конвертер валют!'
                                      'Для конвертации валют введите через пробел '                                      
                                      'валюту, цену которой хотите узнать, '
                                      'валюту, в которой хотите узнать цену первой валюты, '
                                      'а также желаемую сумму.'
                                      'Для получения информации о доступных валютах введите /values')


# На запрос от пользователя выдаем список доступных валют, который получили от банка
@bot.message_handler(commands=['values'])
def values(message):
    bank_data = Converter.get_data()
    currency = 'Доступные валюты: '
    for i in bank_data:
        currency += i['Cur_Name'] + ' (' + i['Cur_Abbreviation'] + ')' + ', '
    bot.reply_to(message, currency)


# Переводим валюту из одной в другую относительно стоимости белорусского рубля.
# Если на сайте указана стоимость 10 или 100 единиц валюты,
# если речь о валюте, цену которой мы хотим узнать, мы делим на это число;
# и мы умножаем на это число, если речь о валюте, в которой мы хотим узнать цену.
@bot.message_handler()
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неправильный формат ввода.')

        base, quote, amount = values
        value1, value2, number1, number2 = Converter.values_for_convert(base, quote)

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}.')
    else:
        converted_currency = (value1 * number2 * amount) / (value2 * number1)
        bot.reply_to(message, converted_currency)


bot.polling(none_stop=True)
