import abc

import six

from zMA_Test.Backend.practice.iteratorpattern import IterableObject
from zMA_Test.Backend.test.iterator_pattern import WordList


class DirectorPracticeSummary:
    def __init__(self, pointer_f):
        self._builder = None
        self.pointer_f = pointer_f

    def constructPracticeSummary(self, builder):
        self._builder = builder
        self._builder.set_practice_words(self.pointer_f)
        self._builder.set_word_history(self.pointer_f)
        self._builder.set_results(self.pointer_f)
        self._builder.getPracticeSummary()


@six.add_metaclass(abc.ABCMeta)
class BuilderPracticeSummary():
    def __init__(self):
        self.practice_words = []
        self.history = {}
        self.correct = {}
        self.wrong = {}
        self.practice_summary_object = PracticeSummary(self.practice_words, self.history, self.correct, self.wrong)

    @abc.abstractmethod
    def set_practice_words(self, pointer_f):
        pass

    @abc.abstractmethod
    def set_word_history(self, pointer_f):
        pass

    @abc.abstractmethod
    def set_results(self, pointer_f):
        pass

    @abc.abstractmethod
    def getPracticeSummary(self):
        pass


class ConcreteBuilderPracticeSummary(BuilderPracticeSummary):
    def set_practice_words(self, pointer_f):
        self.practice_words = pointer_f.words

    def set_word_history(self, pointer_f):
        self.history = pointer_f.history

    def set_results(self, pointer_f):
        for key, value in self.history.items():
            correct_count = 0
            wrong_count = 0

            # ////////////////////////Iterator Pattern//////////////////////////////////
            valueList = IterableObject(value)
            iterator = valueList.iterator()
            while iterator.has_next():
                v = iterator.next()
                if v == 'ik':
                    correct_count += 1
                else:
                    wrong_count += 1
            self.correct[key] = correct_count
            self.wrong[key] = wrong_count

    def getPracticeSummary(self):
        self.practice_summary_object = PracticeSummary(self.practice_words, self.history, self.correct, self.wrong)


class PracticeSummary(object):
    def __init__(self, practice_words, history, correct, wrong):
        self.practice_words = practice_words
        self.history = history
        self.correct = correct
        self.wrong = wrong