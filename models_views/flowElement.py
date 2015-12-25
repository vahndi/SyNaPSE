class FlowElement(object):
    '''
    The base class for all flow elements
    '''    
    elementName = ''
    elementDescription = ''
    elementDocumentation = ''
    precedingElements = []
    doc_root = ''


    def standard_exception(self, e):
        
        return {'Exception': {'__class__': str(e.__class__),
                              '__doc__': e.__doc__,
                              'message': e.message,
                              'args': str(e.args)}}
