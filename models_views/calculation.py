from inspect import getargspec

from atom.api import Atom, ContainerList, List, Value
from atom.api import observe



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


    class __metaclass__(type):
        
        def __str__(self):

            return self.calc_name



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
        
    
    def model(self):
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
        


class CalculationTypeManager(Atom):
    '''
    Stores a list of calculation types `calc_types` and exposes a property
    `selectable_types` indicating which types are selectable based on the 
    type name of the currently selected type `selected_type_name`.
    '''
    calc_types = List()
    selected_calc_type = Value()
    selectable_calc_types = ContainerList()


    def __init__(self, calc_types, preceding_calc_type = None):

        self.calc_types = calc_types
        self.selected_calc_type = None
        self.selectable_calc_types = (
            self.following_calc_types(preceding_calc_type)
            )


    @observe('selected_calc_type')
    def selected_calc_type_changed(self, change):

        self.update_selectable_calc_types(self.selected_calc_type)


    def following_calc_types(self, calc_type):
        '''
        Returns a list of the types of calculation which can follow 
        `calc_type`.
        '''
        if calc_type is None:
            # return all calc types that don't have any preceding types
            return [ct for ct in self.calc_types 
                    if not ct.preceding_calcs]
        else:
            # return all calc types that contain `calc_type` as a preceder
            return [ct for ct in self.calc_types
                    for ct_preceder in ct.preceding_calcs
                    if issubclass(calc_type, ct_preceder)]


    def update_selectable_calc_types(self, preceding_calc_type):
        '''
        Update the list of choosable calculation types based on the preceding 
        calculation type, `preceding_calc_type`.
        '''
        if preceding_calc_type:
            # Return all calc types that can follow `preceding_calc_type`
            self.selectable_calc_types = \
                self.following_calc_types(preceding_calc_type)
        else:
            # Return all calcs that do not follow any other type
            self.selectable_calc_types = [ct
                                          for ct in self.calc_types 
                                          if not ct.preceding_calcs]

