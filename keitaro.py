import os
from typing import List, Dict
import json

import utils

from pprint import pprint


class Keitaro:
    api_endpoint = 'admin_api/v1/'
    report_intervals = (
        ['today', 'за сегодня'],
        ['yesterday', 'за вчера'],
        ['first_day_of_this_week', 'за текущую неделю'],
        ['7_days_ago', 'за последние 7 дней'],
        ['first_day_of_this_month', 'за текущий месяц'],
        ['1_month_ago', 'за предыдущий месяц'],
        ['first_day_of_this_year', 'за текущий год'],
        ['1_year_ago', 'за год'],
        ['all_time', 'за все время'],
    )
    
    def __init__(self, 
        api_key=utils.get_env_variable('KEITARO_API_KEY'),
        host=utils.get_env_variable('KEITARO_HOST')
    ):
        self.api_key = api_key
        self.host = host
        self.api_url = self._build_api_url()

    @staticmethod
    def sort_report_by_keyword(report: Dict, keyword: str, value: str):
        sorted_report = []
        for report_dict in report:
            if report_dict[keyword] == value:
                sorted_report.append(report_dict)
        return sorted_report

    @staticmethod
    def _interval_valid(interval_index: int):
        """ Проверяет существует ли interval_index, если нет,
        то возвращает интервал today """
        index = int(interval_index)
        if index < len(Keitaro.report_intervals):
            return Keitaro.report_intervals[index]
        else:
            return Keitaro.report_intervals[0]

    @staticmethod
    def parse_report_rows(report):
        rows = []
        for row in report:
            parsed_row = [
                row['campaign'],
                row['stream'],
                row['landing'],
                row['clicks'],
                row['stream_unique_clicks'],
                row['conversions'],
                row['sales'],
                row['campaign_group']
            ]
            rows.append(parsed_row)
        return rows

    @staticmethod
    def generate_interval_description_string():
        description = ''
        for row in Keitaro.report_intervals:
            description += row
            print(row)

    def _build_api_url(self):
        if self.host.endswith('/'):
            url = self.host + Keitaro.api_endpoint
        else:
            url = f'{self.host}/{Keitaro.api_endpoint}'
        return url

    def sort_report_by_groups(self, report):
        """
        group_report = {
                'campaign_name': [
                    {
                        "campaign": "ADWORDS - HU+",
                        "stream": "Battle Flow",
                        "landing": "1-den-cardiol",
                        "campaign_group": "leadbit-cod",
                        "clicks": "204",
                        "stream_unique_clicks": "132",
                        "conversions": "0",
                        "sales": "0",
                        "landing_id": "6"
                    },
                   ...
                ]
            }
        """
        group_reports = {}
        for item in report:
            campaign_group = item['campaign_group']
            if campaign_group not in group_reports:
                # Создаю ключ-лист с названием группы 
                group_reports[campaign_group] = []
            group_reports[campaign_group].append(item)       
        return group_reports

    def build_custom_report(self,
            interval_index: int=0,
            timezone: str='Europe/Moscow',
            grouping: List=['campaign', 'stream', 'landing', 'campaign_group'],
            metrics: List=['clicks', 'stream_unique_clicks', 'conversions', 'sales']):
        """ Получает кастомный отчет из keitaro за интервал времени interval,
        с часовым поясом timezone, группировкой grouping (см. документацию
        Keitaro Admin API v1), метриками metrics """
        if interval_index or interval_index == 0:
            print(f'Создаю отчет {Keitaro._interval_valid(interval_index)[1]}')
        return utils.send_http_request(
            method='POST',
            url=utils.build_request_url(self.api_url, 'report', 'build'),
            headers={'Api-Key': self.api_key},
            payload={
                'range': {
                    'interval': Keitaro._interval_valid(interval_index)[0],
                    'timezone': timezone
                },
                'grouping': grouping,
                'metrics': metrics
            }
        )
