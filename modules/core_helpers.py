import numpy as np
from pandas import DataFrame, Index, Series



def get_public_attr_names(obj):
    '''
    Returns a list of an object's public attributes
    '''
    return [a for a in dir(obj) 
            if not a.startswith('_') 
            and not callable(getattr(obj, a))]


def _iterable_to_series(iterable):
    
    return Series(iterable, 
                  name = 'value')

    
def _items_to_series(name, item_names, item_values):
    
    return Series(data = item_values,
                  name = 'value',
                  index = Index(data = item_names,
                                name = name))


# Build a list of type-names and associated types


def _group_single_values(dictionary):
    '''
    Takes a dict and groups all items of type bool, float, int or str into 
    separate lists
    '''
    item_type_lists = {'bool': [bool, np.bool],
                       'float': [float, np.float32, np.float64],
                       'int': [int, np.int32, np.int64],
                       'str': [str]} 
    new_dict = {}
    
    # Group item types and add to a new dict as a Series
    for item_type_name in item_type_lists.keys():
        k_list = []
        v_list = []
        for k, v in dictionary.items():
            if type(v) in item_type_lists[item_type_name]:
                k_list.append(k)
                v_list.append(v)
        if k_list:
            new_dict[item_type_name + 's'] = _items_to_series(
                                                 name = item_type_name,
                                                 item_names = k_list,
                                                 item_values = v_list
                                                 )

    # Add other types directly to the new dict
    for k, v in dictionary.items():
        if type(v) in (DataFrame, dict, list, np.ndarray, Series, tuple):
            new_dict[k] = v
        
    return new_dict


def _dict_repr(dictionary):
    '''
    Takes a dict of values or dicts and returns a representation suitable for
    display.
    '''
    grouped_dict = _group_single_values(dictionary)
    
    new_dict = {}
    for key in grouped_dict.keys():
        
        value = grouped_dict[key]
        value_type = type(value)

        if ((value_type in (list, Series, tuple)) or
            (value_type is np.ndarray and value.ndim == 1)):
            
            new_dict[key] = _iterable_to_series(iterable = value)
        
        elif (value_type is DataFrame or 
              (value_type is np.ndarray and value.ndim == 2)):
                  
            new_dict[key] = DataFrame(value)
        
        elif value_type is dict:
            
            new_dict[key] = {_dict_repr(value[k])
                             for k in value.keys()} 
        
    return new_dict


def public_attrs_to_dict(obj):
    '''
    Takes an object `obj`'s public attributes and splits them up into different
    types. Returns a dict where the keys are the names of the types and the 
    values are series with the attribute names as keys and the attribute values
    as values.
    '''
    # Get all the attrs from the object
    obj_attrs = {attr_name: getattr(obj, attr_name) 
                 for attr_name in get_public_attr_names(obj)}
    return _dict_repr(obj_attrs)    
    

if __name__ == '__main__':
    
    import seaborn as sns
    iris = sns.load_dataset('iris')
    d = public_attrs_to_dict(iris.blocks)
    print(d)


    