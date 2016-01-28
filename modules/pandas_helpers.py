from collections import Iterable
import numpy as np
from copy import deepcopy
import pandas as pd


pandas_freqs = ['B', 'C', 'D', 'W', 'M', 'BM', 'CBM', 'MS', 'BMS', 
                'CBMS', 'Q', 'BQ', 'BQS', 'A', 'BA', 'AS', 'BAS', 
                'BH', 'H', 'T', 'S', 'L', 'U', 'N']

pandas_freq_tooltip = (
    'Frequency to conform the data to before computing the statistic.\n' + 
    'B: business day frequency\n' + 
    'C: custom business day frequency (experimental)\n' + 
    'D: calendar day frequency\nW: weekly frequency\n' + 
    'M: month end frequency\nBM: business month end frequency\n' + 
    'CBM: custom business month end frequency\n' + 
    'MS: month start frequency\nBMS: business month start frequency\n' + 
    'CBMS: custom business month start frequency\n' + 
    'Q: quarter end frequency\n' + 
    'BQ: business quarter endfrequency\n' + 
    'QS: quarter start frequency\n' + 
    'BQS: business quarter start frequency\n' + 
    'A: year end frequency\n' + 
    'BA: business year end frequency\n' + 
    'AS: year start frequency\n' + 
    'BAS: business year start frequency\n' + 
    'BH: business hour frequency\n' +
    'H: hourly frequency\n' +
    'T: minutely frequency\n' + 
    'S: secondly frequency\n' +
    'L: milliseonds\n' +
    'U: microseconds\n' +
    'N: nanoseconds'
    )


def get_columns_by_dtype(dataframe, column_type):
    '''
    column_type can be e.g. np.int64, np.float64 or an iterable of such types
    '''
    if isinstance(column_type, Iterable):
        column_types = list(column_type)
    else:
        column_types = [column_type]
        
    return dataframe[[col for col in dataframe.columns 
                      if dataframe[col].dtype in column_types]]


def get_column_names_by_dtype(dataframe, column_type):
    '''
    column_type can be e.g. np.int64, np.float64 or an iterable of types
    '''
    return list(get_columns_by_dtype(dataframe, column_type).columns)


def shuffle_dataframe_rows(dataframe):
    '''
    Returns a copy of the dataframe with rows randomly shuffled
    '''
    return dataframe.reindex(np.random.permutation(dataframe.index))


def split_training_test(dataframe, 
                        training_fraction, shuffle_rows,
                        input_columns = None, target_column = None):
    '''
    Splits the dataframe into training and test dataframes

    Inputs
    ------
    dataframe: the input dataframe
    training_fraction: the fraction of the dataset to put into the training set. Between 0 and 1
    shuffle_rows: whether to randomise the order of the rows before splitting
    input_columns: the names of the columns to use as inputs
    target_column: the name of the target column
    '''
    df = {True: shuffle_dataframe_rows(dataframe),
          False: dataframe
          }[shuffle_rows]

    assert 0.0 < training_fraction < 1.0 

    msk = np.random.rand(len(df)) < training_fraction
    train = df[msk]
    test = df[~msk]

    if input_columns is None:
        if target_column is None:
            return train, test
        else:
            input_columns = df.columns.remove(target_column)
    else:
        if target_column is None:
            train_inputs = train[input_columns]
            test_inputs = test[input_columns]
            return train_inputs, test_inputs
        
    train_inputs = train[input_columns]
    train_target = train[target_column]
    test_inputs = test[input_columns]
    test_target = test[target_column]
    
    return train_inputs, train_target, test_inputs, test_target


def get_column_names(dataframe, 
                     startsWith = None, endsWith = None, 
                     contains = None, doesNotContain = None,
                     orderAlphabetically = False):
    '''
    Returns column names from a dataframe with optional filtering and sorting
    
    Inputs
    ------
    dataframe (pandas.DataFrame):
        the dataframe whose columns to get
    startsWith (str):
        restricts the column names returned to those starting with the filter
    endsWith (str):
        restricts the column names returned to those ending with the filter
    contains (str):
        restricts the column names returned to those containing the filter
    doesNotContain (str):
        restricts the column names returned to those not containing the filter
    orderAlphabetically (bool):
        orders the returned column names alphabetically
    
    Outputs
    -------
    list of str
        The column names selected from the dataframe
    '''
    
    # Get list of files
    cols = dataframe.columns
    
    # Flags
    if orderAlphabetically:
        cols = sorted(cols)
    if startsWith not in (None, ''):
        cols = [col for col in cols if col.startswith(startsWith)]
    if endsWith not in (None, ''):
        cols = [col for col in cols if col.endswith(endsWith)]
    if contains not in (None, ''):
        cols = [col for col in cols if contains in col]
    if doesNotContain not in (None, ''):
        cols = [col for col in cols if doesNotContain not in col]
    
    return cols


