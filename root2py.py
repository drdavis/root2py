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
    """ content:     the height of each bin
        error:       the error of each bin
        bin_edges:   the bin edges |____|____|____|___..
                                  [0]  [1]  [2]  [3]     
        bin_centers: the centers of each bin |_____|_____|_____|__...
                                               [0]   [1]   [2]          """
    def __init__(self,hist):

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

    def draw(self,col='blue',htype='step',titles=['main title','x title','y title']):
        """ draw the histogram in matplotlib """
        plt.hist(self.bin_centers,bins=self.bin_edges,weights=self.content,
                 histtype=htype,color=col)
        plt.title(titles[0])
        plt.xlabel(titles[1])
        plt.ylabel(titles[2])
        plt.show()
        
    
class pyTGraph(object):
    """ xy_pairs : [[x1,y1],...,[xN,yN]] """
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
