from pydoc import locate
import os
import enaml
import copy_reg
import types



# Enable pickling of instance methods for saving graphs
def _pickle_method(method):
    
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
        return func.__get__(obj, cls)

copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)


# A list of tuples (package_path, relative_system_path) of all the locations
# containing calculations. Each calculation consists of a model and a view 
# which are  named after the file e.g. Calc1.enaml contains class Calc1_Model
# and enamldef Calc1_View


def get_enaml_dirs_files(root_dir):
    """
    Creates a nested dictionary that represents the directory and file 
    structure of `root_dir`. Each key is a dict. Each value is a dict if it
    represents a folder or a list if it represents the files in a folder.
    """
    dirs_files = {}
    sub_dirs = [d for d in os.listdir(root_dir)
                if os.path.isdir(os.path.join(root_dir, d))
                and not d.startswith('_')]
    files = [f for f in os.listdir(root_dir)
             if os.path.isfile(os.path.join(root_dir, f))
             and f.endswith('.enaml')]

    for sd in sub_dirs:
        dirs_files[sd] = (get_enaml_dirs_files(os.path.join(root_dir, sd)))
    
    if len(files) > 0:
        dirs_files['files'] = []
        for f in files:
            dirs_files['files'].append(f)

    return dirs_files


def dict_to_path(path_dict, init_path, path_sep, path_list):
    
    # iterate through keys and values at the current level
    for k, v in path_dict.iteritems():
        if isinstance(v, list): # files
            # add the current path to the list
            path_list.append(init_path)
        else: # folder
            # pass pkg_sys into the next level and let it append new paths
            path_list = dict_to_path(v,
                                     init_path + path_sep + k,
                                     path_sep, path_list)          
    return path_list


def get_calc_models(pkg_path, sys_path):
    '''
    Returns a list of the calculation model classes found in the given package
    and system path.
    '''
    model_list = []
    model_files = [fn for fn in os.listdir(sys_path) 
                   if fn.endswith('.enaml')]
    for model_file in model_files:
        model_name = model_file.split('.')[0]
        print 'Loading calculation: %s...' % model_name
        model_list.append(locate('%s.%s.%s_Model' 
                                 % (pkg_path, model_name, model_name)))
            
    return model_list


def get_calc_models_views(pkg_path, sys_path):
    
    model_list = []
    model_files = [fn for fn in os.listdir(sys_path) 
                   if fn.endswith('.enaml')]
    for model_file in model_files:
        model_name = model_file.split('.')[0]
        model_list.append((locate('%s.%s.%s_Model' 
                                 % (pkg_path, model_name, model_name)),
                           locate('%s.%s.%s_View' 
                                 % (pkg_path, model_name, model_name))))
    return model_list
    

# Create a list of the available calculation models
enaml_dict = get_enaml_dirs_files('./calculations/')
pkg_sys = zip(dict_to_path(enaml_dict, 'calculations', '.', []),
              dict_to_path(enaml_dict, './calculations', '/', []))

calculation_models = []
with enaml.imports():
    for pkg_path, sys_path in pkg_sys:
        calculation_models.extend(get_calc_models(pkg_path, sys_path))  

# Create a dict mapping models to views
calculation_models_views = []            
for pkg_path, sys_path in pkg_sys:
    calculation_models_views.extend(get_calc_models_views(pkg_path, sys_path))
model_view_dict = {mv[0]: mv[1]
                   for mv in calculation_models_views}

# Create a menu dict
def get_menus_calcs(root_dir):
    '''
    Creates a nested dictionary that represents the directory and file 
    structure of `root_dir`. Each key is a dict. Each value is a dict if it
    represents a folder or a list of `CalculationItem` types representing the 
    calculations of the files in the folder.
    '''
    menus_calcs = {}
    sub_menus = [d for d in os.listdir(root_dir)
                 if os.path.isdir(os.path.join(root_dir, d))
                 and not d.startswith('_')]
    files = [f for f in os.listdir(root_dir)
             if os.path.isfile(os.path.join(root_dir, f))
             and f.endswith('.enaml')]
    
    calcs = []
    for fname in files:
        for calc_model in calculation_models:
            if calc_model.__name__[: -6] == fname[: -6]:
                calcs.append(calc_model)

    for sd in sub_menus:
        menus_calcs[sd] = (get_menus_calcs(os.path.join(root_dir, sd)))
    
    if len(files) > 0:
        menus_calcs['calcs'] = []
        for calc in calcs:
            menus_calcs['calcs'].append(calc)

    return menus_calcs


menus_calcs = get_menus_calcs('./calculations/')
