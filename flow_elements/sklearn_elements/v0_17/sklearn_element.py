# Parent
from models_views.flowElement import FlowElement

# Preceding elements
from flow_elements.core.ReadDataFrame import ReadDataFrame
from ...pandas_elements.v0_17_1.SelectColumns import SelectColumns_Model


class SKLearnElement(FlowElement):
    
    doc_root = 'http://scikit-learn.org/stable/modules/generated/'
    precedingElements = [ReadDataFrame, SelectColumns_Model]
    