#!/usr/bin/python

import sys, csv, re


class Performance:
    PERFORMANCES = {}

    @classmethod
    def register(c_lass, **defn):
        new = c_lass(**defn)
        c_lass.PERFORMANCES[new.id] = new

    @classmethod
    def list_tunes(c_lass):
        tunes = {}
        for k,p in c_lass.PERFORMANCES.items():
            for t in p.motifs:
                if t:
                    if t not in tunes: tunes[t] = []
                    tunes[t].append(p)
        return tunes

    def __repr__(self):
        if self.given_name:
            name = self.given_name
        else:
            name = self.apparent_name
        return "("+self.id+") "+name                


    def __init__(self,  id='',
                        date='',
                        location='',
                        follows='',
                        given_name='',
                        same_as='',
                        apparent_name='',
                        motifs=[],
                        time='',
                        remarks=''):
        
        self.id = id
        self.date = date
        self.location = location
        self.follows = follows
        self.given_name = given_name
        self.same_as = same_as
        self.apparent_name = apparent_name
        self.motifs = motifs
        self.time = time
        self.remarks = remarks
        
        
POSSIBLE_NOTES = ['C','D','E','F','G','A','B','c,','d,','e,','f,','g,','a,','b,','c','d','e','f','g','a','b',"c'","d'","e'","f'","g'","a'","b'"]

class Note:
    @classmethod
    def read(c_lass, string, key=0):
        notes = []
        for note in string.split(" "):
            if note:
                note = [POSSIBLE_NOTES.index(n) for n in re.split('([A-Ga-g][^A-Ga-g]*)', note)[1::2]]
                notes.append( c_lass(min(note), max(note), key=key) )
        return notes

    def __init__(self, low, high, key):
        self.low = low - key
        self.high = high - key

    def __sub__(self, other):
        if isinstance(other, int):
            return Note(self.low-other, self.high-other, 0)
        else:
            raise TypeError

    def __repr__(self):
        return "("+str(self.low)+"-"+str(self.high)+")"

    def extend(self, other):
        assert isinstance(other, Note)
        if other.low < self.low: self.low = other.low
        if other.high > self.high: self.high = other.high
        

CODE = "1234567IJKLMNOPQRSTUV"
def smoosh_tune(tunedef):
    if ":" not in tunedef:
        key = "C"
        tune = tunedef
    else:
        key, tune = tunedef.split(":")
    key=Note.read(key)
    tune=Note.read(tune, key[0].low)

    if len(key)>1:
        raise ValueError("Only one key per motif please")

    if len(tune)==0:
        return None

    tune = tune[:8]
    offset = min(tune, key=lambda x:x.low).low//7 *7

    result = [note-offset for note in tune]

    # Make even more vague by ensuring each note contains the following note
    for i in range(len(result)-1):
        result[i].extend(result[i+1])

    encoded = ""
    for note in result:
        encoded+=CODE[note.low]
        encoded+=CODE[note.high]

    return encoded

if __name__=="__main__":
    try:
        infile = sys.argv[1]
    except IndexError:
        infile = "index.csv"

    header = True
    date = '?'
    location = '?'
    previous = '?'
    for p in csv.reader(file(infile,'r')):
        if header:
            header = False
        else:
            if p[1]: date = p[1]
            if p[2]: location = p[2]
            if p[3]=='yes':
                follows = previous
            else:
                follows = None
            Performance.register( id=p[0],
                                  date=date,
                                  location=location,
                                  follows=follows,
                                  given_name=p[4],
                                  same_as=p[5],
                                  apparent_name=p[6],
                                  motifs=[smoosh_tune(p[7]),smoosh_tune(p[8])],
                                  time=p[9],
                                  remarks=p[10])
            previous = p[0]

    all_tunes = Performance.list_tunes()

    for motif, p in sorted(list(all_tunes.items())):
        print motif, p 
