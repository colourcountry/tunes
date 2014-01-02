#!/usr/bin/python

import sys, csv, re


class Performance:
    PERFORMANCES = {}

    @classmethod
    def register(c_lass, **defn):
        new = c_lass(**defn)
        c_lass.PERFORMANCES[new.id] = new

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
                        same_as='',
                        apparent_name='',
                        time='',
                        remarks=''):

        # Treat empty strings as None
        
        self.id = id.strip() or None
        self.date = date.strip() or None
        self.location = location.strip() or None

        self.follows = self.__class__.PERFORMANCES.get(follows.strip(), None) or follows.strip() or None
        self.followed_by = None
        if isinstance(self.follows, Performance):
            self.follows.followed_by = self

        self.given_name = given_name.strip() or None
        self.same_as = same_as.strip() or None
        self.apparent_name = apparent_name.strip() or None
        self.time = time.strip() or None
        self.remarks = remarks.strip() or None
        self.tune = None

    def get_id(self):
        return self.id        

class Tune:
    @classmethod
    def list(c_lass, key=None):
        tunes = {}

        for performance in Performance.PERFORMANCES.values():
            if not performance.same_as:
                tunes[performance.id]=Tune(performance)

        for performance in Performance.PERFORMANCES.values():
            if performance.same_as:
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
        self.names = set()
        self.add_performance(performance)
        self.performances = [performance]

    def __str__(self):
        s = '%s %s\n' % (self.id, tuple(self.names))
        for p in sorted(self.performances, key=Performance.get_id):
            s += '    %s\n' % str(p)
        return s

    def add_performance(self, performance):
        self.performances.append(performance)
        self.names.update( (performance.given_name, performance.apparent_name) )
        self.names.discard(None)
        performance.tune = self

    def get_id(self):
        return self.id

    def get_popularity(self):
        return len(self.performances)

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
                follows = ''
            Performance.register( id=p[0],
                                  date=date,
                                  location=location,
                                  follows=follows,
                                  given_name=p[4],
                                  same_as=p[5],
                                  apparent_name=p[6],
                                  time=p[9],
                                  remarks=p[10])
            previous = p[0]

    for tune in Tune.list( key=Tune.get_popularity ):
        print '%s\n\n' % tune


