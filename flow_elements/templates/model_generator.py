from helpers import spc, ToWords, widget, strlist_to_liststr
from atom_generator import getAtomCode



def setInputCode_CheckBoxList(widget):
    
    cbl_items = '???'
    if isinstance(widget.w_value, (str, unicode)):
        cbl_items = str(strlist_to_liststr(widget.w_value))

    return '%sself.%s = CheckBoxList_Model(%s)\n' % (
            spc(8), widget.w_name, cbl_items)


def setInputCode_InputsTargetsSelector(widget):
    
    args = ''
    if isinstance(widget.w_args, (str, unicode)):
        args = str(widget.w_args)
    
    return '%sself.%s = InputsTargetsSelector_Model(%s)\n' \
           % (spc(8), widget.w_name, args)
    

def getOutputCode(widget):

    outputCode = ''

    # Conditionalise
    if isinstance(widget.v_condition, (str, unicode)):
        outputCode = '%sif %s:\n%s' % (spc(8), widget.v_condition, spc(4))
    
    if widget.w_type == 'CheckBoxList':
        outputCode += '%s%s = self.%s.getCheckedItemNames()\n' \
                     % (spc(8), widget.w_name, widget.w_name)
    elif widget.w_type == 'InputsTargetsSelector':
        outputCode += '%sinput_columns = self.%s.checked_inputs()\n' % (spc(8), widget.w_name)
        outputCode += '%starget_column = self.%s.selected_target()\n' % (spc(8), widget.w_name)
    else:
        outputCode += "%s'%s': self.uiModel.%s,\n" \
                     % (spc(8), widget.w_name, widget.w_name)

    return outputCode


def getModelCode(element_name, dataframe):
    
    widgets = [widget.from_DataFrame_row(dataframe.iloc[iRow])
               for iRow in range(len(dataframe))]
    
    modelCode = '\n\n\nclass %s_Model(FlowElement):\n\n' % element_name
    modelCode += "%selementName = '%s'\n" % (spc(4), ToWords(element_name))
    modelCode += '%sprecedingElements = []\n' % spc(4)

    modelCode += getAtomCode(dataframe)
    
    # setInputs code
    modelCode += '\n\n%sdef setInputs(self, ???):\n\n' % spc(4)
    modelCode += '%sself._??? = ???\n' % spc(8)
    
    # Initialise checkboxlist views
    for widge in widgets:  
        if widge.w_type == 'CheckBoxList':
            modelCode += setInputCode_CheckBoxList(widge)
        elif widge.w_type == 'InputsTargetsSelector':
            modelCode += setInputCode_InputsTargetsSelector(widge)
            
    # Create uiModel
    modelCode += '%sself.uiModel = %s_Model.ui(' % (spc(8), element_name)
    uiArgs = []
    for widge in widgets:
        if widge.w_type == 'ObjectCombo':            
            if not(isinstance(widge.w_values, (str, unicode))):
                uiArgs.append('%s_list = [???]' % widge.w_name)
        elif widge.w_type in ('CheckBoxList', 'InputsTargetsSelector'):
            uiArgs.append('%s = self.%s.uiModel' % (widge.w_name, 
                                                    widge.w_name))
    if uiArgs:
        modelCode += ', '.join(uiArgs)                
    modelCode += ')\n'
    
    # Get outputs
    modelCode += '\n\n%sdef getOutputs(self):\n\n' % spc(4)
    modelCode += '%s# Assign local variables\n' % spc(8)
    modelCode += '%sargs = {\n' % spc(8)
    for widge in widgets:
        modelCode += getOutputCode(widge)
    modelCode += '}\n'
    
    modelCode += "\n%sreturn {'Outputs': 'No Output'}" % spc(8)
    
    return modelCode