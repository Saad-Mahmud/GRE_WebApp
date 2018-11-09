from App_Main.Backend.DictionaryCard.Decorator import Decorator


class Translation(Decorator):
    """
    Add responsibilities to the component.
    """

    def get_dict(self):
        ret = self._component.get_dict()
        ret['translations'] = self.Data
        return ret