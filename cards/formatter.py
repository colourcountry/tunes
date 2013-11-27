#!/usr/bin/python

import re, os, sys

class Key:
    # Register keys using the first 4 characters of their ABC definition, lowercased.
    # Note that 'mi' will come out as mixolydian not minor, but it's illegal ABC anyway.
    REGISTER = {}

    def __init__(self, ly, sharps, flats):
        self.acc = {}
        self.ly = ly
        for letter in sharps:
            self.acc[letter] = +1
        for letter in flats:
            self.acc[letter] = -1

    def __getitem__(self, letter):
        return self.acc[letter]
        
    def as_ly(self):
        return self.ly

    @classmethod
    def from_string(c_lass, strg):
        strg = re.sub('[^a-z#_=^]','',strg.lower())
        base = c_lass.REGISTER[strg[:4]]
        if re.search('[_=^]', strg[4:]):
            raise NotImplementedError("keys with random accidentals")
        return base

Key.REGISTER.update( {
    'bb': Key('bes \major', (), ('b', 'e')),
    'f':  Key('f \major', (), ('b')),
    'dm': Key('d \minor', (), ('b')),
    'c':  Key('c \major', (), ()),
    'am': Key('a \minor', (), ()),
    'g':  Key('g \major', ('f'), ()),
    'em': Key('e \minor', ('f'), ()),
    'd':  Key('d \major', ('f', 'c'), ()),
    'bm': Key('b \minor', ('f', 'c'), ()),
    'a':  Key('a \major', ('f', 'c', 'g'), ())
})

Key.REGISTER.update( {
    'cdor': Key.REGISTER['bb']
})

            

class AbcConnector:

    TYPES = ['','--', ' ', '|', '||', '|]', '[|', '|:', '_', '|_', ':|']
    BEAM = 0
    TIE = 1
    BREAK = 2
    BAR = 3
    DOUBLE_BAR = 4
    END_BAR = 5
    REVERSE_END_BAR = 6
    BEGIN_REPEAT = 7
    BEGIN_ALTERNATIVE = 8
    BEGIN_ALTERNATIVE_AT_BAR = 9
    END_REPEAT = 10
    BEGIN_GRACE = 11
    END_GRACE = 12

    def __init__(self, what, newline=False, alts=None):
        self.what = what
        self.newline = newline
        if alts:
            self.alts = tuple(alts)
        else:
            self.alts = ()

    def __repr__(self):
        return '%s%s' % (AbcConnector.TYPES[self.what], ','.join(self.alts))


    def is_phrase_over(self):
        if self.newline:
            return True
        elif self.what == AbcConnector.DOUBLE_BAR:
            return True
        elif self.what == AbcConnector.END_REPEAT and not self.alts:
            return True
        elif self.what == AbcConnector.END_BAR:
            return True
        return False

    def is_bar_line(self):
        if self.what == AbcConnector.BAR:
            return True
        elif self.what == AbcConnector.DOUBLE_BAR:
            return True
        elif self.what == AbcConnector.END_BAR:
            return True
        elif self.what == AbcConnector.REVERSE_END_BAR:
            return True
        elif self.what == AbcConnector.END_REPEAT:
            return True
        elif self.what == AbcConnector.BEGIN_REPEAT:
            return True
        elif self.what == AbcConnector.BEGIN_ALTERNATIVE_AT_BAR:
            return True
        return False

    def as_ly(self):
        if self.what == AbcConnector.BEAM:
            return ' '
        elif self.what == AbcConnector.TIE:
            return ' ~ '
        elif self.what == AbcConnector.BREAK:
            return ' '
        elif self.what == AbcConnector.BAR:
            return ' | '
        elif self.what == AbcConnector.DOUBLE_BAR:
            return ' \\bar "||" \\set Score.repeatCommands = #\'((volta #f)) '
        elif self.what == AbcConnector.END_BAR:
            return ' \\bar "|." \\set Score.repeatCommands = #\'((volta #f)) '
        elif self.what == AbcConnector.REVERSE_END_BAR:
            return ' \\bar ".|" '
        elif self.what == AbcConnector.BEGIN_REPEAT:
            return ' \\set Score.repeatCommands = #\'(start-repeat) '
        elif self.what == AbcConnector.END_REPEAT:
            if self.alts:
                return ' \\set Score.repeatCommands = #\'((volta #f) end-repeat (volta "%s.")) ' % '., '.join(self.alts)
            else:
                return ' \\set Score.repeatCommands = #\'((volta #f) end-repeat) '
        elif self.what == AbcConnector.BEGIN_ALTERNATIVE:
            return ' \\set Score.repeatCommands = #\'((volta "%s.")) ' % '., '.join(self.alts)
        elif self.what == AbcConnector.BEGIN_ALTERNATIVE_AT_BAR:
            return ' | \\set Score.repeatCommands = #\'((volta "%s.")) ' % '., '.join(self.alts)
        else:
            raise NotImplementedError("Bar type %s needs help to be lilyfied" % self.what)

    @classmethod
    def from_string(c_lass, strg):
        s = strg.strip().replace('\\\n','')
        if '\n' in strg:
            newline = True
        else:
            newline = False

        if '"' in strg:
            raise NotImplementedError('" character (chord) in %s' % strg)

        if '!' in strg:
            raise NotImplementedError('! character (decoration) in %s' % strg)

        if s.endswith('{'):
            return c_lass.from_string(s[:-1]) + [c_lass(c_lass.BEGIN_GRACE,newline)]
        elif s.startswith('}'):
            return [c_lass(c_lass.END_GRACE,newline)] + c_lass.from_string(s[1:])

        elif s=='-':
            return [c_lass(c_lass.TIE,newline)]
        elif s=='|':
            return [c_lass(c_lass.BAR,newline)]
        elif s=='||':
            return [c_lass(c_lass.DOUBLE_BAR,newline)]
        elif s=='|]':
            return [c_lass(c_lass.END_BAR,newline)]
        elif s=='[|':
            return [c_lass(c_lass.REVERSE_END_BAR,newline)]
        elif s=='|:':
            return [c_lass(c_lass.BEGIN_REPEAT,newline)]
        elif s.startswith(':|'):
            m = re.match(':[|][ ]*[[]?([0-9,]+)', s)
            if not m:
                return [c_lass(c_lass.END_REPEAT,newline)]
            alts = m.group(1).split(',')
            return [c_lass(c_lass.END_REPEAT,newline,alts)]
        elif s.startswith('|'):
            m = re.match('[|][ ]*[[]?([0-9,]+)', s)
            if not m:
                return [c_lass(c_lass.BEGIN_ALTERNATIVE_AT_BAR,newline)]
            alts = m.group(1).split(',')
            return [c_lass(c_lass.BEGIN_ALTERNATIVE_AT_BAR,newline,alts)]
        elif s.startswith('['):
            m = re.match('[[]([0-9,]+)', s)
            if not m:
                return [c_lass(c_lass.BEGIN_ALTERNATIVE,newline)]
            alts = m.group(1).split(',')
            return [c_lass(c_lass.BEGIN_ALTERNATIVE,newline,alts)]
        elif s==strg:
            return [c_lass(c_lass.BEAM,newline)]
        else:
            return [c_lass(c_lass.BREAK,newline)]

