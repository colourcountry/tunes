#!/usr/bin/python

import re, os, sys

PAUSE_ON_ERROR = False
CRIB = False

def log_to_stderr(format, *args):
    # Log with prejudice. Attempt to get something printable out of whatever is supplied.
    x = []
    for item in args:
        try:
            x.append( item.decode('utf-8') )
        except UnicodeDecodeError:
            x.append( item.decode('iso-8859-1') )
        except UnicodeEncodeError:
            x.append( item.encode('iso-8859-1').decode('utf-8') )
        except AttributeError:
            x.append( repr(item).decode('iso-8859-1') )
    try:
        sys.stderr.write(format % tuple(i.encode('utf-8') for i in x))
    except TypeError:
        sys.stderr.write(format)
        sys.stderr.write(repr(x))
        
    sys.stderr.write("\n")



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
        try:
            base = c_lass.REGISTER[strg[:4]]
        except KeyError:
            raise NotImplementedError("Key %s" % strg)
        if re.search('[_=^]', strg[4:]):
            raise NotImplementedError("Key with explicit accidentals: %s" % strg)
        return base

Key.REGISTER.update( {
    'eb': Key('ees \major', (), ('b', 'e', 'a')),
    'cm': Key('c \minor', (), ('b', 'e', 'a')),
    'bb': Key('bes \major', (), ('b', 'e')),
    'gm': Key('g \minor', (), ('b', 'e')),
    'f':  Key('f \major', (), ('b')),
    'dm': Key('d \minor', (), ('b')),
    'c':  Key('c \major', (), ()),
    'am': Key('a \minor', (), ()),
    'g':  Key('g \major', ('f'), ()),
    'em': Key('e \minor', ('f'), ()),
    'd':  Key('d \major', ('f', 'c'), ()),
    'bm': Key('b \minor', ('f', 'c'), ()),
    'a':  Key('a \major', ('f', 'c', 'g'), ()),
    'e':  Key('e \major', ('f', 'c', 'g', 'd'), ())
})

Key.REGISTER.update( {
    'amaj': Key.REGISTER['a'],
    'cmaj': Key.REGISTER['c'],
    'dmaj': Key.REGISTER['d'],
    'emaj': Key.REGISTER['e'],
    'fmaj': Key.REGISTER['f'],
    'gmaj': Key.REGISTER['g'],

    'cdor': Key.REGISTER['bb'],
    'ddor': Key.REGISTER['c'],
    'edor': Key.REGISTER['d'],
    'fdor': Key.REGISTER['eb'],
    'gdor': Key.REGISTER['f'],
    'ador': Key.REGISTER['g'],
    'bdor': Key.REGISTER['a'],

    'dmix': Key.REGISTER['g'],
    'emix': Key.REGISTER['a'],
    'fmix': Key.REGISTER['bb'],
    'gmix': Key.REGISTER['c'],
    'amix': Key.REGISTER['d'],
    'bmix': Key.REGISTER['e'],
    'cmix': Key.REGISTER['f'],
})

            

class AbcConnector:

    TYPES = ['','--', ' ', '|', '||', '|]', '[|', '|:', '_', '|_', ':|', '{', '}']
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

        if '!' in strg:
            strg = strg.replace("!","")
            log_to_stderr("%% Ignoring extra ! character (decoration?) in %s",strg)

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
            try:
                (n, d) = strg.split("/")
            except ValueError:
                raise NotImplementedError("multiple slashes in duration %s" % strg)
            try:
                return c_lass(int(n),int(d))
            except ValueError:
                raise NotImplementedError("non-integer duration %s" % strg)
        else:
            try:
                return c_lass(int(strg),1)
            except ValueError:
                raise NotImplementedError("unparseable duration %s" % strg)

class AbcNote:
    # allow ! as a trill
    RE = re.compile("([~!]?)([_=^]*)([A-Za-z])([,']*)([0-9/]?)")

    # AB does not allow redefining letters, nor the extra space charatcter y
    AB_PITCH = re.compile("[A-Ga-gxz]")

    def __init__(self, pitch, oct, acc, dur, trill):
        if not AbcNote.AB_PITCH.match(pitch):
            raise NotImplementedError("unsupported note %s" % pitch)
        self.pitch = pitch
        self.dur = Duration.from_string(dur)
        self.oct = oct or ''
        self.acc = acc or ''
        self.trill = trill or ''


    def __repr__(self):
        return "%s%s%s%s" % (self.trill or '', self.acc or '', self.pitch or '', self.dur)

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


