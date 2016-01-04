from models_views.flowElement import FlowElement
from flow_elements.pandas_elements.v0_17_1.ReadDataFrame import ReadDataFrame_Model



class ABCDataFrame(FlowElement):

    precedingElements = [ReadDataFrame_Model]
    

    