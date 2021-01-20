import os
import json
from operator import itemgetter

import requests

from datetime import datetime


def send_http_request(method, url, headers, payload=None):
    response = requests.request(method, url,
        headers=headers, data=json.dumps(payload))
    return response.json()


def write_keitaro_report_to_file(json_report):
    sorted_report = sort_report_by_clicks(json_report['rows'])
    with open(build_reports_path(), 'w', encoding='utf-8') as f:
        json.dump(sorted_report, f, sort_keys=False, indent=4, 
            ensure_ascii=False, separators=(',', ': '))


def sort_report_by_clicks(json_report, key='clicks', reverse=True):
    return sorted(json_report, key=lambda i: int(i[key]),
        reverse=reverse)


def get_env_variable(variable):
    return os.getenv(variable)


def get_current_date():
    return str(datetime.date(datetime.now()))


def get_current_datetime():
    return str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))


def get_current_dir():
    return os.getcwd()


def build_reports_path(reports_dir='reports', ext='.json'):
    return os.path.join(get_current_dir(), reports_dir,
        get_current_datetime() + ext)





