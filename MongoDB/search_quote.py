from models import Author, Quote
import redis
from redis_lru import RedisLRU
from mongoengine import DoesNotExist

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_quoter_by_name(value):
    try:
        author = Author.objects(fullname__startswith=value.title())[0]
        quotes = Quote.objects(author=author)
        if quotes:
            result = []
            for quote in quotes:
                r = f"{quote.quote}\n{quote.author.fullname}     tags:{', '.join(quote.tags)}"
                result.append(r)
            return result
    except DoesNotExist:
        print(f'Quotes by {value} is not exists')


@cache
def find_quoter_by_tag(value):
    try:
        result = []
        for quote in Quote.objects(tags__startswith=value):
            r = f"{quote.quote}\n{quote.author.fullname}     tags: {', '.join(quote.tags)}"
            result.append(r)
        return result
    except DoesNotExist:
        print(f'Quotes with tag:{value} is not exists')


def main():
    while True:
        user_command = input("Enter command: ").strip().lower()
        if user_command == "exit":
            print('Good bye!')
            break
        else:
            try:
                command, value = user_command.split(":")
                command, value = command.strip(), value.strip()

                if command == "name":
                    print(*find_quoter_by_name(value), sep='\n')

                elif command == "tag":
                    print(*find_quoter_by_tag(value), sep='\n')

                elif command == "tags":
                    result = []
                    for quote in Quote.objects():
                        for tag in quote.tags:
                            if tag in value.split(","):
                                r = f"{quote.quote}\n{quote.author.fullname}      tags: {', '.join(quote.tags)}"
                                if r not in result:
                                    result.append(r)
                    [print(r) for r in result]
                else:
                    print("Your command is wrong. Please, try again!")
            except Exception as err:
                print(err)


if __name__ == "__main__":
    main()
