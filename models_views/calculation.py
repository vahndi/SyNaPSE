from inspect import getargspec



class Calculation_Model(object): # rename this to Node_Model or something
    '''
    The base class for all calc_models
    '''    
    calc_name = ''
    calc_description = ''
    calc_documentation = ''
    preceding_calcs = []
    calc_outputs = None


    def standard_exception(self, e):
        
        return {'Exception': 
                   {'__class__': str(e.__class__),
                    '__doc__': e.__doc__,
                    'message': e.message,
                    'args': str(e.args)}
                }



class CalculationItem(object):
    '''
    An object which wraps `Calculation_Model`s and links to a container object 
    e.g. a `CalculationGraph`
    '''
    def __init__(self, model, container, x = 0, y = 0):
        '''
        Arguments
        ---------
        model: 
            An instance of a `Calculation_Model`, defined in `Main_Model`.
        container: 
            The container of the `CalculationItem` e.g. a `CalculationGraph`.
            Must have a `select_calc_item` method.
        '''
        self._model = model
        self._container = container
        self.item_name = model.calc_name
        self.x = x
        self.y = y


    def calc_type_name(self):
        '''
        Returns the name of the item's model calculation type
        '''
        return self._model.calc_name
        
    
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
        '''
        Gets the outputs of the model which have already been calculated. If 
        they have not yet been calculated then calculate them first
        '''
        
        if self._model.calc_outputs:
            print 'returning existing calc outputs for %s' % self.item_name
            return self._model.calc_outputs
        else:
            print 'calc outputs for %s do not exist' % self.item_name
            return self.calculate_outputs()


    def calculate_outputs(self):
        '''
        Calculates the outputs of the model and returns them
        '''
        print 'calculating outputs for %s' % self.item_name
        self._model.calc_outputs = self._model.getOutputs()
        return self._model.calc_outputs
        
