from my_token import Token, TokenType

KEYWORDS = ['exp', 'int', 'real']
OPERATORS = ['=','+', '-', '*', '/', '^', '(' , ')', '[', ']', '<', '>', '|', ',', '&']

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def isEnd(self):
        return self.current_char is None

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                tok = Token(TokenType.INT , self.integer())

                if self.current_char == '.':
                    self.advance()
                    return Token(TokenType.REAL, f'{tok.value}.{self.integer()}')

                return tok

            result = ''     
            if self.current_char.isalpha():
                while self.current_char is not None and self.current_char.isalnum():
                    result += self.current_char
                    self.advance()
                if result in KEYWORDS:
                    return Token(TokenType.KEYWORD, result)
                
                if self.current_char == "'":
                    result += self.current_char
                    self.advance()

                return Token(TokenType.ID, result)

            if self.current_char in OPERATORS:
                temp = self.current_char
                self.advance()
                return Token(TokenType.OPERATORS, temp)

            self.error()
                


        return Token.EOF()