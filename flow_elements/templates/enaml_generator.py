from helpers import spc, to_words, widget
import pandas as pd

def get_enaml_Label(widget):
    
    enamlCode = "%sLabel:\n%stext = '%s'\n" % (widget.indent1(), 
                                               widget.indent2(), 
                                              to_words(widget.w_name))
    if widget.has_tooltip():
        enamlCode += '%stool_tip = model.%s_tooltip\n' % (widget.indent2(), 
                                                          widget.w_name)
    return enamlCode


def get_enaml_OptionalStart(widget):
    
    enamlCode = '%sCheckBox:\n' % widget.indent1()
    if widget.has_tooltip():
        enamlCode += '%stool_tip = model.%s_tooltip\n' % (widget.indent2(), 
                                                          widget.w_name)
    enamlCode += "%stext = '%s'\n" % (widget.indent2(), 
                                      to_words(widget.w_name))
    enamlCode += '%schecked := model.use_%s\n' % (widget.indent2(), 
                                                  widget.w_name)
    enamlCode += '%sLabel:\n' % widget.indent1()
    enamlCode += "%stext = 'N/A'\n" % widget.indent2()
    enamlCode += '%svisible << not model.use_%s\n' % (widget.indent2(), 
                                                      widget.w_name)

    return enamlCode


def get_enaml_OptionalEnd(widget):
    
    enamlCode = '%svisible << model.use_%s\n' % (widget.indent2(), 
                                               widget.w_name)
    
    return enamlCode


def get_enaml_Field(widget):
    
    return '%sField:\n%stext := model.%s\n' % (widget.indent1(), 
                                                       widget.indent2(),
                                                       widget.w_name)


def get_enaml_CheckBox(widget):
    
    return '%sCheckBox:\n%schecked := model.%s\n' % (widget.indent1(), 
                                                     widget.indent2(), 
                                                     widget.w_name)


def get_enaml_CheckBoxList_View(widget):
    
    enamlCode = '%sCheckBoxList_View:\n' % widget.indent1()
    enamlCode += '%smodel:= me.model.%s\n' % (widget.indent2(), 
                                                       widget.w_name)
    return enamlCode


def get_enaml_FloatField(widget):
    
    enamlCode = '%sFloatField:\n' % widget.indent1()
    enamlCode += '%svalue := model.%s\n' % (widget.indent2(), 
                                            widget.w_name)
    if widget.get_float_min_value() is not None:
        enamlCode += '%sminimum = model.%s_min\n' % (widget.indent2(), 
                                                     widget.w_name)
    if widget.get_float_max_value() is not None:
        enamlCode += '%smaximum = model.%s_max\n' % (widget.indent2(), 
                                                     widget.w_name)
    return enamlCode


def get_enaml_IntField(widget):
    
    enamlCode = '%sIntField:\n' % widget.indent1()
    enamlCode += '%svalue := model.%s\n' % (widget.indent2(), 
                                            widget.w_name)
    if widget.get_int_min_value() is not None:
        enamlCode += '%sminimum = model.%s_min\n' % (widget.indent2(), 
                                                     widget.w_name)
    if widget.get_int_max_value() is not None:
        enamlCode += '%smaximum = model.%s_max\n' % (widget.indent2(), 
                                                     widget.w_name)
    return enamlCode 


def get_enaml_ObjectCombo(widget):
    
    enamlCode = '%sObjectCombo:\n' % widget.indent1()
    enamlCode += '%sitems = model.%s_list\n' % (widget.indent2(), 
                                                widget.w_name)
    enamlCode += '%sselected := model.%s\n' % (widget.indent2(), 
                                               widget.w_name)
    
    return enamlCode


def get_enaml_Spinbox(widget):
    
    enamlCode = '%sSpinBox:\n' % widget.indent1()
    if widget.get_int_min_value() is not None:
        enamlCode += '%sminimum = model.%s_min\n' % (widget.indent2(), 
                                                     widget.w_name)
    if widget.get_int_max_value() is not None:
        enamlCode += '%smaximum = model.%s_max\n' % (widget.indent2(), 
                                                     widget.w_name)
    
    enamlCode += '%svalue := model.%s' % (widget.indent2(), 
                                          widget.w_name)

    return enamlCode


