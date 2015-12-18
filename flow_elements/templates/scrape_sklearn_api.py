# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:18:19 2015

@author: Vahndi
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


root = 'http://scikit-learn.org/stable/modules/'

# Get links to class pages
classes_address = root + 'classes.html'
r = requests.get(classes_address)
soup = BeautifulSoup(r.content)
body = soup.find('div', {'class': 'body'})
sections = body.findAll('div', 
                        {'class': 'section', 
                         'id': re.compile('module-sklearn\.[a-z_]+$')})[1:]
class_pages = []
for section in sections:
    section_id = section.get('id')
    section_header = section.find('h2').text
    section_name = ' '.join(section_header.split(' ')[1:])[:-1]
    module = section_id.split('-')[1]
    for table in section.findAll('table', {'class': 'longtable docutils'}):
        for row in table.findAll('tr'):
            link = row.find('a').get('href')
            class_name = link.split('.')[2]
            if class_name[0].isupper():
                class_pages.append(
                    {'module': module,
                     'section_name': section_name,
                     'link': root + link,
                     'class_name': class_name})

# Get details for each class
for page in class_pages:
    class_path = '.'.join([page['module'], page['class_name']])
    print 'processing %s' % class_path
    r = requests.get(page['link'])
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
    page['args_vals'] = args_vals
    args_string = ', '.join(['%s=%s' % (av[0], av[1]) for av in args_vals])
    page['args_string'] = args_string
    
df = pd.DataFrame(class_pages)
df.to_csv('sklearn_scrape.csv')
df.to_pickle('sklearn_scrape.pkl')

