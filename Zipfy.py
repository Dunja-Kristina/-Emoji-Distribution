from datetime import date, time
import re 
import emoji # pip3 install msgpack emoji

class Message:
    def __init__(self, date, time, id, content):
        self.id = id
        self.length = len(content)
        self.date = date
        self.time = time
        self.words = list(map(lambda x: len(x), re.findall(r'\w+', content))) # word length list with emoji included
        self.emoji = list(filter(lambda x: x in emoji.UNICODE_EMOJI, content)) 
        #print(self.emoji)
        #print(list(map(emoji.demojize,self.emoji))) # nazivi emoji-ja TODO izbaciti one koji predstavljaju pol/boju kože ? ili ne?
    def __str__(self):
        return self.id + ' ' + self.date + ' ' + self.time
class Citac:
    def WhatsApp(naziv):
        f  = open(naziv,"r")
        ceoText = f.read()
        nizPoruka = []
        #print(list(re.findall(r'[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}\, [0-9]{1,2}\:[0-9]{1,2} *?\-.*?\:.+',ceoText )))# TODO treba dodati da bude re compile multiline
        ri = re.compile(r'([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}\, [0-9]{1,2}\:[0-9]{1,2} *?\-.*?\:.*?(?=[0-9]{1,2}\/[0-9]{1,2}))',
         re.MULTILINE|re.S)
        
        rez = ri.findall(ceoText)
        for i in rez:
            rez = re.search(r'([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2})\, ([0-9]{1,2}\:[0-9]{1,2}) *?\-(.*?)\:(.*)',i,re.MULTILINE|re.S)
            nizPoruka.append(Message(rez.group(1),rez.group(2),rez.group(3),rez.group(4)))
        return nizPoruka

niz = Citac.WhatsApp("probni.txt")
x = {}
for i in niz:
    if i.id not in x:
        x[i.id] = {}
    for e in i.emoji:
        if e not in x[i.id]:
            x[i.id][e] = 1
        else:
            x[i.id][e] = x[i.id][e]+1
for id in x:
    for w in sorted(x[id], key=x[id].get):
        print(w, x[id][w])



    
