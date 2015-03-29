#!/usr/bin/python

import re, os, sys, argparse

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
    'bbma': Key.REGISTER['bb'],
    'ebma': Key.REGISTER['eb'],

    'amin': Key.REGISTER['am'],
    'bmin': Key.REGISTER['bm'],
    'cmin': Key.REGISTER['cm'],
    'dmin': Key.REGISTER['dm'],
    'emin': Key.REGISTER['em'],
    'gmin': Key.REGISTER['gm'],

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
        elif self.what == AbcConnector.END_CHORD:
            return '%s%s' % (AbcConnector.TYPES[self.what], self.value.as_ab())
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


    def is_bar_line(self):
        if self.what == AbcConnector.BAR:
            return True
        elif self.what == AbcConnector.DOUBLE_BAR:
            return True
        elif self.what == AbcConnector.END_BAR:
            return True
        elif self.what == AbcConnector.REVERSE_END_BAR:
            return True

        # these are not necessarily bar lines but they still reset the clock timer
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
                # chord with duration outside bracket
                # keep it here for information, but 'rhythmify' has already applied the multiplier
                value = Duration.from_string(m.group(1))
                result = [c_lass(c_lass.END_CHORD, value)]
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
    '''Represents a length of time expressed as n beats of length d.
Optionally n can be a list, showing that the duration is subdivided.
Arithmetic operations on durations always yield undivided durations.'''

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
        return self.as_ab()

    def __repr__(self):
        return "<dur %s>" % self.as_ab()

    def as_ly(self, unit=None):
        '''Return a lilypond note length with the same duration as self.'''
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
        elif dur.d == 1:
            if dur.n == 2:
                return r'\breve'
            elif dur.n == 4:
                return r'\longa'
            else:
                raise NotImplementedError("note of length %s (%s)" % (dur.n, str(dur)))
        else:
            raise NotImplementedError("note of length %s/%s (%s)" % (dur.n, dur.d, str(dur)))

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
            return "%s/%s" % (self.n, self.d)

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

            dur_match = re.match('([0-9+]+)/([0-9]+)', strg)
            if dur_match:
                n = dur_match.group(1)
                d = dur_match.group(2)
            else:
                raise NotImplementedError("unparseable duration %s" % strg)

            try:
                n = int(n)
                return c_lass(n,int(d))
            except ValueError:
                raise NotImplementedError("non-integer duration %s" % strg)

        else:
            try:
                return c_lass(int(strg),1)
            except ValueError:
                raise NotImplementedError("unparseable duration %s" % list(strg))

class Meter(Duration):
    '''A meter (time signature)

Supported formats:
    simple       4/4
    compound     2+3+2/8
    multiple     2/2,3/2
    both         2+3/8,3+2/8

For multiple meters, the longest duration is the 'master';
bars of shorter duration must be marked up with explicit barlines.
'''

    def __init__(self, n=0, d=1, multiples=None):
        if isinstance(n, list):
            self.n = sum(n)
            self.divisions = n
        else:
            self.n = n
            self.divisions = [n]
        self.d = d
        self.multiples = multiples

    def _compound_meter(self):
        if self.multiples:
            return '(%s)' % (' '.join([multiple._compound_meter() for multiple in self.multiples]))
        else:
            return '(%s %s)' % (' '.join([str(i) for i in self.divisions]), self.d)

    def as_meter(self):
        if self.multiples or len(self.divisions) > 1:
            if self.d < 4:
                # 3/2 and similar is beamed into minims
                three = "\set Timing.beatStructure = #' (%s)" % (' '.join(['1' for i in range(self.n)]))
            elif self.n > 3 and self.n % 3 == 0:
                # anything 3-like is beamed in threes
                three = "\set Timing.beatStructure = #' (%s)" % (' '.join(['3' for i in range(self.n/3)]))
            else:
                # always beam
                three = ''

            return r"\compoundMeter #' %s" % self._compound_meter() + three

        else:
            return r'\time %s/%s' % (self.n, self.d)
            
    def as_ab(self):
        if self.multiples:
            return ','.join(multiple.as_ab() for multiple in self.multiples)

        elif self.d == 1:
            if self.n == 1:
                return ''
            else:
                return str(self.n)

        elif self.n == 1 and self.d == 2:
            return '/'

        else:
            return "%s/%s" % ("+".join([str(i) for i in self.divisions]), self.d)

    def __repr__(self):
        return "<meter %s>" % self.as_ab()

    @classmethod
    def from_string(c_lass,strg):
        strg = strg.strip().lower()

        if strg == 'c':
           return c_lass(4,4)
        elif strg == 'c|' or not strg:
           return c_lass(2,2)

        multiple_parts = strg.split(',')

        if len(multiple_parts) > 1:
            multiple_meters = [c_lass.from_string(part) for part in multiple_parts]
            max_meter = max(multiple_meters)
            return c_lass(max_meter.divisions, max_meter.d, multiple_meters)
        else:

            dur_match = re.match('([0-9+]+)/([0-9]+)', strg)
            if dur_match:
                n = dur_match.group(1)
                d = dur_match.group(2)
            else:
                raise NotImplementedError("unparseable meter %s" % strg)

            try:
                n = [int(i) for i in n.split('+')]
                return c_lass(n,int(d))
            except ValueError:
                raise NotImplementedError("non-integer in meter %s" % strg)

