from .token import Token, TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnaryOp, AssignOp, Variable,StatementList, ComplexStatement, Statement, Empty
class Parser():

    def __init__(self):
        self._lexer=Lexer()
        self._current_token = None
    
    def _check_token(self, type_:TokenType) ->None:
        print(self._current_token)
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        else:
            print(self._current_token.value)
            raise SyntaxError('invalid token order')

    def __factor(self)->Number:
        token = self._current_token
        if token.value=="+":
            self._check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())
        if token.value=="-":
            self._check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())
        if token.type_==TokenType.NUMBER:
            self._check_token(TokenType.NUMBER)
            return Number(token)
        if token.type_==TokenType.ID:
            self._check_token(TokenType.ID)
            return Variable(token)
        if token.type_==TokenType.LPAREN:
            self._check_token(TokenType.LPAREN)
            result=self.__expr()
            self._check_token(TokenType.RPAREN)
            return result
        raise SyntaxError("invalid factor")
        
        
    def __term(self)->BinOp:
        result = self.__factor()
        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ['*', '/']:
                break
            token = self._current_token
            self._check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.__factor())
        return result
    
    def __expr(self) ->BinOp:
        result = self.__term()
        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ['+', '-']:
                break
            token = self._current_token
            self._check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.__term())
        return result
    
    def __assign(self) ->AssignOp:
        result=self.__factor()
        while self._current_token and (self._current_token.type_ == TokenType.ASSIGN) and self._current_token.type_ !=TokenType.SEMI:
            if self._current_token.value != ":=":
                break
            token = self._current_token
            self._check_token(TokenType.ASSIGN)
            result = AssignOp(result, token, self.__expr())
        return result
    
    def __statement(self)->Statement:
        if self._current_token.type_==TokenType.BEGIN:
            result = Statement(self.__complex_statement())
            self._check_token(TokenType.SEMI)
        elif self._current_token.type_==TokenType.ID:
            result = Statement(self.__assign())
            if self._current_token.type_!=TokenType.END:
                self._check_token(TokenType.SEMI)

        elif self._current_token.type_==TokenType.END:
            return Empty()
        else:
            raise SyntaxError("Wrong statement")
        return result
    
    def __statement_list(self)->StatementList:
        result=self.__statement()
        print(result)
        while self._current_token and self._current_token.type_ !=TokenType.END:
            result = StatementList(result, self.__statement_list())
        return result
    
    def __complex_statement(self)->ComplexStatement:
        self._check_token(TokenType.BEGIN)
        result = ComplexStatement(self.__statement_list())
        self._check_token(TokenType.END)
        return result
    

    def eval(self, s:str)->ComplexStatement:
        self._lexer.init(s)
        self._current_token=self._lexer.next()
        result = self.__complex_statement()
        self._check_token(TokenType.DOT)
        return result

