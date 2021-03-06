import pandas as pd
from helpers import spc, widget, strlist_to_liststr
from numpy import int32, int64, float32, float64


indent = spc(4)
nums = (int, float, int32, int64, float32, float64)


def get_Atom_Field(widget):

    str_value = ''    
    if isinstance(widget.w_value, (str, unicode)):
        str_value = "'" + widget.w_value + "'"

    return '%s%s = Str(%s)\n' % (indent, widget.w_name, str_value)


def get_Atom_CheckBox(widget):

    str_value = ''    
    if pd.notnull(widget.w_value):
        str_value = str(bool(widget.w_value))

    return '%s%s = Bool(%s)\n' % (indent, widget.w_name, str_value)  
    

def get_Atom_CheckBoxList(widget):
    
    return '%s%s = Value(Atom)\n' % (indent, widget.w_name)


def get_Atom_CheckBoxFloatFieldList(widget):
    
    return '%s%s = Value(Atom)\n' % (indent, widget.w_name)    
    

def get_Atom_InputsTargetsSelector(widget):
    
    return '%s%s = Value(Atom)\n' % (indent, widget.w_name)


def get_Atom_IntField(widget):
    
    str_value = ''
    if isinstance(widget.w_value, nums) and pd.notnull(widget.w_value):
        str_value = str(int(widget.w_value))
    str_atom = '%s%s = Int(%s)\n' % (indent, widget.w_name, str_value)    

    min_val = widget.get_int_min_value()
    if min_val is not None:
        str_atom += '%s%s_min = Int(%i)\n' % (indent, widget.w_name, min_val)
    max_val = widget.get_int_max_value()
    if max_val is not None:
        str_atom += '%s%s_max = Int(%i)\n' % (indent, widget.w_name, max_val)

    return str_atom


def get_Atom_FloatField(widget):
    
    str_value = ''    
    if isinstance(widget.w_value, nums) and pd.notnull(widget.w_value):
        str_value = str(widget.w_value)
    str_atom = '%s%s = Float(%s)\n' % (indent, widget.w_name, str_value) 

    min_val = widget.get_float_min_value()
    if min_val is not None:
        str_atom += '%s%s_min = Float(%i)\n' % (indent, widget.w_name, min_val)
    max_val = widget.get_float_max_value()
    if max_val is not None:
        str_atom += '%s%s_max = Float(%i)\n' % (indent, widget.w_name, max_val)

    return str_atom


def get_Atom_ObjectCombo(widget):
    
    str_value = ''
    str_values = ''
    if isinstance(widget.w_value, (str, unicode)):
        str_value = "'" + str(widget.w_value) + "'"
    if isinstance(widget.w_values, (str, unicode)):
        str_values = ', ' + str(strlist_to_liststr(widget.w_values)) 
    
    str_atom = '%s%s = Str(%s)\n%s%s_list = List(str%s)\n' % (
                indent, widget.w_name, str_value,
                indent, widget.w_name, str_values)
    
    return str_atom 


def get_Atom_SelectableOrderedList(widget):
    
    return '%s%s = Value(Atom)\n' % (indent, widget.w_name)


def get_Atom_RegExFlags(widget):
    
    return '%s%s = Value(Atom)\n' % (indent, widget.w_name)


def get_Atom_SpinBox(widget):
    
    str_value = ''    
    if isinstance(widget.w_value, (int, float)):
        str_value = str(int(widget.w_value))

    str_atom = '%s%s = Int(%s)\n' % (indent, widget.w_name, str_value)     
    min_val = widget.get_int_min_value()
    if min_val is not None:
        str_atom += '%s%s_min = Int(%i)\n' % (indent, widget.w_name, min_val)
    max_val = widget.get_int_max_value()
    if max_val is not None:
        str_atom += '%s%s_max = Int(%i)\n' % (indent, widget.w_name, max_val)

    return str_atom


getAtomFunc = {'Field': get_Atom_Field,
               'CheckBox': get_Atom_CheckBox,
               'CheckBoxFloatFieldList': get_Atom_CheckBoxFloatFieldList,
               'CheckBoxList': get_Atom_CheckBoxList,
               'FloatField': get_Atom_FloatField,
               'InputsTargetsSelector': get_Atom_InputsTargetsSelector,
               'IntField': get_Atom_IntField,
               'ObjectCombo': get_Atom_ObjectCombo,
               'SelectableOrderedList': get_Atom_SelectableOrderedList,
               'RegExFlags': get_Atom_RegExFlags,
               'SpinBox': get_Atom_SpinBox}


def getAtomWidgetCode(widget_row):
    
    widge = widget.from_DataFrame_row(widget_row)
    atomCode = '%s# %s\n' % (indent, widge.w_name)
    atomCode += getAtomFunc[widge.w_type](widge)
    if widge.is_optional():
        true_str = ('True' if widge.option_is_True()
                      else '')
        atomCode += '%suse_%s = Bool(%s)\n' % (indent, widge.w_name, true_str)
            
    if widge.has_tooltip():
        atomCode += "%s%s_tooltip = %s\n" % (indent, widge.w_name, 
                                               widge.get_tooltip())
    return atomCode


def getAtomCode(dataframe, calc_name):

    atomCode = '\n\n\nclass %s_UI(Atom):\n\n' % calc_name
    
    for iRow in range(len(dataframe)):
        
        widget_row = dataframe.iloc[iRow]
        atomCode += getAtomWidgetCode(widget_row)

        
    return atomCode