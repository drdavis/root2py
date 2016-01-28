import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import root2py

x = numpy.arange(-25,25,1.0)
y = x*x

tg = ROOT.TGraph(x.size,x,y)

uo = root2py.single_tgraph(tg,objtype='TGraph')

print uo.x

uo.draw()

tg.Draw('AP')
tg.SetMarkerStyle(8)
raw_input('')