def get_row_names(dataframe, 
                  startsWith = None, endsWith = None, 
                  contains = None, doesNotContain = None,
                  orderAlphabetically = False):
    '''
    Returns row names from a dataframe with optional filtering and sorting
    N.B. Assumes that the dataframe index is of dtype object
    Inputs
    ------
    dataframe (pandas.DataFrame):
        the dataframe whose columns to get
    startsWith (str):
        restricts the column names returned to those starting with the filter
    endsWith (str):
        restricts the column names returned to those ending with the filter
    contains (str):
        restricts the column names returned to those containing the filter
    doesNotContain (str):
        restricts the column names returned to those not containing the filter
    orderAlphabetically (bool):
        orders the returned column names alphabetically
    
    Outputs
    -------
    list of str
        The row names selected from the dataframe
    '''

    # Get list of files
    rows = dataframe.index
    
    # Flags
    if orderAlphabetically:
        rows = sorted(rows)
    if startsWith not in (None, ''):
        rows = [row for row in rows if row.startswith(startsWith)]
    if endsWith not in (None, ''):
        rows = [row for row in rows if row.endswith(endsWith)]
    if contains not in (None, ''):
        rows = [row for row in rows if contains in row]
    if doesNotContain not in (None, ''):
        rows = [row for row in rows if doesNotContain not in row]
    
    return rows
    

def get_confusion_matrix(dataframe, actual_value_column, predicted_value_column):
    '''
    Creates a DataFrame representing a confusion matrix where the name of each 
    column represents the predicted value and the name of each row represents 
    the actual value. The value at cell i,j represents the number of values 
    which are actually i and predicted to be j.

    Inputs
    ------
    dataframe:
        a long-form dataframe where each row contains an actual value and a
        predicted value
    actual_value_column:
        the name of the column with the actual values
    predicted_value_column:
        the name of the column with the predicted values
    '''
    actual_values = sorted(dataframe[actual_value_column].unique())
    predicted_values = sorted(dataframe[predicted_value_column].unique())
    conf_mat = {}
    for p in predicted_values:
        p_mat = {}
        for a in actual_values:
            df_count = dataframe[(dataframe[predicted_value_column] == p) &
                                 (dataframe[actual_value_column] == a)]            
            p_mat[a] = len(df_count)
        conf_mat[p] = deepcopy(p_mat)

    return pd.DataFrame(conf_mat)


def join_inputs_targets_predictions(
                            train_inputs, train_targets, train_predictions,
                            test_inputs, test_targets, test_predictions,
                            target_column_name = None, 
                            predicted_column_name = None
                            ):
    '''
    Joins training and test inputs, targets and predictions together into a 
    dataframe. Inputs should be DataFrames. Targets should be Series. 
    Predictions are typically ndarrays.
    '''
    if target_column_name is None:
        target_column_name = 'Target ' +  train_targets.name
    if predicted_column_name is None:
        predicted_column_name = 'Predicted ' + train_targets.name

    # Fix an issue that can arise e.g. from linear_model.Lars    
    if train_predictions.ndim == 2 and train_predictions.shape[1] == 1:
        train_predictions = np.squeeze(train_predictions)
    if test_predictions.ndim == 2 and test_predictions.shape[1] == 1:
        test_predictions = np.squeeze(test_predictions)

    df_train = pd.concat([train_inputs, 
                          pd.Series(train_targets,
                                    name = target_column_name),
                          pd.Series(train_predictions, 
                                    name = predicted_column_name,
                                    index = train_targets.index)],
                         axis = 1)
    df_train['Set'] = 'Training'

    df_test = pd.concat([test_inputs, 
                         pd.Series(test_targets,
                                   name = target_column_name),
                         pd.Series(test_predictions, 
                                   name = predicted_column_name,
                                   index = test_targets.index)],
                         axis = 1)
    df_test['Set'] = 'Test'
    
    df_pred = pd.concat([df_train, df_test])
    
    return df_pred
