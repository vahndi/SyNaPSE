import pandas as pd
from enaml_generator import getEnamlCode
from model_generator import getModelCode
from imports_generator import getImportsCode
from copy import deepcopy
import seaborn as sns


def generate_element(spreadsheet_name, element_name):

    # TODO: add element path and filename (create one for each library)
    df = pd.read_excel(spreadsheet_name.rstrip('.xls') + '.xls', 
                       sheetname = element_name)

    # TODO: write to a new .enaml file
    print getImportsCode(element_name, df)
    print getModelCode(element_name, df)
    print getEnamlCode(element_name, df)


def inspect_element_args(spreadsheet_name, sheet_name):
    '''
    Find the number of occurences of each named argument in the list of models
    Sheet Columns should be ['Model', 'Args']
    '''
    df = pd.read_excel(spreadsheet_name.rstrip('.xls') + '.xls', 
                       sheetname = sheet_name)
    
    # get all the arguments
    argCount = {}
    for ix in df.index:
        row = df.iloc[ix]
        argsvals = [av.encode('utf8').lstrip('\xc2\xa0') 
                    for av in row['Args'].split(',')]
        args_vals = [av.split('=') for av in argsvals]
        for arg_val in args_vals:
            if arg_val[0] in argCount.keys():
                argCount[arg_val[0]] += 1
            else:
                argCount[arg_val[0]] = 1
    
    print argCount
    
    # create a new dataframe showing which arguments are in which model
    model_names = list(df['Model'].unique())
    arg_names = argCount.keys()
    models_args_dict = {}    
    for model_name in model_names:
        model_dict = {}
        args_vals = df[df['Model'] == model_name].iloc[0]['Args']
        lst_args_vals = [av.split('=') for av in args_vals.encode('utf8').split(',')]
        model_args = [av[0].strip().lstrip('\xc2\xa0') for av in lst_args_vals]
        for arg_name in arg_names:
            if arg_name in model_args:
                model_dict[arg_name] = True
            else:
                model_dict[arg_name] = False
        models_args_dict[model_name] = deepcopy(model_dict)
    
    df_grid = pd.DataFrame(models_args_dict)
    sns.heatmap(df_grid, linewidths=.5)
    
    
    # find pairs of arguments which are always present together in models
    

if __name__ == '__main__':
    
#    generate_element(spreadsheet_name = 'sklearn.linear_model',
#                     element_name = 'LogisticRegression')
    inspect_element_args(spreadsheet_name = 'sklearn.ensemble',
                         sheet_name = 'All Models')
