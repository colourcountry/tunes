#!/usr/bin/python

import sys, csv, re, argparse


class Performance:
    PERFORMANCES = {}
    SESSIONS = []
    BY_SESSION = {}

    @classmethod
    def register(c_lass, **defn):
        new = c_lass(**defn)
        c_lass.PERFORMANCES[new.id] = new
        if new.session not in c_lass.BY_SESSION:
            c_lass.SESSIONS.append(new.session)
            c_lass.BY_SESSION[new.session] = []
        c_lass.BY_SESSION[new.session].append(new)

    @classmethod
    def list(c_lass):
        return c_lass.PERFORMANCES.items()

    def __str__(self):
        if not self.follows:
            return ">> %s" % ( self.str_set() )
    
        start = self.follows
        while start.follows:
            start = start.follows

        return "%s >> %s" % ( start.str_set(self), self.str_set() )

    def str_set(self,stop=None):
        name = None
        if self.tune:
            name = "%s %s" % (self.id, tuple(self.tune.names))
        else:
            name = self.id

        if self.followed_by and self.followed_by is not stop:
            return "%s -> %s" % (name, self.followed_by.str_set(stop))
        else:
            return name


    def __init__(self,  id='',
                        date='',
                        location='',
                        follows='',
                        given_name='',
                        led_by='',
                        same_as='',
                        apparent_name='',
                        ext_references='',
                        ext_performances='',
                        derived_name='',
                        remarks=''):

        # Treat empty strings as None
        
        self.id = id.strip() or None
        self.session = re.match('(.*) [0-9]+$',self.id).group(1)

        self.date = date.strip() or None
        self.location = location.strip() or None

        self.follows = self.__class__.PERFORMANCES.get(follows.strip(), None) or follows.strip() or None
        self.followed_by = None
        if isinstance(self.follows, Performance):
            self.follows.followed_by = self

        self.given_name = given_name.strip() or None
        self.same_as = same_as.strip() or None
        if apparent_name == 'FALSE' or apparent_name == '#N/A' or apparent_name == '0':
            # the openoffice macro deriving the name failed in some way
            self.apparent_name = None 
        else:
            self.apparent_name = apparent_name.strip() or None
        if derived_name == 'FALSE' or derived_name == '#N/A' or derived_name == '0':
            # the openoffice macro deriving the name failed in some way
            self.derived_name = None 
        else:
            self.derived_name = derived_name.strip() or None
        self.ext_references = set(ext_references.strip().split(',')) or None
        self.ext_performances = set(ext_performances.strip().split(',')) or None
        self.remarks = remarks.strip() or None
        self.tune = None

    def get_id(self):
        return self.id        

class Tune:
    @classmethod
    def list(c_lass, key=None):
        tunes = {}

        for performance in Performance.PERFORMANCES.values():
            if not performance.same_as or performance.same_as == performance.id:
                tunes[performance.id]=Tune(performance)

        for performance in Performance.PERFORMANCES.values():
            if performance.same_as and performance.same_as != performance.id:
                try:
                    orig_tune = tunes[performance.same_as]
                except KeyError:
                    raise KeyError("tune %s is marked same as %s, but %s is not listed" % (performance.id, performance.same_as, performance.same_as) )
                orig_tune.add_performance(performance)

        if not key:
            key = Tune.get_id

        return sorted( tunes.values(), key=key )


    def __init__(self, performance):
        self.id = performance.id
        self.performances = []
        self.last_name = None
        self.names = set()
        self.ext_references = set()
        self.ext_performances = set()
        self.add_performance(performance)
        self.performances = [performance]
        

    def __str__(self):
        s = '%s %s %s\n' % (self.id, self.get_index_name(), tuple(self.names))
        for p in sorted(self.performances, key=Performance.get_id):
            s += '    %s\n' % str(p)
        if self.ext_references:
            s += 'References: %s\n' % ', '.join(sorted(self.ext_references))
        if self.ext_performances:
            s += 'Performances: %s\n' % ', '.join(sorted(self.ext_performances))
        return s

    def add_performance(self, performance):
        self.performances.append(performance)
        self.names.update( (performance.given_name, performance.apparent_name, performance.derived_name) )
        self.names.discard(None)

        if performance.derived_name:
            self.last_name = performance.derived_name

        self.ext_references.update(performance.ext_references)
        self.ext_references.discard(None)
        self.ext_references.discard('')
        self.ext_performances.update(performance.ext_performances)
        self.ext_performances.discard(None)
        self.ext_performances.discard('')
        performance.tune = self

    def get_index_name(self):
        if not self.last_name:
            return '(%s)' % self.id
        elif self.last_name.lower().startswith("the "):
            return self.last_name[4:]
        else:
            return self.last_name

    def get_id(self):
        return self.id

    def get_popularity(self):
        # count number of session appearances
        # (!= number of performances if played more than once in a session)
        count = 0
        appearances = []
        for session in Performance.SESSIONS:
            for performance in self.performances:
                if performance.session == session:
                    count += 1
                    appearances.insert(0,True)
                    break
            else:
                appearances.insert(0,False)

        # make number of session appearances override recentness
        appearances.insert(0,count)

        return appearances



