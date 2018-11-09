import abc
import six

from App_Main.Backend.DictionaryCard.Cards import Cards


@six.add_metaclass(abc.ABCMeta)
class Decorator(Cards):
    """
    Maintain a reference to a Component object and define an interface
    that conforms to Component's interface.
    """

    def __init__(self, component):
        self._component = component
        self.Data = None

    @abc.abstractmethod
    def get_dict(self):
        pass

    def setData(self, data):
        self.Data = data