from zMA_Test.Backend.practice.iteratorpattern import IterableObject


class SummaryObj:
    def __init__(self, wordname, wordmeaning, correct, wrong):
        self.wordname = wordname
        self.wordmeaning = wordmeaning
        self.correct = correct
        self.wrong = wrong


def create_summary(words, history):
    correct = {}
    wrong = {}

    for key, value in history.items():
        correct_count = 0
        wrong_count = 0

        valueList = IterableObject(value)
        iterator = valueList.iterator()
        while iterator.has_next():
            v = iterator.next()
            if v == 'ik':
                correct_count += 1
            else:
                wrong_count += 1

        correct[key] = correct_count
        wrong[key] = wrong_count

    return correct, wrong
