import os
from typing import List

import utils


class Keitaro:
    api_endpoint = 'admin_api/v1/'
    report_intervals = (
        'today',
        'yesterday',
        '7_days_ago',
        'first_day_of_this_week',
        '1_month_ago',
        'first_day_of_this_month',
        '1_year_ago',
        'first_day_of_this_year',
        'all_time'
    )


    def __init__(self, 
        api_key=utils.get_env_variable('KEITARO_API_KEY'),
        host=utils.get_env_variable('KEITARO_HOST')
    ):
        self.api_key = api_key
        self.host = host
        self.api_url = self._build_api_url()


    @staticmethod
    def _interval_valid(interval):
        """ Проверяет существует ли interval, если нет,
        то возвращает интервал today """
        if interval in Keitaro.report_intervals:
            return interval
        else:
            return Keitaro.report_intervals[0]

    
    def _build_api_url(self):
        if self.host.endswith('/'):
            url = self.host + Keitaro.api_endpoint
        else:
            url = f'{self.host}/{Keitaro.api_endpoint}'
        return url


    def build_custom_report(self,
            interval: str='today',
            timezone: str='Europe/Moscow',
            grouping: List=['campaign', 'stream', 'landing'],
            metrics: List=['clicks', 'stream_unique_clicks', 'conversions', 'sales']):
        """ Получает кастомный отчет из keitaro за интервал времени interval,
        с часовым поясом timezone, группировкой grouping (см. документацию
        Keitaro Admin API v1), метриками metrics """
        return utils.send_http_request(
            method='POST',
            url=utils.build_request_url(self.api_url, 'report', 'build'),
            headers={'Api-Key': self.api_key},
            payload={
                'range': {
                    'interval': Keitaro._interval_valid(interval),
                    'timezone': timezone
                },
                'grouping': grouping,
                'metrics': metrics
            }
        )