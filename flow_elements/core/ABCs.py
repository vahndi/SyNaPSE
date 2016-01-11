from models_views.flowElement import FlowElement



class ABCOutputsDataFrame(FlowElement):
    
    pass



class ABCTakesDataFrame(FlowElement):

    precedingElements = [ABCOutputsDataFrame]



class ABCOutputsSeries():
    
    pass



class ABCTakesSeries():
    
    precedingElements = [ABCOutputsSeries]



class ABCDataFrameToDataFrame(ABCTakesDataFrame, 
                              ABCOutputsDataFrame):
    
    pass


class ABCDataFrameToDataFrameOrSeries(ABCTakesDataFrame, 
                                      ABCOutputsDataFrame,
                                      ABCOutputsSeries):
    
    pass


class ABCDataFrameToSeries(ABCTakesDataFrame, 
                           ABCOutputsSeries):
    
    pass

class ABCSeriesToSeries(ABCTakesSeries,
                        ABCOutputsSeries):
    
    pass

