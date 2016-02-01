from inspect import getargspec

from atom.api import Atom, ContainerList, List
from atom.api import observe
from collections import OrderedDict



class Calculation_Model(object):
    '''
    The base class for all calc_models
    '''    
    calc_name = ''
    calc_desc = 'No Description'
    calc_docs = ''
    preceding_calcs = []
    calc_outputs = None


    def standard_exception(self, e):
        
        return {'Exception': 
                   {'__class__': str(e.__class__),
                    '__doc__': e.__doc__,
                    'message': e.message,
                    'args': str(e.args)}
               }
               

    def not_configured(self):
        
        return {'Outputs': 'Not configured correctly'}


    @classmethod
    def can_precede(cls, other_cls):
        '''
        Returns a boolean indicating if this calc can precede `other' calc
        '''        
        for other_preceder in other_cls.preceding_calcs:
            if issubclass(cls, other_preceder):
                return True
        return False
   
    
    @classmethod
    def can_follow(cls, other_classes = None):
        '''
        Returns a boolean indicating if this calc can follow a list of calcs 
        whose types are given by `other_classes`.
        The length of `other_classes` needs to be the same as the length of 
        `cls.preceding_calcs` and the types must match one for one in any 
        order.
        To test if the calc can follow just one calc, pass a list with one 
        item.
        '''
        # create a temp list of calc types which precede this one
        my_preceders = [pc for pc in cls.preceding_calcs]
        if len(my_preceders) == 0:
            # If there are no preceding calcs then this can't follow anything
            return False

        # iterate over the other classes                        
        for other_class in other_classes:
            # iterate over preceding calcs in this class
            for my_preceder in my_preceders:
                if issubclass(other_class, my_preceder):
                    # match: remove my_preceder from the temp list
                    my_preceders.remove(my_preceder)
                    break
        if len(my_preceders) == 0:
            return True
        return False                        


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
        '''
        Return the input argument names for the underlying model, excluding
        `self`
        '''
        arg_names = getargspec(self._model.setInputs).args
        arg_names.remove('self')
        return arg_names


    def get_arg_mappings(self, preceding_calc_items):
        '''
        Takes a list of preceding `CalculationItem`s, extracts the appropriate 
        keyword arguments and returns a dict of dicts, one for each preceding 
        `CalculationItem`. Output dict is of the form: 
        
        {preceding_calc_item: 
            {preceding_item_output_arg_name: 
                this_item_input_arg_name}
        }
        '''
        # create a list of dicts representing the outputs of the 
        # `preceding_calc_items`
        outs_list = [item.get_outputs() for item in preceding_calc_items]
        # set up the keys of the output dict
        arg_mappings = OrderedDict()
        for calc_item in preceding_calc_items:
            arg_mappings[calc_item] = {}
        # iterate over model's input argument names
        self_arg_names = self.model_arg_names()
        while len(self_arg_names) > 0:
            arg_name = self_arg_names[0]
            # first look for an exact match in each dict
            match_found = False
            for i, prev_outputs in enumerate(outs_list):
                if arg_name in prev_outputs.keys():
                    match_found = True
                    arg_mappings[preceding_calc_items[i]][arg_name] = arg_name
                    prev_outputs.pop(arg_name)
                    self_arg_names.remove(arg_name)
                    break
            if match_found:
                continue
            # else look for a match where the arg_name begins with the output 
            # name e.g. `series_1` starts with `series`
            for i, prev_outputs in enumerate(outs_list):
                if match_found:
                    continue
                for key in prev_outputs.keys():
                    if arg_name.startswith(key):
                        match_found = True
                        arg_mappings[preceding_calc_items[i]][key] = arg_name
                        prev_outputs.pop(key)
                        self_arg_names.remove(arg_name)
                        break

        # assign the outputs to the input of the model
        return arg_mappings


    def set_model_inputs(self, arg_mappings):
        '''
        '''
        # assign the outputs to the input of the model
        inputs_dict = {}
        for calc_item in arg_mappings.keys():
            calc_outputs = calc_item.get_outputs()
            out_in_args = arg_mappings[calc_item]
            for out_arg_name in out_in_args.keys():
                inputs_dict[out_in_args[out_arg_name]] = \
                    calc_outputs[out_arg_name]

        self._model.setInputs(** inputs_dict)
            
    
    def get_outputs(self):
        '''
        Gets the outputs of the model which have already been calculated. If 
        they have not yet been calculated then calculate them first.
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
        


#class CalculationTypeManager(Atom):
#    '''
#    Stores a list of calculation types `calc_types` and exposes a property
#    `selectable_calc_types` indicating which types are selectable based on the 
#    type of the currently selected type `selected_calc_type`.
#    '''
#    calc_types = List()
#    selected_calc_type = Value()
#    selectable_calc_types = ContainerList()
#
#
#    def __init__(self, calc_types, preceding_calc_type = None):
#
#        self.calc_types = calc_types
#        self.selected_calc_type = None
#        self.selectable_calc_types = (
#            self.following_calc_types(preceding_calc_type)
#            )
#
#
#    @observe('selected_calc_type')
#    def selected_calc_type_changed(self, change):
#
#        self.update_selectable_calc_types(self.selected_calc_type)
#
#
#    def following_calc_types(self, calc_type):
#        '''
#        Returns a list of the types of calculation which can follow 
#        `calc_type`.
#        '''
#        if calc_type is None:
#            # return all calc types that don't have any preceding types
#            return [ct for ct in self.calc_types 
#                    if not ct.preceding_calcs]
#        else:
#            # return all calc types that contain `calc_type` as a preceder
#            return [ct for ct in self.calc_types
#                    for ct_preceder in ct.preceding_calcs
#                    if issubclass(calc_type, ct_preceder)]
#
#
#    def update_selectable_calc_types(self, preceding_calc_type):
#        '''
#        Update the list of choosable calculation types based on the preceding 
#        calculation type, `preceding_calc_type`.
#        '''
#        if preceding_calc_type:
#            # Return all calc types that can follow `preceding_calc_type`
#            self.selectable_calc_types = \
#                self.following_calc_types(preceding_calc_type)
#        else:
#            # Return all calcs that do not follow any other type
#            self.selectable_calc_types = [ct
#                                          for ct in self.calc_types 
#                                          if not ct.preceding_calcs]



class CalculationTypeManager(Atom):
    '''
    Stores a list of calculation types `calc_types` and exposes a property
    `selectable_types` indicating which types are selectable based on the 
    type name of the currently selected types `selected_calc_types`.
    '''
    calc_types = List()
    selected_calc_types = ContainerList()
    selectable_calc_types = ContainerList()


    def __init__(self, calc_types, preceding_calc_types = None):

        self.calc_types = calc_types
        self.selected_calc_types = []
        

    @observe('selected_calc_types')
    def selected_calc_types_changed(self, change):

        self.update_selectable_calc_types(self.selected_calc_types)


    def update_selectable_calc_types(self, preceding_calc_types):
        '''
        Update the list of selectable calculation types based on the preceding 
        calculation types, `preceding_calc_types`.
        '''                
        if preceding_calc_types:
            # Return all calc types that can follow `preceding_calc_types`
            self.selectable_calc_types = \
                [ct for ct in self.calc_types
                if ct.can_follow(other_classes = preceding_calc_types)]
        else:
            # Return all calcs that do not follow any other type
            self.selectable_calc_types = [ct for ct in self.calc_types 
                                          if not ct.preceding_calcs]