# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:18:19 2015

@author: Vahndi
"""

from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
from sklearn.neighbors import DistanceMetric
from sklearn.cross_validation import KFold
from numpy import ndarray, dtype
from numpy.random import RandomState
from joblib import Memory



root = 'http://scikit-learn.org/stable/modules/'

arg_desc_type = OrderedDict([
    (r'an integer', int),
    (r'array-like of shape \(n_samples,\)', ndarray),
    (r'array-like of shape \[n_classes\]', ndarray),
    (r'array-like, shape = \[n_classifiers\]', ndarray),
    (r'array-like, shape \(n_samples,\) or float', ndarray),
    (r'array-like, shape \(n_samples, n_features\)', ndarray),
    (r'array-like, shape = \[n_samples, n_features\]', ndarray),
    (r'array-like, shape \(n_samples,\)', ndarray),
    (r'array-like, size \(n_classes,\)', ndarray),
    (r'array-like, size=\[n_classes,\]', ndarray),
    (r'array-like or callable', (callable, ndarray)),
    (r'array-like with shape \(n_samples, \)', ndarray),
    (r'array-like', ndarray),
    (r'array, \[n_components, n_features\]', ndarray),
    (r'array of shape \(n_samples, n_components\)', ndarray),
    (r'array of shape \(n_components, n_features\)', ndarray),
    (r'array_like or sparse matrix, shape = \[n_samples, n_features\]', ndarray),
    (r'array-like, \[n_samples\]', ndarray),
    (r'array-like of int with shape \(n_samples,\)', ndarray),
    (r'array, \[n_samples\]', ndarray),
    (r'array, shape=\[n_samples, n_features\]', ndarray),
    (r'array', ndarray),
    (r'BaseEstimator', BaseEstimator),
    (r'boolean, scale data\?', bool),
    (r'boolean or integer', bool),
    (r'boolean', bool),
    (r'Boolean', bool),
    (r'bool or integer', (bool, int)),
    (r'bool or int', (bool, int)),
    (r'bool', bool),
    (r'callable', callable),
    (r'callabale', callable),
    (r'dictionary of string to any', dict),
    (r'dictionary', dict),
    (r'dict of string to sequence, or sequence of such', dict),
    (r'dict or list of dictionaries', dict),
    (r'dict', dict),
    (r'double array_like', ndarray),
    (r'double or ndarray', (float, ndarray)),
    (r'double', float),
    (r'estimator object', BaseEstimator),
    (r'float, int, or None', (float, int, None)),
    (r'float or int', (float, int)),
    (r'float or None', (float, None)),
    (r'\{float, array-like\}, shape = \[n_targets\]', (float, ndarray)),
    (r'float or array of floats', (float, ndarray)),
    (r'\{float, array-like\}, shape \(n_targets\)', (float, ndarray)),
    (r'float in range \[0, 1\]', float),
    (r'float', float),
    (r'instance BaseEstimator', BaseEstimator),
    (r'Instance of joblib\.Memory or string', (Memory, str)),
    (r'integer, RandomState instance or None', (int, None, RandomState)),
    (r'integer or cross-validation generator', int),
    (r'integer or None', (int, None)),
    (r'integer seed, RandomState instance, or None', (int, None, RandomState)),
    (r'integer, or list positive float', (int, [float])),
    (r'integer or numpy.RandomState', (int, RandomState)),
    (r'integer', int),
    (r'int \(>= 1\) or float \(\[0, 1\]\)', (float, int)),
    (r'int, or string', (int, str)),
    (r'int, RandomState instance, or None', (int, None, RandomState)),
    (r'\{int, RandomState\}', (int, RandomState)),
    (r'int, float, string or None', (int, float, None, str)),
    (r'int or float', (int, float)),
    (r'int or str or array of shape = \[n_outputs\]', (int, ndarray, str)),
    (r'int or RandomState instance or None', (int, None, RandomState)),
    (r'int, RandomState instance or None', (int, None, RandomState)),
    (r'int or float or array of shape = \[n_outputs\]', (float, int, ndarray)),
    (r'int or None', (int, None)),
    (r'int, None or string', (int, None, str)),
    (r'int or RandomState', (int, RandomState)),
    (r'int, cross-validation generator or an iterable', (int, KFold)),
    (r'int, instance of sklearn.cluster model', (int, ClusterMixin)),
    (r'int seed, RandomState instance, or None', (int, None, RandomState)),
    (r'int \| None', (int, None)),
    (r'int', int),
    (r'list of floats \| int', ([float], int)),
    (r'list of \(string, estimator\) tuples', ([str, BaseEstimator])),
    (r'list of \(string, transformer\) tuples',([str, TransformerMixin])),
    (r'list', list),
    (r'mapping of string to any', dict),
    (r'non-negative real', float),
    (r'None of an \(n_components, n_components\) ndarray', (ndarray, None)),
    (r'None \| array, shape=\(n_features,\)', (ndarray, None)),
    (r'None, int or RandomState', (int, None, RandomState)),
    (r'number type', dtype),
    (r'numpy array of shape \[n_alphas\]', ndarray),
    (r'numpy array of shape \[n_samples, n_samples\]', ndarray),
    (r'numpy array', ndarray),
    (r'numpy type', dtype),
    (r'numpy\.RandomState or int', (int, RandomState)),
    (r'numpy\.RandomState', RandomState),
    (r'object or None', (None, object)),
    (r'object', object),
    (r'positive float', float),
    (r'positive integer', int),
    (r'RandomState or an int seed', (int, RandomState)),
    (r'strictly positive float', float),
    (r'strictly positive integer', int),
    (r'string, or callable', (callable, str)),
    (r'string, callable or None', (callable, None, str)),
    (r'string or callable', (callable, str)),
    (r'string or class name', str),
    (r'string or DistanceMetric object', (DistanceMetric, str)),
    (r'string, float', (float, str)),
    (r'string', str),
    (r'str or callable', (callable, str)),
    (r'str', str),
    (r'tuple \(min, max\)', tuple)
    ])

    

def get_module_sections(main_page):

    body = main_page.find('div', {'class': 'body'})
    sections = body.findAll('div', 
                            {'class': 'section', 
                             'id': re.compile('module-sklearn\.[a-z_]+$')
                             })[1:]
    return sections


def get_module_class_pages(module_section):
    
    module_pages = []
    section_id = module_section.get('id')
    section_header = module_section.find('h2').text
    section_name = ' '.join(section_header.split(' ')[1:])[:-1]
    module = section_id.split('-')[1]
    for table in module_section.findAll('table', 
                                        {'class': 'longtable docutils'}):
        for row in table.findAll('tr'):
            link = row.find('a').get('href')
            class_name = link.split('.')[2]
            if class_name[0].isupper():
                module_pages.append({'module': module,
                                     'section_name': section_name,
                                     'link': root + link,
                                     'class_name': class_name})
    return module_pages


def add_class_details(class_page_dict):
    
    class_path = '.'.join([class_page_dict['module'], 
                           class_page_dict['class_name']])
    print('processing %s' % class_path)
    r = requests.get(class_page_dict['link'])
    soup = BeautifulSoup(r.content)
    class_def = soup.find('dt', {'id': class_path})
    argsvals = class_def.findAll('em', {'class': None})
    args_vals = [str(av.text).split('=', 1) for av in argsvals]
    args = [av[0] for av in args_vals]
    vals = []
    for av in args_vals:
        if len(av) > 1:
            vals.append(av[1])
        else:
            vals.append(None)
    args_vals = zip(args, vals)
    class_page_dict['args_vals'] = args_vals
    args_string = ', '.join(['%s=%s' % (av[0], av[1]) for av in args_vals])
    class_page_dict['args_string'] = args_string  
    
    # Get the list of arguments
    params = soup.find('th', {'class': 'field-name'}, 
                       text = 'Parameters:').findNext()
    p_args = params.findChildren('p', recursive = False)
    arg_names = [re.sub(ur'(\u2018)|(\u2019)|(\u201c)|(\u201d)', 
                        "'", 
                        p.find('strong').text) 
                 for p in p_args]
    arg_text = [re.sub(ur'(\u2018)|(\u2019)|(\u201c)|(\u201d)', 
                       "'", 
                       p.text) 
                for p in p_args]
    class_page_dict['arg_names'] = [str(a) for a in arg_names]
    class_page_dict['arg_text'] = [str(t) for t in arg_text]
    class_page_dict['arg_types'] = []
    for t in arg_text:
        argtypefound = False
        for k in arg_desc_type:
            if re.search(k, t):
                class_page_dict['arg_types'].append(str(arg_desc_type[k]))
                argtypefound = True
                break
        if not argtypefound:
            class_page_dict['arg_types'].append(None)


# Load main api page and find module sections
classes_address = root + 'classes.html'
r = requests.get(classes_address)
soup = BeautifulSoup(r.content)
sections = get_module_sections(soup)
body = soup.find('div', {'class': 'body'})

# Get links to class pages
class_pages = []
for section in sections:
    class_pages.extend(get_module_class_pages(section))

# Get details for each class
for page in class_pages:    
    add_class_details(page)


df = pd.DataFrame(class_pages)
df.to_csv('sklearn_scrape.csv')
df.to_pickle('sklearn_scrape.pkl')
