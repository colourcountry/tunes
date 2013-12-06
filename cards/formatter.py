#!/usr/bin/python

import re, os, sys

PAUSE_ON_ERROR = False
REMOVE_KEY_SIGNATURES = True
CRIB = False
LIMIT = None
BUCKET_SIZE = 500

def log_to_stderr(format, *args):
    # Log with prejudice. Attempt to get something printable out of whatever is supplied.
    x = []
    for item in args:
        try:
            x.append( item.decode('utf-8') )
        except UnicodeDecodeError:
            x.append( item.decode('iso-8859-1') )
        except UnicodeEncodeError:
            x.append( re.sub('[^ -~]','',item).decode('ascii') )
        except AttributeError:
            x.append( repr(item).decode('iso-8859-1') )
    try:
        sys.stderr.write(format % tuple(i.encode('utf-8') for i in x))
    except TypeError:
        sys.stderr.write(repr(format))
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

    def __repr__(self):
        return u'<key '+repr(self.acc)+'>'

    def __getitem__(self, letter):
        return self.acc[letter]
        
    def as_ly(self):
        return self.ly

    def as_ab(self):
        s = ""
        for pitch, value in sorted(self.acc.items()):
            if value > 0:
                s += " "+pitch + ('^'*value)
            else:
                s += " "+pitch + ('_'*-value)
        return "C exp"+s

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

    TYPES = [r'\n','--', ' ', '|', '||', '|]', '[|', '|:', '_', '|_', ':|', '{', '}', '(', ')', '[', ']', '(', '>', '<', '::']
    NEW_LINE = 0
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
    BEGIN_SLUR = 13
    END_SLUR = 14
    BEGIN_CHORD = 15
    END_CHORD = 16
    TUPLET = 17
    SWING = 18
    SNAP = 19
    DOUBLE_REPEAT = 20

    def __init__(self, what, value=None):
        self.what = what
        self.value = value

    def __repr__(self):
        if self.value is None:
            return '`%s`' % AbcConnector.TYPES[self.what]
        else:
            return '`%s,%s`' % (AbcConnector.TYPES[self.what], repr(self.value))

    def as_ab(self):
        if self.value is None:
            return AbcConnector.TYPES[self.what]
        elif self.what == AbcConnector.BEGIN_ALTERNATIVE:
            return '%s%s' % (AbcConnector.TYPES[self.what], ','.join(self.value))
        elif self.what == AbcConnector.END_REPEAT:
            return '%s%s' % (AbcConnector.TYPES[self.what], ','.join(self.value))
        elif self.what == AbcConnector.TUPLET:
            if self.value[0]==self.value[2]:
                value = ':'.join(str(x) for x in self.value[:2])
                if value=='3:2':
                    value = '3'
                if value=='2:3':
                    value = '2'
            else:
                value = ':'.join(str(x) for x in self.value)
            return '%s%s' % (AbcConnector.TYPES[self.what], value)



    def is_phrase_over(self):
        if self.what == AbcConnector.NEW_LINE:
            return True
        elif self.what == AbcConnector.DOUBLE_BAR:
            return True
        elif self.what == AbcConnector.END_REPEAT and not self.value:
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

        # these are not really bar lines but they still reset the clock timer
        # so we can hack lilypond to do what we want
        elif self.what == AbcConnector.END_REPEAT:
            return True
        elif self.what == AbcConnector.BEGIN_REPEAT:
            return True
        elif self.what == AbcConnector.DOUBLE_REPEAT:
            return True
        return False

    def allow_short_bar(self):
        # if the space between BAR connectors contains one of these,
        # do not enforce bar length
        if self.what == AbcConnector.END_REPEAT:
            return True
        elif self.what == AbcConnector.BEGIN_REPEAT:
            return True
        elif self.what == AbcConnector.DOUBLE_REPEAT:
            return True
        elif self.what == AbcConnector.DOUBLE_BAR:
            return True
        elif self.what == AbcConnector.END_BAR:
            return True
        return False


    def as_ly(self):
        if self.what == AbcConnector.TIE:
            result = ' ~ '
        elif self.what == AbcConnector.BREAK:
            result = ' '
        elif self.what == AbcConnector.BAR:
            result = '' # bar check is dealt with elsewhere
        elif self.what == AbcConnector.SWING:
            result = '' # already had effect in 'rhythmify'
        elif self.what == AbcConnector.SNAP:
            result = '' # already had effect in 'rhythmify'
        elif self.what == AbcConnector.TUPLET:
            result = ' \\times %s/%s { ' % (self.value[1], self.value[0]) # phrase is responsible for closing this bracket
        elif self.what == AbcConnector.DOUBLE_BAR:
            result = ' \\bar "||" \\set Score.repeatCommands = #\'((volta #f)) '
        elif self.what == AbcConnector.END_BAR:
            result = ' \\bar "|." \\set Score.repeatCommands = #\'((volta #f)) '
        elif self.what == AbcConnector.REVERSE_END_BAR:
            result = ' \\bar ".|" '
        elif self.what == AbcConnector.BEGIN_REPEAT:
            result = ' \\set Score.repeatCommands = #\'(start-repeat) '
        elif self.what == AbcConnector.DOUBLE_REPEAT:
            # FIXME; this doesn't work
            result = ' \\set Score.repeatCommands = #\'((volta #f) end-repeat) \\set Score.repeatCommands = #\'(start-repeat) '
        elif self.what == AbcConnector.END_REPEAT:
            if self.value:
                result = ' \\set Score.repeatCommands = #\'((volta #f) end-repeat (volta "%s.")) ' % '., '.join(self.value)
            else:
                result = ' \\set Score.repeatCommands = #\'((volta #f) end-repeat) '
        elif self.what == AbcConnector.BEGIN_ALTERNATIVE:
            result = ' \\set Score.repeatCommands = #\'((volta "%s.")) ' % '., '.join(self.value)
        else:
            raise NotImplementedError("Bar type %s needs help to be lilyfied" % self.what)

        if self.is_phrase_over():
            result += ' \\break '
        return result

    @classmethod
    def from_string(c_lass, s):
        if not s:
            return []

        skip = 1
        if s.startswith('{'):
            result = [c_lass(c_lass.BEGIN_GRACE)]
        elif s.startswith('}'):
            result = [c_lass(c_lass.END_GRACE)]
        elif s.startswith('>'):
            result = [c_lass(c_lass.SWING)]
        elif s.startswith('<'):
            result = [c_lass(c_lass.SNAP)]
        elif s.startswith('('):
            m = re.match('[(]([0-9:]+)(.*)', s)
            if m:
                value = (m.group(1).split(':') + ['',''])[:3]
                if value[1]=='':
                    if int(value[0]) in (2,4,8):
                        value = [value[0], 3, value[2]]
                    elif int(value[0]) in (3,6):
                        value = [value[0], 2, value[2]]
                    else:
                        raise NotImplementedError('tuple %s' % value)
                if value[2]=='':
                    value[2] = value[0]
                return [c_lass(c_lass.TUPLET, tuple(int(x) for x in value))] + c_lass.from_string(m.group(2))
            else:
                result = [c_lass(c_lass.BEGIN_SLUR)]
        elif s.startswith(')'):
            result = [c_lass(c_lass.END_SLUR)]
        elif s.startswith('-'):
            result = [c_lass(c_lass.TIE)]
        elif s.startswith('||'):
            result = [c_lass(c_lass.DOUBLE_BAR)]
            skip = 2
        elif s.startswith('|]'):
            result = [c_lass(c_lass.END_BAR)]
            skip = 2
        elif s.startswith('[|'):
            result = [c_lass(c_lass.REVERSE_END_BAR)]
            skip = 2
        elif s.startswith('|:'):
            result = [c_lass(c_lass.BEGIN_REPEAT)]
            skip = 2
        elif s.startswith('::'):
            result = [c_lass(c_lass.DOUBLE_REPEAT)]
            skip = 2
        elif s.startswith(':|'):
            m = re.match(':[|][ ]*[[]?([0-9,]+)(.*)', s)
            if m:
                value = tuple(m.group(1).split(','))
                result = [c_lass(c_lass.END_REPEAT,value)]
                skip = m.group(2)
            else:
                result = [c_lass(c_lass.END_REPEAT)]
                skip = 2
        elif s.startswith('|'):
            m = re.match('[|][ ]*[[]?([0-9,]+)(.*)', s)
            if m:
                # |3 is genuinely a shorthand for | [3 so implement it like this
                value = tuple(m.group(1).split(','))
                result = [c_lass(c_lass.BAR),c_lass(c_lass.BEGIN_ALTERNATIVE,value)]
                skip = m.group(2)
            else:
                result = [c_lass(c_lass.BAR)]
        elif s.startswith('['):
            m = re.match('[[]([0-9,]+)(.*)', s)
            if m:
                value = tuple(m.group(1).split(','))
                result = [c_lass(c_lass.BEGIN_ALTERNATIVE,value)]
                skip = m.group(2)
            else:
                result = [c_lass(c_lass.BEGIN_CHORD)]
        elif s.startswith(']'):
            # after chord, may have a duration, which multiplies the duration of notes within the chord
            m = re.match('[]]([0-9/]+)(.*)', s)
            if m:
                value = Duration.from_string(m.group(1))
                result = [c_lass(c_lass.END_CHORD)]
                skip = m.group(2)
            else:
                result = [c_lass(c_lass.END_CHORD)]
        elif s.startswith('\\'):
            # FIXME: continuations are crazy in abc, this doesn't support their full craziness
            m = re.match(r'\\[ \n\r\t]*(.*)', s)
            result = []
            skip = m.group(1)
        elif s.startswith('\n'):
            result = [c_lass(c_lass.NEW_LINE)]
        elif s.startswith(' '):
            m = re.match(' +(.*)', s)
            result = [c_lass(c_lass.BREAK)]
            skip = m.group(1)
        else:
            raise NotImplementedError("connector type %s" % s)

        if isinstance(skip, int):
            skip = s[skip:]

        remains = c_lass.from_string(skip)
        result.extend( remains )
        return result

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
        if isinstance(other, Duration):
            new = self.__class__( self.n * other.n, self.d * other.d )
        else:
            new = self.__class__( self.n * other, self.d)
        new.lower()
        return new

    def __div__(self, other):
        if isinstance(other, Duration):
            new = self.__class__( self.n * other.d, self.d * other.n)
        else:
            new = self.__class__( self.n, self.d * other )
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

    def __str__(self):
        if self.d == 1:
            return "%s" % self.n
        else:
            return "%s/%s" % (self.n, self.d)

    def __repr__(self):
        if self.d == 1:
            return "<dur %s>" % self.n
        else:
            return "<dur %s/%s>" % (self.n, self.d)

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

    def as_ab(self):
        if self.d == 1:
            if self.n == 1:
                return ''
            else:
                return str(self.n)
        elif self.n == 1 and self.d == 2:
            return '/'
        else:
            return '%s/%s' % (self.n, self.d)

    @classmethod
    def from_string(c_lass,strg):
        if not strg:
            return c_lass(1,1)

        elif "/" in strg:
            # replace //, /// with /4, /8 etc
            strg = re.sub('(//+)', (lambda m: '/'+str(2**len(m.group(1)))), strg)

            if strg.startswith("/"):
                strg = "1"+strg
            if strg.endswith("/"):
                strg = strg+"2"

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
    # allow ! before note, pretend it's a trill
    RE = re.compile("([~!]?)([_=^]*)([A-Za-z])([,']*)([0-9/]*)")

    # AB does not allow redefining letters, nor the extra space character y
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

    def as_ab(self):
        return "%s%s%s%s" % (self.trill or '', self.acc or '', self.pitch or '', self.dur.as_ab())

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
            items = AbcConnector.from_string(m[i])
            s.extend(items)
            if len(m)>=i+4:
                s.append(c_lass(m[i+3],m[i+4],m[i+2],m[i+5],m[i+1]))
        return s


