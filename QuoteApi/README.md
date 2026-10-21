# QuoteAPI

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