1. Клонировать проект

```bash
$ git clone https://github.com/Infvmous/gsheets-export-from-keitaro.git
```

2. Создать виртуальное окружение в директории проекта

```bash
$ python -m venv env
```

3. Установить зависимости

```bash
$ pip install -r requirements.txt
```

4. Создать файл `<НАЗВАНИЕ_ФАЙЛА>.sh` с переменными окружения

```bash
export KEITARO_HOST='домен, где установлен keitaro'
export KEITARO_API_KEY='keitaro admin api ключ'
export GSHEETS_API_KEY='секретный ключ google таблиц'
python .
```

5. Включить [Google Sheets API v4](https://developers.google.com/sheets/api/quickstart/python) в аккаунте

6. Запустить скрипт

```bash
$ source `<НАЗВАНИЕ_ФАЙЛА>.sh`
```
