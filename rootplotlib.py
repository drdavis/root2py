import ROOT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gsc
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from pylab import setp

mpl.rcParams['xtick.labelsize']  = 16
mpl.rcParams['ytick.labelsize']  = 16
mpl.rcParams['mathtext.fontset'] = 'stixsans'

mpl.rcParams['figure.facecolor']      = 'white'
mpl.rcParams['figure.subplot.bottom'] = 0.16
mpl.rcParams['figure.subplot.top']    = 0.95
mpl.rcParams['figure.subplot.left']   = 0.16
mpl.rcParams['figure.subplot.right']  = 0.95

# axes
mpl.rcParams['axes.labelsize']   = 18
mpl.rcParams['xtick.labelsize']  = 14
mpl.rcParams['xtick.major.size'] = 8
mpl.rcParams['xtick.minor.size'] = 4
mpl.rcParams['ytick.labelsize']  = 14
mpl.rcParams['ytick.major.size'] = 8
mpl.rcParams['ytick.minor.size'] = 4
mpl.rcParams['lines.markersize'] = 7

# legend
mpl.rcParams['legend.numpoints']    = 1
mpl.rcParams['legend.fontsize']     = 14
mpl.rcParams['legend.labelspacing'] = 0.3
mpl.rcParams['legend.frameon']      = False

plt.rcParams['image.cmap'] = 'viridis'
max_ratio_yticks           = 4

custom_plt = plt

def canvas_with_ratio(figsize=(8.75,5.92),height_ratios=[3.25,1]):
    fig = custom_plt.figure(figsize=figsize)
    gs  = gsc.GridSpec(2,1,height_ratios=height_ratios)
    gs.update(hspace=0.075)
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1],sharex=ax0)
    ax0.xaxis.set_minor_locator(AutoMinorLocator())
    ax0.yaxis.set_minor_locator(AutoMinorLocator())
    setp(ax0.get_xticklabels(),visible=False)

    return fig, ax0, ax1

class binned_object(object):
    """     
    A class to simply convert a single binned object
    into a set of numpy arrays.

    The general form of the numpy arrays which
    contain the bin centers, bin edges, bin contents
    (heights), and contents errors, is used througout
    other rootplotlib classes.
    
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
        self.contents = np.array([hist.GetBinContent(i+1)
                                  for i in range(hist.GetNbinsX())])
        self.error    = np.array([hist.GetBinError(i+1)
                                  for i in range(hist.GetNbinsX())])
        self.edges    = np.array([hist.GetXaxis().GetBinLowEdge(i+1)
                                  for i in range(hist.GetNbinsX()+1)])
        self.centers  = np.array([(hist.GetXaxis().GetBinWidth(i+1)*0.5 +
                                   hist.GetXaxis().GetBinLowEdge(i+1))
                                  for i in range(hist.GetNbinsX())])


class hist_stack(object):
    """
    A class to organize a set of histograms to be stacked. Optional to
    include data and a ratio plot.
    """
    def __init__(self,root_hists,data=None,ratio=None,colors=['black'],labels=['hist']):
        super(hist_stack,self).__init__()
        self.stack  = [binned_object(hist) for hist in root_hists]
        self.labels = labels
        self.colors = colors
        if data is None:
            self.data = data
        else:
            self.data = binned_object(data)
        if ratio is None:
            self.ratio = ratio
        else:
            self.ratio = binned_object(ratio)
            
    def draw(self,axis,ratio_axis=None,legend=True):
        axis.hist([stk.centers for stk in self.stack],bins=self.stack[0].edges,
                  weights=[stk.contents for stk in self.stack],color=self.colors,
                  label=self.labels,histtype='stepfilled',stacked=True)
        if self.data is not None:
            axis.errorbar(self.data.centers,self.data.contents,fmt='ko',
                          yerr=self.data.error,label='Data')
        if self.ratio is not None:
            ratio_axis.yaxis.set_major_locator(plt.MaxNLocator(max_ratio_yticks))
            ratio_axis.errorbar(self.ratio.centers,self.ratio.contents,fmt='ko',
                                yerr=self.ratio.error,label='Ratio')
            ratio_axis.plot(self.ratio.edges,np.array([1 for _ in self.ratio.edges]),'k--')
            ratio_axis.set_xlim([self.ratio.edges[0],self.ratio.edges[-1]])
        if legend:
            if self.data is not None:
                handles, labels = axis.get_legend_handles_labels()
                handles.insert(0,handles.pop(-1))
                labels.insert(0,labels.pop(-1))
                axis.legend(handles,labels,loc='best')
            else:
                axis.legend(loc='best')
