from author import Author
from schema import SAuthor
from marshmallow import EXCLUDE, INCLUDE, RAISE

json_data = """
{
    "id": 1,
    "name": "Ivan",
    "email": "ivan@mail.ru",
    "age": 12
}
"""

schema = SAuthor(unknown=EXCLUDE) # unknown - как обрабатывать неизвестные поля
json_to_dict = schema.loads(json_data) # загрузка из строки JSON
result = schema.load(json_to_dict) # загрузка из словаря
print(result)