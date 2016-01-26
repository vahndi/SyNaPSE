import numpy as np
from pandas import Series, Index



def get_public_attr_names(obj):
    '''
    Returns a list of an object's public attributes
    '''
    return [a for a in dir(obj) 
            if not a.startswith('_') 
            and not callable(getattr(obj, a))]


def public_attrs_to_dict(obj):
    '''
    Takes an object `obj`'s public attributes and splits them up into different
    types. Returns a dict where the keys are the names of the types and the 
    values are series with the attribute names as keys and the attribute values
    as values.
    '''
    # Build a list of type-names for the output and associated types
    item_type_lists = {'bool': [bool, np.bool],
                       'float': [float, np.float32, np.float64],
                       'int': [int, np.int32, np.int64],
                       'str': [str]} 
    iterable_type_lists = {'list': [list],
                           'ndarray': [np.ndarray],
                           'tuple': [tuple]}
    dict_type_lists = {'dict': [dict]}

    # Get all the attrs from the object
    obj_attrs = {attr_name: getattr(obj, attr_name) 
                 for attr_name in get_public_attr_names(obj)}
    
    attr_dict = {}

    # item types
    for item_type in item_type_lists.keys():
        # Get all the attriutes of that type, if any
        type_attr_names = [attr_name for attr_name in obj_attrs.keys()
                           if type(obj_attrs[attr_name]) 
                           in item_type_lists[item_type]]
        num_attrs = len(type_attr_names)
        if num_attrs > 0:
            # Create a series of the values and add it to the attribute dict
            attr_dict[item_type + 's'] = Series(
                                           data = [obj_attrs[a] 
                                                   for a in type_attr_names],
                                           name = 'value',
                                           index = Index(
                                             [a for a in type_attr_names],
                                             name = item_type))

    # iterable types
    for iterable_type in iterable_type_lists.keys():
        # Get all the attributes of that type, if any
        type_attr_names = [attr_name for attr_name in obj_attrs.keys()
                           if type(obj_attrs[attr_name]) 
                           in iterable_type_lists[iterable_type]]
        if len(type_attr_names) > 0:

            # Create a series of the values and add it to the attribute dict
            attr_dict[iterable_type + 's'] = {type_attr_name:
                                              Series(obj_attrs[type_attr_name],
                                                     name = type_attr_name)
                                        for type_attr_name in type_attr_names}

    return attr_dict
    

if __name__ == '__main__':
    
    import seaborn as sns
    iris = sns.load_dataset('iris')
    d = public_attrs_to_dict(iris.columns)
    for k in d.keys():
        print k, d[k]


    