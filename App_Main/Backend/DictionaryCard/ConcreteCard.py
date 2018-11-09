from App_Main.Backend.DictionaryCard.Cards import Cards


class ConcreteCard(Cards):
    """
    Define an object to which additional responsibilities can be
    attached.
    """
    def __init__(self,wordID,TYPE,word):
        self.dict = {'wordID' : wordID,
                     'word': word,
                     'TYPE': TYPE
                     }

    def get_dict(self):
        return self.dict