class Duration:
    def __init__(self, n=0, d=1):
        self.n = n
        self.d = d

    def lower(self):
        for prime in [2,3,5,7,11]: # that's enough primes --ed.
            while (self.n % prime == 0) and (self.d % prime == 0):
                self.n = self.n // prime
                self.d = self.d // prime
        return self

    def __add__(self, other):
        new = self.__class__( (self.n * other.d) + (other.n * self.d), self.d * other.d )
        new.lower()
        return new

    def __sub__(self, other):
        new = self.__class__( (self.n * other.d) - (other.n * self.d), self.d * other.d )
        new.lower()
        return new

    def __mul__(self, other):
        new = self.__class__( self.n * other.n, self.d * other.d )
        new.lower()
        return new

    def __mod__(self, other):
        new = self.__class__( (self.n * other.d) % (other.n * self.d), self.d * other.d )
        new.lower()
        return new

    def mod_nonzero(self, other):
        new = self % other
        if new.n == 0: new.n = new.d
        return new

    def __lt__(self, other):
        return (self.n * other.d) < (other.n * self.d)

    def __eq__(self, other):
        ns = self.__class__(self.n, self.d).lower()
        no = self.__class__(other.n, other.d).lower()
        return (ns.n == no.n and ns.d == no.d)

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return (self < other or self == other)

    def __repr__(self):
        if self.d == 1:
            return "%s" % self.n
        else:
            return "%s/%s" % (self.n, self.d)

    def as_ly(self, unit=None):
        if unit is None:
            unit = Duration(1,1)
        dur = self * unit
        dur.lower()

        if dur.n == 1:
            return str(dur.d)
        elif dur.n == 3 and (dur.d % 2 == 0):
            return str(dur.d // 2)+'.'
        elif dur.n == 7 and (dur.d % 4 == 0):
            return str(dur.d // 4)+'..'
        elif dur.n == 15 and (dur.d % 8 == 0):
            return str(dur.d // 8), '...'
        else:
            raise NotImplementedError("note of length %s/%s" % (dur.n, dur.d))

    def as_moment(self):
        return '%s/%s' % (self.n, self.d)

    @classmethod
    def from_string(c_lass,strg):
        if not strg:
            return c_lass(1,1)
        elif re.match("/+$",strg):
            return c_lass(1,2**len(strg))
        elif "/" in strg:
            (n, d) = strg.split("/")
            return c_lass(int(n),int(d))
        else:
            return c_lass(int(strg),1)

class AbcNote:
    RE = re.compile("([~]?)([_=^]*)([A-Ga-gxyz])([,']*)([0-9/]?)")

    def __init__(self, pitch, oct, acc, dur, trill):
        self.pitch = pitch
        self.dur = Duration.from_string(dur)
        self.oct = oct or ''
        self.acc = acc or ''
        self.trill = trill or ''


    def __repr__(self):
        return "%s%s%s%s" % (self.trill or '_', self.acc or '_', self.pitch or '_', self.dur)

    def as_ly(self, key, unit):
        octave = 0

        if self.pitch=="z":
            note="r"
        elif self.pitch=="x":
            note="s"
        elif self.pitch in "abcdefg":
            note = self.pitch.lower()
            octave += 1
        else:
            note = self.pitch.lower()

        acc = 0
        nat = False
        for o in self.acc:
            if o=="_": acc -= 1
            elif o=="^": acc += 1
            elif o=="=": nat = True
        for o in self.oct:
            if o==",": octave -= 1
            elif o=="'": octave += 1
        if octave > 0: octave = "'"*octave
        elif octave < 0: octave = ","*-octave
        else: octave = ""

        if acc == 0 and not nat:
            try:
                acc = key[note]
            except KeyError:
                pass

        if acc > 0: acc = "is"*acc
        elif acc < 0: acc = "es"*-acc
        else: acc = ""

        x = self.dur * unit
        length = (self.dur * unit).as_ly()

        return ' '+note+acc+octave+length+' '



    @classmethod
    def from_string(c_lass, strg):
        m = c_lass.RE.split(strg)
        s = []
        for i in range(0,len(m),6):
            s.extend(AbcConnector.from_string(m[i]))
            if len(m)>=i+4:
                s.append(c_lass(m[i+3],m[i+4],m[i+2],m[i+5],m[i+1]))
        return s

        

class Phrase:
    def __init__(self, key, rhythm=None, name=None, time='4/4', unit='1/8', notes=[]):
        # notes = a list of tuples, one per beat.
        self.rhythm = rhythm
        self.key = key
        self.name = name
        self.time = Duration.from_string(time)
        self.unit = Duration.from_string(unit)
        self.notes = []
        sys.stderr.write("New phrase %s\n" % self.name)
        self.add_notes(notes)


    def __repr__(self):
        return "<phrase %s %s>" % (self.name, self.notes[:8])

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
        
    def add_notes(self, notes):
        self.notes.extend(notes)

    def get_code(self):
        def transpose(n,key=self.key):
            if n=="x": return "x"
            elif n=="z": return "x"
            return str( ( ord(n.lower()) - ord(key.lower()[0]) ) %7 +1 )

        notes = []
        ticks = Duration()
        bar_length = self.time 

        if not self.notes:
            return "(empty)"

        return "(code)" #TODO

        for beat in self.notes[0]:
            connector = beat[-1]
            for note in beat[:-1]:
                m = re.match(ABC_NOTE, note)
                if m:
                    if re.match("/+$",m.group(4)):
                        n = 1
                        d = 2**len(m.group(4))
                    elif "/" in m.group(4):
                        (n, d) = m.group(4).split("/")
                        n = int(n)
                        d = int(d)
                    else:
                        n = int(m.group(4))
                        d = 1

                    length = 1.0*n/d
                    ticks += length
                    notes.append(beat[0])

            if connector=="|":
                if ticks < self.time:
                    # skip anacrusis
                    notes = []

        return (''.join(transpose(note[0]) for note in notes)).ljust(8,"0")

    def render_ly(self, key=None, partial=None, bar_limit=None, no_repeats=False):

        if key == self.key:
            ly = ''
        else:
            ly = '\key %s\n' % self.key.as_ly()

        ticks = Duration()
        if not partial:
            partial = Duration()    

        tune_ly = ''
        cur_bar = []
        cur_bar_length = self.time
        cur_bar_nr = 1

        pause = False
        new_bar = None
        last_note_index = 0

        for i, item in enumerate(self.notes):
            if isinstance(item, AbcNote):

                if pause:
                    # time is suspended so just add the note
                    pass
                else:
                    if new_bar:
                        if ticks.n != 0:
                            cur_bar_nr += 1                            

                            if ticks != cur_bar_length:
                                if cur_bar_nr == 2:
                                    # add invisible bar line to suppress line before anacrusis
                                    cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment(), r'\bar ""'] + cur_bar
                                    cur_bar = [r'\partial %s ' % ticks.mod_nonzero(cur_bar_length).as_ly()] + cur_bar
                                    cur_bar_nr = 1
                                else:
                                    cur_bar_length = ticks
                                    cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment()] + cur_bar
                                    cur_bar_nr -= 1 # short bar doesn't count
                            elif cur_bar_nr == 2:
                                cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment()] + cur_bar


                            ticks = Duration()

                            if pause:
                                sys.stderr.write("Warning, new bar encountered during pause in %s\n" % ' '.join(cur_bar))
                                tune_ly += "%s \n" % (' '.join(cur_bar) )
                            else:
                                tune_ly += "%s %s \n" % (' '.join(cur_bar), new_bar)

                            cur_bar = []

                        if bar_limit and cur_bar_nr >= bar_limit:
                            break

                        new_bar = None

                    ticks += item.dur * self.unit
                    if self.time <= ticks:
                        new_bar = '|'

                last_note_index = len(cur_bar)
                cur_bar.append( item.as_ly(self.key, self.unit) )

            elif isinstance(item, AbcConnector):
                if item.is_bar_line() :
                    if no_repeats:
                        new_bar = "|"
                    else:
                        new_bar = item.as_ly()
                    if pause:
                        # grace notes can't span a bar line
                        cur_bar.append('}')
                        pause = False


                if item.what == AbcConnector.BEGIN_GRACE:
                    pause = True # grace notes take up no time
                    if tune_ly == '' and len(cur_bar)==0:
                        cur_bar.append(r'\grace {')
                    else:
                        cur_bar.insert(last_note_index, r'\afterGrace')
                        cur_bar.append(r'{')
                elif item.what == AbcConnector.END_GRACE:
                    cur_bar.append('}')
                    pause = False
                else:
                    if not no_repeats:
                        cur_bar.append(item.as_ly())


        # allow last bar in phrase to be any length. going to assume it's not also the first bar
        if ticks != cur_bar_length:
            cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % ticks.as_moment()] + cur_bar
            if cur_bar_nr == 1:
                cur_bar = [r'\partial %s ' % ticks.mod_nonzero(cur_bar_length).as_ly()] + cur_bar

        tune_ly += ' '.join(cur_bar)

        leftover_duration = ticks % self.time

        return (tune_ly, leftover_duration)


