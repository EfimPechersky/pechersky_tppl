from .parser import Parser
from .token import Token, TokenType
from .ast import Number, CmpOp, Condition, Key, AnyKey

class HashMap(dict):
    def visit(self, node):
        if isinstance(node, Key):
            return self._visit_key(node)
        elif isinstance(node, Number):
            return self._visit_number(node)
        elif isinstance(node, Condition):
            return self._visit_cond(node)
        elif isinstance(node, CmpOp):
            return self._visit_cmp(node)
        elif isinstance(node, AnyKey):
            return self._visit_anykey(node)
        
    def _visit_key(self, node:Key):
            nk=self.visit(node.key)
            if isinstance(nk,tuple):
                return (self.visit(node.num),)+nk
            else:
                return (self.visit(node.num),)+(nk,)
            
    def _visit_number(self, node:Number):
        return float(node.token.value)
    
    def _visit_cond(self, node:Condition):
        nc=self.visit(node.cond)
        if isinstance(nc[0],tuple):
            return (self.visit(node.cmp),)+nc
        else:
            return (self.visit(node.cmp),)+(nc,)
        
    def _visit_cmp(self, node:CmpOp):
        return node.op.value, self.visit(node.number)
    
    def _visit_anykey(self, node:AnyKey):
        return 'any', 'key'
    
    def _check_condition(self, cond, key):
        if (type(key)==float and type(cond[0])!=str)\
              or (type(cond[0])==str and type(key)!=float) :
            return False
        elif type(key)==float and type(cond[0])==str:
            return self._check_cmp(key, cond[0], cond[1])
        if len(key)!=len(cond):
            return False
        for i in range(len(key)):
            if not self._check_cmp(key[i], cond[i][0], cond[i][1]):
                return False
        return True
    
    def _check_cmp(self, key, op, num):
        match(op):
            case ">":
                return key>num
            case "<":
                return key<num
            case "=":
                return key==num
            case ">=":
                return key>=num
            case "<=":
                return key<=num
            case "<>":
                return key!=num
            case "any":
                return True
    
    def _check_key(self, key):
        for i in key:
            if i not in "1234567890()<>= ,.":
                return False
        return True

    def ploc(self, cond:str):
        parsedcond=Parser().eval_cond(cond)
        vcond=self.visit(parsedcond)
        print(vcond)
        ans={}
        for k,v in self.__dict__.items():
            if self._check_key(k):
                parsedkey=Parser().eval_key(k)
                print(parsedkey)
                keys=self.visit(parsedkey)
                if self._check_condition(vcond, keys):
                    ans[keys]=v
        return ans
    
    def iloc(self, key:int):
        sorted_dict=sorted(self.__dict__)
        return self.__dict__[sorted_dict[key]]
    
    def __setitem__(self, key:str, value):
        self.__dict__[key]=value
    def __getitem__(self, key:str):
        return self.__dict__[key]
    
                
    
