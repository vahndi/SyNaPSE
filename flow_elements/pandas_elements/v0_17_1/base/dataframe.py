from models_views.flowElement import FlowElement
from ...core.ReadDataFrame import ReadDataFrame



class ABCDataFrame(FlowElement):

    precedingElements = [ReadDataFrame]
    

    