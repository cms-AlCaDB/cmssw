#!/usr/bin/python

import sys

import pandas as pd
import time
from   pandas import Series
from   datetime import datetime, timedelta

def parseBeamSpotFile(theFileName, theVariable="Z0"):
    print "parseBeamSpotFile acting on %s"%(theFileName)

    if not theVariable in ["Z0","X0"]:
        print "theVariable set to invalide value"
        sys.exit()

    theOffset = {}
    theOffset["Z0"]=7
    theOffset["Y0"]=6
    theOffset["X0"]=5

    # turn the text file into a list of lines
    with open(theFileName, "r") as theFile:
        lines = theFile.read().splitlines()

    # this is the dictionary which will hold the key=run*10000+ls value=Z0/Y0/X0
    theTimeSeriesDic = {}

    # loop over the whole file putting run-ls->var into the dict
    for lineNum in range( len(lines)):

        # intercept the line with run number and LS number (tagging with "for runs")
        # create one run-ls->var object
        if "for runs" in lines[lineNum]:
            run = lines[lineNum].split()[2]
            ls  = lines[lineNum].split()[4]
            # parse the value of the coordinate, which we know is a fixed number of lines down
            lineNum+=theOffset[theVariable]
            var = lines[lineNum].split()[2]
            #print "var %s is: %s"%(theVariable, var)

            # the 1970-Jan-1 is a simbolic date; the run counts 5000 seconds from a reference number (273291), the ls counts 1 second 
            theTimeSeriesDic[  pd.Timestamp(datetime(1970, 1, 1))   +     timedelta( seconds= ( (int(run)-273291)*5000 + int(ls) )   )  ] = float(var)
            print run, ls, timedelta( seconds= ( (int(run)-273291)*5000 + int(ls) )   )

    # keys() and values() from the same dictionary are in the same order
    # see : https://docs.python.org/3/library/stdtypes.html#dict-views
    theTimeSeries =  Series( theTimeSeriesDic.values(), index=theTimeSeriesDic.keys() )

    return theTimeSeries





if __name__ == '__main__':

    if(len(sys.argv) != 3):
        print "usage:    compare-time-series.py file-with-path1.txt file-with-path2.txt"
        sys.exit()
    else:
        print '\tNumber of arguments:', len(sys.argv), 'arguments (as expected).'
        print '\tArgument List: %s \n\n'%str(sys.argv)
    

        file1 = sys.argv[1]
        file2 = sys.argv[2]

        timeSeries1 = parseBeamSpotFile(file1)
        print timeSeries1
        print "timeSeries1 has a size of %s"%len( timeSeries1 )

        timeSeries2 = parseBeamSpotFile(file2)
        print timeSeries2
        print "timeSeries2 has a size of %s"%len( timeSeries2 )


        print
        print
        print
        print
        print
        print
        print


        print "align the two series in order to have the same time stamps"
        timeSeries1, timeSeries2 = timeSeries1.align(timeSeries2)
        
        print
        print
        print timeSeries1
        print
        print
        print timeSeries2


        print "interpolate the two series to make up for the missing values"
        timeSeries1inter =  timeSeries1.interpolate(method='time')
        print
        print
        print timeSeries1inter

        timeSeries2inter =  timeSeries2.interpolate(method='time')        
        print
        print
        print timeSeries2inter
