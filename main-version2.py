import math
from datetime import datetime, timedelta
from csv_parse import InstallsObject, PurchasesObject
from mycsv import write_csv_table, read_csv_table
import argparse


'''
brief: Высчитывает количество установок по странам и RPI
args:   filter_installs - итератор для данных installs
        filter_purchases - итератор для данных purchases
        rpi_count - количество RPI (default = 10): int
        delta_date - временной интервал для вычисления RPI (default = 1 day): datetime.timedelta
'''


def calc(filter_installs, filter_purchases, rpi_count=10, delta_date=timedelta(days=1)):
    result = []
    INSTALLS_KEY = 'installs'
    template_row = {i: 0.0 for i in range(1, rpi_count+1)}

    total_result = {}
    for data in filter_installs:
        if data.country not in total_result:
            total_result[data.country] = {INSTALLS_KEY: 0, **template_row}
        total_result[data.country][INSTALLS_KEY] += 1

    for data in filter_purchases:
        interval = data.created - data.install_date
        index = math.ceil(interval / delta_date)
        index = index if index < rpi_count else rpi_count
        if index <= rpi_count:
            total_result[data.country][index] += data.revenue

    for country in total_result.keys():
        result.append([country, total_result[country][INSTALLS_KEY]] +
                      [total_result[country][index] / total_result[country][INSTALLS_KEY] for index in range(1, rpi_count+1)])

    return sorted(result, key=lambda x: x[1], reverse=True)


'''
brief: Основная функция скрипта, служит для запуска вычислений
args:   start_date - дата начала анализируемого периода
        end_date - дата конца анализируемого периода
        app_id - идентификатор приложения
'''


def main(start_date, end_date, app_id):
    # фильтр для первоначльной фильтрации csv файла (до приобразования к модели)

    def filter_for_csv(x):
        try:
            return int(x[1]) == app_id
        except ValueError as err:
            print('filter_for_csv!!!: ', err)
            return False
    # итератор данных installs
    filter_installs = filter(lambda x: start_date <= x.created < end_date, read_csv_table('./installs.csv', InstallsObject, filter_for_csv))
    # итератор данных purchases
    filter_purchases = filter(lambda x: start_date <= x.install_date < end_date, read_csv_table('./purchases.csv', PurchasesObject, filter_for_csv))
    # запуск вычислений
    return calc(filter_installs, filter_purchases)


if __name__ == '__main__':
    command_parser = argparse.ArgumentParser()
    command_parser.add_argument('-s', '--start',
                                help='start datetime year-month-day hour:minute:second',
                                default='2016-05-02 0:0:0')
    command_parser.add_argument('-e', '--end',
                                help='end datetime year-month-day hour:minute:second',
                                default='2016-05-10 0:0:0')
    command_parser.add_argument('-a', '--app',
                                help='id of application',
                                default='2',
                                type=int)
    args = command_parser.parse_args()
    start = datetime.strptime(args.start, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(args.end, '%Y-%m-%d %H:%M:%S')
    result = main(start, end, args.app)
    write_csv_table('result.csv', result, ['country', 'installs'] +
                    ['RPI{0}'.format(i) for i in range(1, 11)])
