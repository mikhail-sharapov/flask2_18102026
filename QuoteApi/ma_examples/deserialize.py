from author import Author
from schema import SAuthor
from marshmallow import EXCLUDE, INCLUDE, RAISE

json_data = """
[
   {
       "id": 1,
       "name": "Alex",
       "email": "alex@mail.ru"
   },
   {
       "id": 2,
       "name": "Ivan",
       "email": "ivan@mail.ru"
   },
   {
       "id": 4,
       "name": "Tom",
       "email": "tom@mail.ru"
   }
]
"""

schema = SAuthor(unknown=EXCLUDE, many=True) # unknown - как обрабатывать неизвестные поля
json_to_list_of_dicts = schema.loads(json_data) # загрузка из строки JSON
result = schema.load(json_to_list_of_dicts)
authors = []
for item in result:
    authors.append(Author(**item))

print(authors)