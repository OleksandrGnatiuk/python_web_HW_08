import json

from models import Author, Quote

with open('authors.json', 'r', encoding='utf-8') as fd:
    authors = json.load(fd)

    for author in authors:
        fullname = author.get('fullname', None)
        born_date = author.get('born_date', None)
        born_location = author.get('born_location', None)
        description = author.get('description', None)
        new_author = Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
        new_author.save()


with open('quotes.json', 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)

    for one_quote in quotes:
        tags = one_quote.get('tags', None)
        quote = one_quote.get('quote', None)
        authors = Author.objects(fullname=one_quote['author'])
        new_quote = Quote(tags=tags, quote=quote, author=authors[0])
        new_quote.save()