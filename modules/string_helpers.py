def ToWords(CamelCaseString):

    words = CamelCaseString[0]    
    for i in range(1, len(CamelCaseString)):
        if CamelCaseString[i].isupper():
            words += ' '
        words += CamelCaseString[i]
    return words