class AbcHeader:
    RE = re.compile("[[](.):([^]]*)[]]")

    AREA = "A"
    BOOK = "B"
    COMPOSER = "C"
    DISCOGRAPHY = "D"
    FILE_URL = "F"
    GROUP = "G"
    HISTORY = "H"
    INSTRUCTION = "I"
    KEY = "K"
    UNIT_NOTE_LENGTH = "L"
    METER = "M"
    MACRO = "m"
    NOTES = "N"
    ORIGIN = "O"
    PARTS = "P"
    TEMPO = "Q"
    RHYTHM = "R"
    REMARK = "r"
    SOURCE = "S"
    SYMBOL_LINE = "s"
    TUNE_TITLE = "T"
    USER_DEFINED = "U"
    VOICE = "V"
    WORDS_AFTER = "W"
    WORDS = "w"
    REFERENCE = "X"
    TRANSCRIPTION = "Z"
    DIRECTIVE = "%"
    DECORATION = "!"
    CHORD = '"'
    PLUS = '+'

    @classmethod
    def from_string(c_lass, strg):
        m = c_lass.RE.split(strg)
        s = []
        for i in range(0,len(m),3):
            s.extend(AbcNote.from_string(m[i]))
            if len(m)>=i+4:
                s.append(c_lass(m[i+1],m[i+2]))
        return s

    def __init__(self, what, value):
        self.what = what
        self.value = value

    def get_clean_value(self):
        if self.value is None:
            return '(unknown)'
        # remove characters which excite lilypond
        strg = re.sub(r"[\\{}]","",self.value)
        try:
            strg = strg.decode('utf-8')
        except UnicodeDecodeError:
            strg = strg.decode('iso-8859-1')
        return strg



class Phrase:
    def __init__(self, name=None, key='c', time='4/4', unit='1/8', rhythm=None):
        # notes = a list of tuples, one per beat.
        self.rhythm = rhythm
        self.key = Key.from_string(key)
        self.name = name or '(no name)'
        self.time = Duration.from_string(time)
        self.unit = Duration.from_string(unit)
        self.notes = []
        #log_to_stderr("New phrase %s",self.name)


    def __repr__(self):
        return "<%s: %s>" % (self.name, ''.join([repr(x) for x in self.notes[:16]]))

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
        
    def extend(self, notes):
        self.notes.extend(notes)

    def append(self, note):
        self.notes.append(note)

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
        prev_item = None

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
                                    try:
                                        cur_bar = [r'\partial %s ' % ticks.mod_nonzero(cur_bar_length).as_ly()] + cur_bar
                                    except TypeError:
                                        raise NotImplementedError("partial yielded unexpected result: %s" % ticks.mod_nonzero(cur_bar_length))
                                    cur_bar_nr = 1
                                else:
                                    cur_bar_length = ticks
                                    cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment()] + cur_bar
                                    cur_bar_nr -= 1 # short bar doesn't count
                            elif cur_bar_nr == 2:
                                cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment()] + cur_bar


                            ticks = Duration()

                            if pause:
                                log_to_stderr("%% Warning, new bar encountered during pause in %s",' '.join(cur_bar))
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
                elif item.what == AbcConnector.TIE:
                    # tie must immediately follow a note, not a barline or other such
                    if isinstance(prev_item, AbcNote):
                        cur_bar.append(item.as_ly())
                    else:
                        raise NotImplementedError("tie from non-note %s" % prev_item)
                else:
                    if not no_repeats:
                        cur_bar.append(item.as_ly())

            prev_item = item

        # allow last bar in phrase to be any length. going to assume it's not also the first bar
        if ticks != cur_bar_length:
            cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % ticks.as_moment()] + cur_bar
            if cur_bar_nr == 1:
                cur_bar = [r'\partial %s ' % ticks.mod_nonzero(cur_bar_length).as_ly()] + cur_bar

        tune_ly += ' '.join(cur_bar)

        leftover_duration = ticks % self.time

        return (tune_ly, leftover_duration)