def output_jekyll(out_tunes,sessions):
    print '''---
title: Session tunes
categories: colour
tags: folk music tunes
layout: post
bg: "url(/2013/patterns/chequers_teal.png)"
fg: "#000"
---

These are the most popular tunes played at Walthamstow folk session
'''

    print '''<table><tr><th></th>'''

    for session in sessions:
        print '''<th>%s</th>''' % session

    print '''</tr>'''

    twice = []
    once = []
    for tune in reversed(list(Tune.list( key=Tune.get_popularity ))):
        pop = Tune.get_popularity(tune)
        if pop[0]>2:
            print '''<tr><td>%s</td>''' % tune.last_name

            for i,session in enumerate(Performance.SESSIONS):
                if pop[len(pop)-i-1]:
                    print '''<td class="col_%s">&#x2713;</td>''' % ((i%7)+1)
                else:
                    print '''<td class="grey">&#x274c;</td>'''
            print '''</tr>'''
        elif pop[0]==2:
            twice.append(tune)
        elif pop[0]==1:
            once.append(tune)
    print '''</table>'''

    print '''\n%s tunes have been played twice: %s.''' % (len(twice), ', '.join(sorted([tune.last_name for tune in twice])))

    print '''\n%s more tunes have been played only once.''' % len(once)

    print '''\nThe source data and indexer script can be found [on github](https://github.com/colourcountry/tunes/tree/master/src)'''

if __name__=="__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", help="CSV tune index file to read", default="index.csv")
    parser.add_argument("-f", "--filter", metavar="PREFIX", help="Only look at sessions whose ID begins with PREFIX")
    parser.add_argument("-k", "--sort-key", help="Sort results by this key", choices=["popularity","name"], default="popularity")
    parser.add_argument("-p", "--popularity", help="Minimum popularity (over the filtered sessions)",type=int)
    parser.add_argument("-P", "--max-popularity", help="Maximum popularity (over the filtered sessions)",type=int)
    parser.add_argument("-r", "--reverse", help="Reverse order of results", action="store_true")
    parser.add_argument("format", help="Format of desired output", choices=["ids","info","jekyll","popularity"])

    ARGS = parser.parse_args()

    header = True
    date = '?'
    location = '?'
    previous = '?'
    for p in csv.reader(file(ARGS.source,'r')):
        if header:
            header = False
        elif len(p)>=10:
            if p[1]: date = p[1]
            if p[2]: location = p[2]
            if p[3]=='yes':
                follows = previous
            else:
                follows = ''
            Performance.register( id=p[0],
                                  date=date,
                                  location=location,
                                  follows=follows,
                                  given_name=p[4],
                                  led_by=p[5],
                                  same_as=p[6],
                                  apparent_name=p[7],
                                  ext_references=p[8],
                                  ext_performances=p[9],
                                  derived_name=p[10],
                                  remarks=p[11])
            previous = p[0]
        else:
            sys.stderr.write("WARNING: short line %s\n" % p)


    if ARGS.filter:
        for i in range(len(Performance.SESSIONS)-1,-1,-1):
            if not Performance.SESSIONS[i].startswith(ARGS.filter):
                Performance.SESSIONS.pop(i)

    if ARGS.sort_key=='name':
        KEY = Tune.get_index_name
    else:
        KEY = Tune.get_popularity

    out_tunes = []
    for tune in Tune.list( key=KEY ):
        if not ARGS.popularity or Tune.get_popularity(tune)[0]>=ARGS.popularity:
            if not ARGS.max_popularity or Tune.get_popularity(tune)[0]<ARGS.max_popularity:
                out_tunes.append(tune)

    if ARGS.reverse:
        out_tunes.reverse()

    if ARGS.format=='jekyll':
        output_jekyll(out_tunes,Performance.SESSIONS)

    elif ARGS.format=='info':
        for tune in out_tunes:
           print '%s\n\n' % tune

    elif ARGS.format=='ids':
        for tune in out_tunes:
            print tune.id

    elif ARGS.format=='popularity':
        for tune in out_tunes:
            p = Tune.get_popularity(tune)

            ticks = ''
            for column in p[1:]:
                ticks += 'y ' if column else '. '

            print p[0],ticks,tune.id,tune.get_index_name()


