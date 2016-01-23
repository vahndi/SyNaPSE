# Parent
from models_views.calculation import Calculation_Model

# Preceding elements
from calculations._core.ABCs import ABCOutputsDataFrame



class SKLearnElement(Calculation_Model):
    
    doc_root = 'http://scikit-learn.org/stable/modules/generated/'
    preceding_calcs = [ABCOutputsDataFrame]
    