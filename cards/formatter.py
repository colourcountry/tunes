#!/usr/bin/python

import re, os, sys

PREAMBLE = open("preamble.ly.fragment","r").read()

KEYS = {
    "G": { "ly": "g \major ","f": +1 },
    "D": { "ly": "d \major ","f": +1,"c": +1 }
}

class Phrase:
    def __init__(self, key, rhythm=None, name=None, bar_length=2, ab=[]):
        # notes = a list of tuples, one per beat.
        self.rhythm = rhythm
        self.key = key
        self.bar_length = bar_length
        self.name = name
        self.notes = []
        sys.stderr.write("New phrase %s\n" % self.name)
        self.add_lines(*ab)

    def __repr__(self):
        return "<phrase %s>" % self.name

    def rhythmify(self, notes):
        if self.rhythm is None:
            rhythm = []
        else:
            try:
                rhythm = self.rhythm[len(notes)-1]  
            except IndexError:
                rhythm = []

        for note in notes:
            if re.match(".+[0-9/][<>]?$", note):
                # explicit lengths given
                # add "1" to notes which don't have a length
                for i,note in enumerate(notes):
                    if re.match(".+[0-9/][<>]?$", note):
                        pass
                    else:
                        m = re.match("(.+)([<>])$", note)
                        if m:
                            # FIXME: support > <
                            notes[i] = m.group(1)+"1"
                        else:
                            notes[i] += "1"
                break

        for i,note in enumerate(notes):
            if re.match(".+[0-9/][<>]?$", note):
                pass
            else:
                m = re.match("(.+)[<>]$", note)
                if m:
                    # FIXME: support > <
                    note = m.group(1)
                try:
                    notes[i] = note+rhythm[i]
                except IndexError: # no defined rhythm, assume 1
                    notes[i] = note+"1"

        return notes
        

    def add_lines(self, *ab):
        connector = ''
        for lineno, line in enumerate(ab):
            line = re.split("([^A-Ga-gzx0-9/,'_=^<>]+)", line+" ")
            lineNotes = []
            for i in range(0,len(line)-1,2):
                beat = i/2
                notes = line[i]
                connector = line[i+1].strip()
                s = re.split('([A-Ga-gzx])', notes)
                splitNotes = []
                for i in range(1,len(s)-1,2):
                    splitNotes.append( s[i]+s[i+1] )
                if splitNotes:
                    lineNotes.append( self.rhythmify(splitNotes)+[connector] )

            if lineNotes:
                sys.stderr.write("lineNotes %s\n" % lineNotes)
                self.notes.append(lineNotes)
        return connector



    def get_code(self):
        def transpose(n,key=self.key):
            if n=="x": return "x"
            elif n=="z": return "x"
            return str( ( ord(n.lower()) - ord(key.lower()) ) %7 +1 )

        notes = []
        ticks = 0
        for beat in self.notes[0]:
            connector = beat[-1]
            for note in beat[:-1]:
                m = re.match("([A-Ga-gzx])([,'_=^]*)([0-9/]+)", note)
                if re.match("/+$",m.group(3)):
                    n = 1
                    d = 2**len(m.group(3))
                elif "/" in m.group(3):
                    (n, d) = m.group(3).split("/")
                    n = int(n)
                    d = int(d)
                else:
                    n = int(m.group(3))
                    d = 1

                length = 1.0*n/d
                ticks += length
            notes.append(beat[0])

            if connector=="|":
                if ticks < self.bar_length:
                    # skip anacrusis
                    notes = []

        return (''.join(transpose(note[0]) for note in notes)).ljust(8,"0")

    def render_ly(self, key=None, partial=0):
        def get_ly_length(l):
            if l==0.5: return '16'
            elif l==1: return '8'
            elif l==2: return '4'
            elif l==3: return '4.'
            elif l==4: return '2'
            elif l==6: return '2.'
            elif l==8: return '1'
            elif l==12: return '1.'
            raise ValueError("Couldn't make lilypond note of length %s" % l)

        if key == self.key:
            ly = ''
        else:
            ly = '\key %s\n' % KEYS[self.key]["ly"]

        for count, line in enumerate(self.notes):
            ticks = 0
            line_ly = ''
            for beat in line:
                beat_ly = ''
                connector = beat[-1]
                for note in beat[:-1]:
                    m = re.match("([A-Ga-gzx])([,'_=^]*)([0-9/]+)", note)
                    if not m:
                        raise ValueError("Bad note %s in line %s" % (note,line))

                    octave = 0

                    note = m.group(1)
                    if note=="z": note="r"
                    elif note=="x": note="s"
                    elif note in "abcdefg": octave += 1
                    else: note = note.lower()

                    acc = 0
                    nat = False
                    for o in m.group(2):
                        if o==",": octave -= 1
                        elif o=="'": octave += 1
                        elif o=="_": acc -= 1
                        elif o=="^": acc += 1
                        elif o=="=": nat = True
                    if octave > 0: octave = "'"*octave
                    elif octave < 0: octave = ","*-octave
                    else: octave = ""

                    if acc == 0 and not nat:
                        try:
                            acc = KEYS[self.key][note]
                        except KeyError:
                            pass

                    if acc > 0: acc = "is"*acc
                    elif acc < 0: acc = "es"*-acc
                    else: acc = ""

                    if re.match("/+$",m.group(3)):
                        n = 1
                        d = 2**len(m.group(3))
                    elif "/" in m.group(3):
                        (n, d) = m.group(3).split("/")
                        n = int(n)
                        d = int(d)
                    else:
                        n = int(m.group(3))
                        d = 1

                    length = 1.0*n/d
                    note += acc+octave+get_ly_length(length)
                    beat_ly += note+" "
                    ticks += length

                if connector=="|":
                    if ticks+partial < self.bar_length:
                        beat_ly = r'\partial %s %s' % (get_ly_length(ticks), beat_ly)
                    ticks = 0
                elif connector=="-":
                    beat_ly += r' ~ '
                elif connector=="||":
                    beat_ly += r' \bar "||" '
                elif connector=="|]":
                    beat_ly += r' \bar "|." '

                line_ly += beat_ly

            partial = ticks % self.bar_length

            if connector=="" and partial>0:
                # line ends in middle of bar
                sys.stderr.write("Line ended within bar: %s, %s ticks (%s bar length)\n" % (line, ticks, self.bar_length))
                line_ly += r'\bar ""'
            line_ly += r"\break "

            ly += line_ly

        return (ly, partial)


