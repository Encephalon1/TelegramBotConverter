import requests
import json


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    # Получаем данные от нацбанка РБ на сегодняшний день
    def get_data():
        r = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
        bank_data = json.loads(r.content)
        bank_data.append({'Cur_Name': 'Белорусский рубль', 'Cur_Abbreviation': 'BYN',
                          'Cur_Scale': 1, 'Cur_OfficialRate': 1})
        return bank_data

    @staticmethod
    def values_for_convert(base: str, quote: str):
        if base == quote:
            raise APIException('Невозможно перевести одинаковые валюты.')

        bank_data = Converter.get_data()
        value1 = None
        value2 = None
        number1 = None
        number2 = None
        for i in bank_data:
            if base == i['Cur_Name'] or base == i['Cur_Abbreviation']:
                value1 = float(i['Cur_OfficialRate'])
                number1 = float(i['Cur_Scale'])
            if quote == i['Cur_Name'] or quote == i['Cur_Abbreviation']:
                value2 = float(i['Cur_OfficialRate'])
                number2 = float(i['Cur_Scale'])

        # Если value1 или value2 имеют значение None, значит,
        # введенные данные не были найдены в доступном перечне валют
        # (условие не выполнялось ни в одном из полученных словарей).
        if not value1:
            raise APIException(f'Не удалось обработать данные {base}')

        if not value2:
            raise APIException(f'Не удалось обработать данные {quote}')

        return value1, value2, number1, number2
