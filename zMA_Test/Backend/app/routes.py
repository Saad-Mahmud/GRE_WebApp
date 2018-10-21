from zMA_Test.Backend.app import APP_MAIN
from flask import render_template
from zMA_Test.Backend.practice.fetch_practice import fetch_easy_words


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/practice')
def practice():
    words = fetch_easy_words()
    for i in words:
        print("jejjejjejeje :", i.wordID, i.word, i.meanings)
    '''
    words = [
        {
            'word': "Sweet",
            'TYPE': "Adjective",
            'meaning': "Mishty",
            'usages': "Aditi claims that she's still in her sweet sixteen."
        },
        {
            'word': "Affection",
            'TYPE': "Noun",
            'meaning': "Love",
            'usages': "Nobody has affection for me. Sad lief"
        }

    ]
    
    for wordID, ratings in words:
        print("Word List is Easy : ", wordID, ratings)
        '''
    counter = []
    for idx in range(0, len(words)):
        counter.append(idx)
    listt = [
        {
            'word': 'abcdef',
            'meanings': 'Beautiful day in Portland!'
        },
        {
            'word': 'ghijkl',
            'meanings': 'baaaaaaaaaaaaaaaaaaaaaal!'
        }
    ]
    print("listtt e: ", listt)

    return render_template('practice.html', words=words, counter=counter)
    #return render_template('practice.html')


@APP_MAIN.route('/test')
def test():
    return render_template('test.html')