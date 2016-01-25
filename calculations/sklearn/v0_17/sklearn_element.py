# Parent
from models_views.calculation import Calculation_Model

# Preceding elements
from calculations._core.ABCs import ABCOutputsDataFrame, ABCTakesDataFrame



class SKLearnElement(ABCTakesDataFrame):
    
    doc_root = 'http://scikit-learn.org/stable/modules/generated/'

    