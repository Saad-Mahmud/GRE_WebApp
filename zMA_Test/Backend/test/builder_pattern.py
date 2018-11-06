import random

import operator


class OptionBuilder(object):
    def __init__(self):
        self.random_idx = []
        self.option = []
        self.random_idx_option = []
        self.option_dict = {}
        self.sorted_dict = []
        self.test_line = ''
        self.test_multi_choice_word = ''

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
        #test_words are the list of all the 10 words only, not including meaning, usage etc
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
        return Option(self.option, self.random_idx_option, self.random_idx, self.option_dict, self.sorted_dict, self.test_line, self.test_multi_choice_word)


class Option(object):
    def __init__(self, option, random_idx_option, random_idx, option_dict, sorted_dict, test_line, test_multi_choice_word):
        self.option = option
        self.random_idx_option = random_idx_option
        self.random_idx = random_idx
        self.option_dict = option_dict
        self.sorted_dict = sorted_dict
        self.test_line = test_line
        self.test_multi_choice_word = test_multi_choice_word




