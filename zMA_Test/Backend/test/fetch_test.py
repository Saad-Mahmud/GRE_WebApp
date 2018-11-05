from zKM_Test.Backend.app.model import Gre_data
from zMA_Test.Backend.app.model import session_test


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