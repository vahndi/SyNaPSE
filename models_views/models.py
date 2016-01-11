import enaml
from atom.api import Atom, ContainerList, Dict, Int, Str, Value
from inspect import getargspec
from pydoc import locate
from fileFunctions import getFileNames


pkg_sys = (('flow_elements.pandas.v0_17_1', 
            './flow_elements/pandas/v0_17_1'),
           ('flow_elements.sklearn.v0_17.generate',
            './flow_elements/sklearn/v0_17/generate'),
           ('flow_elements.pandas.v0_17_1.Statistics', 
            './flow_elements/pandas/v0_17_1/Statistics'),
           ('flow_elements.pandas.v0_17_1.CumulativeStatistics', 
            './flow_elements/pandas/v0_17_1/CumulativeStatistics'),
           ('flow_elements.pandas.v0_17_1.ExpandingWindowStatistics', 
            './flow_elements/pandas/v0_17_1/ExpandingWindowStatistics'),
           ('flow_elements.pandas.v0_17_1.ExponentiallyWeightedStatistics', 
            './flow_elements/pandas/v0_17_1/ExponentiallyWeightedStatistics'),
           ('flow_elements.pandas.v0_17_1.RollingWindowStatistics', 
            './flow_elements/pandas/v0_17_1/RollingWindowStatistics'),
           ('flow_elements.sklearn.v0_17.linear_model',
            './flow_elements/sklearn/v0_17/linear_model'),
           ('flow_elements.sklearn.v0_17.cluster',
            './flow_elements/sklearn/v0_17/cluster'),
           ('flow_elements.sklearn.v0_17.ensemble',
            './flow_elements/sklearn/v0_17/ensemble'),
           ('flow_elements.sklearn.v0_17.decomposition',
            './flow_elements/sklearn/v0_17/decomposition'))


def getModels(package_path, sys_path):
    
    model_list = []
    model_files = getFileNames(sys_path, endsWith = '.enaml')
    for model_file in model_files:
        model_name = model_file.split('.')[0]
        print 'Loading element: %s...' % model_name
        model_list.append(locate('%s.%s.%s_Model' 
                                     % (package_path, model_name, model_name)))
#        try:
#            model_list.append(locate('%s.%s.%s_Model' 
#                                     % (package_path, model_name, model_name)))
#        except Exception as e:
#            print '!!! Error !!!'
#            print {'__class__': str(e.__class__),
#                   '__doc__': e.__doc__,
#                   'message': e.message,
#                   'args': str(e.args)}
            
    return model_list
    

element_models = []
with enaml.imports():
    for pkg_path, sys_path in pkg_sys:
        element_models.extend(getModels(pkg_path, sys_path))               



class Main_Model(object):
    

    elementModels = element_models


    def __init__(self):

        self.elementDict = {e.elementName: e for e in Main_Model.elementModels}                     

        self.chooseElement = ChooseElement(parent = self,
                                           elementTypes = 
                                           Main_Model.elementModels)

        self.flowList = FlowList(parent = self,
                                 elementDict = self.elementDict)


    def updateChooseElementTypes(self, precedingElementTypeName):
        
        self.chooseElement.updateUIElementTypes(precedingElementTypeName)



class FlowElementType(object):

    
    def __init__(self, elementTypeName, elementType):
        
        self._elementTypeName = elementTypeName
        self._elementType = elementType  

        
    def __str__(self):
        
        return self._elementTypeName
        
        
    def getType(self):
        
        return self._elementType



