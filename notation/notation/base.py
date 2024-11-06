
class ExpressionException(Exception):
    pass

def ChangeNotation(expression: str)->str:
    splited_expression = expression.split(" ")
    splited_expression = list(filter(lambda x: x!='', splited_expression))
    if len(splited_expression)==0:
        raise ExpressionException('Empty expression')
    numbers = []
    signs = []
    result = 0
    for i in splited_expression:
        if i.isdigit():
            numbers+=[i]
        elif len(i)==1 and i in "+-/*":
            signs+=[i]
        else:
            raise ExpressionException('Wrong symbol "'+i+'"')

    nc = 0
    sc = 0
    result =  numbers[nc]
    nc+=1
    while nc<len(numbers) or sc<len(signs):
        if nc>=len(numbers) or sc>=len(signs):
            raise ExpressionException('Expression has excess number or sign')
        result +=" "+signs[sc]+" "+ numbers[nc]      
        nc+=1
        sc+=1
    
    return result
        
        
