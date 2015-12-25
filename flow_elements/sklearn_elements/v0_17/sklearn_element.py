# Parent
from models_views.flowElement import FlowElement

# Preceding elements
from flow_elements.LoadDataFrame import LoadDataFrame
from flow_elements.GetColumns import GetColumns


class SKLearnElement(FlowElement):
    
    doc_root = 'http://scikit-learn.org/stable/modules/generated/'
    precedingElements = [LoadDataFrame, GetColumns]
    