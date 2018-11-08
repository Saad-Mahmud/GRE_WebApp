import abc

import six

from zMA_Test.Backend.test.iterator_pattern import WordList


class DirectorSummary:
    def __init__(self, pointer_f, isWhat):
        self._builder = None
        self.pointer_f = pointer_f
        self.isWhat = isWhat

    def constructSummary(self, builder):
        self._builder = builder
        self._builder.setTestWords(self.pointer_f)
        self._builder.setQuestions(self.pointer_f, self.isWhat)
        self._builder.setAns(self.pointer_f)
        self._builder.getSummary()


@six.add_metaclass(abc.ABCMeta)
class BuilderSummary():
    def __init__(self):
        self.test_words = []
        self.ques = []
        self.correct_ans = []
        self.your_ans = []
        self.summary_object = Summary(self.test_words, self.ques, self.correct_ans, self.your_ans)

    @abc.abstractmethod
    def setTestWords(self, pointer_f):
        pass

    @abc.abstractmethod
    def setQuestions(self, pointer_f, isWhat):
        pass

    @abc.abstractmethod
    def setAns(self, pointer_f):
        pass

    @abc.abstractmethod
    def getSummary(self):
        pass


class ConcreteBuilderSummary(BuilderSummary):

    def setTestWords(self, pointer_f):
        self.test_words = pointer_f.words

    def setQuestions(self, pointer_f, isWhat):
        if isWhat == 'true':
            self.ques = pointer_f.ques_blank
        else:
            self.ques = pointer_f.ques_multi

#........................................Iterator pattern is used to iterate the wordlist...................................................
    def setAns(self, pointer_f):
        words = pointer_f.words
        wordlist = WordList(words)
        iterator = wordlist.iterator()
        while iterator.has_next():
            word = iterator.next()
            for the_key, the_value in pointer_f.status.items():
                if word[1] == the_key:
                    self.correct_ans.append(the_value[0])
                    self.your_ans.append(the_value[1])

    def getSummary(self):
        self.summary_object = Summary(self.test_words, self.ques, self.correct_ans, self.your_ans)


class Summary(object):
    def __init__(self, test_words, ques, correct_ans, your_ans):
        self.test_words = test_words
        self.ques = ques
        self.correct_ans = correct_ans
        self.your_ans = your_ans