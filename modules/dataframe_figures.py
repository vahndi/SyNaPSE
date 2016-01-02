from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix
from matplotlib.markers import MarkerStyle
from plotFunctions import getFigureShape
import seaborn as sns
from pandas import melt
markers = MarkerStyle.filled_markers

# Definitions
# -----------
# A wide-form dataframe is a dataframe where each column represents a variable
# A long-form dataframe is a dataframe where the each row represents the value
# of a variable, and one or more of the columns contains a categorical value,
# which represents the corresponding variable(s)

def bar_fig_grouped_wf(dataframe):
    '''
    Returns a bar chart, grouped by the category in the index column.
    
    Inputs
    ------
    dataframe:
        A wide-form dataframe with an index with unique categorical values.
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    df_plot = dataframe.copy(deep = True)
    float_cols = list(df_plot.select_dtypes(['floating']).columns)
    df_plot['index'] = df_plot.index
    dfMelt = melt(df_plot, 
                  id_vars = 'index', 
                  value_vars = float_cols)
    sns.barplot(data = dfMelt, ax = ax, hue = 'variable',
                x = 'index', y = 'value')
    return fig


def box_fig_lf(dataframe):
    '''
    Returns a figure with a boxplot

    Inputs
    ------
    dataframe:
        a long-form dataframe with a dtype=object column containing the 
        instance categories and a dtype=numeric column containing the 
        associated instance values
    '''    
    fig = Figure()
    ax = fig.add_subplot(111)
    sns.boxplot(data = dataframe, ax = ax,
                x = dataframe.select_dtypes([object]).columns[0], 
                y = dataframe.select_dtypes(['number']).columns[0])
    return fig


def box_fig_wf(dataframe):
    '''
    Returns a figure with a boxplot
    
    Inputs
    ------
    dataframe:
        A wide-form dataframe with all numeric columns. Each column represents
        a separate variable.
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    sns.boxplot(data = dataframe, ax = ax)
    return fig    


def box_fig_grouped_wf(dataframe):
    '''
    Returns a figure with a grouped boxplot, where the hue corresponds to the 
    value in the first column with object dtype
    
    Inputs
    ------
    dataframe:
        A wide-form dataframe, with multiple numeric columns and an object
        column
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    df_numeric = dataframe.select_dtypes(['number'])
    df_object = dataframe.select_dtypes([object])
    dfMelt = melt(dataframe,
                  value_vars = list(df_numeric.columns), 
                  id_vars = list(df_object.columns))
    sns.boxplot(data = dfMelt, 
                x = 'variable', y = 'value',
                hue = df_object.columns[0],
                ax = ax)
    return fig


def confmat_fig(dataframe):
    '''
    Returns a figure with a confusion matrix.
    
    Inputs
    ------
    dataframe:
        a wide-form dataframe where all column dtypes are integer
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    sns.heatmap(dataframe,
                annot = True, square = True,
                fmt = 'd', ax = ax)
    ax.set_xlim([0, len(dataframe.columns)])
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    return fig


def confmat_cat__a_fig(dataframe):
    '''
    Returns a figure with multiple confusion matrices, categorised by the 3rd
    column with dtype=object. Each category is plotted on a separate axis.
    
    Inputs
    ------
    dataframe: 
        A long-form dataframe where the first two columns represent the
        categories to display along the x and y axes. The number of repeats of 
        each pair of values will be the count plotted in the heatmap. The value
        in the third column determines which axis each pair of values
        corresponds to.
    '''
    fig = Figure()
    col0 = dataframe.columns[0]
    col1 = dataframe.columns[1]
    axis_col = dataframe.columns[2]
    axis_names = list(dataframe[axis_col].unique())
    r, c = getFigureShape(len(axis_names))
    i_ax = 0
    for a in axis_names:
        i_ax += 1
        ax = fig.add_subplot(r, c, i_ax)
        ax.set_title(a)
        sub_df = dataframe[dataframe[axis_col] == a]
        conf_mat = confusion_matrix(sub_df[col0], sub_df[col1])
        sns.heatmap(conf_mat,
                    annot = True, square = True,
                    fmt = 'd', ax = ax)
        ax.legend()
    return fig    


