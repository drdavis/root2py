import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import root2py

in_file = sys.argv[1]
in_file = ROOT.TFile(sys.argv[1])
root_prof = in_file.Get('p_pHTvsSL_ECA')
py_prof = root2py.pyTProfile(root_prof,color='blue')
py_prof.plt.xlabel('lol')
py_prof.draw()
