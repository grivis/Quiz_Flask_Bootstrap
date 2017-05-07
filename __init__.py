from flask import Flask, render_template, request, redirect, make_response
import glob
import random
import time, datetime

app = Flask(__name__)

ads = ['Bootstrap - отличный пакет для быстрой разработки сайтов',
       'Bootstrap хорошо работает совместно с Flask']
FooterText = 'Неавторизованный пользователь'
#topic_selected = None
topicdic = {}
flag_topicdic = False

@app.route('/')
def mainpage():
    uid = request.cookies.get('userID')
    lname = request.cookies.get('lName')
    fname = request.cookies.get('fName')
    if uid or lname or fname:
        FooterText = 'Пользователь: {}, {} {}'.format(uid, lname, fname)
    else:
        FooterText = 'Неавторизованный пользователь'

    return render_template('rootpage.html', ads=ads, FooterText=FooterText)

@app.route('/topics')
def topics():
    global topicdic, flag_topicdic
    '''
{'Животные':['trivia2.txt', 'trivia5.txt']}

    quest_set = set()
    for file in glob.glob('./static/trivia*.txt'):
        #print(file)
        f = open(file, "r", encoding="utf-8")
        quest_set.add(f.readline().replace("\n", ""))
        f.close()
    quest_list = list(quest_set)
    '''
    uid = request.cookies.get('userID')
    lname = request.cookies.get('lName')
    fname = request.cookies.get('fName')
    if uid or lname or fname:
        FooterText = 'Пользователь: {}, {} {}'.format(uid, lname, fname)
    else:
        FooterText = 'Неавторизованный пользователь'

    if not flag_topicdic:
        for file in glob.glob('/var/www/QuizApp/QuizApp/static/trivia*.txt'):
            f = open(file, "r", encoding="utf-8")
            topic = f.readline().replace("\n", "")
            if not topicdic.get(topic):
                topicdic[topic] = [file]
            else:
                flist = topicdic[topic]
                flist.append(file)
                topicdic[topic] = flist
        flag_topicdic = True
    #print(topicdic)
    quest_list = [(item, len(topicdic[item])) for item in sorted(topicdic.keys())]


    if 'Столицы стран Европы' in quest_list:
        ads[0] = '<a href="https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%93%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F">Портал Географии на Википедии</a>'
    if 'Виды животных' in quest_list:
        ads[1] = '<a href="https://ru.wikipedia.org/wiki/%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5">Статья Животные на Википедии</a>'
    if request.args:
        opt = request.args['optradio']
        topic_selected = quest_list[int(opt)-1][0]
        resp = make_response(redirect('/selected'))
        resp.set_cookie('TopicSelected', topic_selected, max_age=30)
        return resp


    return render_template('topicspage.html', quest_list=quest_list, ads=ads, FooterText=FooterText)

@app.route('/selected')
def selected():
    global topicdic
    uid = request.cookies.get('userID')
    lname = request.cookies.get('lName')
    fname = request.cookies.get('fName')
    if uid or lname or fname:
        FooterText = 'Пользователь: {}, {} {}'.format(uid, lname, fname)
    else:
        FooterText = 'Неавторизованный пользователь'
    topic_selected = request.cookies.get('TopicSelected')
    files = topicdic[topic_selected]

    '''Получить количество минут в данный момент'''
    t = datetime.datetime.now()
    minnow = t.timetuple().tm_min
    order = minnow % len(files)
    #order = minnow % 5
    # print('Minutes', minnow)
    file = (files[order])
    #print(files)
    f = open(file, "r", encoding="utf-8")
    topic = f.readline()
    question = f.readline()
    options = []
    for i in range(1, 5):
        options.append(f.readline().replace('\n', ''))
    right_answer = f.readline().replace('\n', '')
    f.close()
    # print(right_answer)
    if request.args:
        opt = request.args['optradio']
        # print(type(opt), opt)
        if opt == right_answer:
            topicdic.clear()
            topic_selected = None
            return render_template('reply.html', answer=True, ads=ads, FooterText=FooterText)
        else:
            topicdic.clear()
            topic_selected = None
            return render_template('reply.html', answer=False, ads=ads, FooterText=FooterText)

    return render_template('onequest-jum.html', topic=topic, question=question, options=options, ads=ads,
                           FooterText=FooterText)



@app.route('/onequestion')
def onequestion():
    files = glob.glob('/var/www/QuizApp/QuizApp/static/trivia*.txt')
    '''Получить количество минут в данный момент'''
    uid = request.cookies.get('userID')
    lname = request.cookies.get('lName')
    fname = request.cookies.get('fName')
    if uid or lname or fname:
        FooterText = 'Пользователь: {}, {} {}'.format(uid, lname, fname)
    else:
        FooterText = 'Неавторизованный пользователь'
    t = datetime.datetime.now()
    minnow = t.timetuple().tm_min
    order = minnow%len(files)
    #print('Minutes', minnow)
    file = (files[order])
    #print(file)
    f = open(file, "r", encoding="utf-8")
    topic = f.readline()
    question = f.readline()
    options = []
    for i in range(1,5):
        options.append(f.readline().replace('\n', ''))
    right_answer = f.readline().replace('\n', '')
    f.close()
    #print(right_answer)
    if request.args:
        opt = request.args['optradio']
        #print(type(opt), opt)
        if opt == right_answer:
            return render_template('reply.html', answer=True,  ads=ads, FooterText=FooterText)
        else:
            return render_template('reply.html', answer=False, ads=ads, FooterText=FooterText)

    return render_template('onequest-jum.html', topic=topic, question=question, options=options, ads=ads, FooterText=FooterText)

@app.route('/user/')
def login():
    uid = request.args.get('uid')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    FooterText = 'Пользователь: {}, {} {}'.format(uid, last_name, first_name)
    resp = make_response(render_template('rootpage.html', ads=ads, FooterText=FooterText))
    resp.set_cookie('userID', uid, max_age=24*60*60)
    resp.set_cookie('fName', first_name, max_age=24*60*60)
    resp.set_cookie('lName', last_name, max_age=24*60*60)
    return resp
    #render_template('rootpage.html', ads=ads, FooterText=FooterText)



if __name__ == '__main__':
    app.run(debug=True)
