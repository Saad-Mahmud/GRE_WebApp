import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Cards():
    """
    Define the interface for objects that can have responsibilities
    added to them dynamically.
    """

    @abc.abstractmethod
    def get_dict(self):
        pass


