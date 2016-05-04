import ROOT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gsc
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from pylab import setp

families = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']

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
max_ratio_yticks           = 5
            
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
        self.rhist  = hist

        self.contents = np.array([self.rhist.GetBinContent(i+1)
                                  for i in range(self.rhist.GetNbinsX())])
        self.error    = np.array([self.rhist.GetBinError(i+1)
                                  for i in range(self.rhist.GetNbinsX())])
        self.edges    = np.array([self.rhist.GetXaxis().GetBinLowEdge(i+1)
                                  for i in range(self.rhist.GetNbinsX()+1)])
        self.centers  = np.array([(self.rhist.GetXaxis().GetBinWidth(i+1)*0.5 +
                                   self.rhist.GetXaxis().GetBinLowEdge(i+1))
                                  for i in range(self.rhist.GetNbinsX())])


class hist_stack(object):
    """
    A class to organize a set of histograms to be stacked. Optional to
    include data and a ratio plot.
    """
    def __init__(self,root_hists,data=None,colors=['black' for _ in range(len(root_hists))],
                 labels=['hist'+str(i) for i in range(len(root_hists))],ratio=None):
        super(binned_object,self).__init__()
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
            
    def draw(self,axis,ratio_axis=None):
        axis.hist([stk.centers for stk in self.stack],bins=self.stack[0].bin_edges,
                  weights=[stk.contents for stk in self.stack],color=self.color,
                  label=self.labels,histtype='stepfilled',stacked=True)
        if self.data is None:
            pass
        else:
            axis.errorbar(self.data.centers,self.data.contents,fmt='ko',
                          yerr=self.data.error,label='Data')
        if self.ratio is None:
            pass
        else:
            ratio_axis.errorbar(self.ratio.centers,self.ratio.contents,fmt='ko',
                                yerr=self.ratio.error,label='Ratio')
