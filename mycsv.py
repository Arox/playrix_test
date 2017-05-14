import csv
from csv_parse import ParseCSVFormat


'''
brief:  чтение данных из csv файла
args:   filename - имя файла
        parse_class - класс модели в которую необходимо преобразовать
        filter_func - функция для фильтрации данных (default = None)
'''


def read_csv_table(filename: str, parse_class: ParseCSVFormat, filter_func=None):
    assert isinstance(filename, str)
    with open(filename, newline='') as file:
        if filter_func is None:
            container = csv.reader(file, delimiter=',')
        else:
            container = filter(filter_func, csv.reader(file, delimiter=','))
        for row in container:
            try:
                yield parse_class.from_row(row)
            except Exception as err:
                print(err)
                print('Error row = ', row)


'''
brief:  запись данных в csv файл
args:   filename - имя файла
        data - данные для записи
        title - заголовок csv таблицы (default = None)
'''


def write_csv_table(filename, data, title=None):
    assert isinstance(filename, str)
    with open(filename, 'w', newline='') as file:
        csvwriter = csv.writer(file, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if title is not None:
            csvwriter.writerow(title)
        csvwriter.writerows(data)
