import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import rootplotlib

x = numpy.arange(-25,25,1.0)
y = x*x

tg = ROOT.TGraph(x.size,x,y)

uo = rootplotlib.single_tgraph(tg,objtype='TGraph',titles=[r'$x$',r'$y$'],
                           xlim=[-30,30],ylim=[-10,1000])

print uo.x

uo.draw()

tg.Draw('AP')
tg.SetMarkerStyle(8)
raw_input('')
