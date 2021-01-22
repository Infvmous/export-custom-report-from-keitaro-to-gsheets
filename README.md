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
export KEITARO_HOST='Домен, на котором установлен Keitaro'
export KEITARO_API_KEY='Keitaro Admin API ключ'
python .
```

5. [Создать приложение в Google API, скачать credentials.json, необходимые для работы OAuth2 и Google Sheets, Drive APIs](https://developers.google.com/sheets/api/quickstart/python)

6. Запустить скрипт

```bash
$ source `<НАЗВАНИЕ_ФАЙЛА>.sh`
```
