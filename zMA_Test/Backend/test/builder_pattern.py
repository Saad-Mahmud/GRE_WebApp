import random
import abc
import operator

import six


class Director:
    def __init__(self, word, pointer, test_words, wordline1, wordans, wordline2):
        self._builder = None
        self.word = word
        self.pointer = pointer
        self.test_words = test_words
        self.wordline1 = wordline1
        self.wordans = wordans
        self.wordline2 = wordline2

    def construct(self, builder, option):
        self._builder = builder
        self._builder.initOptionList(self.word)
        if option == 1:
            self._builder.initRandomIdx()
        else:
            self._builder.setRandomIdx(self.pointer)
        self._builder.setOptionList(self.test_words)
        self._builder.setRandomOption()
        self._builder.setOptionDict()
        self._builder.setQuestionLine1(self.wordline1, self.wordans)
        self._builder.setQuestionLine2(self.wordline2)
        self._builder.getOption()


@six.add_metaclass(abc.ABCMeta)
class Builder:
    def __init__(self):
        self.random_idx = []
        self.option = []
        self.random_idx_option = []
        self.option_dict = {}
        self.sorted_dict = []
        self.test_line = ''
        self.test_multi_choice_word = ''
        self.option_object = Option(self.option, self.random_idx_option, self.random_idx, self.option_dict, self.sorted_dict, self.test_line, self.test_multi_choice_word)

    @abc.abstractmethod
    def initOptionList(self, word):
        pass

    @abc.abstractmethod
    def initRandomIdx(self):
        pass

    @abc.abstractmethod
    def setRandomIdx(self, pointer):
        pass

    @abc.abstractmethod
    def setOptionList(self, test_words):
        pass

    @abc.abstractmethod
    def setRandomOption(self):
        pass

    @abc.abstractmethod
    def setOptionDict(self):
        pass

    @abc.abstractmethod
    def setQuestionLine1(self, wordline, wordans):
        pass

    @abc.abstractmethod
    def setQuestionLine2(self, wordline):
        pass

    @abc.abstractmethod
    def getOption(self):
        pass


class ConcreteBuilder(Builder):

    def initOptionList(self, word):
        self.option.append(word)

    def initRandomIdx(self):
        self.random_idx = random.sample(range(1, 10), 3)

    def setRandomIdx(self, pointer):
        if pointer <= 3:
            random_idx1 = random.sample(range(0, pointer), 1)
            random_idx2 = random.sample(range(pointer + 1, 10), 2)
            self.random_idx = random_idx1 + random_idx2
        elif pointer <= 7:
            random_idx1 = random.sample(range(0, pointer), 2)
            random_idx2 = random.sample(range(pointer + 1, 10), 1)
            self.random_idx = random_idx1 + random_idx2
        else:
            self.random_idx = random.sample(range(0, pointer), 3)

    def setOptionList(self, test_words):
        #test_words are the list of all the 10 Words only, not including meaning, usage etc
        for i in range(3):
            self.option.append(test_words[self.random_idx[i]])

    def setRandomOption(self):
        self.random_idx_option = random.sample(range(1, 5), 4)

    def setOptionDict(self):
        for i in range(4):
            self.option_dict[self.option[i]] = self.random_idx_option[i]
        self.sorted_dict = sorted(self.option_dict.items(), key=operator.itemgetter(1))

    def setQuestionLine1(self, wordline, wordans):
        self.test_line = wordline
        self.test_line = self.test_line.replace(wordans, "___")

    def setQuestionLine2(self, wordline):
        self.test_multi_choice_word += 'Meaning of '
        choice_word = wordline
        choice_word = choice_word.upper()
        self.test_multi_choice_word += choice_word

    def getOption(self):
        self.option_object = Option(self.option, self.random_idx_option, self.random_idx, self.option_dict, self.sorted_dict, self.test_line, self.test_multi_choice_word)


class Option(object):
    def __init__(self, option, random_idx_option, random_idx, option_dict, sorted_dict, test_line, test_multi_choice_word):
        self.option = option
        self.random_idx_option = random_idx_option
        self.random_idx = random_idx
        self.option_dict = option_dict
        self.sorted_dict = sorted_dict
        self.test_line = test_line
        self.test_multi_choice_word = test_multi_choice_word