class Tune:
    def __init__(self, phrases=None, name=None, meter=''):
        if phrases is None:
            self.phrases = {}
        else:
            self.phrases = phrases

        self.set_name(name)
        self.set_meter(meter)

        # These may change as the tune is created
        # so refer to the state at the end.
        # Phrases have a single value throughout
        self.unit = '1/8'
        self.set_time('4/4')
        self.set_key('C')
        self.set_phrase('A')
        self.set_rhythm('')

    def set_time(self,time):
        self.time = time

    def set_unit(self,unit):
        self.unit = unit

    def set_key(self,key):
        self.key = key

    def set_phrase(self,phrase):
        self.phrase = phrase

    def set_rhythm(self,rhythm):
        self.rhythm = rhythm

    def set_name(self,name):
        self.name = name

    def set_meter(self,meter):
        self.meter = meter

    def add_notes(self,notes):
        sys.stderr.write( 'Adding %s notes to phrase %s\n' % (len(notes),self.phrase) )
        new_phrase = Phrase(Key.from_string(self.key),
                            self.rhythm,
                            "%s %s" % (self.name, self.phrase),
                            self.time, self.unit, notes)
        # The same phrase should not be defined twice. If it is, the notes get appended
        if self.phrase not in self.phrases:
            self.phrases[self.phrase]=[]
        self.phrases[self.phrase].append(new_phrase)

    def render_ly(self, phrase_separator=None, end=None, bar_limit=None, page_break=True, no_repeats=False):

        if not phrase_separator:
            phrase_separator = '''    \\set Score.repeatCommands = #\'((volta #f)) \\break \\bar "" \\mark "%s"\n'''

        if not end:
            end = '    \\set Score.repeatCommands = #\'((volta #f)) \\bar "|." \\break'

        s = r'''
\score{{
\transpose d d' {
\time %s
''' % self.time

        key = None
        continuation = False

        for id,phrase_list in self.phrases.items():

            if continuation:
                if "%s" in phrase_separator:
                    assert '"' not in id
                    s += phrase_separator % id
                else:
                    s += phrase_separator

            for phrase in phrase_list:
                phrase_ly, leftover_duration = phrase.render_ly(key, None, bar_limit, no_repeats)
                s += phrase_ly
                key = phrase.key
                continuation = True

        s += end + r'''
}}
\header{
    piece = "%s"
    opus = "%s"
    meter = "%s"
}}
''' % (self.name, '', self.meter)

        if page_break:
            s += '\\pageBreak\n'

        return s

