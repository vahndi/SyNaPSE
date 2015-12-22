import enaml
from atom.api import Atom, ContainerList, Dict, Int, Str, Value
from inspect import getargspec


with enaml.imports():
    
    from flow_elements.GetColumns import GetColumns
    from flow_elements.PandasPlot import PandasPlot
    from flow_elements.LoadDataFrame import LoadDataFrame

    from flow_elements.sklearn_elements.v0_17.decomposition.PCA import PCA_Model
    from flow_elements.sklearn_elements.v0_17.linear_model.LinearRegression import LinearRegression_Model
    from flow_elements.sklearn_elements.v0_17.linear_model.LogisticRegression import LogisticRegression_Model
    from flow_elements.sklearn_elements.v0_17.cluster.KMeans import KMeans_Model
    from flow_elements.sklearn_elements.v0_17.ensemble.RandomForestClassifier import RandomForestClassifier_Model



class Main_Model(object):
    
    ### Move this to outside the class and bootstrap it ###
    ### See if it is possible to automatically detect and import elements from 
    ### the filesystem at startup ###
    elementModels = [PandasPlot, 
                     GetColumns, 
                     LoadDataFrame, 
                     PCA_Model,
                     LinearRegression_Model,
                     LogisticRegression_Model,
                     KMeans_Model,
                     RandomForestClassifier_Model]

    
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
                    if forElementType in et.precedingElements]



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
        
        self._model.setInputs(**inputs_dict)
        
        
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
                    # Map outputs of the previous element to the inputs of
                    # this element.
                    inputArgNames = newElement.getModelArgNames()
                    prevOutputs = self.uiModel.elements[-1].getOutputs()
                    # TODO: write a function to replace prevOutputs[a] in the 
                    # following line that also traverses through the outputs in
                    # case the required argument is nested below the top level 
                    # of the outputs
                    inputArgsDict = {a: prevOutputs[a] for a in inputArgNames}
                    newElement.setInputs(inputArgsDict)             
                except Exception as e:                    
                    print 'Error adding new element'
                    print e.__doc__
                    print e.message
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

