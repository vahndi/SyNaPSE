# Parent
from models_views.flowElement import FlowElement

# Preceding elements
from flow_elements.pandas_elements.v0_17_1.ReadDataFrame import ReadDataFrame_Model
from ...pandas_elements.v0_17_1.SelectColumns import SelectColumns_Model


class SKLearnElement(FlowElement):
    
    doc_root = 'http://scikit-learn.org/stable/modules/generated/'
    precedingElements = [ReadDataFrame_Model, SelectColumns_Model]
    