class Tune:
    OK = 0
    FATAL = 1
    DIRECTIVE_IGNORED = 2
    HEADER_IGNORED = 4
    DECORATION_IGNORED = 8
    CHORD_IGNORED = 16
    PLUS_IGNORED = 32

    def __init__(self):

        self.status = Tune.OK
        self.phrases = {}
        self.fields = {}
        self.name = '(no name)'
        self.ref = None

    def get_header(self, key, idx=0):
        if key not in self.fields:
            return ''

        return self.fields[key][idx]

    def set_ref(self, item):
        self.ref = item.get_clean_value()

    def set_name(self, item):
        self.name = item.get_clean_value()

    def add_header(self, item):
        if item.what not in self.fields:
            self.fields[item.what] = []
        self.fields[item.what].append(item.get_clean_value())

    def render_ly(self, phrase_separator=None, end=None, bar_limit=None, page_break=True, no_repeats=False):

        if not phrase_separator:
            phrase_separator = '''    \\set Score.repeatCommands = #\'((volta #f)) \\break \\bar "" \\mark "%s"\n'''

        if not end:
            end = '    \\set Score.repeatCommands = #\'((volta #f)) \\bar "|." \\break'

        s = r'''
\score{{
\transpose d d' {
'''

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
''' % (self.name.replace('"',"'").encode('utf-8'), '', self.get_header('meter').replace('"',"'").encode('utf-8'))

        if page_break:
            s += '\\pageBreak\n'

        return s

    @classmethod
    def from_string(c_lass, ab, strictness=None):
        '''Parse an inlined AB with inlined headers into a Tune object.'''

        # normalize space
        ab = re.sub(r'[\r\n\t ]+', ' ', ab.strip())

        # Obtain a stream of AbcHeader|AbcNote|AbcConnector objects.
        try:
            stream = AbcHeader.from_string(ab)
        except NotImplementedError, e:
            ref = re.match("^[[](X:[^]]*)[]]",ab)
            if ref:
                log_to_stderr("%% Unknown item in tune %s: %s" ,ref.group(1), e)
            else:
                log_to_stderr("%% Unknown item in tune also missing id: ", e)
            # this is automatically fatal
            return None

        if strictness is None:
            strictness = Tune.FATAL #| Tune.DIRECTIVE_IGNORED

        in_header = True
        tune = c_lass()
        tune.src = ab

        cur_key = 'C'
        cur_time = '4/4'
        cur_unit = '1/8'
        cur_phrase_id = 'A'
        cur_phrase = None

        for item in stream:
            try:
                if isinstance(item, AbcHeader):
                    # log_to_stderr("% Finished tune %s: %s\n",finished.name, finished.phrases)
                    if item.what == AbcHeader.REFERENCE:
                        tune.set_ref( item )
                    elif item.what == AbcHeader.TUNE_TITLE:
                        tune.set_name( item )
                    elif item.what == AbcHeader.METER:
                        value = item.value.lower()
                        if value == 'c':
                            value = '4/4'
                        elif value == 'c|':
                            value = '2/2'
                        cur_time = value
                    elif item.what == AbcHeader.PARTS:
                        if in_header:
                            tune.add_header( item )
                        else:
                            cur_phrase = None
                            cur_phrase_id = item.value
                    elif item.what ==  AbcHeader.UNIT_NOTE_LENGTH:
                        parts = item.value.split(" ")
                        cur_unit = parts[0]
                        #rhythm = []
                        #if len(parts)>1:
                        #    for i,item in enumerate(parts[1:]):
                        #        v = item.split(",")
                        #        if len(v)!=i+1:
                        #            raise ValueError("Invalid L: %s should have length %s" % (item, i+1))
                        #        rhythm.append( item.split(",") )
                        #curtune.set_rhythm( rhythm )
                    elif item.what ==  AbcHeader.KEY:
                        cur_key = item.value
                        in_header = False
                    elif item.what ==  AbcHeader.DIRECTIVE:
                        tune.status |= Tune.DIRECTIVE_IGNORED
                        if strictness & Tune.DIRECTIVE_IGNORED:
                            log_to_stderr("%% Unsupported directive in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored directive in tune %s: '%s'",tune.ref,item.value)
                    elif item.what ==  AbcHeader.CHORD:
                        tune.status |= Tune.CHORD_IGNORED
                        if strictness & Tune.CHORD_IGNORED:
                            log_to_stderr("%% Unsupported chord in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored chord in tune %s: '%s'",tune.ref,item.value)
                    elif item.what ==  AbcHeader.DECORATION:
                        tune.status |= Tune.DECORATION_IGNORED
                        if strictness & Tune.DECORATION_IGNORED:
                            log_to_stderr("%% Unsupported decoration in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored decoration in tune %s: '%s'",tune.ref,item.value)
                    elif item.what ==  AbcHeader.PLUS:
                        tune.status |= Tune.PLUS_IGNORED
                        if strictness & Tune.PLUS_IGNORED:
                            log_to_stderr("%% Unsupported plus (may be chord or decoration) in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored plus (may be chord or decoration) in tune %s: '%s'",tune.ref,item.value)
                    else:
                        tune.add_header(item)
                else:
                    if not cur_phrase:
                        cur_phrase = Phrase("%s %s" % (tune.name, cur_phrase_id),
                                            cur_key, cur_time, cur_unit)
                        if cur_phrase_id not in tune.phrases:
                            tune.phrases[cur_phrase_id] = []
                        tune.phrases[cur_phrase_id].append(cur_phrase)
                    cur_phrase.append(item)
            except NotImplementedError, e:
                log_to_stderr("%% Unknown item in tune X:%s: %s",tune.ref, e)
                tune.status |= Tune.FATAL

        if tune.status & strictness:
            return None
        else:
            return tune


class ABCollection:
    def __init__(self, include_duplicates=False):
        self.tunes = []
        self.tune_check = {}
        self.include_duplicates = include_duplicates

    def add_file(self, file):
        count = 0
        original_abc = None
        abc = ""
        finished_ab = None
        ab = ""
        x_line = "" # only used when reporting a duplicate
        pause = False
        for line in data.readlines()+["X::"]:
            if line.startswith("X:") or line.startswith("[X:"):
                if pause and PAUSE_ON_ERROR:
                    pause = raw_input("continue?")
                    if "yes".startswith(pause):
                        pause = False
                    else:
                        raise SystemExit
                finished_ab = ab
                original_abc = abc
                if line.startswith("X:"):
                    ab = "["+line.replace("]",r"\u005d").replace("[",r"\u005b").strip()+"]"
                else:
                    ab = line
                abc = line
                x_line = line
            else:
                abc += line

                if line.startswith("%"):
                    ab += "[%:"+line.strip()+"]"
                elif re.match("[A-Za-z]:", line):
                    ab += "["+line.replace("]",")").replace("[","(").strip()+"]"
                else:
                    # music line
                    # replace decorations with inline decoration header
                    line = re.sub('[!]([^!]*)[!]', r'[!:\1]', line)
                    # chords
                    line = re.sub('["]([^"]*)["]', r'[":\1]', line)
                    # old style chords/decorations, can't tell which but don't support either
                    # (do this last as + is legal within chords and decorations)
                    line = re.sub('[+]([^+]*)[+]', r'[+:\1]', line)

                    ab += line

            if finished_ab:
                # remove score line breaks
                finished_ab = re.sub('[!+][\r\n]+|$', '', finished_ab)
                finished_ab = re.sub('^|[\r\n][!+]', '', finished_ab)

                # normalize space
                finished_ab = re.sub(r'[\r\n\t ]+', ' ', finished_ab.strip())

                # use entire tune after X: as its own id
                check_id = re.sub("^[[]X:[^]]*[]]","",finished_ab)

                if check_id in self.tune_check:
                    log_to_stderr("%% Skipped %s as exactly duplicated %s", x_line.strip(), self.tune_check[check_id])
                else:
                    tune = Tune.from_string(finished_ab)

                    if tune:
                        self.tune_check[check_id] = tune.ref
                        self.tunes.append(tune)
                        count += 1
                    else:
                        self.tune_check[check_id] = x_line.strip()
                        sys.stderr.write("%% Couldn't process the following tune:\n%s\n")
                        sys.stderr.write(original_abc)
                        pause = True

                finished_ab = None
                original_abc = None
        return count


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







if __name__=="__main__":

    PHRASES = {}

    TUNES = ABCollection()

    if len(sys.argv)>1:
        for filename in sys.argv[1:]:
            loadFile(filename)
    else:
        for (path, dirs, files) in os.walk('data'):
            for filename in files:
                data = open(os.path.join(path,filename), 'r')
                count = TUNES.add_file(data)
                log_to_stderr("%% Finished %s , found %s tunes.\n\n",filename, count)
    #PHRASES.update(abfile.get_phrases())


    if CRIB:
        PREAMBLE = open("preamble.crib.ly.fragment","r").read()
    else:
        PREAMBLE = open("preamble.ly.fragment","r").read()

    print PREAMBLE
    for tune in TUNES.tunes:
            try:
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
            except NotImplementedError, e:
                log_to_stderr("%% Couldn't render %s: %s\n",tune.name or '(unknown)', e)
            

    #for code,phrases in sorted(PHRASES.items()):
    #    log_to_stderr( code+": "+",".join(phrase.name for phrase in phrases)+"\n" )
