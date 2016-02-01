import seaborn as sns
from matplotlib.figure import Figure
import numpy as np


def bar_fig(series):
    '''
    Returns a bar chart of the values for the series.
    Inputs
    ------
    series:
        A pandas Series where the index will represent the x-axis and the 
        values will represent the y-axis.
    '''
    # Create figure and axes
    fig = Figure()
    ax = fig.add_subplot(111)
    
    sns.barplot(x = series.index, 
                y = series.values, 
                ax = ax)
    if series.name:
        ax.set_ylabel(series.name)

    return fig
    

def bar_count_fig(series):
    '''
    Returns a bar chart of the number of times each item appears in the index.

    Inputs
    ------
    series:
        a pandas Series of dttype object, with one or more repeated values
    '''
    # Create figure and axes
    fig = Figure()
    ax = fig.add_subplot(111)
    
    counts = series.value_counts()
    sns.barplot(x = counts.index, 
                y = counts.values, 
                ax = ax)

    return fig


def confmat_fig(series):
    '''
    Returns a figure with a confusion matrix.
    
    Inputs
    ------
    series:
        a pandas Series with a number of values
    '''
    # Create figure and axes
    fig = Figure()
    ax = fig.add_subplot(111)
    srs = series.apply(str)
    series_name = srs.name
    y = srs.reset_index()
    index_name = srs.index.name
    if not index_name:
        index_name = 'index'
    y['value'] = 1
    z = y.pivot(index = index_name, 
                columns = series_name, 
                values = 'value')
    z[z.isnull()] = 0
    z = z.T
    sns.heatmap(z, square = True, ax = ax)
    
    return fig
    

def distribution_fig(series):
    '''
    Returns a figure with a distribution plot
    
    Inputs
    ------
    series:
        a pandas Series with numeric values
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    
    series = series.replace([np.inf, -np.inf], np.nan).dropna()
    sns.distplot(series, ax = ax)
    
    return fig
    

def pie_fig(series):
    '''
    Returns a figure with a pie chart with slice angle proportional to the
    relative size of the values in the series.

    Inputs
    ------
    series:
        a pandas Series with numeric values
    '''
    fig = Figure()
    ax = fig.add_subplot(111)

    series.plot(kind = 'pie', ax = ax)
    return fig
    