class ABFile:
    def __init__(self, data):
        curtune = None
        curphrase = None
        curkey = None
        self.tunes = []
        stopped = False
        header = False
        finished = None
        abc = ""
        for line in data.readlines()+["X::"]:
            if line.startswith("%%"):
                pass
            elif line.startswith("X:"):
                header = True
                finished = curtune
                curtune = Tune()
            elif line.startswith("T:"):
                curtune.set_name( line[2:].strip() )
            elif line.startswith("r:"):
                curtune.set_meter( line[2:].strip() )
            elif line.startswith("M:"):
                curtune.set_time( line[2:].strip() )
            elif line.startswith("P:"):
                if header:
                    curtune.set_meter( line[2:].strip() )
                else:
                    if abc:
                        curtune.add_notes(AbcNote.from_string(abc))
                    curtune.set_phrase( line[2:].strip() )
                    abc=""
            elif line.startswith("L:"):
                parts = line[2:].strip().split(" ")
                curtune.set_unit( parts[0] )
                rhythm = []
                if len(parts)>1:
                    for i,item in enumerate(parts[1:]):
                        v = item.split(",")
                        if len(v)!=i+1:
                            raise ValueError("Invalid L: %s should have length %s" % (item, i+1))
                        rhythm.append( item.split(",") )
                curtune.set_rhythm( rhythm )
            elif line.startswith("K:"):
                curtune.set_key( line[2:].strip() )
                header = False
            elif header:
                sys.stderr.write("Found unknown header line %s\n" % line)
            else:
                abc += line

            if finished:

                # remove score line breaks
                abc = re.sub('[!+]\n|$', '', abc)
                abc = re.sub('^|\n[!+]', '', abc)
                # remove decorations
                abc = re.sub('[!][^!]+[!]', '', abc)
                # remove chords
                abc = re.sub('["][^"]+["]', '', abc)
                # remove old style decorations (do this last as + is legal within chords and decorations)
                abc = re.sub('[+][^+]+[+]', '', abc)

                finished.add_notes(AbcNote.from_string(abc))
                sys.stderr.write("Finished tune %s: %s\n" % (finished.name, finished.phrases))
                if finished.name is None:
                    finished.name = '?'#finished.phrases[0].get_code()
                self.tunes.append(finished)
                finished = None
                abc = ""

    def get_tunes(self):
        return self.tunes

    def get_phrases(self):
        p = {}
        for tune in self.tunes:
              for phrase_list in tune.phrases.values():
                    for phrase in phrase_list:
                        c = phrase.get_code()
                        if c in p:
                            p[c].append(phrase)
                        else:
                            p[c] = [phrase]
        return p      


def loadFile(filename):
    data = open(filename, 'r')
    abfile = ABFile(data)
    tunes = abfile.get_tunes()
    sys.stderr.write("Found %s tunes in %s\n" % (len(tunes), filename))
    TUNES.extend(tunes)
    #PHRASES.update(abfile.get_phrases())





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


    CRIB = True

    if CRIB:
        PREAMBLE = open("preamble.crib.ly.fragment","r").read()
    else:
        PREAMBLE = open("preamble.ly.fragment","r").read()

    print PREAMBLE
    for tune in TUNES:
        if CRIB:
            z=tune.render_ly(\
                phrase_separator=r'''    \set Score.repeatCommands = #'((volta #f)) 
\bar ":" \stopStaff 
\set Timing.measureLength = #(ly:make-moment 1/4) s4
\startStaff
''',
                end='    \\set Score.repeatCommands = #\'((volta #f)) \\bar ":"',
                bar_limit=3,
                page_break=False,
                no_repeats=True
            )
        else:
            z=tune.render_ly()
        print z

    #for code,phrases in sorted(PHRASES.items()):
    #    sys.stderr.write( code+": "+",".join(phrase.name for phrase in phrases)+"\n" )
