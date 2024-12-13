from .token import Token, TokenType
class Lexer():
    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def _forward(self):
        self._pos+=1
        if self._pos > len(self._text)-1:
            self._current_char=None
        else:
            self._current_char=self._text[self._pos]
    
    def __skip(self):
        while (self._current_char is not None and self._current_char.isspace()):
            self._forward()

    def _number(self):
        result = ""
        while (self._current_char is not None and
               (self._current_char.isdigit() or self._current_char=='.')):
            result+=self._current_char
            self._forward()
        return result

    def init(self, s:str):
        self._pos = 0
        self._text=s
        if len(s)>0:
            self._current_char = self._text[self._pos]
    
    def next(self) ->Token:
        while self._current_char is not None:
            if self._current_char.isspace():
                self.__skip()
                continue
            elif self._current_char.isdigit():
                return Token(TokenType.NUMBER, self._number())
            elif self._current_char in ['<', '>', '=']:
                op = self._current_char
                if self._text[self._pos+1] in ['<','>', '=']:
                    self._forward()
                    op += self._current_char
                self._forward()
                if not self._current_char.isdigit():
                    raise SyntaxError("Wrong operator")
                return Token(TokenType.OPERATOR, op)
            elif self._current_char=="(":
                val = self._current_char
                self._forward()
                return Token(TokenType.LPAREN, val)
            elif self._current_char==")":
                val = self._current_char
                self._forward()
                return Token(TokenType.RPAREN, val)
            elif self._current_char==",":
                val = self._current_char
                self._forward()
                return Token(TokenType.COMMA, val)
            else:
                raise SyntaxError("bad token")