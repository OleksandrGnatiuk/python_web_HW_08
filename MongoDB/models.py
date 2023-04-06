from mongoengine import *
connect(host="mongodb+srv://userweb10:567234@cluster0.oqyfihy.mongodb.net/?retryWrites=true&w=majority")




class Author(Document):
    fullname = StringField(max_length=250)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=250)
    description = StringField()


class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    meta = {'allow_inheritance': True}


