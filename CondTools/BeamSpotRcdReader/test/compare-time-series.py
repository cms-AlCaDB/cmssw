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
            theTimeSeriesDic[  pd.Timestamp(datetime(2000, 1, 1))   +     timedelta( seconds= ( (int(run)-273291)*5000 + int(ls) )   )  ] = float(var)
            print run, ls, timedelta( seconds= ( (int(run)-273291)*5000 + int(ls) )   )

    # keys() and values() from the same dictionary are in the same order
    # see : https://docs.python.org/3/library/stdtypes.html#dict-views
    theTimeSeries =  Series( theTimeSeriesDic.values(), index=theTimeSeriesDic.keys() )
    #theTimeTimes =  Series( theTimeSeriesDic.values(), index=theTimeSeriesDic.keys() )
    
    return theTimeSeries






if __name__ == '__main__':

    if(len(sys.argv) != 3):
        print "usage:    compare-time-series.py file-with-path1.txt file-with-path2.txt"
        sys.exit()
    
    print '\tNumber of arguments:', len(sys.argv), 'arguments (as expected).'
    print '\tArgument List: %s \n\n'%str(sys.argv)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    myVariable = "Z0"
    
    timeSeries1 = parseBeamSpotFile(file1,myVariable)
    #print timeSeries1
    print "timeSeries1 has a size of %s"%len( timeSeries1 )
    print

    timeSeries2 = parseBeamSpotFile(file2,myVariable)
    #print timeSeries2
    print "timeSeries2 has a size of %s"%len( timeSeries2 )
    print

    print "align the two series in order to have the same time stamps"
    timeSeries1, timeSeries2 = timeSeries1.align(timeSeries2)
    
    print
    print "TS1 aligned w/2"
    print timeSeries1
    print "timeSeries1 aligned has a size of %s"%len( timeSeries1 )
    print
    print "TS2 aligned w/ 1"
    print timeSeries2
    print "timeSeries2 aligned has a size of %s"%len( timeSeries2 )


    print "interpolate the two series to make up for the missing values"
    timeSeries1inter =  timeSeries1.interpolate(method='time')
    print
    print "TS1 interpolated"
    print timeSeries1inter
    print "timeSeries1 interpolated has a size of %s"%len( timeSeries1inter )
    
    timeSeries2inter =  timeSeries2.interpolate(method='time')        
    print
    print "TS2 interpolated"
    print timeSeries2inter
    print "timeSeries2 interpolated has a size of %s"%len( timeSeries2inter )
    
    difference = timeSeries1inter - timeSeries2inter
    print
    print "TS1 - TS2"
    print difference
    print "difference has a size of %s"%len( difference )
    
    #import matplotlib.pyplot as plt
    #import numpy as np
    # import plotly.plotly as py

    theNPDifferences = difference.values
    theDifferences   = theNPDifferences.tolist()
    #theDifferences   = difference.values.tolist()
    theS1            = timeSeries1inter.values
    theS2            = timeSeries2inter.values
    print "differences are:"
    print theDifferences


    print
    print
    print
    print
    import ROOT
    differences_1D = ROOT.TH1F("Deltas","Deltas",100,-5.,5.);
    for u in theDifferences:
        differences_1D.Fill(u)
        if abs(u) > 0.4: # tuned for variable = Z0
            theIndexOfU = theDifferences.index(u)
            print "at index: %s diff: %s   BS_s1: %s BS_s2: %s"%( theIndexOfU, u, timeSeries1inter[theIndexOfU], timeSeries2inter[theIndexOfU] )
    
    theDiff = ROOT.TCanvas("Diff for %s"%(myVariable),"Diff for %s"%(myVariable),1200,900)
    theDiff.SetFillColor(ROOT.kWhite)
    theDiff.cd(1)
    differences_1D.Draw()
    theDiff.SaveAs("broken-reference.png")
    theDiff.SaveAs("broken-reference.root")

    timeStart = ROOT.TDatime(2000,1,1,0,0,0)
    ROOT.gStyle.SetTimeOffset(timeStart.Convert(1) )
    print  timeSeries1inter.index.format()   # this works nicely
    import numpy as np
    theMin = 0.
    theMax = 0.
    times = np.empty(len(theS1))
    for mydate in timeSeries1inter.index.format():
        da = ROOT.TDatime(
            int(mydate.split()[0].split("-")[0]),
            int(mydate.split()[0].split("-")[1]),
            int(mydate.split()[0].split("-")[2]),
            int(mydate.split()[1].split(":")[0]),
            int(mydate.split()[1].split(":")[1]),
            int(mydate.split()[1].split(":")[2])
            )
        print mydate
        #print da
        times.fill(da.Convert())
        #print "**XX"
        #print da.Convert()

        if theMin==0:
            theMin=da.Convert()
        elif da.Convert() < theMin:
            theMin=da.Convert()

        if theMax==0:
            theMax=da.Convert()
        elif da.Convert() > theMax:
            theMax=da.Convert()

    print "*******"
    print times
    print "*******"
    print theMax
    print theMin

    #history_s1 = ROOT.TGraph( len(times), times, theS1);
    #theHistory = ROOT.TCanvas("History for %s"%(myVariable),"History for %s"%(myVariable),1200,900)
    #theHistory.cd(1)
    #history_s1.GetXaxis().SetTimeDisplay(1);
    #history_s1.GetXaxis().SetNdivisions(-503);
    #history_s1.GetXaxis().SetTimeFormat("%Y-%m-%d %H:%M");
    #history_s1.GetXaxis().SetTimeOffset(0,"gmt");
    #history_s1.Draw("AP")
    #theHistory.SaveAs("tovalid-reference-history.png")

    #print len(times) 
    #print len(theS1)
    
    #import matplotlib.pyplot as plt
    #import matplotlib
    #matplotlib.style.use('ggplot')
    #plt.figure();
    #timeSeries1inter.plot()
    #timeSeries2inter.plot()


    #histo1 = ROOT.TH1F("histo1","histo1", (theMax-theMin) ,theMin,theMax);
    histo1 = ROOT.TH1F("histo1","histo1", len(theS1) ,0,len(theS1));
    histoDiff = ROOT.TH1F("histoDiff","histoDiff", len(theS1) ,0,len(theS1));
    for u in range ( len (theDifferences)) :
        #histo1.Fill( times[u], theS1[u] )
        histo1.SetBinContent(u,theS1[u])
        histoDiff.SetBinContent(u,theDifferences[u])
    theHistory = ROOT.TCanvas("History for %s"%(myVariable),"History for %s"%(myVariable),1200,900)
    theHistory.SetFillColor(ROOT.kWhite)
    theHistory.cd(1)
    histo1.Draw()
    histoDiff.SetLineColor(2)
    histoDiff.SetLineStyle(9)
    histoDiff.Draw("same")
    theHistory.SaveAs("broken-reference-HISTORY.png")
    theHistory.SaveAs("broken-reference-HISTORY.root")

