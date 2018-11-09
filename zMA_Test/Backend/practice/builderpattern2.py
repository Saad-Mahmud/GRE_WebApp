import abc
from random import randint
import six
from zMA_Test.Backend.practice.practice_util import showstat


class DirectorNextWord:
    def __init__(self, pointer_f, buttonID, user_history):
        self._builder = None
        self.pointer_f = pointer_f
        self.buttonID = buttonID
        self.user_history = user_history

    def constructNextWord(self, builder):
        self._builder = builder
        self._builder.initNext(self.pointer_f)
        self._builder.set_history(self.buttonID)
        self._builder.modifyWords(self.buttonID)
        self._builder.updateDB(self.pointer_f)
        self._builder.saveUserHistory(self.user_history)
        self._builder.getNextWord()


@six.add_metaclass(abc.ABCMeta)
class BuilderNextWord:
    def __init__(self):
        self.pointer = 0
        self.words = []
        self.oldStatus = {}
        self.newStatus = {}
        self.currentWord = {}
        self.currentWordID = ' '
        self.history = {}
        self.newWord = {}
        self.mastered = 0
        self.reviewing = 0
        self.learning = 0

        self.next_word_object = NextWord(self.pointer, self.words, self.oldStatus, self.newStatus, self.currentWord,
                                         self.currentWordID, self.history, self.newWord, self.mastered, self.reviewing,
                                         self.learning)

    @abc.abstractmethod
    def initNext(self, pointer_f):
        pass

    @abc.abstractmethod
    def set_history(self, buttonID):
        pass

    @abc.abstractmethod
    def modifyWords(self, buttonID):
        pass

    @abc.abstractmethod
    def updateDB(self, pointer_f):
        pass

    @abc.abstractmethod
    def saveUserHistory(self, user_history):
        pass

    @abc.abstractmethod
    def getNextWord(self):
        pass


class ConcreteBuilderNextWord(BuilderNextWord):
    def initNext(self, pointer_f):
        self.pointer = pointer_f.idx
        self.words = pointer_f.edited_words
        self.oldStatus = pointer_f.status
        self.newStatus = self.oldStatus
        self.currentWord = self.words[self.pointer]
        self.currentWordID = self.currentWord['wordID']
        self.history = pointer_f.history

    def set_history(self, buttonID):
        if self.currentWordID not in self.history:
            self.history[self.currentWordID] = {buttonID}
        else:
            self.history[self.currentWordID].append(buttonID)

    def modifyWords(self, buttonID):
        if buttonID == 'ik':
            if self.newStatus[self.currentWordID] == 'firstseen':
                self.newStatus[self.currentWordID] = 'yellow'
                self.words.remove(self.currentWord)
                rand = randint(0, len(self.words))
                self.words.insert(rand, self.currentWord)

            elif self.newStatus[self.currentWordID] == 'red':
                self.newStatus[self.currentWordID] = 'yellow'
                self.words.remove(self.currentWord)
                rand = randint(0, len(self.words))
                self.words.insert(rand, self.currentWord)

            elif self.newStatus[self.currentWordID] == 'yellow':
                self.newStatus[self.currentWordID] = 'green'
                self.words.remove(self.currentWord)

        elif buttonID == 'idk':
            if self.newStatus[self.currentWordID] == 'firstseen':
                self.newStatus[self.currentWordID] = 'red'
                self.words.remove(self.currentWord)
                rand = randint(0, len(self.words))
                self.words.insert(rand, self.currentWord)

            elif self.newStatus[self.currentWordID] == 'yellow':
                self.newStatus[self.currentWordID] = 'yellow'
                self.words.remove(self.currentWord)
                rand = randint(0, len(self.words))
                self.words.insert(rand, self.currentWord)

    def updateDB(self, pointer_f):
        if len(self.words) != 0:
            self.pointer = (self.pointer + 1) % len(self.words)
            self.newWord = self.words[self.pointer]
            pointer_f.edited_words = self.words
            pointer_f.status = self.newStatus
            pointer_f.idx = self.pointer
            pointer_f.history = self.history
            pointer_f.save()
        else:
            self.pointer = -1
            self.newWord = {'wordID': '$null$'}
            pointer_f.history = self.history
            pointer_f.save()

    def saveUserHistory(self, user_history):
        user_history.status[self.currentWordID] = self.newStatus[self.currentWordID]
        user_history.save()
        self.mastered, self.reviewing, self.learning = showstat(self.newStatus)

    def getNextWord(self):
        self.next_word_object = NextWord(self.pointer, self.words, self.oldStatus, self.newStatus, self.currentWord,
                                         self.currentWordID, self.history, self.newWord, self.mastered, self.reviewing,
                                         self.learning)


class NextWord(object):
    def __init__(self, pointer, words, oldStatus, newStatus, currentWord, currentWordID, history, newWord, mastered,
                 reviewing, learning):
        self.pointer = pointer
        self.words = words
        self.oldStatus = oldStatus
        self.newStatus = newStatus
        self.currentWord = currentWord
        self.currentWordID = currentWordID
        self.history = history
        self.newWord = newWord
        self.mastered = mastered
        self.reviewing = reviewing
        self.learning = learning