#!/usr/bin/env python

from __future__ import print_function
from sys import stdin, argv
from re import search

def read_cijfers(f):
    ''' yield year week number '''

    previous = None 

    for line in f:
        data=search(r'"(\d{4}) week(.+)";"(\d+)"', line)
        if data:
            year, week, number = data.groups()

            partial = search(r'\(\d dag.*\)', week)
            week = search(r'\d+', week).group(0)

            year, week, number = map(int, [ year, week, number ])

            if partial:

                if previous:

                    py, pw, pn = previous
                    previous = None

                    if week == 0:
                        # add week 0 to week 53
                        pn += number 
                        yield py, pw, pn

                    elif week == 1:
                        # add week 53 to week 1
                        number += pn
                        yield year, week, number

                    else:
                        raise AssertionError('week={}!'.format(week))

                else:
                    previous = year, week, number
                    # yield total during the next iteration

            else:
                previous = None

                yield year, week, number
        

if __name__ == '__main__':

    ''' https://opendata.cbs.nl/statline/#/CBS/nl/dataset/70895ned/table?dl=35C26 '''

    if len(argv)>1:
        f=open(argv[1])
    else:
        f=stdin

    cijfers = {}
    for year, week, number in read_cijfers(f):
        if year not in cijfers:
            cijfers[year]={}
        cijfers[year][week]=number


    print('"wk"', end=''),
    for year in sorted(cijfers.keys()):
        print(';"{:d}"'.format(year), end='')
    print()

    for week in range(1, 53+1):
        print('"{:d}"'.format(week), end='')
        for year in sorted(cijfers.keys()):
            if week in cijfers[year]:
                print(';"{:d}"'.format(cijfers[year][week]), end='')
            else:
                print(';""', end='')
        print()

# vim: set ai si sw=4 ts=4 et
