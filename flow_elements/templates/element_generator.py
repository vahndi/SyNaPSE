import pandas as pd
from enaml_generator import getEnamlCode
from model_generator import getModelCode
from imports_generator import getImportsCode
from copy import deepcopy
import seaborn as sns


def generate_element(spreadsheet_name, element_name):

    # TODO: add element path and filename (create one for each library)
    ss_name = spreadsheet_name
    if not ss_name.endswith('.xls'):
        ss_name += '.xls'
    df = pd.read_excel(ss_name, 
                       sheetname = element_name)

    # TODO: write to a new .enaml file
    print getImportsCode(element_name, df)
    print getModelCode(element_name, df)
    print getEnamlCode(element_name, df)


def inspect_element_args(pickle_name, module_name = ''):
    '''
    Find the number of occurences of each named argument in the list of models
    Sheet Columns should be ['Model', 'Args']
    '''
    pkl_name = pickle_name;
    if not pkl_name.endswith('.pkl'):
        pkl_name += '.pkl'
    df = pd.read_pickle(pkl_name)
    if module_name:
        df = df[df.module == module_name]
    print len(df)
    # get all the arguments
    argCount = {}
    for loc in df.index:
        row = df.loc[loc]
        args_vals = row.args_vals
        for arg_val in args_vals:
            if arg_val[0] in argCount.keys():
                argCount[arg_val[0]] += 1
            else:
                argCount[arg_val[0]] = 1
    
    for arg in sorted(argCount.keys()):
        print arg, argCount[arg]

    
    # create a new dataframe showing which arguments are in which model
    model_names = list(df['class_name'].unique())
    arg_names = argCount.keys()
    models_args_dict = {}
    for model_name in model_names:
        model_dict = {}
        args_vals = df[df.class_name == model_name].iloc[0].args_vals
        model_args = [av[0] for av in args_vals]
        for arg_name in arg_names:
            if arg_name in model_args:
                model_dict[arg_name] = True
            else:
                model_dict[arg_name] = False
        models_args_dict[model_name] = deepcopy(model_dict)
    
    df_grid = pd.DataFrame(models_args_dict)
    sns.heatmap(df_grid, linewidths=.5)
    
    # find pairs of arguments which are always present together in models
    always_together_pairs = []
    for a1 in arg_names:
        for a2 in arg_names:
            if a1 != a2:
                always_together = True
                for m in model_names:
                    if models_args_dict[m][a1] != models_args_dict[m][a2]:
                        always_together = False
                if always_together:
                    always_together_pairs.append(tuple(sorted([a1, a2])))
    
    at_set = set(always_together_pairs)
    at_list = sorted(list(at_set))
    
    # merge tuples
    merges_made = True
    while merges_made:
        merges_made = False
        new_list = []
        for at in at_list:
            merge_made = False
            for i, new_at in enumerate(new_list):
                if len(set(at).intersection(new_at)) > 0:
                    new_list[i] = tuple(
                                    sorted(list(set(at).union(new_at)))
                                    )
                    merge_made = True
                    merges_made = True
                    break
            if not merge_made:
                new_list.append(at)
                
        at_list = new_list
    
    # count how many times each set of arguments appears
    at_num_list = sorted([(argCount[a[0]], a) for a in at_list], 
                         reverse = True)
    for at in at_num_list:
        print at



if __name__ == '__main__':
    
    generate_element(spreadsheet_name = 'pandas.DataFrame',
                     element_name = 'ColumnwiseCovariance')

#    inspect_element_args(pickle_name = 'sklearn_scrape',
#                         module_name = 'sklearn.linear_model')
