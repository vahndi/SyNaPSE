from models_views.flowElement import FlowElement
from flow_elements.pandas_elements.v0_17_1 import ReadDataFrame



class ABCDataFrame(FlowElement):

    precedingElements = [ReadDataFrame]
    

    