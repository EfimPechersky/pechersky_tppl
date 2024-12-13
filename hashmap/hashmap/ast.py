from .token import Token

class Node:
    pass

class Number(Node):

    def __init__(self, token:Token):
        self.token=token

    def __str__(self):
        return f"{self.__class__.__name__}  ({self.token})"

class CmpOp(Node):
    def __init__(self, op:Token, number:Node):
        self.op=op
        self.number=number
        

    def __str__(self):
        return f"{self.__class__.__name__}  ({self.op} {self.number})"
    
class Condition(Node):
    def __init__(self,cmp:Node, cond:Node):
        self.cmp=cmp
        self.cond=cond
    def __str__(self):
        return f"{self.__class__.__name__}  {self.cmp},{self.cond}"

class Key(Node):
    def __init__(self,num:Node, key:Node):
        self.num=num
        self.key=key
    def __str__(self):
        return f"{self.__class__.__name__}  {self.num},{self.key}"
    
class AnyKey(Node):
    def __init__(self):
        self.value=''
    def __str__(self):
        return f"{self.__class__.__name__} anykey"
