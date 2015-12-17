from helpers import spc



custom_widgets = ('CheckBoxList_View',
                  'RadioButtonList_View')
                  
fields_widgets = ('FloatField', 
                  'IntField')

widgets_atoms = {'AutoSyncField': ['Str'],
                 'CheckBox': ['Bool'],
                 'CheckBoxList_View':['Atom', 'Value'],
                 'IntField': ['Int'],
                 'FloatField': ['Float'],
                 'ObjectCombo': ['List', 'Str'],                 
                 'RadioButtonList_View': ['ContainerList', 'Int', 'Value'],
                 'SpinBox': ['Int', 'Value']} 


def getImportsCode(element_name, dataframe):
          
    widget_types = sorted(list(set(dataframe['Widget Type'])))

    # Atom
    # ---- 
    atom_types = {'Atom'}
    for widget_type in widget_types:
        atom_types = atom_types.union(widgets_atoms[widget_type])    

    importsCode = '# Atom\n'
    importsCode += 'from atom.api import %s\n\n' \
                   % ', '.join(sorted(atom_types))

    # Enaml    
    # -----
    standard_widgets = ', '.join(sorted(['Form', 'GroupBox', 'Label'] + 
                                        [e for e in widget_types 
                                         if e not in custom_widgets
                                         and e not in fields_widgets]))    
    importsCode += '\n# Enaml\n'
    # conditional
    conditions = dataframe['Visibility Condition']
    if not conditions.isnull().all():
        importsCode += 'from enaml.core.api import Conditional\n'
    # standard
    importsCode += 'from enaml.widgets.api import %s\n' % standard_widgets
    # fields
    reqd_field_widgets = set(widget_types).intersection(fields_widgets)
    if len(reqd_field_widgets) > 0:
        importsCode += 'from enaml.stdlib.fields import %s\n' \
                       % ', '.join([w for w in reqd_field_widgets])
    # custom
    reqd_custom_widgets = set(widget_types).intersection(custom_widgets)
    for w in reqd_custom_widgets:
        w_root = w[: -5]
        importsCode += 'from custom_views.%s import %s_Model, %s_View\n' \
                       % (w_root, w_root, w_root)
    
    # Models
    importsCode += '\n# Models\n'
    importsCode += 'from models_views.flowElement import FlowElement\n'

    return importsCode
