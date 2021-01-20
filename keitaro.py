import os

import utils


class Keitaro:
    api_endpoint = 'admin_api/v1/'
    report_intervals = [
        'today',
        'yesterday',
        '7_days_ago',
        'first_day_of_this_week',
        '1_month_ago',
        'first_day_of_this_month',
        '1_year_ago',
        'first_day_of_this_year',
        'all_time'
    ]


    def __init__(self, 
        api_key=utils.get_env_variable('KEITARO_API_KEY'),
        host=utils.get_env_variable('KEITARO_HOST')
    ):
        self.api_key = api_key
        self.host = host


    @staticmethod
    def _interval_valid(interval):
        if interval in Keitaro.report_intervals:
            return interval
        

    def _build_request_url(self, resource_endpoint=None):
        if self.host.endswith('/'):
            host = self.host + Keitaro.api_endpoint
        else:
            host = f'{self.host}/{Keitaro.api_endpoint}'
        return host + resource_endpoint


    def build_custom_report(self, interval='today'):
        """ limit = YEAR-MONTH-DAY """
        payload = {
            'range': {'interval': interval},
            'grouping': ['campaign', 'stream', 'landing'],
            'metrics': [
                'clicks',
                'stream_unique_clicks', 
                'conversions'
            ]
        }
        return utils.send_http_request(
            method='POST',
            url=self._build_request_url('report/build'),
            headers={'Api-Key': self.api_key},
            payload=payload
        )
