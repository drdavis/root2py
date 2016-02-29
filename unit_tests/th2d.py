import os,sys

import ROOT
from ROOT import TRandom3
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import rootplotlib


rand = TRandom3(0)

th2d = ROOT.TH2D("th",";;",5,0,15,15,0,15)

#c1 = ROOT.TCanvas()
for i in xrange(100000):
    th2d.Fill(rand.Gaus(5,3),
              rand.Gaus(5,3))
#th2d.Draw("COLZ")
#c1.Update()

rplth2d = rootplotlib.th2d(th2d,titles=['Victor','Ashley'])
rplth2d.draw(save='alright.eps',show=False)
