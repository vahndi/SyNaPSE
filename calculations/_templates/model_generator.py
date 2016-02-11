from helpers import spc, ToWords, widget, strlist_to_liststr
from atom_generator import getAtomCode



def setInputCode_CheckBoxList(widget):
    
    cbl_items = '[???]'
    if isinstance(widget.w_value, (str, unicode)):
        cbl_items = str(strlist_to_liststr(widget.w_value))

    return '%sself.%s = CheckBoxList_Model(%s)\n' % (
            spc(8), widget.w_name, cbl_items)


def setInputCode_CheckBoxFloatFieldList(widget):
    
    cbl_items = '[???]'
    if isinstance(widget.w_value, (str, unicode)):
        cbl_items = str(strlist_to_liststr(widget.w_value))

    return '%sself.%s = CheckBoxFloatFieldList_Model(%s)\n' % (
            spc(8), widget.w_name, cbl_items)


def setInputCode_OrderedList(widget):
    
    return '%sself.%s = OrderedList_Model()\n' % (
            spc(8), widget.w_name)


def setInputCode_InputsTargetsSelector(widget):
    
    args = ''
    if isinstance(widget.w_args, (str, unicode)):
        args = str(widget.w_args)
    
    return '%sself.%s = InputsTargetsSelector_Model(%s)\n' \
           % (spc(8), widget.w_name, args)
    

def getOutputCode(widget):

    outputCode = ''

    # Conditionalise
    start_cond = end_cond = ''
    if isinstance(widget.v_condition, (str, unicode)):
        start_cond = '('
        cond_indent = len(widget.w_name) + 21
        end_cond = '\n%sif self.uiModel.%s \n%selse None)' \
                   % (spc(cond_indent), widget.v_condition, spc(cond_indent))
    
    if widget.w_type == 'CheckBoxList':
        outputCode += '%s%s = %sself.%s.checked_item_names()%s\n' \
                      % (spc(16), widget.w_name, start_cond, widget.w_name, end_cond)
    elif widget.w_type == 'CheckBoxFloatFieldList':
        outputCode += '%s%s = %sself.%s.checked_item_values()%s\n' \
                      % (spc(16), widget.w_name, start_cond, widget.w_name, end_cond)
    elif widget.w_type == 'InputsTargetsSelector':
        outputCode += '%sinput_columns = %sself.%s.checked_inputs()%s\n' \
                      % (spc(16), start_cond, widget.w_name, end_cond)
        outputCode += '%starget_column = %sself.%s.selected_target()%s\n' \
                      % (spc(16), start_cond, widget.w_name, end_cond)
    elif widget.w_type == 'OrderedList':
        outputCode += '%s%s = %sself.%s.selected_item_names()%s\n' \
                      % (spc(16), widget.w_name, start_cond, widget.w_name, end_cond)
    else:
        opt_start = opt_end = ''
        if widget.is_optional():
            opt_start = '(None \nif not self.uiModel.use_%s \nelse ' \
                        % widget.w_name 
            opt_end = ')'
        outputCode += "%s'%s': %s%sself.uiModel.%s%s%s,\n" \
                     % (spc(16), widget.w_name, opt_start, start_cond, 
                                 widget.w_name, end_cond, opt_end)

    return outputCode


def getModelCode(calc_name, dataframe):
    
    widgets = [widget.from_DataFrame_row(dataframe.iloc[iRow])
               for iRow in range(len(dataframe))]
    
    modelCode = getAtomCode(dataframe, calc_name)    
    
    modelCode += '\n\n\nclass %s_Model(Calculation_Model):\n\n' % calc_name
    modelCode += "%scalc_name = '%s'\n" % (spc(4), ToWords(calc_name))
    
    
    # setInputs code
    modelCode += '\n\n%sdef setInputs(self, ???):\n\n' % spc(4)
    modelCode += '%sself._??? = ???\n' % spc(8)
    
    # Initialise checkboxlist views
    for widge in widgets:  
        if widge.w_type == 'CheckBoxList':
            modelCode += setInputCode_CheckBoxList(widge)
        if widge.w_type == 'CheckBoxFloatFieldList':
            modelCode += setInputCode_CheckBoxFloatFieldList(widge)
        elif widge.w_type == 'OrderedList':
            modelCode += setInputCode_OrderedList(widge)
        elif widge.w_type == 'InputsTargetsSelector':
            modelCode += setInputCode_InputsTargetsSelector(widge)
            
    # Create uiModel
    modelCode += '%sself.uiModel = %s_UI(' % (spc(8), calc_name)
    uiArgs = []
    for widge in widgets:
        if widge.w_type == 'ObjectCombo':            
            if not(isinstance(widge.w_values, (str, unicode))):
                uiArgs.append('%s_list = [???]' % widge.w_name)
        elif widge.w_type in ('CheckBoxList', 
                              'InputsTargetsSelector',
                              'OrderedList'):
            uiArgs.append('%s = self.%s.uiModel' % (widge.w_name, 
                                                    widge.w_name))
        elif widge.w_type == 'CheckBoxFloatFieldList':
            uiArgs.append('%s = self.%s' % (widge.w_name, 
                                            widge.w_name))            
    if uiArgs:
        modelCode += ', '.join(uiArgs)                
    modelCode += ')\n'
    
    # Get outputs
    modelCode += '\n\n%sdef getOutputs(self):' % spc(4)
    modelCode += '\n\n%stry:' % spc(8)
    modelCode += '\n\n%s# Assign local variables\n' % spc(12)
    modelCode += '%sargs = {\n' % spc(12)
    for widge in widgets:
        modelCode += getOutputCode(widge)
    modelCode = modelCode[:-2]
    modelCode += '\n%s}' % spc(16)
    modelCode += '\n\n%sexcept Exception as e:' % spc(8)
    modelCode += "\n\n%sreturn self.standard_exception(e)" % spc(12)
    
    return modelCode