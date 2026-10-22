from author import Author
from schema import SAuthor

author = Author(1, "Alex", "alex5@mail.ru")
author_schema = SAuthor()
result = author_schema.dump(author)
print(result)