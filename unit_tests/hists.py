import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import rootplotlib

hist1 = ROOT.TH1D('hist1','hist',100,-10,10)
hist2 = ROOT.TH1D('hist2','hist',100,-10,10)
hist3 = ROOT.TH1D('hist3','hist',100,-10,10)

hist1.FillRandom('gaus',2000)
hist2.FillRandom('gaus',10000)
hist3.FillRandom('gaus',1000)
hist3.Scale(10.2/hist3.Integral())

def check_multi_hist():
    stack = rootplotlib.hist_stack([hist1,hist2,hist3],
                                   data=hist1,ratio=hist3,
                                   colors=['red','green','orange'],
                                   labels=['a','b','c'])

    fig, ax0, ax1 = rootplotlib.canvas()
    stack.draw(ax0,ratio_axis=ax1)
    ax1.set_xlabel('lol')
    ax1.set_ylabel('ratio')
    ax0.set_ylabel('alright')

    fig.savefig('test.eps')

check_multi_hist()
