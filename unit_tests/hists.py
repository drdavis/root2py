import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import rootplotlib

hist1 = ROOT.TH1D('hist1','hist',11,-3.5,3.5)
hist2 = ROOT.TH1D('hist2','hist',11,-3.5,3.5)
hist3 = ROOT.TH1D('hist3','hist',11,-3.5,3.5)
hist4 = ROOT.TH1D('hist4','hist',11,-3.5,3.5)
hist5 = ROOT.TH1D('hist5','hist',11,-3.5,3.5)
hist1.FillRandom('gaus',2000)
hist2.FillRandom('gaus',2000)
hist3.FillRandom('gaus',10)
hist3.Scale(10.2/hist3.Integral())
hist4.Add(hist1)
hist4.Divide(hist2)

hist5.Add(hist1)
hist5.Add(hist2)
hist5.Add(hist3)

def check_multi_hist():
    stack = rootplotlib.hist_stack([hist1,hist2,hist3],
                                   data=hist5,ratio=hist4,
                                   colors=['blue','orange','green'],
                                   labels=['a','b','c'])

    fig, ax0, ax1 = rootplotlib.canvas_with_ratio()
    stack.draw(ax0,ratio_axis=ax1)
    ax1.set_xlabel('lol')
    ax1.set_ylabel('ratio')
    ax0.set_ylabel('alright')

    fig.savefig('test.eps')

def check_profile():
    profstuff = rootplotlib.profile_set([hist1,hist2,hist3],
                                        colors=['blue','orange','green'],
                                        labels=['a','b','c'],
                                        ratio=hist4)
    fig, ax0, ax1 = rootplotlib.canvas_with_ratio()
    profstuff.draw(ax0,ratio_axis=ax1)
    fig.savefig('prof.eps')

    p2 = rootplotlib.profile_set([hist1,hist2],
                                 colors=['black','green'],
                                 labels=['z','w'])
    fig, ax0 = rootplotlib.canvas(xtitle='ok')
    p2.draw(ax0)
    fig.savefig('prof2.eps')
    
check_multi_hist()
check_profile()
