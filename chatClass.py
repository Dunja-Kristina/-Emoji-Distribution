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
chat = chatClass(paths[40])
chat_len = len(chat.msgs)

msgg_first = msgClass(chat.msgs[0])
sender1 = msgg_first.sender
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
#print(emojis_sort1)
data1 = pd.DataFrame(data_raw1)
#data1.to_csv("jedna.csv", index=True, header=False)

data_raw2 = list(emojis_sort2.keys())
data_raw2 = np.vstack((data_raw2, list(emojis_sort2.values())))
data_raw2 = data_raw2.transpose()
#print(emojis_sort2)
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


N1, s1 = 80, 0.95
N2, s2 = 80, 1.2

n1 = list(emojis_sort1.values())[0]
n2 = list(emojis_sort2.values())[0]

pmf_values = list(zipf_pmf(N1, s1))
pmf_values1 = list(zipf_pmf(N2, s2))

fig, axs = plt.subplots(1, 2)
axs[0].bar(coded_emojis1, height=emojis_sort1.values(), label= 'Emojiji')
axs[0].bar(range(N1), pmf_values, color='r', alpha=0.5, label= "Zipf 0.9")
axs[0].legend(loc='upper right')
axs[1].bar(coded_emojis2, height=emojis_sort2.values(), label="Emojiji")
axs[1].bar(range(N2), pmf_values1, color='r', alpha=0.5, label='Zipf 1.2')
axs[1].legend(loc='upper right')

plt.show()


