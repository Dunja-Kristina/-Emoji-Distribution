import sys
import re
import emoji
import emojis
import glob
import numpy as np
import pandas as pd
import collections
import matplotlib.pyplot as plt
import math

class chatClass:

    def __init__(self, path):
        # Regex za <div> poruke.
        ri = re.compile(
            r'<div\s+class="_3-94 _2lem"\s*>.*?</div>\s*(?=<div\s+class="_3-94 _2lem)',
            re.MULTILINE | re.S)

        try:
            f = open(path, "r")
        except IOError:
            sys.error("Fajl ne postoji.")

        # U buf se ucitava cela html stranica, a match je kolekcija svih poruka.
        buf = f.read()
        match = ri.findall(buf)

        if match is None:
            sys.exit()
        else:
            self.msgs = match


class msgClass:
    def __init__(self, msg):

        #ri_date_time = re.compile(r'(?<=<div class="_3-94 _2lem">).+?(?=</div>)', re.MULTILINE | re.S)
        ri_snd = re.compile(r'(?<=_2lel">).+?(?=</div>)', re.MULTILINE | re.S)
        ri_msg = re.compile(r'(?<=<div class="_3-96 _2let"><div><div></div><div>).+?(?=</div>)', re.MULTILINE | re.S)

        #dt = ri_date_time.search(msg)
        snd = ri_snd.search(msg)
        mssg = ri_msg.search(msg)

        #self.date_time = dt.group()
        self.sender = snd.group()
        mssgS = mssg.group()

        if mssg is not None:
            #self.msg_len = len(mssgS)
            self.emojis_used = list(filter(lambda x: x in emoji.UNICODE_EMOJI, emojis.encode(mssgS)))

    def __str__(self):
        st = self.sender+'\n'+str(self.emojis_used)
        return st

paths = glob.glob("*.html")
emojiss1 = {}
emojiss2 = {}
'''for pth in paths:
    chat = chatClass(pth)
    chat_len = len(chat.msgs)

    for i in range(0, int(chat_len)):
        msgg = msgClass(chat[i])
        if msgg.emojis_used is not None:
            emojiss = np.append(emojiss, msgg.emojis_used)
        else:
            emojiss = np.append(emojiss, [list('no emojis')])

'''
chat = chatClass(paths[50])
chat_len = len(chat.msgs)

msgg_first = msgClass(chat.msgs[0])
sender1 = msgg_first.sender
sender2 = ""
print(sender1)
first = 0
second = 0

for i in range(0, int(chat_len)):
    msgg = msgClass(chat.msgs[i])

    for emodzi in msgg.emojis_used:
        if msgg.sender == sender1:
            first += 1
            if emodzi not in emojiss1.keys():
                emojiss1[emodzi] = 1
            else:
                emojiss1[emodzi] += 1
        else:
            sender2 = msgg.sender
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
data1 = pd.DataFrame(data_raw1)
#data1.to_csv("jedna.csv", index=True, header=False)

data_raw2 = list(emojis_sort2.keys())
data_raw2 = np.vstack((data_raw2, list(emojis_sort2.values())))
data_raw2 = data_raw2.transpose()
data2 = pd.DataFrame(data_raw2)
#data2.to_csv("druga.csv", index=True, header=False)
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


def harmonicNum(n, m):
    sum = 0
    for k in range(1, n):
        sum += 1/pow(k, m)
    return sum


def zipf_cdf(N, s):
    x = []
    for k in range(0, N):
        x.append(harmonicNum(k+1, s)/harmonicNum(N, s))
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
    return ks_test(zipf_cdf(n, s), ecdf(samp))


N1, s1 = 80, 0.95
N2, s2 = 80, 1.2

n1 = len(emojis_sort1)
n2 = len(emojis_sort2)

tete = np.arange(0, 3, 0.01)
min1 = 1
teta1 = -1
rangovi1 = [rangAproksimacije(n1, i, emojis_sort1.values()) for i in tete]


min2 = 1
teta2 = -1
rangovi2 = [rangAproksimacije(n2, i, emojis_sort2.values()) for i in tete]

for i in rangovi1: #korak(preciznost) je 0.1 TODO proveriti za razlicite N-ove, mozda malo vece
    if min1 > i:
        min1 = i
        teta1 = tete[rangovi1.index(i)]

for i in rangovi2: #korak(preciznost) je 0.1 TODO proveriti za razlicite N-ove, mozda malo vece
    if min2 > i:
        min2 = i
        teta2 = tete[rangovi2.index(i)]

print("Moja procena koeficijenta je " + str(teta1))
print("Moja procena koeficijenta je " + str(teta2))

'''
fig, axs = plt.subplots(1, 2)
axs[0].bar(tete, rangovi1)
axs[1].bar(tete, rangovi2)
'''
pmf_values1 = list(zipf_pmf(n1, teta1))
pmf_values2 = list(zipf_pmf(n2, teta2))

fig, axs = plt.subplots(1, 2)
axs[0].bar(coded_emojis1, height=emojis_sort1.values(), label= 'Emojiji '+emoji.demojize(sender1))
axs[0].bar(range(0, n1), height=pmf_values1, color='r', alpha=0.5, label= "Zipf "+str(teta1))
axs[0].legend(loc='upper right')
axs[1].bar(coded_emojis2, height=emojis_sort2.values(), label="Emojiji "+emoji.demojize(sender2))
axs[1].bar(range(0, n2), height=pmf_values2, color='r', alpha=0.5, label='Zipf '+str(teta2))
axs[1].legend(loc='upper right')
plt.show()
