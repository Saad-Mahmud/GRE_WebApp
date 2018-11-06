from zKM_Test.Backend.app.model import Gre_data
from zMA_Test.Backend.app.model import session_test
from datetime import datetime


def create_session_test(status, words, idx, ques_multi, ques_blank):
    session= session_test(status=status, words=words, idx=idx, ques_multi=ques_multi, ques_blank=ques_blank)
    session2 = session.save()
    return session2


# def create_gre_test(username, history, how_many_test, best_score, avg_score, rating):
#     gre_test = Gre_data(username=username, history=history,how_many_test=how_many_test,best_score=best_score,avg_score=avg_score,rating=rating)
#     gre_test = gre_test.save()
#     return gre_test


def create_gre_test(username, history, test_date, how_many_test, best_score, avg_score, rating, country, rating_chart,
                    rate_date, all_scores):
    gre_test = Gre_data(username=username, history=history, test_date=test_date, how_many_test=how_many_test,best_score=best_score,
                        avg_score=avg_score,rating=rating, country=country, rating_chart=rating_chart, rate_date=rate_date, all_scores=all_scores)
    gre_test = gre_test.save()
    return gre_test


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