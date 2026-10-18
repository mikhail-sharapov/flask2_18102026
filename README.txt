#Flask2_18102026

Создать виртуальное окружение
python3 -m venv flask_venv

Активировать виртуальное окружение
source flask_venv/bin/activate

Установить нужные библиотеки
python -m pip install -r requirements.txt

Применить миграции
flask db migrate

Запустить приложение
python run.py