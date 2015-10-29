import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import root2py

root_hist = ROOT.TH1D('h','hist',100,-10,10)
root_hist.FillRandom('gaus',10000)

#help(root2py)

py_hist = root2py.pyTH1(root_hist)
py_hist.draw()
