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
    
    def _id(self):
        result = ""
        while (self._current_char is not None and self._current_char not in '!:@#$.%;^&*()-+=<>?/{}"|' and not self._current_char.isspace()):
            result+=self._current_char
            self._forward()
        return result

    def init(self, s:str):
        self._pos = 0
        self._text=s
        self._current_char = self._text[self._pos]
    
    def next(self) ->Token:
        while self._current_char is not None:
            if self._current_char.isspace():
                self.__skip()
                continue
            elif self._current_char.isdigit():
                return Token(TokenType.NUMBER, self._number())
            elif self._current_char in ['-', '+','/','*']:
                op = self._current_char
                self._forward()
                return Token(TokenType.OPERATOR, op)
            elif self._current_char=="(":
                val = self._current_char
                self._forward()
                return Token(TokenType.LPAREN, val)
            elif self._current_char==")":
                val = self._current_char
                self._forward()
                return Token(TokenType.RPAREN, val)
            elif self._current_char==":":
                val = self._current_char
                self._forward()
                if self._current_char=="=":
                    val+=self._current_char
                    self._forward()
                    return Token(TokenType.ASSIGN, val)
                else:
                    raise SyntaxError("bad token")
            elif self._current_char==';':
                val = self._current_char
                self._forward()
                return Token(TokenType.SEMI, val)
            elif self._current_char=='.':
                val = self._current_char
                self._forward()
                return Token(TokenType.DOT, val)
            elif self._current_char not in '!:@#.$%^&()=<>?{}"|':
                val = self._id()
                if val=="BEGIN":
                    return Token(TokenType.BEGIN, val)
                elif val=="END":
                    return Token(TokenType.END, val)
                else:
                    return Token(TokenType.ID, val)
            else:
                raise SyntaxError("bad token")
        return Token(TokenType.EOL,"")
    
