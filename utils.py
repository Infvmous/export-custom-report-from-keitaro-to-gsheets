import os
import json

import requests

from datetime import datetime
from typing import Dict


def send_http_request(method: str, url: str, headers: Dict,
        payload: Dict=None):
    """ Отправляет HTTP запрос на url с httml заголовками header и
    телом запроса payload"""
    response = requests.request(method, url,
        headers=headers, data=json.dumps(payload))
    return response.json()


def write_keitaro_report_to_file(json_report):
    """ Записывает отсортированный отчет из keitaro в файл с
    названием <год-месяц-день_часы-мин-сек>.json """
    sorted_report = _sort_keitaro_report(json_report['rows'])
    with open(_build_reports_path(), 'w', encoding='utf-8') as f:
        json.dump(sorted_report, f, sort_keys=False, indent=4, 
            ensure_ascii=False, separators=(',', ': '))


def build_request_url(api_url, *parts):
    endpoint = '/'.join(str(part).rstrip('/') for part in parts)
    return api_url + endpoint


def get_env_variable(variable):
    return os.getenv(variable)


def get_current_date():
    return str(datetime.date(datetime.now()))


def get_current_datetime():
    return str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))


def _sort_keitaro_report(json_report, sort_by='clicks', reverse=True):
    return sorted(json_report, key=lambda i: int(i[sort_by]),
        reverse=reverse)


def _get_current_dir():
    return os.getcwd()


def _build_reports_path(reports_dir='reports', ext='.json'):
    return os.path.join(_get_current_dir(), reports_dir,
        get_current_datetime() + ext)





