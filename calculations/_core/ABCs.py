from models_views.calculation import Calculation_Model



# Outputs
# -------
class ABCOutputsValue(Calculation_Model):
    pass

class ABCOutputsBool(ABCOutputsValue):    
    pass

class ABCOutputsDataFrame(Calculation_Model):
    pass

class ABCOutputsFloat(ABCOutputsValue):
    pass

class ABCOutputsIndex(Calculation_Model):    
    pass

class ABCOutputsInt(ABCOutputsValue):    
    pass

class ABCOutputsSeries(ABCOutputsValue):    
    pass



# Takes
# -----
class ABCTakesDataFrame(Calculation_Model):
    preceding_calcs = [ABCOutputsDataFrame]

class ABCTakesIndex(Calculation_Model):    
    preceding_calcs = [ABCOutputsIndex]

class ABCTakesSeries(Calculation_Model):    
    preceding_calcs = [ABCOutputsSeries]

class ABCTakes2Series(Calculation_Model):
    preceding_calcs = [ABCOutputsSeries, ABCOutputsSeries]



# To
# --
class ABCDataFrameToDataFrame(ABCTakesDataFrame, ABCOutputsDataFrame):
    pass

class ABCDataFrameToIndex(ABCTakesDataFrame, ABCOutputsIndex):
    pass

class ABCDataFrameToSeries(ABCTakesDataFrame, ABCOutputsSeries):    
    pass

class ABCSeriesToBool(ABCTakesSeries, ABCOutputsBool):                          
    pass

class ABCSeriesToInt(ABCTakesSeries, ABCOutputsInt):                 
    pass

class ABCSeriesToDataFrame(ABCTakesSeries, ABCOutputsDataFrame):
    pass

class ABCSeriesToFloat(ABCTakesSeries, ABCOutputsFloat):
    pass

class ABCSeriesToSeries(ABCTakesSeries, ABCOutputsSeries):
    pass

class ABCSeriesToValue(ABCTakesSeries, ABCOutputsValue):
    pass

class ABC2SeriesToSeries(ABCTakes2Series, ABCOutputsSeries):
    pass
