from helpers import custom_widgets 


fields_widgets = ('Field',
                  'FloatField', 
                  'IntField')

widgets_atoms = {'Field': ['Str'],
                 'CheckBox': ['Bool'],
                 'CheckBoxList': ['Atom', 'Value'],
                 'CheckBoxFloatFieldList': ['Atom', 'Value'],
                 'FloatField': ['Float'],
                 'InputsTargetsSelector': ['Atom', 'Value'],
                 'IntField': ['Int'],
                 'ObjectCombo': ['List', 'Str'],  
                 'SelectableOrderedList': ['Atom', 'Value'],               
                 'RadioButtonList': ['ContainerList', 'Int', 'Value'],
                 'RegExFlags': ['Atom', 'Value'],
                 'SpinBox': ['Int', 'Value']} 


def getImportsCode(calc_name, dataframe):
          
    widget_types = sorted(list(set(dataframe['Widget Type'])))

    # Atom
    # ---- 
    atom_types = {'Atom'}
    for widget_type in widget_types:
        atom_types = atom_types.union(widgets_atoms[widget_type])
    try:
        if dataframe['Widget Args'].str.contains('optional').any():
            atom_types = list(set(list(atom_types) + ['Bool']))
    except:
        pass
    importsCode = '# Atom\n'
    importsCode += 'from atom.api import %s\n\n' \
                   % ', '.join(sorted(atom_types))

    # Enaml    
    # -----
    standard_widgets = ['Form', 'GroupBox', 'Label', 'Notebook', 'Page'] + \
                       [e for e in widget_types 
                        if e not in custom_widgets
                        and e not in fields_widgets]
    try:
        if dataframe['Widget Args'].str.contains('optional').any():
            standard_widgets = set(standard_widgets + ['CheckBox'])
    except:
        pass
    str_standard_widgets = ', '.join(sorted(standard_widgets))
    
    importsCode += '\n# Enaml\n'
    # conditional
    conditions = dataframe['Visibility Condition']
    if not conditions.isnull().all():
        importsCode += 'from enaml.core.api import Conditional\n'
    # standard
    importsCode += 'from enaml.widgets.api import %s\n' % str_standard_widgets
    # fields
    reqd_field_widgets = set(widget_types).intersection(fields_widgets)
    if len(reqd_field_widgets) > 0:
        importsCode += 'from custom_views.fields import %s\n' \
                       % ', '.join([w for w in reqd_field_widgets])
    # custom
    reqd_custom_widgets = set(widget_types).intersection(custom_widgets)
    for w in reqd_custom_widgets:
        importsCode += 'from custom_views.%s import %s_Model, %s_View\n' \
                       % (w, w, w)
    
    # Models
    importsCode += '\n# Models\n'
    importsCode += 'from models_views.calculation import Calculation_Model\n'

    return importsCode
