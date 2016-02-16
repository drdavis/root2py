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
                if self.xlim != False:
                    raise err('xlim must be a two element list')
        else:
            self.xlim = False
            
        if 'ylim' in kwargs:
            self.ylim = kwargs.get('ylim')
            if type(self.ylim) is not type([0,0]) or len(self.ylim) != 2:
                if self.ylim != False:
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

    contents: the height of each bin

    error:    the error of each bin height

    edges:    the bin edges |____|____|____|___..
                           [0]  [1]  [2]  [3]     

    centers:  the centers of each bin |_____|_____|_____|__...
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

        self.plt.xlabel(self.titles[0],size=14)
        self.plt.ylabel(self.titles[1],size=14)
            
        if save:
            self.plt.savefig(save)
        self.plt.show()

class multi_hist(plot_base):
    """
    A set of histograms on a single canvas
    """
    def __init__(self,hists,histtype='stepfilled',figsize=(8.5,6),stacked=False,
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
        if 'ratiotitle' in kwargs:
            self.ratiotitle = kwargs.get('ratiotitle')
        else:
            self.ratiotitle = 'Ratio'
        self.contents = [bo.contents for bo in self.bos]
        self.errors = [bo.error for bo in self.bos]
        self.edges = [bo.edges for bo in self.bos]
        self.centers = [bo.centers for bo in self.bos]
        self.colors = kwargs.get('colors')
        self.fmts = kwargs.get('fmts')
        self.histtype = histtype
        self.scatter = scatter
        self.histlabels = kwargs.get('histlabels')
        self.stacked = stacked
        if len(self.bos) != len(self.colors) or len(self.bos) != len(self.histlabels) or len(self.fmts) != len(self.bos):
            raise err('colors, fmts, and histlabels must have length equal the number of histograms')

        self.fig = self.plt.figure(figsize=figsize)

        if self.ratio:
            self.gs  = gsc.GridSpec(2,1,height_ratios=[3.25,1])
            self.gs.update(hspace=0.075)
            self.ax0 = self.fig.add_subplot(self.gs[0])
            self.ax1 = self.fig.add_subplot(self.gs[1],sharex=self.ax0)
            setp(self.ax0.get_xticklabels(),visible=False)
            self.c0 = self.ax0
            self.c1 = self.ax1
        else:
            self.ax0 = self.fig.add_subplot(111)
            self.c0  = self.ax0

    def text(self,x,y,line,style=None,size=12,manualcoords=False):
        if not manualcoords:
            self.c0.text(x,y,line,transform=self.c0.transAxes,style=style,size=size)
        else:
            self.c0.text(x,y,line,style=style,size=size)
            
    def draw(self,show=True,save=None,legend=True,legendloc='best',legendfontsize=12,
             asi=False,awip=False,ai=False):

        if self.scatter == False:
            self.c0.hist(self.centers,bins=self.edges[0],weights=self.contents,
                         label=self.histlabels,color=self.colors,
                         histtype=self.histtype,stacked=self.stacked)
        else:
            for i in xrange(len(self.bos)):
                self.c0.errorbar(self.centers[i],
                                 self.contents[i],
                                 yerr=self.errors[i],
                                 fmt=self.fmts[i],color=self.colors[i],
                                 label=self.histlabels[i])
            
        if self.data:
            self.c0.errorbar(self.data.centers,self.data.contents,
                             fmt='ko',yerr=self.data.error,label='Data')
        else:
            pass

        if self.ratio:
            self.c1.errorbar(self.ratio.centers,self.ratio.contents,
                             fmt='ko',yerr=self.ratio.error)
            self.c1.plot(np.linspace(self.edges[0][0],self.edges[0][-1],100),
                         np.array([1 for i in xrange(100)]),'k--')

            self.c0.set_ylabel(self.titles[1],size=14)
            self.c1.set_xlabel(self.titles[0],size=14)
            self.c1.set_ylabel(self.ratiotitle,size=14)
            self.c1.yaxis.set_major_locator(self.plt.MaxNLocator(max_yticks))

        else:
            self.plt.xlabel(self.titles[0],size=14)
            self.plt.ylabel(self.titles[1],size=14)
            
        if self.xlim:
            if self.ratio:
                self.c1.set_xlim(self.xlim)
            else:
                self.c0.set_xlim(self.xlim)
        if self.ylim:
            if self.ratio:
                self.c0.set_ylim(self.ylim)
            else:
                self.c0.set_ylim(self.ylim)

        if int(asi + awip + ai) > 1:
            raise err('you can only choose one of the keywords si, awip, ai to be true')

        pa   = lambda s     : self.text(.02,.92,'ATLAS',style='italic',size=s)
        psup = lambda st, s : self.text(.12,.92,st,size=s)        
        if asi:  pa(14), psup('Simulation Internal',14)
        if awip: pa(14), psup('Work in Progress',14)
        if ai:   pa(14), psup('Internal',14)
            
        if legend:
            self.c0.legend(loc=legendloc,numpoints=1,fontsize=legendfontsize)
            
        if save:
            self.plt.savefig(save)
        
        if show:
            self.plt.show()
        else:
            pass

class unbinned_object(object):
    def __init__(self,obj,objtype='TGraph'):
        super(unbinned_object,self).__init__()
        if objtype != 'TGraph':
            raise err('only objtype \'TGraph\' supported at this time')
        self.root_tgraph = obj

        self.xy_pairs = np.vstack((np.frombuffer(self.root_tgraph.GetX(),
                                                 count=self.root_tgraph.GetN()),
                                   np.frombuffer(self.root_tgraph.GetY(),
                                                 count=self.root_tgraph.GetN()))).T

class single_tgraph(plot_base):
    def __init__(self,obj,objtype='TGraph',**kwargs):
        super(single_tgraph,self).__init__(**kwargs)
        self.xy_pairs = unbinned_object(obj,objtype).xy_pairs
        self.x = self.xy_pairs.T[0]
        self.y = self.xy_pairs.T[1]

    def draw(self,save=None):
        self.plt.plot(self.x,self.y,'bo')

        if self.xlim:
            self.plt.xlim(self.xlim)
        if self.ylim:
            self.plt.ylim(self.ylim)

        self.plt.xlabel(self.titles[0])
        self.plt.ylabel(self.titles[1])
            
        if save:
            self.plt.savefig(save)
        self.plt.show()