def distribution_fig(dataframe):
    '''
    Returns a figure with a distribution plot
    
    Inputs
    ------
    dataframe:
        a dataframe with a single numeric column variable
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    sns.distplot(dataframe, ax = ax)
    return fig


def scatter_fig(dataframe):
    '''
    Returns a figure with a scatter plot
    
    Inputs
    ------    
    dataframe:
        a long-form dataframe with 2 numeric columns
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    sns.regplot(data = dataframe, fit_reg = False, ax = ax,
                x = dataframe.select_dtypes(['number']).columns[0], 
                y = dataframe.select_dtypes(['number']).columns[1])
    return fig


def scatter_cat__c_fig(dataframe):
    '''
    Returns a figure with a scatter plot.
    The instances are coloured by the category given by the value in the first 
    object-dtype column.
    
    Inputs
    ------    
    dataframe:
        a long-form dataframe with 2 numeric columns and 1 object column
    '''
    fig = Figure()
    ax = fig.add_subplot(111)    
    categorical = dataframe.select_dtypes([object])
    numeric = dataframe.select_dtypes(['number'])
    cat_col = categorical.columns[0]
    cat_col_values = categorical[cat_col].unique()
    for cat_col_value in cat_col_values:
        sub_df = dataframe[dataframe[cat_col] ==  cat_col_value]
        sns.regplot(data = sub_df, fit_reg = False, ax = ax,
                    x = numeric.columns[0], y = numeric.columns[1], 
                    label = cat_col_value)
        ax.legend()
    return fig
    

def scatter_cat__cm_fig(dataframe):
    '''
    Returns a figure with a scatter plot.
    The instances are coloured by the category given by the value in the first 
    object-dtype column and have a marker shape determined by the value in the
    second object-dtype column.

    Inputs
    ------    
    dataframe:
        a long-form dataframe with 2 numeric columns and 2 object columns
    '''
    fig = Figure()
    ax = fig.add_subplot(111)
    categorical = dataframe.select_dtypes([object])
    numeric = dataframe.select_dtypes(['number'])
    colour_col = categorical.columns[0]
    marker_col = categorical.columns[1]
    colour_labels = sorted(categorical[colour_col].unique())
    marker_labels = sorted(categorical[marker_col].unique())
    palette = sns.color_palette('cubehelix', len(colour_labels))
    for m in marker_labels:
        for c in colour_labels:
            sub_df = dataframe[(dataframe[marker_col] == m) &
                               (dataframe[colour_col] == c)]            
            sns.regplot(
                    data = sub_df, fit_reg = False, ax = ax,
                    x = numeric.columns[0], y = numeric.columns[1], 
                    color = palette[colour_labels.index(c)],
                    marker = markers[marker_labels.index(m)],
                    label = '%s - %s' % (m, c))
    ax.legend()
    return fig


def scatter_cat__acm_fig(dataframe):
    '''
    Returns a figure with multiple scatter plots.
    The instances are coloured by the category given by the value in the first 
    object-dtype column and have a marker shape determined by the value in the
    second object-dtype column. The third object-dtype column determines which
    axis the data is plotted on.
    
    Inputs
    ------    
    dataframe:
        a long-form dataframe with 2 numeric columns and 3 object columns
    '''
    categorical = dataframe.select_dtypes([object])
    numeric = dataframe.select_dtypes(['number'])
    colour_col = categorical.columns[0]
    marker_col = categorical.columns[1]
    axis_col = categorical.columns[2]
    colour_labels = sorted(categorical[colour_col].unique())
    marker_labels = sorted(categorical[marker_col].unique())
    axis_labels = sorted(categorical[axis_col].unique())
    palette = sns.color_palette('cubehelix', len(colour_labels))

    fig = Figure()
    fig_nrows, fig_ncols = getFigureShape(len(axis_labels))
    
    i_ax = 0
    for a in axis_labels:
        i_ax += 1
        ax = fig.add_subplot(fig_nrows, fig_ncols, i_ax)
        ax.set_title(a)
        for m in marker_labels:
            for c in colour_labels:
                sub_df = dataframe[(dataframe[axis_col] == a) &
                                      (dataframe[marker_col] == m) &
                                      (dataframe[colour_col] == c)]
                sns.regplot(
                        data = sub_df, fit_reg = False, ax = ax,
                        x = numeric.columns[0], y = numeric.columns[1], 
                        color = palette[colour_labels.index(c)],
                        marker = markers[marker_labels.index(m)],
                        label = '%s - %s' % (m, c))
        ax.legend()
        return fig