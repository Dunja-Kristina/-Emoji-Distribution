import re
import emoji  # pip3 install msgpack emoji
import numpy as np
import pandas as pd
import collections
import matplotlib.pyplot as plt
import math
import operator
from matplotlib.font_manager import FontProperties


class Message: 
    def __init__(self, id, content):
        self.id = id
        self.emoji = list(filter(lambda x: x in emoji.UNICODE_EMOJI and not x  in ['♀','♂','🏻','🏼','🏽','🏾','🏿'], content))
        # print(self.emoji)
        # print(list(map(emoji.demojize,self.emoji))) # nazivi emoji-ja TODO izbaciti one koji predstavljaju pol/boju kože ? ili ne?



def WhatsApp(fileName):
    f = open(fileName, "r")
    text = f.read()
    msgArr = []
    ri = re.compile(
        r'([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}\, [0-9]{1,2}\:[0-9]{1,2} *?\-.*?\:.*?(?=[0-9]{1,2}\/[0-9]{1,2}))',
        re.MULTILINE | re.S)

    rez = ri.findall(text)
    for i in rez:
        rez = re.search(r'[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}\, [0-9]{1,2}\:[0-9]{1,2} *?\- (.*?)\:(.*)', i,
                        re.MULTILINE | re.S)
        msgArr.append(Message(rez.group(1), rez.group(2)))
        
        
    return msgArr

def emoji_pmf(msgArr): #vraca recnik sa procentima
    emojiDict = {}
    for msg in msgArr:
        if(not(msg.id in emojiDict.keys())):
            emojiDict[msg.id] = {}
        for emoji in msg.emoji:
            if not (emoji in (emojiDict[msg.id]).keys()):
                emojiDict[msg.id][emoji] = 1
            else:
                emojiDict[msg.id][emoji] += 1
    for ime in emojiDict.keys():
        zb = sum(emojiDict[ime].values())
        for key in emojiDict[ime]:
            emojiDict[ime][key] /= zb; 
            
    return emojiDict
        
def zipf_pmf(N, s):
    H = 0
    for k in range(0, N):
        H += 1/math.pow(k+1, s)

    list_values = np.empty(N)
    for k in range(0, N):
        list_values[k] = 1/(math.pow(k+1, s)*H)
    return list_values

def harmonicNum(n,m):
    sum = 0
    for k in range(1, n):
        sum += 1/pow(k,m)
    return sum

def zipf_cdf(N, s):
    x = []
    for k in range(0, N):
        x.append(harmonicNum(k+1,s)/harmonicNum(N,s))
    return x
def ecdf(arr):
    x = [0]
    sum = 0
    for i in arr:
        sum += i
        x.append(sum)
    return x
def ks_test(dist, samp):
    max = 0
    for i in range(0, len(dist)):
        if(max < abs(dist[i]-samp[i])):
            max = abs(dist[i]-samp[i])
    return max
def rangAproksimacije(n, s, samp): #treba da bude sto manji!!!!
    #
    return ks_test(zipf_cdf(n,s),ecdf(samp))

niz = WhatsApp("probni.txt")

broj = emoji_pmf(niz)


fstPsn = list(broj.keys())[0] #First persons name
scdPsn = list(broj.keys())[1]
fst = sorted(broj[fstPsn].items(),key=operator.itemgetter(1), reverse=True)
scd = sorted(broj[scdPsn].items(),key=operator.itemgetter(1), reverse=True)

fstValues = [x[1] for x in fst]
scdValues = [x[1] for x in scd]
print("Ako ne radim, molim te obrisi prvu poruku u WA porukama koja nije stvarno poruka, nego neki random tekst")
min = 1
s = -1
for i in np.arange(0,3,0.1): #korak(preciznost) je 0.1 TODO proveriti za razlicite N-ove, mozda malo vece
    rang = rangAproksimacije(len(fstValues), i, fstValues)
    print(i," ",rang)
    if min > rang :
        min = rang
        s = i
print("Moja procena koeficijenta je " + str(s))


