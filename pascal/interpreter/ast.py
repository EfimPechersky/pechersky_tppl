from .token import Token

class Node:
    pass

class Number(Node):

    def __init__(self, token:Token):
        self.token=token

    def __str__(self):
        return f"{self.__class__.__name__}  ({self.token})"

class Variable(Node):

    def __init__(self, token:Token):
        self.token=token

    def __str__(self):
        return f"{self.__class__.__name__}  ({self.token})"

class BinOp(Node):
    def __init__(self,left:Node, op:Token, right:Node):
        self.left=left
        self.op=op
        self.right=right
        

    def __str__(self):
        return f"{self.__class__.__name__}  ({self.left} {self.op} {self.right})"
    
class UnaryOp(Node):
    def __init__(self,op:Token, expr:Node):
        self.op=op
        self.expr=expr
    def __str__(self):
        return f"{self.__class__.__name__}  {self.op.value}({self.expr})"



class AssignOp(Node):
    def __init__(self,var:Variable,op:Token, expr:Node):
        self.var=var
        self.op=op
        self.expr=expr
    def __str__(self):
        return f"{self.__class__.__name__}  {self.var}{self.op.value}{self.expr}"

class Statement(Node):
    def __init__(self,stat:Node):
        self.stat=stat
    def __str__(self):
        return f"{self.__class__.__name__}  {self.stat}"
    
class StatementList(Node):
    def __init__(self,stat:Node,statlist:Node=None):
        self.stat=stat
        self.statlist=statlist
    def __str__(self):
        return f"{self.__class__.__name__}  {self.stat}{self.statlist}"
    
class ComplexStatement(Node):
    def __init__(self, statlist:Node):
        self.statlist = statlist
    def __str__(self):
        return f"{self.__class__.__name__}  {self.statlist}"

class Empty(Node):
    def __str__(self):
        return f"{self.__class__.__name__}"

