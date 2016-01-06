custom_widgets = ('CheckBoxList',
                  'RadioButtonList',
                  'InputsTargetsSelector')
                  
fields_widgets = ('Field',
                  'FloatField', 
                  'IntField')

widgets_atoms = {'Field': ['Str'],
                 'CheckBox': ['Bool'],
                 'CheckBoxList':['Atom', 'Value'],
                 'FloatField': ['Float'],
                 'InputsTargetsSelector': ['Atom', 'Value'],
                 'IntField': ['Int'],
                 'ObjectCombo': ['List', 'Str'],                 
                 'RadioButtonList': ['ContainerList', 'Int', 'Value'],
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
    standard_widgets = ', '.join(sorted(['Form', 'GroupBox', 'Label', 
                                         'Notebook', 'Page'] + 
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
        importsCode += 'from custom_views.fields import %s\n' \
                       % ', '.join([w for w in reqd_field_widgets])
    # custom
    reqd_custom_widgets = set(widget_types).intersection(custom_widgets)
    for w in reqd_custom_widgets:
        importsCode += 'from custom_views.%s import %s_Model, %s_View\n' \
                       % (w, w, w)
    
    # Models
    importsCode += '\n# Models\n'
    importsCode += 'from models_views.flowElement import FlowElement\n'

    return importsCode
