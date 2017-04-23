from flask import Flask, render_template, request
import glob
import random

app = Flask(__name__)

ads = ['Bootstrap - отличный пакет для быстрой разработки сайтов',
       'Bootstrap хорошо работает совместно с Flask']
FooterText = 'Наш проект разработки на Flask и Bootstrap'

@app.route('/')
def mainpage():
    return render_template('rootpage.html', ads=ads, FooterText=FooterText)

@app.route('/topics')
def topics():
    quest_set = set()
    for file in glob.glob('./static/trivia*.txt'):
        #print(file)
        f = open(file, "r", encoding="utf-8")
        quest_set.add(f.readline().replace("\n", ""))
        f.close()
    quest_list = list(quest_set)
    if 'Столицы стран Европы' in quest_list:
        ads[0] = '<a href="https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%93%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F">Портал Географии на Википедии</a>'
    if 'Виды животных' in quest_list:
        ads[1] = '<a href="https://ru.wikipedia.org/wiki/%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5">Статья Животные на Википедии</a>'

    print(ads)
    print(quest_list)
    return render_template('topicspage.html', quest_list=quest_list, ads=ads, FooterText=FooterText)

@app.route('/onequestion')
def onequestion():
    files = glob.glob('./static/trivia*.txt')
    file = random.choice(files)
    print(file)
    f = open(file, "r", encoding="utf-8")
    topic = f.readline()
    question = f.readline()
    options = []
    for i in range(1,5):
        options.append(f.readline().replace('\n', ''))
    right_answer = f.readline().replace('\n', '')
    f.close()
    print(right_answer)
    if request.args:
        opt = request.args['optradio']
        print(type(opt), opt)
        if opt == right_answer:
            return render_template('reply.html', answer=True,  ads=ads, FooterText=FooterText)
        else:
            return render_template('reply.html', answer=False, ads=ads, FooterText=FooterText)

    return render_template('onequest-jum.html', topic=topic, question=question, options=options, ads=ads, FooterText=FooterText)







app.run()