# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 14:52:16 2016

@author: vahndi
"""

import os
import pprint
pp = pprint.PrettyPrinter(indent=4)


def get_dirs_files(root_dir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dirs_files = {}
    sub_dirs = [d for d in os.listdir(root_dir)
                if os.path.isdir(os.path.join(root_dir, d))
                and not d.startswith('_')]
    files = [f for f in os.listdir(root_dir)
             if os.path.isfile(os.path.join(root_dir, f))
             and f.endswith('.enaml')]

    for sd in sub_dirs:
        dirs_files[sd] = (get_dirs_files(os.path.join(root_dir, sd)))
        
    for f in files:
        dirs_files[f] = None

    return dirs_files


edf = get_dirs_files('../calculations/')
pp.pprint(edf)