class Tune:
    def __init__(self, phrases=None, name=None, meter="A A B B"):
        self.time = '4/4'
        self.unit = '1/8'
        self.rhythm = None
        self.set_bar_length()

        if phrases is None:
            self.phrases = []
        else:
            self.phrases = phrases

        self.name = name
        self.meter = meter

    def set_bar_length(self):
        un, ud = self.unit.split('/')
        un=int(un)
        ud=int(ud)
        tn, td = self.time.split('/')
        tn=int(tn)
        td=int(td)
        self.bar_length = tn * (ud/td)
        sys.stderr.write("%s contains %s %s\n" % (self.time, self.bar_length, self.unit))
        return self.bar_length

    def add_phrase(self,phrase):
        self.phrases.append(phrase)

    def render_ly(self):

        s = r'''
\score{{
\transpose d d' {
\time %s
''' % self.time

        key = None
        partial = 0
        for phrase in self.phrases:
            s += '    \\mark \\default\n'
            phrase_ly, partial = phrase.render_ly(key, partial)
            s += phrase_ly
            key = phrase.key

        s += r'''
}}
\header{
    piece = "%s"
    opus = "%s"
    meter = "%s"
}}
\pageBreak
''' % (self.name, self.phrases[0].get_code(), self.meter)

        return s

class ABFile:
    def __init__(self, data):
        curtune = None
        curphrase = None
        curkey = None
        self.tunes = []
        stopped = False
        for line in data.readlines():
          line = line.strip()
          if stopped:
            if line.startswith("%%start"):
                stopped = False
          else:
            if line.startswith("%%stop"):
                stopped = True
            elif line.startswith("X:"):
                if curphrase:
                    curtune.add_phrase(curphrase)
                    curphrase = None
                if curtune:
                    sys.stderr.write("Finished tune %s: %s\n" % (curtune.name, curtune.phrases))
                    if curtune.name is None:
                        curtune.name = curtune.phrases[0].get_code()
                    self.tunes.append(curtune)
                curtune = Tune()
            elif line.startswith("T:"):
                curtune.name = line[2:]
            elif line.startswith("r:"):
                curtune.meter = line[2:]
            elif line.startswith("M:"):
                curtune.time = line[2:]
            elif line.startswith("L:"):
                curtune.unit = line[2:]
            elif line.startswith("R:"):
                parts = line[2:].strip().split(" ")
                curtune.rhythm = []
                for i,item in enumerate(parts):
                    v = item.split(",")
                    if len(v)!=i+1:
                        raise ValueError("Invalid R: %s should have length %s" % (item, i+1))
                    curtune.rhythm.append( item.split(",") )
            elif line.startswith("K:"):
                curkey = line[2:]
                #must be after all other headers so work out bar length here
                curtune.set_bar_length()
            else:
                if curphrase is None:
                    curphrase = Phrase(curkey, curtune.rhythm, "%s %s" % (curtune.name,chr(65+len(curtune.phrases))), curtune.bar_length)
                connector = curphrase.add_lines(line)
                if connector == "||" or connector == "|.":
                    #end of phrase
                    curtune.add_phrase(curphrase)
                    curphrase = None

        if curphrase:
            curtune.add_phrase(curphrase)
            curphrase = None
        if curtune:
            sys.stderr.write("Finished file with tune %s: %s\n" % (curtune.name, curtune.phrases))
            if curtune.name is None:
                curtune.name = curtune.phrases[0].get_code()
            self.tunes.append(curtune)

    def get_tunes(self):
        return self.tunes

    def get_phrases(self):
        p = {}
        for tune in self.tunes:
              for phrase in tune.phrases:
                    c = phrase.get_code()
                    if c in p:
                        p[c].append(phrase)
                    else:
                        p[c] = [phrase]
        return p      


def loadFile(filename):
    data = open(filename, 'r')
    abfile = ABFile(data)
    TUNES.extend(abfile.get_tunes())
    PHRASES.update(abfile.get_phrases())


if __name__=="__main__":
    TUNES = []
    PHRASES = {}

    if len(sys.argv)>1:
        for filename in sys.argv[1:]:
            loadFile(filename)
    else:
        for (path, dirs, files) in os.walk('data'):
            for filename in files:
                loadFile(os.path.join(path,filename))


    print PREAMBLE
    for tune in TUNES:
        z=tune.render_ly()
        print z

    for code,phrases in sorted(PHRASES.items()):
        sys.stderr.write( code+": "+",".join(phrase.name for phrase in phrases)+"\n" )