class AbcField:
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
    CHORD_NAME = '"'
    PLUS = '+'

    @classmethod
    def from_string(c_lass, strg):
        m = c_lass.RE.split(strg)
        s = []
        for i in range(0,len(m),3):
            s.extend(AbcNote.from_string(m[i]))
            if len(m)>i+2:
                field = c_lass(m[i+1],c_lass.value_from_string(m[i+1],m[i+2]))
                s.append(field)
        return s

    @classmethod
    def value_from_string(c_lass, what, value):
        if what == AbcField.METER:
            value = value.lower()
            if value == 'c':
               value = Duration(4,4)
            elif value == 'c|':
               value = Duration(2,2)
            else:
                value = Duration.from_string(value)
        elif what == AbcField.UNIT_NOTE_LENGTH:
            value = Duration.from_string(value)
        elif what == AbcField.KEY:
            value = Key.from_string(value)
        return value

    def __init__(self, what, value):
        self.what = what
        self.value = value

    def __repr__(self):
        return u'<field '+self.what+':'+repr(self.value)+u'>'

    def as_ab(self):
        if isinstance(self.value, unicode):
            return u'[%s:%s]\n' % (self.what, self.value)
        else:
            return u'[%s:%s]\n' % (self.what, self.value.as_ab())

    def get_clean_value(self):
        if isinstance(self.value, unicode):
            if self.value is None:
                return u'(unknown)'
            # remove characters which excite lilypond
            strg = re.sub(r"[\\{}]","",self.value)
        else:
            strg = unicode(self.value)
        assert isinstance(strg, unicode)
        return strg



