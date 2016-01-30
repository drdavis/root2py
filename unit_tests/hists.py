import ROOT
import numpy
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import root2py

hist1 = ROOT.TH1D('hist1','hist',100,-10,10)
hist2 = ROOT.TH1D('hist2','hist',100,-10,10)
hist3 = ROOT.TH1D('hist3','hist',100,-10,10)

hist1.FillRandom('gaus',2000)
hist2.FillRandom('gaus',10000)
hist3.FillRandom('gaus',1000)
hist3.Scale(10.2/hist3.Integral())

def check_plot_base():
    y = root2py.plot_base(xlim=[1,0],ylim=[1,2],titles=['b','c'])
    print y.xlim
    print y.ylim
    print y.titles

def check_single_hist():
    m = root2py.single_hist(hist1,
                            xlim=[-20,20],
                            ylim=[-100,1000],
                            titles=['a','b'],
                            color='green')
    m.draw(save='ok.eps')


def check_multi_hist():
    m = root2py.multi_hist((hist1,hist2),
                           colors=['red','green'],
                           histlabels=['redd','greenn'],
                           titles=['xaxis','yaxis'],
                           stacked=False,
                           data=None,
                           scatter=False,ratio=hist3)
    m.text(.05,.6,'testtext',style='italic')
    m.draw(awip=True)
    
check_plot_base()
check_single_hist()
check_multi_hist()
