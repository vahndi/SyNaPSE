# Parent
from models_views.flowElement import FlowElement

# Preceding elements
from flow_elements.pandas.v0_17_1.base.ABCs import ABCOutputsDataFrame



class SKLearnElement(FlowElement):
    
    doc_root = 'http://scikit-learn.org/stable/modules/generated/'
    precedingElements = [ABCOutputsDataFrame]
    