class Phrase:
    def __init__(self, name, key, time, unit, rhythm=None):
        # notes = a list of tuples, one per beat.
        self.rhythm = rhythm
        self.key = key
        self.name = name or u'(no name)'
        assert isinstance(self.name, unicode)
        self.time = time
        self.unit = unit
        self.notes = []
        #log_to_stderr("New phrase %s",self.name)


    def __repr__(self):
        return "<%s: %s>" % (self.name, ''.join([repr(x) for x in self.notes[:16]]))

    def rhythmify(self):
        #if self.rhythm is None:
        #    rhythm = []
        #else:
        #    try:
        #        rhythm = self.rhythm[len(items)-1]  
        #    except IndexError:
        #        rhythm = []
        for i, item in enumerate(self.notes):
            if isinstance(item, AbcConnector):
                if item.what == AbcConnector.SWING:
                    if isinstance(self.notes[i-1], AbcNote) and isinstance(self.notes[i+1], AbcNote):
                        self.notes[i-1].dur *= Duration(3,2)
                        self.notes[i+1].dur /= 2
                    else:
                        raise NotImplementedError("swing between non-notes")
                elif item.what == AbcConnector.SNAP:
                    if isinstance(self.notes[i-1], AbcNote) and isinstance(self.notes[i+1], AbcNote):
                        self.notes[i-1].dur /= 2
                        self.notes[i+1].dur *= Duration(3,2)
                    else:
                        raise NotImplementedError("snap between non-notes")
        return self
    
    def extend(self, items):
        self.notes.extend(items)
        return self

    def append(self, note):
        self.notes.append(note)
        return self

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

    def as_ab(self):
        value = ''.join(item.as_ab() for item in self.notes)
        return "%s\n" % value

    def render_ly(self, key=None, partial=None, bar_limit=None, no_repeats=False):

        #if key == self.key and not REMOVE_KEY_SIGNATURES:
        #    ly = ''
        #else:
        #    ly = '\key %s\n' % self.key.as_ly()

        ticks = Duration()
        if not partial:
            partial = Duration()    

        tune_ly = ''
        cur_bar = []
        cur_bar_length = self.time
        cur_bar_nr = 1
        warn_bar_length = 0

        pause = False
        last_note_index = None
        prev_item = None
        new_bar = None
        end_tuplet_count = None
        cur_tuplet_stretch = None

        if not isinstance(self.notes[-1], AbcConnector) or not self.notes[-1].is_bar_line():
            self.notes.append( AbcConnector(AbcConnector.END_BAR) )

        for i, item in enumerate(self.notes):

            if isinstance(item, AbcNote):
                last_note_index = len(cur_bar)
                cur_bar.append( item.as_ly(self.key, self.unit) )

                if not pause:
                    if cur_tuplet_stretch:
                        ticks += item.dur * self.unit * cur_tuplet_stretch
                    else:
                        ticks += item.dur * self.unit

                if end_tuplet_count:
                    end_tuplet_count -=1
                    if end_tuplet_count == 0:
                        cur_bar.append( "}" )
                        cur_tuplet_stretch = None


            elif isinstance(item, AbcConnector):
                if item.is_bar_line() :
                    bar_check = "|"

                    if no_repeats:
                        new_bar = ""
                    else:
                        new_bar = item.as_ly()

                    if pause:
                        raise NotImplementedError("bar line whilst paused")
                        # grace notes can't span a bar line
                        cur_bar.append('}')
                        pause = False

                    if ticks.n != 0:
                        if ticks != cur_bar_length:
                            if cur_bar_nr == 1:
                                cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % self.time.as_moment(), r'\bar ""'] + cur_bar
                                cur_bar_length = self.time
                                try:
                                    cur_bar = [r'\partial %s ' % ticks.mod_nonzero(cur_bar_length).as_ly()] + cur_bar
                                except TypeError:
                                    raise NotImplementedError("partial yielded unexpected result: %s" % ticks.mod_nonzero(cur_bar_length))
                            else:
                                cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % ticks.as_moment()] + cur_bar                    
                                cur_bar_length = ticks

                        if ticks < self.time:
                            if item.allow_short_bar():
                                warn_bar_length = 0
                            else:
                                if warn_bar_length > 2:
                                    log_to_stderr("%% Warning in %s bar %s: short bar of length %s, expected %s", self.name, cur_bar_nr, ticks, self.time)
                                cur_bar_nr -= 1 # short bar doesn't count
                        elif ticks > self.time:
                            log_to_stderr("%% Warning in %s bar %s: long bar of length %s, expected %s", self.name, cur_bar_nr, ticks, self.time)

                        cur_bar_nr += 1                            
                        tune_ly += ' '.join(cur_bar + [bar_check, new_bar, '\n'])
                        ticks = Duration()
                        cur_bar = []

                        if bar_limit and cur_bar_nr >= bar_limit:
                            break

                if item.what == AbcConnector.BAR:
                    # The only connector which is definitely on a real bar line is the bar line itself.
                    # Plus we don't know the proper length for the bar immediately after a bar we know to be short.
                    # So wait for 3 consecutive bar lines before warning.
                    warn_bar_length += 1
                    # (bar check was already added above)

                elif item.what == AbcConnector.BEGIN_GRACE:
                    pause = True # grace notes take up no time
                    if i==0 or not isinstance(self.notes[i-1], AbcNote):
                        cur_bar.append(r'\grace {')
                    else:
                        cur_bar.insert(last_note_index, r'\afterGrace')
                        cur_bar.append(r'{')
                elif item.what == AbcConnector.END_GRACE:
                    if not pause:
                        raise NotImplementedError("} character outside gracenote")
                    cur_bar.append('}')
                    pause = False

                elif item.what == AbcConnector.BEGIN_SLUR:
                    raise NotImplementedError("slur")
                elif item.what == AbcConnector.END_SLUR:
                    raise NotImplementedError("slur")
                elif item.what == AbcConnector.BEGIN_CHORD:
                    raise NotImplementedError("chord")
                elif item.what == AbcConnector.END_CHORD:
                    raise NotImplementedError("chord")

                elif item.what == AbcConnector.TIE:
                    # tie must immediately follow a note, not a barline or other such
                    if isinstance(prev_item, AbcNote):
                        cur_bar.append(item.as_ly())
                    else:
                        raise NotImplementedError("tie from non-note %s" % prev_item)

                elif item.what == AbcConnector.TUPLET:
                    end_tuplet_count = item.value[2]
                    cur_tuplet_stretch = Duration(item.value[1], item.value[0])
                    cur_bar.append(item.as_ly())

                else:
                    if not no_repeats:
                        cur_bar.append(item.as_ly())

            elif isinstance(item, AbcField):
                if item.what == AbcField.METER:
                    cur_bar.append(r'\time %s' % item.value.as_moment())
                elif item.what == AbcField.KEY:
                    cur_bar.append(r'\key %s' % item.value.as_ly())
                else:
                    raise NotImplementedError("inline field: %s" % item)

            prev_item = item

        leftover_duration = ticks % self.time

        return (tune_ly, leftover_duration)


