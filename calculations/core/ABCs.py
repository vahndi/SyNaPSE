from models_views.calculation import Calculation_Model



class ABCOutputsDataFrame(Calculation_Model):
    
    pass



class ABCTakesDataFrame(Calculation_Model):

    preceding_calcs = [ABCOutputsDataFrame]



class ABCOutputsSeries():
    
    pass



class ABCTakesSeries():
    
    preceding_calcs = [ABCOutputsSeries]



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

