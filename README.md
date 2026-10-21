# Flask2

## Инструкция по развертыванию проекта
1. Создать виртуальное окружение
```
python3 -m venv flask_venv
```
2. Активировать виртуальное окружение
```
source flask_venv/bin/activate
```
3. Установить нужные библиотеки
```
pip install -r requirements.txt
```
4. Применить миграции
```
flask db upgrade
```
5. Создаем файл '.flaskenv'
```
FLASK_APP = run.py
FLASK_DEBUG = 1
```
6. Запустить приложение
```
flask run
```

## Ссылки на документацию
1. Настройки для запуска 'flask run' [тут](https://flask.palletsprojects.com/en/stable/cli/)
2. Настройки для конфигов [тут](https://flask.palletsprojects.com/en/stable/config/)

## Работа с sqlite3

1. Установка **CLI** для **sqlite**: 
```
sudo apt install sqlite3
```
2. Создать дамп БД (схема + данные): 
```
sqlite3 quotes.db .dump > db_sql/db_data.sql
```
3. Создать дамп БД (только схема): 
```
sqlite3 quotes.db ".schema quotes" > db_sql/db_schema.sql
```
4. Загрузить данные в БД: 
```
sqlite3 new_store.db ".read db_sql/db_data.sql"
```