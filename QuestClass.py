'''
Создаем класс Question,

который будет содержать информацию
о каждом вопросе викторины
'''
import glob

class Question(object):
    '''One Quiz Question'''

    __total = 0
    __alltops = set()
    __allquests = []

    @staticmethod
    def howmany():
        return Question.__total

    @staticmethod
    def gettops():
        return sorted(list(Question.__alltops))

    @staticmethod
    def getquests():
        return Question.__allquests

    @staticmethod
    def readall():
        for filename in glob.glob('trivia*.txt'):
            q = Question(filename)
            Question.__allquests.append(q)

    def __init__(self, fstring):
        Question.__total += 1
        self.id = Question.__total
        self.options = []
        f = open(fstring, 'r', encoding='utf-8')
        self.topic = f.readline().replace('\n', '')
        self.thequestion = f.readline().replace('\n', '')
        for i in range(4):
                 self.options.append(f.readline().replace('\n', ''))
        self.correct = int(f.readline().replace('\n', ''))
        Question.__alltops.add(self.topic)
        print('One more question...')

    def __str__(self):
        reply = str(self.id) + ' : '
        reply += self.topic + ' : '
        reply += self.thequestion
        return reply

class Topic(object):
    '''One topic in a quiz'''
    __total = 0
    __alltops = []

    @staticmethod
    def collectall(): 
        for t in Question.gettops():
            qids = []
            for q in Question.getquests():
                if t == q.topic:
                    qids.append(q.id)      
            Topic.__alltops.append(Topic(t, qids))
    

    @staticmethod
    def gettops():
        return Topic.__alltops
    
    def __init__(self, thetopic, qids):
        Topic.__total += 1
        self.topic = thetopic
        self.quests = qids

    def __str__(self):
        reply = self.topic + ' : '
        reply += ' '.join([str(i) for i in self.quests])
        return reply
    
        
    


print(Question.howmany())


Question.readall()
print(Question.howmany())
print(Question.gettops())
##qs = Question.getquests()
##qs.sort(key=lambda x: x.topic)
##for item in qs:
##    print(item)
##qs.sort(key=lambda x: x.id)
##for item in qs:
##    print(item)
###one = Question('trivia1.txt')
Topic.collectall()
for t in Topic.gettops():
    print(t)

                 
                 
    
    
