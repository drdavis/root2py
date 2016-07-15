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
mpl.rcParams['axes.labelsize']   = 16
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

def canvas_with_ratio(figsize=(8.75,5.92),height_ratios=[3.25,1],
                      xtitle='x title',ytitle='ytitle',ratio_title='Ratio'):
    fig = custom_plt.figure(figsize=figsize)
    gs  = gsc.GridSpec(2,1,height_ratios=height_ratios)
    gs.update(hspace=0.075)
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1],sharex=ax0)
    ax0.xaxis.set_minor_locator(AutoMinorLocator())
    ax0.yaxis.set_minor_locator(AutoMinorLocator())
    setp(ax0.get_xticklabels(),visible=False)

    ax0.set_ylabel(ytitle)
    ax1.set_ylabel(ratio_title)
    ax1.set_xlabel(xtitle)
    return fig, ax0, ax1

def canvas(figsize=(8.75,5.92),height_ratios=[3.25,1],xtitle='x title',ytitle='ytitle'):
    fig = custom_plt.figure(figsize=figsize)
    ax0 = fig.add_subplot(111)
    ax0.set_ylabel(ytitle)
    ax0.set_xlabel(xtitle)
    ax0.xaxis.set_minor_locator(AutoMinorLocator())
    ax0.yaxis.set_minor_locator(AutoMinorLocator())
    return fig, ax0

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

    errors:    the error of each bin height

    edges:    the bin edges |____|____|____|___..
                           [0]  [1]  [2]  [3]     

    centers:  the centers of each bin |_____|_____|_____|__...
                                        [0]   [1]   [2]

    """
    def __init__(self,hist):
        super(binned_object,self).__init__()
        self.contents = np.array([hist.GetBinContent(i+1)
                                  for i in range(hist.GetNbinsX())])
        self.errors   = np.array([hist.GetBinError(i+1)
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
    def __init__(self,root_hists,data=None,ratio=None,colors=['black'],labels=['hist'],
                 histtype='stepfilled',stacked=True,normed=False):
        super(hist_stack,self).__init__()
        self.stack    = [binned_object(hist) for hist in root_hists]
        self.labels   = labels
        self.colors   = colors
        self.histtype = histtype
        self.stacked  = stacked
        self.normed   = normed
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
                  label=self.labels,histtype=self.histtype,stacked=self.stacked,
                  normed=self.normed)
        if self.data is not None:
            axis.errorbar(self.data.centers,self.data.contents,fmt='ko',
                          yerr=self.data.errors,label='Data')
        if self.ratio is not None:
            ratio_axis.yaxis.set_major_locator(plt.MaxNLocator(max_ratio_yticks))
            ratio_axis.errorbar(self.ratio.centers,self.ratio.contents,fmt='ko',
                                yerr=self.ratio.errors,label='Ratio')
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

class profile_set(object):
    """
    A class to organize a set of profile histograms. Optional to
    include a ratio plot.
    """
    def __init__(self,root_profiles,ratio=None,colors=['black'],labels=['hist'],delzeros=False):
        super(profile_set,self).__init__()
        self.profiles = [binned_object(prof) for prof in root_profiles]
        self.labels   = labels
        self.colors   = colors
        if ratio is None:
            self.ratio = ratio
        else:
            self.ratio = binned_object(ratio)

        self.og_min, self.og_max = self.profiles[0].edges[0], self.profiles[0].edges[-1]
        if delzeros:
            for prof in self.profiles:
                indices = [i for i, co in enumerate(prof.contents) if co == 0]
                for index in sorted(indices, reverse=True):
                    prof.contents = np.delete(prof.contents,index)
                    prof.centers  = np.delete(prof.centers, index)
                    prof.edges    = np.delete(prof.edges,   index)
                    prof.errors   = np.delete(prof.errors,  index)
            if ratio is not None:
                indices = [i for i, co in enumerate(self.ratio.contents) if co == 0]
                for index in sorted(indices, reverse=True):
                    self.ratio.contents = np.delete(self.ratio.contents,index)
                    self.ratio.centers  = np.delete(self.ratio.centers, index)
                    self.ratio.edges    = np.delete(self.ratio.edges,   index)
                    self.ratio.errors   = np.delete(self.ratio.errors,  index)

    def draw(self,axis,ratio_axis=None,legend=True):
        for prof, label, color in zip(self.profiles,self.labels,self.colors):
            axis.errorbar(prof.centers,prof.contents,yerr=prof.errors,label=label,color=color,fmt='o')
            axis.set_xlim([self.og_min,self.og_max])
        if self.ratio is not None:
            ratio_axis.yaxis.set_major_locator(custom_plt.MaxNLocator(max_ratio_yticks))
            ratio_axis.errorbar(self.ratio.centers,self.ratio.contents,yerr=self.ratio.errors,fmt='ko')
            ratio_axis.plot(np.linspace(self.og_min,self.og_max,100),
                            np.array([1 for _ in range(100)]),'k--')
            ratio_axis.set_xlim([self.og_min,self.og_max])
        if legend:
            axis.legend(loc='best')
