from models import Author, Quote
import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def main():

    while True:
        user_command = input("Enter command: ").strip().lower()
        if user_command == "exit":
            break
        else:
            try:
                command, value = user_command.split(":")
                cache.set(command.strip(), value.strip())

                if command == "name":
                    quote_list = []
                    value = cache.get(command)
                    uuid = Author.objects(fullname__startswith=value.strip().title())[0]
                    quotes = Quote.objects(author=uuid)
                    if quotes:
                        for quote in quotes:
                            quote_list.append(quote.quote)
                    print(*quote_list, sep="\n")

                elif command == "tag":
                    quote_list = []
                    value = cache.get(command)
                    for quote in Quote.objects(tags__startswith=value):
                        quote_list.append(quote.quote)
                    print(*quote_list, sep="\n")

                elif command == "tags":
                    quote_list = []
                    value = cache.get(command)
                    for quote in Quote.objects(tags__in=value.strip().split(",")):
                        quote_list.append(quote.quote)
                    print(*quote_list, sep="\n")
                else:
                    print("Your command is wrong. Please, try again!")

                
            except Exception as err:
                print(err)


if __name__ == "__main__":
    main()
