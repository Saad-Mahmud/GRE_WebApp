from App_Main.Backend.DictionaryMaker.DictionaryMaker import DictionaryMaker


class AnonDict(DictionaryMaker):
    """
    Override the factory method to return an instance of a
    ConcreteProduct2.
    """

    def build(self):
        pass


    def get(self):
        ret = [value.get_dict() for key, value in self.dict.items()]
        return ret