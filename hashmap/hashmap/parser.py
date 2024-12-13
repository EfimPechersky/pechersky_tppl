from .lexer import Lexer
from .token import Token, TokenType
from .ast import Number, CmpOp, Condition, Key, AnyKey
class Parser():
    def __init__(self):
        self._lexer=Lexer()
        self._current_token = None
    
    def _check_token(self, type_:TokenType) ->None:
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        else:
            print(self._current_token.value)
            raise SyntaxError('invalid token order')

    def __cond_factor(self):
        token = self._current_token
        if token.value in ["<", ">", "<>", ">=", "<=", "="]:
            self._check_token(TokenType.OPERATOR)
            num=self.__cond_factor()
            return CmpOp(token, num)
        if token.type_==TokenType.NUMBER:
            self._check_token(TokenType.NUMBER)
            return Number(token)
        #if token.type_==TokenType.LPAREN:
        #    self._check_token(TokenType.LPAREN)
        #    result=self.__expr()
        #    self._check_token(TokenType.RPAREN)
        #    return result
        raise SyntaxError("invalid factor")
    
    def __key_factor(self):
        token = self._current_token
        if token.type_==TokenType.NUMBER:
            self._check_token(TokenType.NUMBER)
            return Number(token)
        raise SyntaxError("invalid factor")    
        
    def __cond(self):
        if not (self._current_token):
            result = AnyKey()
        elif (self._current_token.type_ == TokenType.COMMA):
            result = AnyKey()
        else:
            result = self.__cond_factor()
        if not (isinstance(result, AnyKey) or isinstance(result, CmpOp)):
            raise SyntaxError("Wrong condition")
        while self._current_token:
            self._check_token(TokenType.COMMA)
            result = Condition(result, self.__cond())
        return result
    
    def __key(self):
        if self._current_token.type_==TokenType.LPAREN:
                self._check_token(TokenType.LPAREN)
        result = self.__key_factor()
        while self._current_token:
            if self._current_token.type_==TokenType.RPAREN:
                self._check_token(TokenType.RPAREN)
                continue
            self._check_token(TokenType.COMMA)
            result = Key(result, self.__key())
        return result

    def eval_key(self, s:str):
        self._lexer.init(s)
        self._current_token=self._lexer.next()
        return self.__key()
    def eval_cond(self, s:str):
        self._lexer.init(s)
        self._current_token=self._lexer.next()
        return self.__cond()