"""
root2py
 
  a utility for converting ROOT (http://root.cern.ch/)
  objects into numpy arrays for plotting in matplotlib.

  authors: Doug Davis < ddavis@phy.duke.edu       >
           Vic Genty  < vgenty@nevis.columbia.edu >
"""

import ROOT
import numpy as np
import matplotlib.pyplot as plt

class pyTH1(object):
    """     
    A class to simply convert a single histogram from ROOT
    into a matplotlib histogram.
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

    def __init__(self,hist,color='blue',histtype='step'):

        self._root_hist = hist

        self.content = np.array([self._root_hist.GetBinContent(i+1)
                                 for i in xrange(self._root_hist.GetNbinsX())])
        self.error =  np.array([self._root_hist.GetBinError(i+1)
                                for i in xrange(self._root_hist.GetNbinsX())])
        self.bin_edges = np.array([self._root_hist.GetXaxis().GetBinLowEdge(i+1)
                                   for i in xrange(self._root_hist.GetNbinsX()+1)])
        self.bin_centers = np.array([(self._root_hist.GetXaxis().GetBinWidth(i+1)*0.5 +
                                      self._root_hist.GetXaxis().GetBinLowEdge(i+1))
                                     for i in xrange(self._root_hist.GetNbinsX())])

        self.plt = plt

        self.col   = color
        self.htype = histtype
        
    def draw(self):
        """ 
        draw the histogram in matplotlib
        """
        plt.hist(self.bin_centers,bins=self.bin_edges,weights=self.content,
                 histtype=self.htype,color=self.col)
        plt.show()
        

class pyTH1multi(object):
    """
    A class to plot multiple histograms from a set of
    ROOT histograms. This class is basically identical to
    pyTH1, but with the members now being lists, and a slightly
    more complex draw() function.

    created with pyTH1multi(hist1,hist2,...,hist2,keywords arguments)

    The labels and colors for this
    class must be given to the class definition function with
    the keywords labels and cols. For example:
    labels=['a','b','c'] 
    cols=['blue,'red','green']

    other keywords: histtype, stacked
    """

    def __init__(self,*args,**kwargs):
        self.hists  = args
        self.pyTH1s = [pyTH1(hist) for hist in self.hists]

        self.content_list     = [h.content     for h in self.pyTH1s]
        self.error_list       = [h.error       for h in self.pyTH1s]
        self.bin_edges_list   = [h.bin_edges   for h in self.pyTH1s]
        self.bin_centers_list = [h.bin_centers for h in self.pyTH1s]

        self.plt = plt

        if 'labels' not in kwargs:
            self.labels = ['hist'+str(i) for i in xrange(len(args))]
        else:
            self.labels = kwargs.get('labels')
            if len(self.labels) != len(args):
                exit('bad labels length')

        if 'cols' not in kwargs:
            self.cols = ['blue' for _ in xrange(len(args))]
        else:
            self.cols = kwargs.get('cols')
            if len(self.cols) != len(args):
                exit('bad cols length')

        if 'histtype' in kwargs:
            self.htype = kwargs.get('histtype')
        else:
            self.htype = 'step'

        if 'stacked' in kwargs:
            self.stk = kwargs.get('stacked')
        else:
            self.stk = False
            
            
    def draw(self,legend=True):
        """
        Draw the stacked histograms.
        The legend can be turned off with legend=False
        """
        plt.hist(self.bin_centers_list,
                 bins=self.bin_edges_list[0],
                 weights=self.content_list,
                 label=self.labels,
                 color=self.cols,
                 histtype=self.htype,
                 stacked=self.stk)
        if legend:
            plt.legend(loc='best')
        else:
            pass
        plt.show()

class pyTH1multiWithRatio(pyTH1multi):
    """
    Similar to pyTH1multi but with the added
    feature of handling a ratio histogram.
    Needless to say the ratio histogram is assumed
    to have the same binning as the main histograms.
    """

    def __init__(self,*args,**kwargs):
        pyTH1multi.__init__(self,*args,**kwargs)
        if 'ratio' not in kwargs:
            exit('specify ratio histogram')
        self.ratio_hist = kwargs.get('ratio')
        
    def draw(self,legend=True):
        print 'tbi'

        
class pyTGraph(object):
    """
    xy_pairs : [[x1,y1],...,[xN,yN]]
    """
    def __init__(self,tgraph):
        self._root_tgraph = tgraph
        self.xy_pairs = np.vstack((np.frombuffer(self._root_tgraph.GetX(),
                                                 count=self._root_tgraph.GetN()),
                                   np.frombuffer(self._root_tgraph.GetY(),
                                                 count=self._root_tgraph.GetN()))).T
        
    def draw(self):
        """ draw the scatter in matplotlib """
        plt.plot(self.xy_pairs.T[0],self.xy_pairs.T[1],'bo')
        plt.show()
