class Calculation_Model(object): # rename this to Node_Model or something
    '''
    The base class for all flow elements
    '''    
    calculation_name = ''
    calculation_description = ''
    calculation_documentation = ''
    preceding_elements = []
    doc_root = ''


    def standard_exception(self, e):
        
        return {'Exception': {'__class__': str(e.__class__),
                              '__doc__': e.__doc__,
                              'message': e.message,
                              'args': str(e.args)}}
