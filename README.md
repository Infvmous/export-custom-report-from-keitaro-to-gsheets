1. Клонировать проект

```bash
$ git clone https://github.com/Infvmous/gsheets-export-from-keitaro.git
```

2. Создать виртуальное окружение в директории проекта

```bash
$ python3 -m venv env
```

3. Создать файл `<НАЗВАНИЕ_ФАЙЛА>.sh` с переменными окружения

```bash
export KEITARO_API_KEY='admin api key'
export GSHEETS_CLIENT_SECRET='google sheets client secret key'
python .
```

4. Включить [Google Sheets API v4](https://developers.google.com/sheets/api/quickstart/python)
   `
