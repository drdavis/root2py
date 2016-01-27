import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import root2py

hist1 = ROOT.TH1D('hist1','hist',100,-10,10)
hist2 = ROOT.TH1D('hist2','hist',100,-10,10)

hist1.FillRandom('gaus',2000)
hist2.FillRandom('gaus',10000)

def check_plotBase():
    y = root2py.plotBase(xlim=[1,0],ylim=[1,2],titles=['b','c'])
    print y.xlim
    print y.ylim
    print y.titles

def check_binnedObject():
    m = root2py.binnedObject(hist1,xlim=[-20,20],ylim=[-100,1000])
    print m.color
    print m.xlim
    
    if m.xlim:
        print 'yes'
    else:
        print 'no'

    m.draw(save='ok.eps')

check_plotBase()
check_binnedObject()
    
"""
py_stack = root2py.pyTH1multi(hist1,hist2,cols=['red','blue'],
                              labels=['a','b'],stacked=True)
py_stack.plt.xlabel('wowowow')
#py_stack.draw(legend=True)

pywratio = root2py.pyTH1multiWithRatio(hist1,hist2,cols=['red','blue'],ratio=hist1)
pywratio.plt.xlabel('wut')
pywratio.draw(save='lol.pdf')
"""
