import ROOT
from ROOT import TRandom3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

rand = TRandom3(0)

#Make TCanvas+TH2D
#c1 = ROOT.TCanvas()
#c1.cd()
th2d = ROOT.TH2D("th",";;",10,0,1,10,0,1)


#Fill with TRandom data
for i in xrange(100000):
    th2d.Fill(rand.Gaus(.5,0.1),
              rand.Gaus(.5,0.1))

#Draw TH2D
#th2d.Draw("COLZ")
#c1.Update()


# numpy read raw TArray buffer that TH2D is sitting on, +2 on box nBins...
data  = np.frombuffer(th2d.GetArray(),count=th2d.GetSize())

#split the data on Y
data  = np.array(np.split(data,th2d.GetNbinsY()+2))

#remove overflow/underflow
data = data[1:-1,1:-1]

#draw in pyplot
fig,ax = plt.subplots(figsize=(10,6))

#matshow mimics output of TH2D.Draw("COLZ"), put the origin a the bottom like ROOT
cb = ax.matshow(data,origin='lower')

#Move the xticks down there
ax.xaxis.set_ticks_position('bottom')

#Set the XTicks to be the same as default on TCanvas
nticks = float(1.0)
nbinsx = th2d.GetNbinsX()
print nbinsx
nbinsy = th2d.GetNbinsY()

ax.set_xticks(np.arange(0,nbinsx,nticks))
ax.set_yticks(np.arange(0,nbinsy,nticks))

#Set the labels to match whats on TCanvas
ax.set_xticklabels(np.around(np.arange(0,th2d.GetXaxis().GetXmax(),nticks/nbinsx),2))
ax.set_yticklabels(np.around(np.arange(0,th2d.GetYaxis().GetXmax(),nticks/nbinsy),2)) #ROOT doesn't have GetYmax lol

#Z axis like root
plt.colorbar(cb)

#Draw
plt.show()


