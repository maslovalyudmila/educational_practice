# импортируем необходимые библиотеки
import xml.etree.ElementTree as et
import requests
import datetime as dt
import pandas as pd

# определим переменные, хранящие значения параметров запроса - даты и уникальный код валюты
# и приведем значения дат к фиксированному строковому формату, чтобы API распознал запрос
date_req1 = (dt.date.today() - dt.timedelta(5)).strftime('%d.%m.%Y') # дата 5 дней назад
date_req2 = dt.date.today().strftime('%d.%m.%Y') # актуальная дата
val_code = 'R01235' # уникальный код валюты

# определим переменную, хранящую значение адреса ресурса, к которому выполняем запрос
url = 'https://cbr.ru/scripts/XML_dynamic.asp?date_req1=%s&date_req2=%s&VAL_NM_RQ=%s' % (date_req1, date_req2, val_code)

# отправим HTTP-запрос 'GET' вместе с переданными параметрами
# и сохраним результат запроса в объект response в текстовом формате
response = requests.get(url).text

# определим переменную, хранящую XML-дерево
tree = et.ElementTree(et.fromstring(response))
# определим переменную, хранящую значение корневого элемента в дереве, т.е. 'ValCurs'
root = tree.getroot()

# сформируем табличную структуру для хранения данных, которые будем извлекать из XML-дерева
# определим список атрибутов
df_cols = ['date',
           'value']
# определим строки, в которые будут сохраняться значения атрибутов
rows = []

# произведем поиск значений необходимых атрибутов - даты и суммы на заданную дату
for node in root:
  n_date = node.attrib['Date'] if node is not None else None
  n_value = node.find('Value').text if node is not None else None
  #заполним строки значениями атрибутов
  rows.append({'date': n_date,
               'value': n_value})

df = pd.DataFrame(rows, columns=df_cols)

# сохраним полученную таблицу с данными в файл
df.to_csv('currency_rate.csv')