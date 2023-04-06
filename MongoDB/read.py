from mongoengine import disconnect

from models import Author, Quote

if __name__ == '__main__':

    author_list = Author.objects()
    for author in author_list:
        print(author.to_mongo().to_dict())

    quoter_lists = Quote.objects()
    for quote in quoter_lists:
        print(quote.to_mongo().to_dict())

    disconnect()
