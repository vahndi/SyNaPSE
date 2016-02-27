from matplotlib.figure import Figure


def dataframegroupby_fig(dataframegroupby):
    '''
    Returns a figure with a boxplot
    
    Inputs
    ------
    dataframegroupby
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    dataframegroupby.boxplot(ax = ax)
    return fig   