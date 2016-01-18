from pydoc import locate
import os
import enaml


# A list of tuples (package_path, relative_system_path) of all the locations
# containing calculations. Each calculation consists of a model and a view 
# which are  named after the file e.g. Calc1.enaml contains class Calc1_Model
# and enamldef Calc1_View
pkg_sys = (('flow_elements.pandas.v0_17_1', 
            './flow_elements/pandas/v0_17_1'),
           ('flow_elements.pandas.v0_17_1.IO', 
            './flow_elements/pandas/v0_17_1/IO'),
           ('flow_elements.sklearn.v0_17.generate',
            './flow_elements/sklearn/v0_17/generate'),
           ('flow_elements.pandas.v0_17_1.Statistics', 
            './flow_elements/pandas/v0_17_1/Statistics'),
           ('flow_elements.pandas.v0_17_1.CumulativeStatistics', 
            './flow_elements/pandas/v0_17_1/CumulativeStatistics'),
           ('flow_elements.pandas.v0_17_1.ExpandingWindowStatistics', 
            './flow_elements/pandas/v0_17_1/ExpandingWindowStatistics'),
           ('flow_elements.pandas.v0_17_1.ExponentiallyWeightedStatistics', 
            './flow_elements/pandas/v0_17_1/ExponentiallyWeightedStatistics'),
           ('flow_elements.pandas.v0_17_1.RollingWindowStatistics', 
            './flow_elements/pandas/v0_17_1/RollingWindowStatistics'),
           ('flow_elements.sklearn.v0_17.linear_model',
            './flow_elements/sklearn/v0_17/linear_model'),
           ('flow_elements.sklearn.v0_17.cluster',
            './flow_elements/sklearn/v0_17/cluster'),
           ('flow_elements.sklearn.v0_17.ensemble',
            './flow_elements/sklearn/v0_17/ensemble'),
           ('flow_elements.sklearn.v0_17.decomposition',
            './flow_elements/sklearn/v0_17/decomposition'))


def get_calculation_models(package_path, sys_path):
    '''
    Returns a list of the calculation model classes found in the given package
    and system path.
    '''
    model_list = []
    model_files = [fn for fn in os.listdir(sys_path) if fn.endswith('.enaml')]
    for model_file in model_files:
        model_name = model_file.split('.')[0]
        print 'Loading calculation: %s...' % model_name
        model_list.append(locate('%s.%s.%s_Model' 
                                 % (package_path, model_name, model_name)))
            
    return model_list


# Create a list of the available calculation models
calculation_models = []
with enaml.imports():
    for pkg_path, sys_path in pkg_sys:
        calculation_models.extend(get_calculation_models(pkg_path, sys_path))  


def _getModelsViews(package_path, sys_path):
    
    model_list = []
    model_files = [fn for fn in os.listdir(sys_path) if fn.endswith('.enaml')]
    for model_file in model_files:
        model_name = model_file.split('.')[0]
        model_list.append((locate('%s.%s.%s_Model' 
                                 % (package_path, model_name, model_name)),
                           locate('%s.%s.%s_View' 
                                 % (package_path, model_name, model_name))))
    return model_list
    

calculation_models_views = []            
for pkg_path, sys_path in pkg_sys:
    calculation_models_views.extend(_getModelsViews(pkg_path, sys_path))
model_view_dict = {mv[0]: mv[1]
                   for mv in calculation_models_views}
