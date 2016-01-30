from models_views.calculation import Calculation_Model



class ABCOutputsDataFrame(Calculation_Model):
    
    pass



class ABCTakesDataFrame(Calculation_Model):

    preceding_calcs = [ABCOutputsDataFrame]



class ABCOutputsSeries():
    
    pass



class ABCTakesSeries(Calculation_Model):
    
    preceding_calcs = [ABCOutputsSeries]



class ABCTakes2Series(Calculation_Model):
    
    preceding_calcs = [ABCOutputsSeries, ABCOutputsSeries]



class ABCOutputsIndex(Calculation_Model):
    
    pass



class ABCTakesIndex(Calculation_Model):
    
    preceding_calcs = [ABCOutputsIndex]



class ABCDataFrameToIndex(ABCTakesDataFrame,
                          ABCOutputsIndex):

    pass



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


