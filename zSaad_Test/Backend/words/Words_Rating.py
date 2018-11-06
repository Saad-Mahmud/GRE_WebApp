from mongoengine import Document, StringField, ListField


class Words_Rating(Document):
    wordID = StringField(required=True, max_length=50, primary_key=True)
    Ratings = ListField()