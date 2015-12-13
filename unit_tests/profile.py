import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import root2py

in_file = sys.argv[1]
in_file = ROOT.TFile(sys.argv[1])
root_prof1 = in_file.Get('h_pHT_v_SL_ECA')
root_prof2 = in_file.Get('h_pHT_v_SL_ECC')

py_profs = root2py.pyTProfileMulti(root_prof1,root_prof2,
                                   cols=['red','orange'],
                                   labels=['ECA','ECC'])
py_profs.plt.xlabel('Straw Layer')
py_profs.plt.ylabel(r'$p_{\mathrm{HT}}$')
py_profs.draw(legend=True)

#py_prof = root2py.pyTProfile(root_prof,color='blue')
#py_prof.plt.xlabel('lol')
#py_prof.draw()


