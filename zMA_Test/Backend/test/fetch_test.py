from zKM_Test.Backend.app.model import Gre_data
from zMA_Test.Backend.app.model import session_test, test_summary
from datetime import datetime

from zMA_Test.Backend.test.iterator_pattern import WordList


def create_session_test(status, words, idx, ques_multi, ques_blank):
    session= session_test(status=status, words=words, idx=idx, ques_multi=ques_multi, ques_blank=ques_blank)
    session2 = session.save()
    return session2


def create_gre_test(username, history, test_date, how_many_test, best_score, avg_score, rating, country, rating_chart,
                    rate_date, all_scores):
    gre_test = Gre_data(username=username, history=history, test_date=test_date, how_many_test=how_many_test,best_score=best_score,
                        avg_score=avg_score,rating=rating, country=country, rating_chart=rating_chart, rate_date=rate_date, all_scores=all_scores)
    gre_test = gre_test.save()
    return gre_test

def create_test_summary(username, summary):
    sum = test_summary(username=username, summary=summary)
    sum = sum.save()
    return sum


def update_gre_data(username, test_key, session_data, correct):
    gre_data = Gre_data.objects(username=username)[0]
    gre_data.history[test_key] = session_data.status
    gre_data.test_date = datetime.utcnow()
    gre_data.how_many_test = gre_data.how_many_test + 1

    current_score = correct * 10

    if gre_data.best_score < current_score:
        gre_data.best_score = current_score

    gre_data.rating = gre_data.rating + current_score
    gre_data.avg_score = gre_data.rating / gre_data.how_many_test

    gre_data.rating_chart.append(gre_data.rating)
    gre_data.rate_date.append(gre_data.test_date)
    gre_data.all_scores.append(current_score)

    gre_data.save()


def update_test_summary(username, ques, your_ans, correct_ans):
    prev_sum = []
    prev_sum.append(ques)
    prev_sum.append(your_ans)
    prev_sum.append(correct_ans)
    test_sum = test_summary.objects(username=username)[0]
    test_sum.summary.append(prev_sum)
    test_sum.save()
    return prev_sum


def update_initial_session_test(sessionID, test_words, test_line, test_multi_choice_word):
    pointer_f = session_test.objects(id=sessionID.id)[0]
    pointer_f.words = test_words
    pointer_f.ques_blank.append(test_line)
    pointer_f.ques_multi.append(test_multi_choice_word)
    pointer_f.save()


def update_next_session_test(sessionID, isWhat, answer, type, test_line):
    pointer_f = session_test.objects(id=sessionID)[0]

    if type == 1:
        valueList = []
        pointer = pointer_f.idx + 1
        test_words = pointer_f.words

        if isWhat == 'true':
            valueList.append(test_words[pointer_f.idx][1])
            valueList.append(answer)
            pointer_f.status[test_words[pointer_f.idx][1]] = valueList
        else:
            valueList.append(test_words[pointer_f.idx][2])
            valueList.append(answer)
            pointer_f.status[test_words[pointer_f.idx][1]] = valueList

        pointer_f.idx = pointer
        pointer_f.save()
        return test_words, pointer

    elif type == 2:
        pointer_f.ques_blank.append(test_line)
        pointer_f.save()
        return pointer_f.status

    elif type == 3:
        pointer_f.ques_multi.append(test_line)
        pointer_f.save()
        return pointer_f.status

    elif type == 4:
        pointer_f.save()
        return pointer_f.status

    elif type == 5:
        test_words = pointer_f.words
        if isWhat == 'true':
            answer = test_words[pointer_f.idx][1]
        else:
            answer = test_words[pointer_f.idx][2]
        return answer

    elif type == 6:
        return pointer_f