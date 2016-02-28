import ROOT
from ROOT import TRandom

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

rand = TRandom(0)

#Make TCanvas+TH2D
c1 = ROOT.TCanvas()
c1.cd()
th2d = ROOT.TH2D("th",";;",19,0,1,13,0,1)


#Fill with TRandom data
for i in xrange(1000):
    th2d.Fill(rand.Gaus(0.5,0.2),
              rand.Gaus(0.5,0.2))

#Draw TH2D
th2d.Draw("COLZ")
c1.Update()


# numpy read raw TArray buffer that TH2D is sitting on, +2 on box nBins...
data  = np.frombuffer(th2d.GetArray(),count=th2d.GetSize())

#split the data on Y
data  = np.split(data,th2d.GetNbinsY()+2)

#draw in pyplot
fig,ax = plt.subplots(figsize=(10,6))

#matshow mimics output of TH2D.Draw("COLZ"), put the origin a the bottom like ROOT
cb = ax.matshow(data,origin='lower')

#Move the xticks down there
ax.xaxis.set_ticks_position('bottom')

#Set the XTicks to be the same as default on TCanvas
nticks = float(3.0)
nbinsx = th2d.GetNbinsX()+2
nbinsy = th2d.GetNbinsY()+2

ax.set_xticks(np.arange(0,nbinsx,nticks))
ax.set_yticks(np.arange(0,nbinsy,nticks))

#Set the labels to match whats on TCanvas
ax.set_xticklabels(np.arange(0,th2d.GetXaxis().GetXmax(),nticks/nbinsx))
ax.set_yticklabels(np.arange(0,th2d.GetYaxis().GetXmax(),nticks/nbinsy)) #ROOT doesn't have GetYmax lol

#Z axis like root
plt.colorbar(cb)

#Draw
plt.show()

