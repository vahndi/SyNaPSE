from models_views.flowElement import FlowElement
from ...core.LoadDataFrame import LoadDataFrame



class ABCDataFrame(FlowElement):

    precedingElements = [LoadDataFrame]
    

    