from App_Main.Backend.DictionaryCard.Decorator import Decorator


class Usage(Decorator):
    """
    Add responsibilities to the component.
    """

    def get_dict(self):
        ret = self._component.get_dict()
        ret['usages'] = self.Data
        return ret