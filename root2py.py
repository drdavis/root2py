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

class plotBase(object):
    def __init__(self,**kwargs):
        super(plotBase,self).__init__()
        
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
            
class binnedObject(plotBase):
    """     
    A class to simply convert a single binned object
    from ROOT into a matplotlib histogram/plot.

    The general form of the numpy arrays which
    contain the bin centers, bin edges, bin content
    (heights), and content errors, is used througout.
    
    This class has access to matplotlib.pyplot as plt
    for configuring titles, axes, rangers, etc.
    This configuring must be handled before the draw(...)
    function is called.

    Members
    -------

    content:     the height of each bin
    error:       the error of each bin
    bin_edges:   the bin edges |____|____|____|___..
                              [0]  [1]  [2]  [3]     
    bin_centers: the centers of each bin |_____|_____|_____|__...
                                           [0]   [1]   [2]

    possible keywords: color, histtype
    """
    def __init__(self,hist,color='blue',histtype='step',**kwargs):
        super(binnedObject,self).__init__(**kwargs)
        self._root_hist  = hist
        self.content     = np.array([self._root_hist.GetBinContent(i+1)
                                     for i in xrange(self._root_hist.GetNbinsX())])
        self.error       =  np.array([self._root_hist.GetBinError(i+1)
                                      for i in xrange(self._root_hist.GetNbinsX())])
        self.bin_edges   = np.array([self._root_hist.GetXaxis().GetBinLowEdge(i+1)
                                     for i in xrange(self._root_hist.GetNbinsX()+1)])
        self.bin_centers = np.array([(self._root_hist.GetXaxis().GetBinWidth(i+1)*0.5 +
                                      self._root_hist.GetXaxis().GetBinLowEdge(i+1))
                                     for i in xrange(self._root_hist.GetNbinsX())])
    
        self.color = color
        self.htype = histtype

    def draw(self,save=None):
        self.plt.hist(self.bin_centers,self.bin_edges,weights=self.content,
                      histtype=self.htype,color=self.color)
        if self.xlim:
            self.plt.xlim(self.xlim)
        if self.ylim:
            self.plt.ylim(self.ylim)

        self.plt.xlabel(self.titles[0])
        self.plt.ylabel(self.titles[1])
            
        if save:
            self.plt.savefig(save)
        self.plt.show()
        
