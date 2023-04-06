from models import Author, Quote


def main():

    while True:
        user_command = input("Enter command: ").strip().lower()
        if user_command == "exit":
            break
        else:
            command, value = user_command.split(":")

            if command == "name":
                quote_list = []
                uuid = Author.objects(fullname__startswith=value.strip().title())[0]
                quotes = Quote.objects(author=uuid)
                if quotes:
                    for quote in quotes:
                        quote_list.append(quote.quote)

            elif command == "tag":
                quote_list = []
                for quote in Quote.objects(tags__startswith=value):
                    quote_list.append(quote.quote)

            elif command == "tags":
                quote_list = []
                # for t in value.strip().split(","):
                for quote in Quote.objects(tags__in=value.strip().split(",")):
                    quote_list.append(quote.quote)
            print(*quote_list, sep="\n")


if __name__ == "__main__":
    main()
