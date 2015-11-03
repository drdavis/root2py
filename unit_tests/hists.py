import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import root2py

"""
root_hist = ROOT.TH1D('h','hist',100,-10,10)
root_hist.FillRandom('gaus',10000)

#help(root2py)

py_hist = root2py.pyTH1(root_hist)
py_hist.plt.xlabel('lolol')
py_hist.draw()
"""


hist1 = ROOT.TH1D('hist1','hist',100,-10,10)
hist2 = ROOT.TH1D('hist2','hist',100,-10,10)

hist1.FillRandom('gaus',2000)
hist2.FillRandom('gaus',10000)

py_stack = root2py.pyTH1multi(hist1,hist2,cols=['red','blue'],
                              labels=['a','b'],stacked=True)
py_stack.plt.xlabel('wowowow')
py_stack.draw(legend=True)