class Tune:
    OK = 0
    FATAL = 1
    DIRECTIVE_IGNORED = 2
    HEADER_IGNORED = 4
    DECORATION_IGNORED = 8
    CHORD_NAME_IGNORED = 16
    PLUS_IGNORED = 32
    SLUR_IGNORED = 32

    def __init__(self):

        self.status = Tune.OK
        self.phrases = []
        self.fields = {}
        self.name = u'(no name)'
        self.ref = None

    def get_header(self, key, idx=0):
        if key not in self.fields:
            return u''

        x = self.fields[key][idx]
        return x
                

    def set_ref(self, item):
        self.ref = item.get_clean_value()

    def set_name(self, item):
        self.name = item.get_clean_value()
        assert isinstance(self.name, unicode)

    def add_header(self, item):
        if item.what not in self.fields:
            self.fields[item.what] = []

        if isinstance(item.value, str) or isinstance(item.value, unicode):
            clean_value = item.get_clean_value()
            assert isinstance(clean_value, unicode)
            self.fields[item.what].append(clean_value)
        else:
            self.fields[item.what].append(item.value)

    def as_ab(self):
        s = u'X:%s\n' % self.ref or id(self)
        keys = self.fields.pop("K",[Key.REGISTER["c"]])
        for field, values in sorted(self.fields.items()):
            for value in values:
                s += u'%s:%s\n' % (field, value)
        for value in keys:
            assert isinstance(value, Key)
            s += u'K:%s\n' % value.as_ab()

        for phrase_id, phrase in sorted(self.phrases):
            value = phrase.as_ab()
            s += u'[P:%s] %s\n' % (phrase_id, value)
        
        return s

    def render_ly(self, phrase_separator=None, end=None, bar_limit=None, page_break=True, no_repeats=False):

        if not phrase_separator:
            phrase_separator = '''    \\set Score.repeatCommands = #\'((volta #f)) \\break \\bar "" \\mark "%s"\n'''

        if not end:
            end = '    \\set Score.repeatCommands = #\'((volta #f)) \\bar "|." \\break'

        s = ur'''
\score{{
\transpose d d' {
'''

        key = None
        continuation = False

        for id,phrase in self.phrases:

            if continuation:
                if "%s" in phrase_separator:
                    assert '"' not in id
                    s += phrase_separator % id
                else:
                    s += phrase_separator
            else:
                s += "\\time %s\n" % phrase.time.as_moment()
                if not REMOVE_KEY_SIGNATURES:
                    s += "\\key %s\n" % phrase.key.as_ly()

            phrase_ly, leftover_duration = phrase.render_ly(key, None, bar_limit, no_repeats)
            s += phrase_ly
            key = phrase.key
            continuation = True

        assert isinstance(self.name, unicode)
        assert isinstance(self.get_header('meter'), unicode)
        s += end + r'''
}}
\header{
    piece = "%s"
    opus = "%s"
    meter = "%s"
}}
''' % (self.name.replace('"',"'"), '', self.get_header('meter').replace('"',"'"))

        if page_break:
            s += '\\pageBreak\n'

        return s

    @classmethod
    def from_string(c_lass, ab, abc=None, strictness=None):
        '''Parse an inlined AB with inlined headers into a Tune object.'''


        def get_next(strg):
            ALPH = "ABCDEFGHKLMNPQRSTUVWXYZ"
            if strg[-1] in ALPH:
                try:
                    return ALPH[ALPH.index(strg)+1]
                except IndexError:
                    pass
            return "?"
            

        # normalize space
        ab = re.sub(r'[\r\n\t ]+', ' ', ab.strip())

        # Obtain a stream of AbcField|AbcNote|AbcConnector objects.
        try:
            stream = AbcField.from_string(ab)
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
        if abc:
            tune.src = abc
        else:
            tune.src = ab

        cur_key = Key.from_string('C')
        cur_time = Duration.from_string('4/4')
        cur_unit = Duration.from_string('1/8')
        cur_phrase_id = 'A'
        cur_phrase = None
        queued_headers = []

        for item in stream:
            try:
                if isinstance(item, AbcField):
                    if item.what == AbcField.REFERENCE:
                        tune.set_ref( item )
                    elif item.what == AbcField.TUNE_TITLE:
                        tune.set_name( item )
                    elif item.what == AbcField.METER:
                        cur_time = item.value
                    elif item.what == AbcField.PARTS:
                        if in_header:
                            tune.add_header( item )
                        else:
                            queued_headers = []
                            cur_phrase = None
                            cur_phrase_id = item.value.replace('"',"'")
                            in_header = None # don't add this header to the phrase
                    elif item.what == AbcField.KEY:
                        cur_key = item.value
                        if in_header:
                            in_header = None # don't add this header to the phrase unless it's actually in the phrase
                    elif item.what ==  AbcField.UNIT_NOTE_LENGTH:
                        cur_unit = item.value
                    elif item.what ==  AbcField.DIRECTIVE:
                        if strictness & Tune.DIRECTIVE_IGNORED:
                            log_to_stderr("%% Unsupported directive in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored directive in tune %s: '%s'",tune.ref,item.value)
                        tune.status |= Tune.DIRECTIVE_IGNORED
                        continue
                    elif item.what ==  AbcField.CHORD_NAME:
                        if strictness & Tune.CHORD_NAME_IGNORED:
                            log_to_stderr("%% Unsupported chord name in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored chord name in tune %s: '%s'",tune.ref,item.value)
                        tune.status |= Tune.CHORD_NAME_IGNORED
                        continue
                    elif item.what ==  AbcField.DECORATION:
                        if strictness & Tune.DECORATION_IGNORED:
                            log_to_stderr("%% Unsupported decoration in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored decoration in tune %s: '%s'",tune.ref,item.value)
                        tune.status |= Tune.DECORATION_IGNORED
                        continue
                    elif item.what ==  AbcField.PLUS:
                        if strictness & Tune.PLUS_IGNORED:
                            log_to_stderr("%% Unsupported plus (may be chord or decoration) in tune %s: '%s'",tune.ref,item.value)
                        else:
                            log_to_stderr("%% Ignored plus (may be chord or decoration) in tune %s: '%s'",tune.ref,item.value)
                        tune.status |= Tune.PLUS_IGNORED
                        continue

                    if in_header is not False:
                        tune.add_header(item)
                        if in_header is not True:
                            in_header = False
                    else:
                        if cur_phrase is None:
                            queued_headers.append(item)
                        else:
                            cur_phrase.append(item)


                else:
                    # allow tune to ignore unsupported items:
                    if isinstance(item, AbcConnector):
                        if item.what == AbcConnector.BEGIN_SLUR or item.what == AbcConnector.END_SLUR:
                            if strictness & Tune.SLUR_IGNORED:
                                log_to_stderr("%% Unsupported slurs in tune %s",tune.ref)
                            elif not (tune.status & Tune.SLUR_IGNORED):
                                log_to_stderr("%% Ignored slurs in tune %s",tune.ref)
                            tune.status |= Tune.SLUR_IGNORED
                            continue
                        elif item.what == AbcConnector.BEGIN_REPEAT:
                            # assume starts a new phrase
                            cur_phrase = None
                            cur_phrase_id = get_next(cur_phrase_id)
                        elif item.what == AbcConnector.DOUBLE_REPEAT:
                            # assume starts a new phrase
                            cur_phrase = None
                            cur_phrase_id = get_next(cur_phrase_id)
                    elif isinstance(item, AbcNote):
                        pass
                    else:
                        raise NotImplementedError("non-abc object (type %s) %s" % (repr(type(item)), repr(item)))

                    if cur_phrase is None:
                        cur_phrase = Phrase(u"%s %s" % (tune.name, cur_phrase_id),
                                            cur_key, cur_time, cur_unit)
                        cur_phrase.extend(queued_headers)
                        tune.phrases.append((cur_phrase_id,cur_phrase))
                    cur_phrase.append(item)
            except NotImplementedError, e:
                log_to_stderr("%% Unknown item in tune X:%s: %s",tune.ref, e)
                tune.status |= Tune.FATAL

        try:
            for phrase_id, phrase in tune.phrases:
                phrase.rhythmify()
        except NotImplementedError, e:
            log_to_stderr("%% Couldn't apply rhythm to tune X:%s: %s",tune.ref, e)
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

    def add_data(self, fileobj, limit=None):
        count = 0
        original_abc = None
        abc = ""
        finished_ab = None
        ab = ""
        x_line = "" # only used when reporting a duplicate
        pause = False
        for line in fileobj.readlines()+["X::"]:
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                line = line.decode('iso-8859-1')

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
                    tune = Tune.from_string(finished_ab, original_abc)

                    if tune:
                        self.tune_check[check_id] = tune.ref
                        self.tunes.append(tune)
                        count += 1
                        if limit is not None and count>=limit:
                            break
                    else:
                        self.tune_check[check_id] = x_line.strip()
                        sys.stderr.write("%% Couldn't process the following tune:\n%s\n")
                        sys.stderr.write(original_abc.encode('utf-8'))
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

    for (path, dirs, files) in os.walk('data'):
        for filename in files:
            data = open(os.path.join(path,filename), 'r')
            count = TUNES.add_data(data, LIMIT)
            log_to_stderr("%% Finished %s , found %s tunes.\n\n",filename, count)
    # PHRASES.update(abfile.get_phrases())


    if CRIB:
        PREAMBLE = open("preamble.crib.ly.fragment","r").read()
    else:
        PREAMBLE = open("preamble.ly.fragment","r").read()


        
    for i in range(0,len(TUNES.tunes),BUCKET_SIZE):
        tuneset = TUNES.tunes[i:i+BUCKET_SIZE]
        ly_filename = 'tunes%s.ly' % i
        ly_file = open(os.path.join('out',ly_filename),'w')
        ly_file.write(PREAMBLE)

        ab_filename = 'tunes%s.ab' % i
        ab_file = open(os.path.join('out',ab_filename),'w')
        for tune in tuneset:
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
                ly_file.write( z.encode('utf-8') )
                ab_file.write( tune.as_ab().encode('utf-8') )
            except NotImplementedError, e:
                log_to_stderr("%% Couldn't render the following tune (%s): %s\n",tune.name or '(unknown)', e)
                sys.stderr.write(tune.src.encode('utf-8'))
          

    #for code,phrases in sorted(PHRASES.items()):
    #    log_to_stderr( code+": "+",".join(phrase.name for phrase in phrases)+"\n" )
