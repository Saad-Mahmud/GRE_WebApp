import six

import abc


@six.add_metaclass(abc.ABCMeta)
class Target():
    def __init__(self):
        self._adaptee = Adaptee()

    @abc.abstractmethod
    def request(self, final_dict):
        pass


class Adapter(Target):
    def request(self, final_dict):
        final_list = self._adaptee.specific_request(final_dict)
        return final_list


class Adaptee:
    def specific_request(self, final_dict):
        final_list = []
        for word in final_dict:
            final_list.append([word['wordID'], word['word'], word['meaning'], word['usage'], word['translations'], word['TYPE']])
        return final_list