class AbcNote:
    # Letters H..W,h..w are assumed to be valid trills but ignored (they don't need to be defined)
    # !, *, q, S have been seen in the wild.
    
    RE = re.compile("([*.~!H-Wh-w]?)([_=^]*)([A-Ga-gxyz])([,']*)([0-9/]*)")

    def __init__(self, pitch, oct, acc, dur, trill):
        self.pitch = pitch
        self.dur = Duration.from_string(dur)
        self.oct = oct or ''
        self.acc = acc or ''
        self.trill = trill or ''
        self.value = self.as_ab()


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

        if unit is None:
            # suppress length (e.g. in a chord)
            length = ''
        else:
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
                if (m[i+3]=='y'):
                    pass # y just adds extra space, is not really a note
                else:
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

            # look for "xxx", !xxx!, +xxx+ and replace with the corresponding inline field notation
            mm = re.sub('[+]([^+]*)[+]',r'[+:\1]', m[i])
            mm = re.sub('["]([^"]*)["]',r'[":\1]', mm)
            mm = re.sub('[!]([^!]*)[!]',r'[!:\1]', mm)

            if mm == m[i]:
                # none, so safe to pass to note handler
                s.extend(AbcNote.from_string(mm))
            else:
                # pass back through here handler
                s.extend(c_lass.from_string(mm))

            if len(m)>i+2:
                field = c_lass(m[i+1],c_lass.value_from_string(m[i+1],m[i+2]))
                s.append(field)
        return s

    @classmethod
    def value_from_string(c_lass, what, value):
        if what == AbcField.METER:
            value = Meter.from_string(value)
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

    def as_ab_bare(self, what=None, pfx=''):
        if not what:
            what = self.what
        if isinstance(self.value, unicode):
            return u'%s:%s' % (what, pfx + self.value)
        else:
            return u'%s:%s' % (what, pfx + self.value.as_ab())

    def as_ab(self):
        if self.what in 'KLMNPQRr':
            return u'['+self.as_ab_bare()+u']\n'
        else:
            return u'['+self.as_ab_bare('N', self.what+':')+u']\n'

    def as_ab_header(self):
        if self.what in 'ABCDFGHKNOPQRrSTWXZ':
            return self.as_ab_bare()+u']\n'
        else:
            return self.as_ab_bare('N', self.what+':')
    

    def as_ly(self):
        if self.what == AbcField.METER:
            return r'\time %s' % self.value.as_moment()
        elif self.what == AbcField.KEY:
            return r'\key %s' % self.value.as_ly()
        elif self.what == AbcField.CHORD_NAME:
            if self.value.startswith("^"):
                # vmp sometimes specifies above or below this way
                return r'<>^\markup { \sans \small "%s" } ' % self.value[1:]
            elif self.value.startswith("_"):
                # vmp sometimes specifies above or below this way
                return r'<>_\markup { \sans \small "%s" } ' % self.value[1:]
            else:
                return r'<>^\markup { \sans \small "%s" } ' % self.value
        else:
            raise NotImplementedError("inline field: %s" % self)

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
        chord_start = None

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
                elif item.what == AbcConnector.BEGIN_CHORD:
                    chord_start = i
                elif item.what == AbcConnector.END_CHORD:
                    if item.value:
                        # chord length multiplier found after chord, do this now
                        if not isinstance(chord_start, int):
                            raise NotImplementedError("chord end did not follow chord start")
                        for j in range(chord_start, i):
                            if isinstance(self.notes[j], AbcNote):
                                self.notes[j].dur *= item.value
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

        #if key == self.key and not ARGS.no_key_signatures:
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

        tune_ly = '\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment()

        bar_check = "|"
        pause = 0
        chord_time = None
        grace_note = None
        last_note_index = None
        prev_item = None
        new_bar = None
        end_tuplet_count = None
        cur_tuplet_stretch = None

        if not isinstance(self.notes[-1], AbcConnector) or not self.notes[-1].is_bar_line():
            # default end of phrase
            self.notes.append( AbcConnector(AbcConnector.DOUBLE_BAR) )

        if isinstance(self.notes[0], AbcConnector) and self.notes[0].what == AbcConnector.BEGIN_GRACE:
            # provide an empty note for grace to attach to
            self.notes.insert( 0, AbcNote('x',None,None,'/16',None) )

        for i, item in enumerate(self.notes):
            if isinstance(item, AbcNote):
                last_note_index = len(cur_bar)

                if cur_tuplet_stretch:
                    ticks_elapsed = item.dur * self.unit * cur_tuplet_stretch
                else:
                    ticks_elapsed = item.dur * self.unit

                if pause < 0:
                    pass # pause until told to stop
                elif pause > 0:
                    # pause after this number of notes
                    pause -= 1
                    if pause == 0:
                        pause = -1
                    if chord_time is True:
                        chord_time = ticks_elapsed
                        ticks += ticks_elapsed
                else:
                    ticks += ticks_elapsed
                    if ticks > self.time:
                        # bar can't be longer than time signature
                        cur_bar_nr += 1

                        if cur_bar_length != self.time:
                            cur_bar_length = self.time
                            cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment()] + cur_bar

                        tune_ly += ' '.join(cur_bar + [bar_check, '\n'])
                        ticks = ticks_elapsed
                        cur_bar = []

                        if bar_limit and cur_bar_nr >= bar_limit:
                            break

                if grace_note:
                    # put passing notes in brackets
                    cur_bar.append( r'\parenthesize' )

                if chord_time:
                    # duration goes after chord in lilypond
                    cur_bar.append( item.as_ly(self.key, None) )
                else:
                    cur_bar.append( item.as_ly(self.key, self.unit) )

                if end_tuplet_count:
                    end_tuplet_count -=1
                    if end_tuplet_count == 0:
                        cur_bar.append( "}" )
                        cur_tuplet_stretch = None


            elif isinstance(item, AbcConnector):
                if item.is_bar_line():

                    if no_repeats:
                        new_bar = ""
                    else:
                        new_bar = item.as_ly()

                    if grace_note:
                        raise NotImplementedError("bar line whilst paused (%s)" % pause)
                        # grace notes can't span a bar line
                        cur_bar.append('}')
                        pause = 0
                        grace_note = 0

                    if chord_time:
                        raise NotImplementedError("bar line during chord (%s)" % pause)
                        # chords can't span a bar line
                        cur_bar.append('>')
                        pause = 0
                        chord_time = 0

                    if ticks.n == 0:
                        # the only situation we want a barline at time 0 is if the phrase is itself empty
                        # (it's probably a repeated phrase)
                        for j, jtem in enumerate(self.notes):
                            if isinstance(jtem, AbcNote):
                                break
                        else:
                            tune_ly += new_bar
                    else:
                        #log_to_stderr("%% End %s bar %s: self.time %s, cur_bar_length %s, ticks %s", self.name, cur_bar_nr, self.time, cur_bar_length, ticks)
                        if ticks != cur_bar_length:
                            if ticks > self.time:
                                cur_bar_length = self.time
                                log_to_stderr("%% Long space without barlines in %s bar %s, reverting to %s", self.name, cur_bar_nr, self.time)
                            else:
                                cur_bar_length = ticks
                            cur_bar = [r'\set Timing.measureLength = #(ly:make-moment %s)' % cur_bar_length.as_moment()] + cur_bar

                        if ticks < self.time:
                            if item.allow_short_bar():
                                warn_bar_length = 0
                            else:
                                if warn_bar_length > 2:
                                    log_to_stderr("%% Warning in %s bar %s: short bar of length %s, expected %s", self.name, cur_bar_nr, ticks, self.time)
                                cur_bar_nr -= 1 # short bar doesn't count towards limit
                        elif ticks > self.time:
                            log_to_stderr("%% Warning in %s bar %s: long bar of length %s, expected %s", self.name, cur_bar_nr, ticks, self.time)
                            

                        cur_bar_nr += 1                            
                        tune_ly += ' '.join(cur_bar + [bar_check, new_bar, '\n'])
                        ticks = Duration()
                        cur_bar = []

                        if bar_limit and cur_bar_nr >= bar_limit:
                            break


                elif item.what == AbcConnector.BEGIN_GRACE:
                    grace_note = True
                    pause = -1 # grace notes take up no time
                    if i==0 or not isinstance(self.notes[i-1], AbcNote):
                        cur_bar.append(r'\afterGrace <> {')
                        #cur_bar.append(r'\grace {')
                    else:
                        cur_bar.insert(last_note_index, r'\afterGrace')
                        cur_bar.append(r'{')
                elif item.what == AbcConnector.END_GRACE:
                    if not grace_note:
                        raise NotImplementedError("} character outside gracenote")
                    cur_bar.append('}')
                    grace_note = False
                    pause = 0

                elif item.what == AbcConnector.BEGIN_SLUR:
                    raise NotImplementedError("slur")
                elif item.what == AbcConnector.END_SLUR:
                    raise NotImplementedError("slur")
                elif item.what == AbcConnector.BEGIN_CHORD:
                    pause = 1 # take the next note as the duration
                    cur_bar.append(r'<')
                    chord_time = True
                elif item.what == AbcConnector.END_CHORD:
                    pause = 0
                    if isinstance(chord_time, Duration):
                        cur_bar.extend([r'>', chord_time.as_ly()])
                        chord_time = None
                    elif chord_time is True:
                        chord_time = None
                        raise NotImplementedError("empty chord")
                    else:
                        chord_time = None
                        raise NotImplementedError("] character outside chord")
                elif item.what == AbcConnector.TIE:
                    # tie must immediately follow a note, not a barline or other such
                    if isinstance(prev_item, AbcNote):
                        cur_bar.append(item.as_ly())
                    else:
                        raise NotImplementedError("tie from non-note %s" % prev_item)

                elif item.what == AbcConnector.TUPLET:
                    if end_tuplet_count:
                        raise NotImplementedError("new tuplet %s started, but expecting %s more notes in previous tuplet" % (item, end_tuplet_count) )
                    end_tuplet_count = item.value[2]
                    cur_tuplet_stretch = Duration(item.value[1], item.value[0])
                    cur_bar.append(item.as_ly())

                else:
                    if not no_repeats:
                        cur_bar.append(item.as_ly())

            elif isinstance(item, AbcField):
                try:
                    cur_bar.append( item.as_ly() )
                except NotImplementedError:
                    log_to_stderr("%% Warning in %s: can't render to ly: %s", self.name, item)

            prev_item = item

        if end_tuplet_count:
            raise NotImplementedError("phrase ended, but expecting %s more notes in tuplet" % end_tuplet_count )

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
    SLUR_IGNORED = 64
    TRILL_IGNORED = 128
    CUSTOM_TRILL_IGNORED = 256

    STATUS_ITEMS = {
        DIRECTIVE_IGNORED: "directive",
        HEADER_IGNORED: "header",
        DECORATION_IGNORED: "decoration",
        CHORD_NAME_IGNORED: "chord name",
        PLUS_IGNORED: "item in +plus+ (either chord name in old format, or decoration)",
        SLUR_IGNORED: "slur",
        TRILL_IGNORED: "trill",
        CUSTOM_TRILL_IGNORED: "custom trill",
    }

    def __init__(self):
        self.status = Tune.OK
        self.phrases = []
        self.fields = {}
        self.ref = None

    def get_header(self, key, idx=0):
        if key not in self.fields:
            return u''
        
        x = self.fields[key][idx]
        return x

    def get_header_list(self, key):
        if key not in self.fields:
            return []
        
        x = self.fields[key]
        return x

    def get_name(self):
        return self.get_header(AbcField.TUNE_TITLE) or self.get_header(AbcField.REFERENCE)

    def set_ref(self, item):
        self.ref = item.get_clean_value()

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

    def render_ly(self, phrase_identifier=None, end=None, bar_limit=None, line_break=True, page_break=True, no_repeats=False):

        if not phrase_identifier:
            phrase_identifier = '''\\markup { \\bold \\sans \\smaller %s }\n'''

        if not end:
            end = ''

        s = ur'''
\score{{
\transpose d d' {
'''

        key = None
        continuation = False
        leftover_duration = None
        for id,phrase in self.phrases:
            id_in_brackets = re.match("[(].*[)]$", id)
            if line_break and not id_in_brackets:
                # if phrase is in brackets, don't force a line break even if specified
                s += '''
 \\break '''

            if id:
                assert '}' not in id
                ly_id = re.sub("([0-9]+)","\\\\finger{\\1.}", id)

                if id_in_brackets:
                    ly_id = ly_id[1:-1]
                    if "%s" in phrase_identifier:
                        # phrase is repeated
                        # insert a special bar of 1/1 and draw a repeat mark with the appropriate markup
                        s += '\\set Timing.measureLength = #(ly:make-moment 1/1) '
                        s += '\\makeDoublePercent s1 \\bar "" \\mark %s s1 ' % (phrase_identifier % ly_id)
                        s += '\\set Timing.measureLength = #(ly:make-moment %s) ' % (phrase.time.as_moment())
                        # return to normal bar length 
                    else:
                        # crib mode, ignore repeated section
                        pass
                else:
                    if "%s" in phrase_identifier:
                        # treat coda specially by converting into sign
                        if ly_id.lower()=="coda":
                            s += '\\mark \\markup { \musicglyph #"scripts.coda" }'
                        else:
                            s += "\\mark" + (phrase_identifier % ly_id)
                    elif continuation:
                        # crib mode, only add phrase identifier (Separator) after the start
                        s += phrase_identifier
            else:
                pass
                # phrase without id, doesn't need identifying

            if not continuation:
                s += phrase.time.as_meter()
                if not ARGS.no_key_signatures:
                    s += "\\key %s\n" % phrase.key.as_ly()

            phrase_ly, leftover_duration = phrase.render_ly(key, None, bar_limit, no_repeats)
            s += phrase_ly
            key = phrase.key
            continuation = True

        piece = self.get_name().replace('"',"'")

        origin = self.get_header_list(AbcField.ORIGIN)
        source = self.get_header_list(AbcField.SOURCE)
        if origin and not ARGS.no_origin:
            if source and not ARGS.no_source:
                arranger = (', '.join(origin) +" via "+ ', '.join(source)).replace('"',"'")
            else:
                arranger = ', '.join(origin).replace('"',"'")
        elif source and not ARGS.no_source:
            arranger = ', '.join(source).replace('"',"'")
        else:
            arranger = ""

        if ARGS.no_ref:
            opus = ""
        else:
            opus = self.ref

        meter = ""
        if not ARGS.no_rhythm:
            meter = self.get_header(AbcField.RHYTHM).replace('"',"'")

        s += end + r'''
}}
\header{
    piece = "%s"
    arranger = "%s"
    opus = "%s"
    meter = "%s"
}}
''' % (piece, arranger, opus, meter)

        # Treat a blank N: line as a paragraph break
        endnotes = '\n'.join(self.get_header_list(AbcField.NOTES)).replace('"',"'")

        if endnotes and not ARGS.no_endnotes:
            s += r'''
\markup {
    \justify-string #"%s"
}
''' % endnotes

        if page_break:
            s += '\\pageBreak\n'

        return s

    @classmethod
    def from_string(c_lass, ab, abc=None, strictness=None):
        '''Parse an inlined AB with inlined headers into a Tune object.'''


        def get_next(strg):
            if not strg:
                strg = 'A'
            ALPH = "ABCDEFGHKLMNPQRSTUVWXYZ"
            if strg[-1] in ALPH:
                try:
                    return strg[:-1]+ALPH[ALPH.index(strg[-1])+1]
                except IndexError:
                    pass
            return "?"

        def update_status(bit):
            if strictness & bit:
               log_to_stderr("%% Unsupported %s in tune %s: '%s'",Tune.STATUS_ITEMS[bit],tune.ref,item.value)
            else:
               log_to_stderr("%% Ignored %s in tune %s: '%s'",Tune.STATUS_ITEMS[bit],tune.ref,item.value)
            tune.status |= bit
            

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
        cur_time = Meter.from_string('2/2')
        cur_unit = Duration.from_string('1/8')
        cur_phrase_id = 'A'
        cur_phrase = None
        queued_headers = []

        for item in stream:
            try:
                if isinstance(item, AbcField):
                    if item.what == AbcField.REFERENCE:
                        tune.set_ref( item )
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
                        update_status(Tune.DIRECTIVE_IGNORED)
                        continue
                    elif item.what ==  AbcField.DECORATION:
                        update_status(Tune.DECORATION_IGNORED)
                        continue
                    elif item.what ==  AbcField.CHORD_NAME and ARGS.no_chords:
                        update_status(Tune.CHORD_NAME_IGNORED)
                        continue
                    elif item.what ==  AbcField.PLUS:
                        update_status(Tune.PLUS_IGNORED)
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
                            update_status(Tune.SLUR_IGNORED)
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
                        if item.trill:
                            update_status(Tune.TRILL_IGNORED)
                            if item.trill not in ".~HLMOPSTuv":
                                update_status(Tune.CUSTOM_TRILL_IGNORED)
                    else:
                        raise NotImplementedError("non-abc object (type %s) %s" % (repr(type(item)), repr(item)))

                    if cur_phrase is None:
                        cur_phrase = Phrase(u"%s %s" % (tune.get_name(), cur_phrase_id),
                                            cur_key, cur_time, cur_unit)
                        cur_phrase.extend(queued_headers)
                        tune.phrases.append((cur_phrase_id,cur_phrase))
                    cur_phrase.append(item)
            except NotImplementedError, e:
                log_to_stderr("%% Unknown item in tune X:%s: %s",tune.ref, e)
                tune.status |= Tune.FATAL


        if in_header:
            log_to_stderr("%% No K: field in tune X:%s",tune.ref)
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
    def __init__(self, include_duplicates=False, ids=None):
        self.ids = ids
        self.tunes = {}
        self.tune_check = {}
        self.include_duplicates = include_duplicates

    def add_data(self, fileobj, limit=None):
        count = 0
        original_abc = None
        abc = ""
        finished_ab = None
        ab = ""
        prev_x_line = ""
        x_line = ""
        pause = 0
        for line in fileobj.readlines()+["X::"]:
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                line = line.decode('iso-8859-1')

            if line.startswith("X:") or line.startswith("[X:"):
                if pause and ARGS.interactive:
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
                prev_x_line = x_line
                x_line = line
            else:
                abc += line

                if line.startswith("%"):
                    ab += "[%:"+line.strip()+"]"
                elif re.match("[A-Za-z]:", line):
                    ab += "["+line.replace("]",")").replace("[","(").strip()+"]"
                else:
                    ab += line

            if finished_ab:
                # remove score line breaks
                finished_ab = re.sub('[!+][\r\n]+|$', '', finished_ab)
                finished_ab = re.sub('^|[\r\n][!+]', '', finished_ab)

                # normalize space
                finished_ab = re.sub(r'[\r\n\t ]+', ' ', finished_ab.strip())

                tune_id = prev_x_line.strip()[2:]

                # use entire tune after X: as its own id for duplicate checking purposes
                check_id = re.sub("^[[]X:[^]]*[]]","",finished_ab)

                if self.ids and tune_id not in self.ids:
                    if ARGS.verbose:
                        log_to_stderr("%% Skipped %s as not in supplied tune list", tune_id)
                elif check_id in self.tune_check:
                    log_to_stderr("%% Skipped %s as exactly duplicated %s", tune_id, self.tune_check[check_id])
                else:
                    if ARGS.verbose:
                        log_to_stderr("%% Formatting %s", tune_id)
                    tune = Tune.from_string(finished_ab, original_abc)

                    if tune:
                        self.tune_check[check_id] = tune.ref
                        if tune_id not in self.tunes:
                            self.tunes[tune_id] = []
                        self.tunes[tune_id].append(tune)
                        count += 1
                        if limit is not None and count>=limit:
                            break
                    else:
                        self.tune_check[check_id] = x_line.strip()
                        sys.stderr.write("% Couldn't process the following tune:\n")
                        sys.stderr.write(original_abc.encode('utf-8'))
                        pause = True

                finished_ab = None
                original_abc = None
        return count


    def get_tunes(self):
        tune_list = []
        if self.ids:
            for id in self.ids:
                if id in self.tunes:
                    tune_list.extend(self.tunes[id])
                else:
                    sys.stderr.write("%% WARNING: Tune with ID %s was not found in the sources\n" % id)
        else:
            for id in sorted(self.tunes.keys()):
                tune_list.extend(self.tunes[id])
        return tune_list

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
    parser = argparse.ArgumentParser(description="Compiles PDFs from a library of ABC files, optionally specifying which tunes to include. Outputs a valid ABC file containing any tunes that were not successfully converted. You can also supply '-' to take tune IDs from standard input, one per line")

    parser.add_argument("-s", "--source-dir", help="Directory to find ABC files", default="data")
    parser.add_argument("-d", "--dest-dir", help="Directory to save PDF files", default="out")
    parser.add_argument("-p", "--preamble", help="Lilypond fragment to append tunes to", default="preamble.ly.fragment")
    parser.add_argument("-c", "--crib", help="Format as crib sheet (only the first 2 bars of each tune, implies -T -C -W -S -O -X)", action="store_true")
    parser.add_argument("-b", "--break", help="Add page break after each tune", action="store_true")
    parser.add_argument("-i", "--interactive", help="Prompt after encountering a tune with errors", action="store_true")
    parser.add_argument("-n", "--tunes-per-pdf", help="Split into separate PDFs each containing this number of tunes", type=int)
    parser.add_argument("-x", "--max-tunes", help="Stop processing after this number of tunes", type=int)
    parser.add_argument("-K", "--no-key-signatures", help="Omit key signatures (print explicit accidentals)", action="store_true")
    parser.add_argument("-C", "--no-chords", help="Omit chord names", action="store_true")
    parser.add_argument("-W", "--no-words", help="Omit words (W:) (Currently always on)", action="store_true")
    parser.add_argument("-N", "--no-endnotes", help="Omit tune endnotes (N:)", action="store_true")
    parser.add_argument("-R", "--no-rhythm", help="Omit tune rhythm (R:)", action="store_true")
    parser.add_argument("-S", "--no-source", help="Omit tune source (S:)", action="store_true")
    parser.add_argument("-O", "--no-origin", help="Omit tune origin (O:)", action="store_true")
    parser.add_argument("-X", "--no-ref", help="Omit tune reference (X:)", action="store_true")
    parser.add_argument("-v", "--verbose", help="Output more information to stderr", action="store_true")
    parser.add_argument("ids", nargs="*", metavar="ID", help="Which tune IDs to include in the output (default: all)")

    ARGS = parser.parse_args()

    if ARGS.ids == ["-"]:
        sys.stderr.write("% Enter tune IDs one per line or finish with EOF (Ctrl-D). Nothing specified = format entire collection\n")
        new_ids = sys.stdin.readlines()
        ARGS.ids = []
        for new_id in new_ids:
            stripped_id = re.sub('#.*$', '', new_id).strip()
            if stripped_id:
                sys.stderr.write("%% Got ID %s\n" % stripped_id)
                ARGS.ids.append(stripped_id)

    if ARGS.crib:
        ARGS.no_chords = True
        ARGS.no_words = True
        ARGS.no_endnotes = True
        ARGS.no_source = True
        ARGS.no_origin = True
        ARGS.no_ref = True

    ids = []
    for id in ARGS.ids:
        try:
            ids.append( id[:id.index('#')].strip() )
        except ValueError:
            ids.append( id.strip() )

    PHRASES = {}
    TUNES = ABCollection(ids=ids)

    if ARGS.verbose:
        log_to_stderr("%% Called formatter with arguments %s", vars(ARGS))

    if os.path.isfile(ARGS.source_dir):
        log_to_stderr("%% Processing single file", ARGS.source_dir)
        data = open(ARGS.source_dir, 'r')
        count = TUNES.add_data(data, ARGS.max_tunes)
        if ARGS.verbose:
            log_to_stderr("%% Scanned %s , found %s tune%s.\n",ARGS.source_dir, count, '' if count==1 else 's')    
    else:
        for (path, dirs, files) in os.walk(ARGS.source_dir, followlinks=True):
            if ARGS.verbose:
                log_to_stderr("%% Looking for .abc files in %s", path)
            for filename in files:
                if filename.lower().endswith(".abc"):
                    data = open(os.path.join(path,filename), 'r')
                    count = TUNES.add_data(data, ARGS.max_tunes)
                    if ARGS.verbose:
                        log_to_stderr("%% Scanned %s , found %s tune%s.\n",filename, count, '' if count==1 else 's')
    # PHRASES.update(abfile.get_phrases())

    all_tunes = TUNES.get_tunes()
    log_to_stderr("%% %s tunes to be formatted." % len(all_tunes));

    if not all_tunes:
        raise SystemExit("% No tunes found, nothing to do.")
    else:
        if ARGS.ids:
            if ARGS.verbose:
                log_to_stderr("%% Found %s tunes of %s requested.", len(all_tunes), len(ARGS.ids))
        else:
            log_to_stderr("%% Found %s tunes.", len(all_tunes))

    PREAMBLE = open(ARGS.preamble,"r").read()

    if not ARGS.tunes_per_pdf:
        ARGS.tunes_per_pdf = len(all_tunes)

    for i in range(0,len(all_tunes),ARGS.tunes_per_pdf):
        tuneset = all_tunes[i:i+ARGS.tunes_per_pdf]
        ly_filename = 'tunes%s.ly' % i
        ly_file = open(os.path.join('out',ly_filename),'w')
        ly_file.write(PREAMBLE)

        ab_filename = 'tunes%s.ab' % i
        ab_file = open(os.path.join('out',ab_filename),'w')
        for tune in tuneset:
            try:
                if ARGS.crib:
                    z=tune.render_ly(\
                        phrase_identifier=r'''    \set Score.repeatCommands = #'((volta #f)) 
\bar "" \stopStaff 
\set Timing.measureLength = #(ly:make-moment 1/4) s4
\startStaff \bar ".|"
''',
                        end='    \\set Score.repeatCommands = #\'((volta #f)) \\bar ""',
                        bar_limit=3,
                        line_break=False,
                        page_break=False,
                        no_repeats=True
                    )
                else:
                    z=tune.render_ly(page_break=True)
                ly_file.write( z.encode('utf-8') )
                ab_file.write( tune.as_ab().encode('utf-8') )
            except NotImplementedError, e:
                log_to_stderr("%% Couldn't render the following tune (%s): %s\n",tune.get_name(), e)
                sys.stderr.write(tune.src.encode('utf-8'))
          

    #for code,phrases in sorted(PHRASES.items()):
    #    log_to_stderr( code+": "+",".join(phrase.name for phrase in phrases)+"\n" )