"""
#Stari Zipfy kod
from datetime import date, time
import re
import emoji  # pip3 install msgpack emoji
import numpy as np
import pandas as pd
import collections
import matplotlib.pyplot as plt
import math

class Message:
    def __init__(self, date, time, id, content):
        self.id = id
        self.length = len(content)
        self.date = date
        self.time = time
        self.words = list(map(lambda x: len(x), re.findall(r'\w+', content)))  # word length list with emoji included
        self.emoji = list(filter(lambda x: x in emoji.UNICODE_EMOJI, content))
        # print(self.emoji)
        # print(list(map(emoji.demojize,self.emoji))) # nazivi emoji-ja TODO izbaciti one koji predstavljaju pol/boju kože ? ili ne?

    def __str__(self):
        return self.id + ' ' + self.date + ' ' + self.time


class Citac:
    def WhatsApp(naziv):
        f = open(naziv, "r")
        ceoText = f.read()
        nizPoruka = []
        # print(list(re.findall(r'[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}\, [0-9]{1,2}\:[0-9]{1,2} *?\-.*?\:.+',ceoText )))# TODO treba dodati da bude re compile multiline
        ri = re.compile(
            r'([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}\, [0-9]{1,2}\:[0-9]{1,2} *?\-.*?\:.*?(?=[0-9]{1,2}\/[0-9]{1,2}))',
            re.MULTILINE | re.S)

        rez = ri.findall(ceoText)
        for i in rez:
            rez = re.search(r'([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2})\, ([0-9]{1,2}\:[0-9]{1,2}) *?\-(.*?)\:(.*)', i,
                            re.MULTILINE | re.S)
            nizPoruka.append(Message(rez.group(1), rez.group(2), rez.group(3), rez.group(4)))
        return nizPoruka


niz = Citac.WhatsApp("probni.txt")
emojiss1 = {}
emojiss2 = {}
sender1 = niz[3].id
print(sender1)
first = 0
second = 0

for message in niz:
    for emodzi in message.emoji:
        if message.id == sender1:
            first += 1
            if emodzi not in emojiss1.keys():
                emojiss1[emodzi] = 1
            else:
                emojiss1[emodzi] += 1
        else:
            second += 1
            if emodzi not in emojiss2.keys():
                emojiss2[emodzi] = 1
            else:
                emojiss2[emodzi] += 1

emojis_sort1 = collections.OrderedDict(sorted(emojiss1.items(), key=lambda x: x[1], reverse=True))
emojis_sort2 = collections.OrderedDict(sorted(emojiss2.items(), key=lambda x: x[1], reverse=True))

data_raw1 = list(emojis_sort1.keys())
data_raw1 = np.vstack((data_raw1, list(emojis_sort1.values())))
data_raw1 = data_raw1.transpose()
print(emojis_sort1)
data1 = pd.DataFrame(data_raw1)
data1.to_csv("jedna.csv", index=True, header=False)

data_raw2 = list(emojis_sort2.keys())
data_raw2 = np.vstack((data_raw2, list(emojis_sort2.values())))
data_raw2 = data_raw2.transpose()
print(emojis_sort2)
data2 = pd.DataFrame(data_raw2)
data2.to_csv("druga.csv", index=True, header=False)
emojis_sort1 = collections.OrderedDict([(a, b/first) for (a, b) in emojis_sort1.items()])
emojis_sort2 = collections.OrderedDict([(a, b/second) for (a, b) in emojis_sort2.items()])

coded_emojis1 = [emoji.demojize(i) for i in emojis_sort1.keys()]
coded_emojis2 = [emoji.demojize(i) for i in emojis_sort2.keys()]


def zipf_pmf(N, s):
    H = 0
    for k in range(0, N):
        H += 1/math.pow(k+1, s)

    list_values = np.empty(N)
    for k in range(0, N):
        list_values[k] = 1/(math.pow(k+1, s)*H)
    return list_values


N1, s1 = 80, 2.2
N2, s2 = 80, 0.9

n1 = list(emojis_sort1.values())[0]
n2 = list(emojis_sort2.values())[0]

pmf_values = list(zipf_pmf(N1, s1))
pmf_values1 = list(zipf_pmf(N2, s2))

fig, axs = plt.subplots(1, 2)
axs[0].bar(coded_emojis1, height=emojis_sort1.values(), label= 'Emojiji')
axs[0].bar(range(N1), pmf_values, color='r', alpha=0.5, label= "Zipf 2.2")
axs[0].legend(loc='upper right')
axs[1].bar(coded_emojis2, height=emojis_sort2.values(), label="Emojiji")
axs[1].bar(range(N2), pmf_values1, color='r', alpha=0.5, label='Zipf 0.9')
axs[1].legend(loc='upper right')

plt.show()
"""