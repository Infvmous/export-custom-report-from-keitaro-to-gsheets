import utils

from keitaro import Keitaro
from gsheets import GSheets


def main():
    # TODO: Взять текст из Keitaro.report_intervals
    interval = input('''Укажите диапозон отчета \
    \nНажмите Enter, чтобы сделать отчет за сегодня \
    \n1 - за вчера \
    \n2 - за текущая неделя \
    \n3 - за последние 7 дней \
    \n4 - за текущий месяц \
    \n5 - за предыдущий месяц \
    \n6 - за текущий год \
    \n7 - за год \
    \n8 - за все время\n''')

    # Если нажат enter (введена пустая строка)
    if interval == '':
        interval = 0

    # Инициализирую приложения кейтаро
    keitaro = Keitaro()
    
    # Создаю отчет из кейтаро и записываю в файл в формате JSON
    report = keitaro.build_custom_report(interval)
    sorted_by_clicks_report = utils.sort_keitaro_report(report)
    utils.write_keitaro_report_to_file(sorted_by_clicks_report)

    # Инициализирую гугл таблицы апи
    gsheets = GSheets()

    # Создаю пустую таблицу в гугл таблицах с названием текущей даты
    spreadsheet = gsheets.create_spreadsheet()

    # Экспортирую отчет в заранее созданную гугл таблицу
    gsheets.export_keitaro_report_to_spreadsheet(spreadsheet,
        sorted_by_clicks_report)
    
    
    