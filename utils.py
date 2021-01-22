import os
import json

import requests

from datetime import datetime
from typing import Dict, List
from pprint import pprint


def send_http_request(method: str, url: str, headers: Dict,
        payload: Dict=None):
    """ Отправляет HTTP запрос на url с httml заголовками header и
    телом запроса payload"""
    response = requests.request(method, url,
        headers=headers, data=json.dumps(payload))
    # print(response.status_code)
    return response.json()


def write_keitaro_report_to_file(json_report):
    """ Записывает отсортированный отчет из keitaro в файл с
    названием <год-месяц-день_часы-мин-сек>.json """
    with open(_build_reports_path(), 'w', encoding='utf-8') as f:
        json.dump(json_report, f, sort_keys=False, indent=4, 
            ensure_ascii=False, separators=(',', ': '))
    return(json_report)


def build_request_url(api_url, *parts):
    endpoint = '/'.join(str(part).rstrip('/') for part in parts)
    return api_url + endpoint


def validate_input_on_enter(input_value, default_value=0):
    if input_value == '':
        return default_value
    return input_value


def count_items(data_structure):
    return len(data_structure)


def replace_string(string, replace=' ',
        replace_to=''):
    return string.replace(replace, replace_to)


def get_env_variable(variable):
    return os.getenv(variable)


def get_current_date():
    return str(datetime.date(datetime.now()))


def get_current_datetime(time_format='%Y-%m-%d_%H-%M-%S'):
    return str(datetime.now().strftime(time_format))


def sort_keitaro_report(json_report, sort_by='clicks', reverse=True):
    return sorted(json_report['rows'], key=lambda i: int(i[sort_by]),
        reverse=reverse)


def _get_current_dir():
    return os.getcwd()


def _build_reports_path(reports_dir='reports', ext='.json'):
    return os.path.join(_get_current_dir(), reports_dir,
        get_current_datetime() + ext)







