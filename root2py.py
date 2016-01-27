import ROOT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gsc
from pylab import setp

mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
max_yticks                      = 5

class err(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class plot_base(object):
    def __init__(self,**kwargs):
        super(plot_base,self).__init__()
        
        self.plt = plt

        if 'xlim' in kwargs:
            self.xlim = kwargs.get('xlim')
            if type(self.xlim) is not type([0,0]) or len(self.xlim) != 2:
                raise err('xlim must be a two element list')
        else:
            self.xlim = False
        if 'ylim' in kwargs:
            self.ylim = kwargs.get('ylim')
            if type(self.ylim) is not type([0,0]) or len(self.ylim) != 2:
                raise err('ylim must be a two element list')
        else:
            self.ylim = False
        if 'titles' in kwargs:
            self.titles = kwargs.get('titles')
            if type(self.titles) is not type(['a','b']) or len(self.titles) != 2:
                raise err('titles must be a two element list')
        else:
            self.titles = [' ',' ']
            
class binned_object(object):
    """     
    A class to simply convert a single binned object
    into a set of numpy arrays.

    The general form of the numpy arrays which
    contain the bin centers, bin edges, bin contents
    (heights), and contents errors, is used througout
    other root2py classes.
    
    Members
    -------

    contents:     the height of each bin
    error:       the error of each bin
    edges:   the bin edges |____|____|____|___..
                              [0]  [1]  [2]  [3]     
    centers: the centers of each bin |_____|_____|_____|__...
                                           [0]   [1]   [2]

    """
    def __init__(self,hist):
        super(binned_object,self).__init__()
        
        self._root_hist  = hist

        self.contents = np.array([self._root_hist.GetBinContent(i+1)
                                  for i in xrange(self._root_hist.GetNbinsX())])
        self.error    = np.array([self._root_hist.GetBinError(i+1)
                                  for i in xrange(self._root_hist.GetNbinsX())])
        self.edges    = np.array([self._root_hist.GetXaxis().GetBinLowEdge(i+1)
                                  for i in xrange(self._root_hist.GetNbinsX()+1)])
        self.centers  = np.array([(self._root_hist.GetXaxis().GetBinWidth(i+1)*0.5 +
                                   self._root_hist.GetXaxis().GetBinLowEdge(i+1))
                                  for i in xrange(self._root_hist.GetNbinsX())])

class single_hist(plot_base):
    """
    A single histogram.
    
    """
    def __init__(self,roothist,color='blue',histtype='step',**kwargs):
        super(single_hist,self).__init__(**kwargs)
        self.bo = binned_object(roothist)
        self.color = color
        self.histtype = histtype

    def draw(self,save=None):
        self.plt.hist(self.bo.centers,bins=self.bo.edges,weights=self.bo.contents,
                      histtype=self.histtype,color=self.color)
        if self.xlim:
            self.plt.xlim(self.xlim)
        if self.ylim:
            self.plt.ylim(self.ylim)

        self.plt.xlabel(self.titles[0])
        self.plt.ylabel(self.titles[1])
            
        if save:
            self.plt.savefig(save)
        self.plt.show()

class multi_hist(plot_base):
    """
    A set of histograms on a single canvas
    """
    def __init__(self,hists,histtype='stepfilled',stacked=False,
                 scatter=False,data=None,ratio=None,**kwargs):
        super(multi_hist,self).__init__(**kwargs)
        self.bos = [binned_object(h) for h in hists]
        if data:
            self.data = binned_object(data)
        else:
            self.data = None
        if ratio:
            self.ratio = binned_object(ratio)
        else:
            self.ratio = None
        self.contents = [bo.contents for bo in self.bos]
        self.errors = [bo.error for bo in self.bos]
        self.edges = [bo.edges for bo in self.bos]
        self.centers = [bo.centers for bo in self.bos]
        self.colors = kwargs.get('colors')
        self.histtype = histtype
        self.scatter = scatter
        self.histlabels = kwargs.get('histlabels')
        self.stacked = stacked
        if len(self.bos) != len(self.colors) or len(self.bos) != len(self.histlabels):
            raise err('colors and histlabels must have length equal the number of histograms')

        if self.ratio:
            self.fig = self.plt.figure(figsize=(9,6))
            self.gs  = gsc.GridSpec(2,1,height_ratios=[3,1])
            self.gs.update(hspace=0.075)
            self.ax0 = self.plt.subplot(self.gs[0])
            self.ax1 = self.plt.subplot(self.gs[1],sharex=self.ax0)
            setp(self.ax0.get_xticklabels(),visible=False)
            self.c0 = self.ax0
            self.c1 = self.ax1
        else:
            self.c0 = self.plt


    def text(self,x,y,line):
        if self.ratio:
            self.c0.text(x,y,line,transform=self.c0.transAxes)
        else:
            print 'Warning: multi_hist.text is only available when plotting with a ratio'
            
    def draw(self,save=None,legend=True,legendfontsize=12):

        if self.scatter == False:
            self.c0.hist(self.centers,bins=self.edges[0],weights=self.contents,
                         label=self.histlabels,color=self.colors,
                         histtype=self.histtype,stacked=self.stacked)
        else:
            for i in xrange(len(self.bos)):
                self.c0.errorbar(self.centers[i],
                                 self.contents[i],
                                 yerr=self.errors[i],
                                 fmt='o',color=self.colors[i],label=self.histlabels[i])
            
        if self.data:
            self.c0.errorbar(self.data.centers,self.data.contents,
                             fmt='ko',yerr=self.data.error)

        if self.ratio:
            self.c1.errorbar(self.ratio.centers,self.ratio.contents,
                             fmt='ko',yerr=self.ratio.error)
            self.c1.plot(np.linspace(self.edges[0][0],self.edges[0][-1],100),
                         np.array([1 for i in xrange(100)]),'k--')
        
        if self.xlim:
            if self.ratio:
                self.c1.set_xlim(self.xlim)
            else:
                self.c0.xlim(self.xlim)
        if self.ylim:
            if self.ratio:
                self.c0.set_ylim(self.xlim)
            else:
                self.c0.ylim(self.ylim)

        if self.ratio:
            self.c0.set_ylabel(self.titles[1])
            self.c1.set_xlabel(self.titles[0])
        else:
            self.plt.xlabel(self.titles[0])
            self.plt.ylabel(self.titles[1])

        if legend:
            self.c0.legend(loc='best',numpoints=1,fontsize=legendfontsize)
            
        if save:
            self.plt.savefig(save)
        self.plt.show()

