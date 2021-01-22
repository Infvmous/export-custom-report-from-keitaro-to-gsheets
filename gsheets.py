from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import utils
from keitaro import Keitaro

from pprint import pprint

import time


class GSheets:
    row_headings = (
        'Кампания',
        'Поток',
        'Лендинг',
        'Клики',
        'Уник. клики потока',
        'Конверсии',
        'Продажи',
        'Группа'
    )
    streams = ('Battle Flow', 'Bots', 'Замыкающий ботов')

    def __init__(self, 
            credentials_path='credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']):
        self.credentials_path = credentials_path
        self.scopes = scopes
        self.creds = self._get_creds()
        self.service = self._get_service() 

    def create_spreadsheet(self, name=''):
        spreadsheet = {
            'properties': {
                'title': f'{name} {utils.get_current_date()}'
            }
        }
        spreadsheet = self.service.spreadsheets().create(
                        body=spreadsheet, fields='spreadsheetId').execute()
        print(f'Создана таблица https://docs.google.com/spreadsheets/d/{GSheets.get_spreadsheet_id(spreadsheet)}')
        # print(self.service.spreadsheets().get(spreadsheetId=GSheets.get_spreadsheet_id(spreadsheet)).execute())
        return spreadsheet

    def export_keitaro_report_to_spreadsheet(self, spreadsheet, report, timeout=0):
        """ 
        1 Взять стату по потокам отдельно
        2 создать листы для потоков + заполнить заголовки строк GSheets.row_headings (Battle Flow, Bots, Замыкающий ботов)
        3 Заполнить
        """
        spreadsheet_id = GSheets.get_spreadsheet_id(spreadsheet)
        for stream in GSheets.streams:
            # Получить репорт по имени потока
            sorted_report = Keitaro.sort_report_by_keyword(
                report=report, keyword='stream', value=stream)
            
            replaced_stream_name = utils.replace_string(stream)
            # Создать лист с именем stream
            sheet = self._add_new_sheet(spreadsheet_id=spreadsheet_id, rows=sorted_report,
                sheet_name=replaced_stream_name, timeout=timeout,
                columns_count=utils.count_items(GSheets.row_headings))

            # Заполнить созданный лист
            values = self._add_headings_to_columns(
                Keitaro.parse_report_rows(sorted_report))
            
            # Если отчетность не пуста, добавить в лист
            if values:
                filled_sheet = self._write_to_sheet(spreadsheet_id,
                    range_name=f'{replaced_stream_name}!A1:H{len(values)}',
                    values=values, timeout=timeout)
  
            # TODO: Удалить нулевой лист
            # deleted_first_list = self._delete_sheet(spreadsheet_id, 0)

    def _change_cell_size(self, spreadsheet_id,
            sheet_id, start_index, end_index, 
            pixel_size, dimension='COLUMNS'):
        body = {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': dimension,
                    'startIndex': start_index,
                    'endIndex': end_index
                },
                'properties': {
                    'pixelSize': pixel_size
                },
                'fields': 'pixelSize'
            }
        }
        return self._send_spreadsheet_request(spreadsheet_id, body)

    def _add_headings_to_columns(self, table):
        try:
            table[0] = list(GSheets.row_headings)
        except IndexError:
            print(table)
            return
        return table

    def _send_spreadsheet_request(self, spreadsheet_id, request=None, values=None, timeout=0):
        body = self._build_request_body(request, values)
        time.sleep(timeout)
        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        return response

    def _write_to_sheet(self, spreadsheet_id, range_name, values, timeout=0):
        body = {
            'values': values,
            'majorDimension': 'ROWS'
        }
        time.sleep(timeout)
        result = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        print(f'{result.get("updatedCells")} ячеек обновлено')

    def _add_new_sheet(self, spreadsheet_id, sheet_name, rows,
            columns_count=None, rows_count=None, timeout=0):
        body = {
            'addSheet': {
                'properties': {
                    'title': sheet_name,
                    'gridProperties': {
                        'rowCount': rows_count,
                        'columnCount': columns_count
                    }
                }    
            }
        }
        sheet = self._send_spreadsheet_request(spreadsheet_id, body, timeout=timeout)
        sheet_name = GSheets.get_sheet_name(sheet)
        sheed_id = GSheets.get_sheet_id(sheet)
        print(f'Создан лист {sheet_name} с ID: {sheed_id}')
        # Расширить заголовок первого столбца
        self._change_cell_size(spreadsheet_id, sheed_id, 0, 1, 450)
        return sheet_name
    
    def _delete_sheet(self, spreadsheet_id, sheet_id):
        body = {
            'deleteSheet': {
                'sheetId': sheet_id
            }
        }
        sheet = self._send_spreadsheet_request(spreadsheet_id, body)
        # print(f'Удален лист {GSheets.get_sheet_name(sheet)} с ID: {GSheets.get_sheet_id(sheet)}')
        return sheet

    def _build_request_body(self, request=None, values=None):
        if request:
            return {'requests': [request]}
        if values:
            return {'values': values}

    @staticmethod
    def get_spreadsheet_id(spreadsheet):
        return spreadsheet.get('spreadsheetId')

    @staticmethod
    def get_sheet_id(sheet, resource_action='addSheet'):
        return sheet['replies'][0]['addSheet']['properties']['sheetId']

    @staticmethod
    def get_sheet_name(sheet, resource_action='addSheet'):
        return sheet['replies'][0]['addSheet']['properties']['title']

    def _get_service(self, api='sheets', ver='v4'):
        return build(api, ver, credentials=self._validate_creds())

    def _validate_creds(self):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.creds = auth_user()
            self._save_creds()
        return self.creds

    def _get_creds(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                return pickle.load(token)

    def _save_creds(self):
        with open('token.pickle', 'wb') as token:
            pickle.dump(self.creds, token)

    def _auth_user(self):
        flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes)
        return flow.run_local_server(port=0)



    

    