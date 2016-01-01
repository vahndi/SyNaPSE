from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix
from matplotlib.markers import MarkerStyle
from plotFunctions import getFigureShape
import seaborn as sns
markers = MarkerStyle.filled_markers



def confmat_fig(dataframe):
    '''
    Returns a figure with a confusion matrix
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


def confmat_cataxes_fig(dataframe):
    '''
    Returns a figure with confusion matrices, categorised by the third column
    with dtype = object
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

    fig = Figure()
    ax = fig.add_subplot(111)
    sns.distplot(dataframe, ax = ax)
    return fig


def box_fig(dataframe):
    
    fig = Figure()
    ax = fig.add_subplot(111)    
    sns.boxplot(data = dataframe, ax = ax,
                x = dataframe.select_dtypes([object]).columns[0], 
                y = dataframe.select_dtypes(['number']).columns[0])
    return fig


def scatter_fig(dataframe):
    
    fig = Figure()
    ax = fig.add_subplot(111)
    sns.regplot(data = dataframe, fit_reg = False, ax = ax,
                x = dataframe.select_dtypes(['number']).columns[0], 
                y = dataframe.select_dtypes(['number']).columns[1])
    return fig


def scatter_cat__c_fig(dataframe):

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