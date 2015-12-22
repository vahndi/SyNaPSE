class FlowElement(object):
    '''
    The base class for all flow elements
    '''    
    elementName = ''
    precedingElements = []


    def standard_exception(self, e):
        
        return {'Exception': {'__class__': str(e.__class__),
                              '__doc__': e.__doc__,
                              'message': e.message,
                              'args': e.args}}