def get_enaml_InputsTargetsSelector(widget):
    
    enamlCode = '%sInputsTargetsSelector_View:\n' % widget.indent1()
    enamlCode += '%smodel := me.model.%s\n' % (widget.indent2(), 
                                               widget.w_name)
    
    return enamlCode


getEnamlfunc = {'Field': get_enaml_Field,
                'CheckBox': get_enaml_CheckBox,
                'CheckBoxList': get_enaml_CheckBoxList_View,
                'FloatField': get_enaml_FloatField,
                'InputsTargetsSelector': get_enaml_InputsTargetsSelector,
                'IntField': get_enaml_IntField,
                'ObjectCombo': get_enaml_ObjectCombo,
                'SpinBox': get_enaml_Spinbox}  


def conditionVisibility(widgetCode, widget, widget_names):
    
    condition = widget.v_condition
    condition_words = condition.split(' ')
    condition_words = ['model.' + w if w in widget_names else w
                                        for w in condition_words]
    formatted_condition = ' '.join(condition_words)
    
    enamlCode = '%sConditional:\n' % widget.indent1()
    enamlCode += '%scondition << %s\n' % (widget.indent2(), formatted_condition)
    code_lines = [spc(4) + line + '\n' for line in widgetCode.split('\n')]
    return enamlCode + ''.join(code_lines)


def getEnamlWidgetCode(widget, widget_names):
    
    # Label (or checkbox for optional values)
    if isinstance(widget.w_args, (str, unicode)):
        if 'optional' in widget.w_args:
            enamlCode = get_enaml_OptionalStart(widget)
        else:
            enamlCode = get_enaml_Label(widget)
    else:
        enamlCode = get_enaml_Label(widget)

    # Widget code        
    enamlCode += getEnamlfunc[widget.w_type](widget)
    
    # Closer for optional values
    if widget.is_optional():
            enamlCode += get_enaml_OptionalEnd(widget)
    
    # Add Tooltip
    if widget.has_tooltip():
        enamlCode += '%stool_tip = model.%s_tooltip\n' % (widget.indent2(), 
                                                          widget.w_name)

    # Add Conditional code
    if isinstance(widget.v_condition, (str, unicode)):
        enamlCode = conditionVisibility(enamlCode, 
                                        widget, 
                                        widget_names)
    
    enamlCode += '\n'
    
    return enamlCode


def getEnamlCode(element_name, dataframe):

    enamlCode = '\n\n\nenamldef %s_View(GroupBox): me:\n\n' % element_name
    enamlCode += '%sattr model\n\n' % spc(4) 
    if not(isinstance(dataframe.iloc[0]['Widget Page'], (str, unicode))):
        enamlCode += '%sForm:\n\n' % spc(4)
    
    widget_names = list(dataframe['Widget Name'])
    
    prev_page = None
    for iRow in range(len(dataframe)):
        widget_row = dataframe.iloc[iRow]
        widget_page = widget_row['Widget Page']
        if pd.isnull(widget_page):
            widget_page = None
        if ((iRow == 0 and widget_page is not None) or 
            (prev_page is not None and widget_page != prev_page)):
            if iRow == 0:
                enamlCode += '%sNotebook:\n\n' % spc(4)
            enamlCode += '%sPage:\n\n' % spc(8)
            enamlCode += "%stitle = '%s'\n" % (spc(12), widget_page)
            enamlCode += '%sclosable = False\n\n' % spc(12)
            enamlCode += '%sForm:\n\n' % spc(12)
        # Add the code for the widget
        widge = widget.from_DataFrame_row(widget_row)
        enamlCode += getEnamlWidgetCode(widge, widget_names)
        prev_page = widget_page
        
    return enamlCode