class ChooseElement(object):
    
    
    class ui(Atom):
        
        elementTypes = ContainerList(str)
        selectedElementType = Str()
        
    
    def __init__(self, parent, elementTypes, precedingElementType = None):

        self._parent = parent

        if not precedingElementType:
            
            self.elementTypes = elementTypes
            ets = self.getFollowingElementTypes(precedingElementType)
            etNames = [et.elementName for et in ets]
            self.uiModel = ChooseElement.ui(elementTypes = etNames)


    def updateUIElementTypes(self, precedingElementTypeName):
        
        elementType = [et for et in self.elementTypes 
                       if et.elementName == precedingElementTypeName][0]
        followingElementTypes = self.getFollowingElementTypes(elementType)
        self.uiModel.elementTypes = [et.elementName 
                                     for et in followingElementTypes]


    def getFollowingElementTypes(self, forElementType):
        
        if forElementType is None:
            return [et for et in self.elementTypes 
                    if not et.precedingElements]
        else:
            return [et for et in self.elementTypes
                    for etPreceder in et.precedingElements
                    if issubclass(forElementType, etPreceder)]



class FlowElement(object):


    def __init__(self, model, container):
        '''
        Arguments
        ---------
        model: 
            An instance of a flow element model, defined in Main_Model.
        container: 
            The container of the element e.g. a FlowList instance.
        '''
        self._model = model
        self._container = container
        
    
    def getModel(self):
        
        return self._model


    def __str__(self):
        
        return self._model.elementName
        
    
    def select(self):

        self._container.selectElement(self)


    def getModelArgNames(self):
        
        arg_names = getargspec(self._model.setInputs).args
        arg_names.remove('self')
        return arg_names


    def setInputs(self, inputs_dict):
        
        self._model.setInputs(** inputs_dict)
        
        
    def getOutputs(self):

        return self._model.getOutputs()



class FlowList(object):

    
    class ui(Atom):
        
        elements = ContainerList(FlowElement)
        selectedElement = Value(FlowElement)
        selectedIndex = Int(-1)
        selectedElementOutputs = Dict(default = {})

        
    def __init__(self, parent, elementDict):
        
        self._parent = parent
        self._elementDict = elementDict
        self.uiModel = FlowList.ui()
        self._elements = []
        
        
    def getElements(self):
        
        return self._elements

    
    def numElements(self):
        
        return len(self._elements)
        

    def selectElement(self, flowElement):
        
        self.uiModel.selectedElement = flowElement        
        self.uiModel.selectedElementOutputs = flowElement.getOutputs()

        
    def refreshSelectedElementOutputs(self):
        
        flowElement = self.uiModel.selectedElement
        self.uiModel.selectedElement = None
        self.uiModel.selectedElementOutputs = {}
        self.selectElement(flowElement)


    def appendElement(self, elementName = None):
        
        if elementName is not None:
            
            constructor = self._elementDict[elementName]
            newElement = FlowElement(model = constructor(),
                                     container = self)

            if self.numElements() > 0:

                try:
                    # Map outputs of previous element to inputs of this element
                    inputArgNames = newElement.getModelArgNames()
                    prevOutputs = self.uiModel.elements[-1].getOutputs()
                    # TODO: write a function to replace prevOutputs[a] in the 
                    # following line that also traverses through the outputs in
                    # case the required argument is nested below the top level 
                    # of the outputs
                    inputArgsDict = {a: prevOutputs[a] 
                                     for a in inputArgNames
                                     if a in prevOutputs}
                    newElement.setInputs(inputArgsDict)  
                    
                except Exception as e:
                    
                    print 'Error adding new element'
                    print '__class__:', str(e.__class__)
                    print '__doc__:', e.__doc__
                    print 'message:', e.message
                    print 'args:', str(e.args)
                    
                    return
            
            self._elements.append(newElement)
            self.uiModel.selectedIndex = len(self._elements) - 1
            self.uiModel.elements = self._elements
            self.selectElement(newElement)
            
            self._parent.updateChooseElementTypes(elementName)

    
    
#class FlowGraph(Atom):
#    
#    flowGraph = nx.DiGraph()
#    elementDict = Dict()
#    numNodes = 1
#    
#    def addElement(self, elementTypeName, parentElementName = None):
#        
#        self.flowGraph.add_node('%s_%i' %(elementTypeName, numNodes)
#        self.elementDict[elementName]

