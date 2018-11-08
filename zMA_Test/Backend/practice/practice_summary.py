
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
        for v in value:
            if v=='ik':
                correct_count += 1
            else:
                wrong_count += 1
        correct[key] = correct_count
        wrong[key] = wrong_count
        print("printing right and wrong ", key, correct_count, wrong_count)

    return correct, wrong
