from author import Author
from schema import SAuthor

# author = Author(1, "Alex", "alex5@mail.ru")
# author_schema = SAuthor()
# result = author_schema.dump(author)
# print(result)

authors = [
   Author("1", "Alex"),
   Author("1", "Ivan"),
   Author("1", "Tom")
]

schema = SAuthor(many=True)
result = schema.dump(authors)
print(result)