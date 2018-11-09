from App_Main.Backend.DictionaryCard.Decorator import Decorator


class Audio(Decorator):
    """
    Add responsibilities to the component.
    """

    def get_dict(self):
        ret = self._component.get_dict()
        ret['audio'] = self.Data
        return ret