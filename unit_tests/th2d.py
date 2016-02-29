import ROOT
from ROOT import TRandom3
import rootplotlib

rand = TRandom3(0)

th2d = ROOT.TH2D("th",";;",20,0,1,20,0,1)

for i in xrange(100000):
    th2d.Fill(rand.Gaus(.5,0.1),
              rand.Gaus(.5,0.1))

rplth2d = rootplotlib.th2d(th2d,xlim=[0,1],ylim=[0,1],nticks=6)
rplth2d.draw()
