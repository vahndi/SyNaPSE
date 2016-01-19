from inspect import getargspec



class Calculation_Model(object): # rename this to Node_Model or something
    '''
    The base class for all calc_models
    '''    
    calc_name = ''
    calc_description = ''
    calc_documentation = ''
    preceding_calcs = []


    def standard_exception(self, e):
        
        return {'Exception': 
                   {'__class__': str(e.__class__),
                    '__doc__': e.__doc__,
                    'message': e.message,
                    'args': str(e.args)}
                }
                              

class CalculationType(object):

    
    def __init__(self, calc_type_name, calc_type):
        
        self._calc_type_name = calc_type_name
        self._calc_type = calc_type  

        
    def __str__(self):
        
        return self._calc_type_name
        
        
    def getType(self):
        
        return self._calc_type



class CalculationItem(object):
    '''
    An object which wraps `Calculation_Model`s and links to a container object 
    e.g. a `CalculationList` or `CalculationGraph`
    '''
    def __init__(self, model, container):
        '''
        Arguments
        ---------
        model: 
            An instance of a `Calculation_Model`, defined in `Main_Model`.
        container: 
            The container of the `CalculationItem` e.g. a `CalculationList`.
            Must have a `select_calc` method.
        '''
        self._model = model
        self._container = container
        self.item_name = model.calc_name
        
    
    def get_model(self):
        '''
        Returns the encapsulated `Calculation_Model` object.        
        '''        
        return self._model


    def __str__(self):
        '''
        Returns the type name of the encapsulated `Calculation_Model` object.        
        '''
        return self._model.calc_name
        
    
    def select(self):
        '''
        Calls the `select_calc` method of the `CalculationItem`'s container
        '''
        self._container.select_calc_item(self)


    def model_arg_names(self):
        
        arg_names = getargspec(self._model.setInputs).args
        arg_names.remove('self')
        return arg_names


    def set_inputs(self, inputs_dict):
        
        self._model.setInputs(** inputs_dict)
        
        
    def get_outputs(self):

        return self._model.getOutputs()