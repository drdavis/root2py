import ROOT
import numpy

import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import root2py

x1 = numpy.arange(-25.0,25.0,1.0)
y1 = numpy.power(x1,2)

tg = ROOT.TGraph(x1.size,x1,y1)

pytg = root2py.pyTGraph(tg)
data = pytg.xy_pairs
#data = root2py.get_tgraph_content(tg)

if numpy.array_equal(data[:,1],y1):
     print "Pass"
     pytg.draw()
else:
    print "Failed"


