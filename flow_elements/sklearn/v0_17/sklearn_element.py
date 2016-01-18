# Parent
from models_views.Calculation import Calculation_Model

# Preceding elements
from flow_elements.core.ABCs import ABCOutputsDataFrame



class SKLearnElement(Calculation_Model):
    
    doc_root = 'http://scikit-learn.org/stable/modules/generated/'
    preceding_calcs = [ABCOutputsDataFrame]
    