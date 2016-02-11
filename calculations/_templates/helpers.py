import sys


custom_widgets = ('CheckBoxList',
                  'CheckBoxFloatFieldList',
                  'InputsTargetsSelector',
                  'OrderedList',
                  'RadioButtonList',
                  'RegExFlags')


def spc(num_spaces):
    
    return ' ' * num_spaces


def to_words(hyphen_string):
    
    words = hyphen_string.split('_')
    words = [word[0].upper() + word[1:] if word not in ('of') else word
             for word in words]
    return ' '.join(words)


def ToWords(CamelCaseString):

    words = CamelCaseString[0]    
    for i in range(1, len(CamelCaseString)):
        if CamelCaseString[i].isupper():
            words += ' '
        words += CamelCaseString[i]
    return words
    

def strlist_to_liststr(strlist):
    '''
    Converts a string of comma separated strings (with or without separating 
    spaces and single or double quotes) to a list of strings
    '''
    liststr = [str(value.strip().strip("'").strip('"'))
               for value in strlist.split(',')]
    return liststr


class widget(object):
    
    @classmethod
    def from_DataFrame_row(cls, widget_row):
        
        return widget(widget_row['Widget Name'], 
                      widget_row['Widget Type'],
                      widget_row['Widget Value'],
                      widget_row['Widget Values'],
                      widget_row['Visibility Condition'],
                      widget_row['Widget Page'],
                      widget_row['Widget Args'],
                      widget_row['Widget Tooltip'])

    
    def __init__(self, w_name, w_type, w_value, w_values, v_condition, w_page,
                 w_args, w_tooltip):
        
        self.w_name = w_name
        self.w_type = w_type
        self.w_value = w_value
        self.w_values = w_values
        self.v_condition = v_condition
        self.w_page = w_page
        self.w_args = w_args
        self.w_tooltip = w_tooltip
        
        
    def get_int_min_value(self):
        
        if isinstance(self.w_values, (str, unicode)):
            try:
                return int(self.w_values.split(',')[0])
            except:
                return None
        else:
            return None


    def get_int_max_value(self):
        
        if isinstance(self.w_values, (str, unicode)):
            try:
                return int(self.w_values.split(',')[1])
            except:
                return None
        else:
            return None


    def get_float_min_value(self):
        
        if isinstance(self.w_values, (str, unicode)):
            try:
                return float(self.w_values.split(',')[0])
            except:
                return None
        else:
            return None


    def get_float_max_value(self):
        
        if isinstance(self.w_values, (str, unicode)):
            try:
                return float(self.w_values.split(',')[1])
            except:
                return None
        else:
            return None
            
            
    def dont_execute_condition(self):
        
        if self.w_type == 'CheckBoxList_View':            
            return 'len(%s) == 0' % self.w_name
            
        elif self.w_type == 'ObjectCombo':
            return "%s == ''" % self.w_name

        else:
            return None
    
    
    def indent1(self):
        
        if isinstance(self.w_page, (str, unicode)):
            return spc(16)
        return spc(8)


    def indent2(self):

        if isinstance(self.w_page, (str, unicode)):
            return spc(20)
        return spc(12)
    
    
    def is_optional(self):
        
        if isinstance(self.w_args, (str, unicode)):
            if 'optional' in self.w_args:
                return True
        return False
        
    
    def option_is_True(self):
        
        if isinstance(self.w_args, (str, unicode)):
            if 'optional(True)' in self.w_args:
                return True
        return False

    
    def has_tooltip(self):
        
        return isinstance(self.w_tooltip, (str, unicode))


    def get_tooltip(self):
        
        try:
            tt = str(self.w_tooltip).encode('string-escape')
            if not '\\n' in tt:
                return "'" + tt + "'"
            else:
                tt_lines = self.w_tooltip.split('\n')
                tt_lines = [l.strip("'") for l in tt_lines]
                tt_lines = ["\t'" + l + "\\n'" for l in tt_lines]
                tt_lines.insert(0, '(')
                tt_lines.append('\t)')
                return '\n'.join(tt_lines)
        except:
            print self.w_tooltip
            sys.exit()
