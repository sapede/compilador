from my_token import Token, TokenType, GenereteIds


FUNCS = ['program', 'begin', 'end', 'read', 'write', 'if', 'then', 'while', 'do', 'else', 'exp']
TYPES = ['integer', 'real', 'numero_int', 'numero_real', 'int']
KEYWORDS = [*FUNCS, *TYPES]

ARITHMETIC_OPERATORS = ['+', '-', '*', '/', '^', '=']
ARITHMETIC_SYMBOLS = ['(' , ')', '[', ']']
RELATIONAL_OPERATORS = ['<>', '>=', '<=', '>', '<']
SYMBOLS = [ '|', ',', ';', ':', '.', 'λ', '$']
COMMENTS = ['{', '}', '/*', '*/']
OPERATORS = [*ARITHMETIC_OPERATORS, *ARITHMETIC_SYMBOLS, *RELATIONAL_OPERATORS, *SYMBOLS , *COMMENTS]

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.generator_ids = GenereteIds()
    
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
    
    def back(self):
        self.pos -= 1
        if self.pos < 0:
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

    def get_next_token(self, with_end_line=False, with_space=False) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                if with_end_line and self.current_char == '\n':
                    self.advance()
                    return Token(TokenType.NEW_LINE, '\n')
                else:
                    if with_space:
                        self.advance()
                        return Token(TokenType.SPACE, ' ')

                    self.skip_whitespace()
                    continue

            if self.current_char.isdigit():
                tok = Token(TokenType.INT , self.integer(), self.generator_ids)

                if self.current_char == '.':
                    self.advance()
                    return Token(TokenType.REAL, f'{tok.value}.{self.integer()}', self.generator_ids)

                return tok

            if self.current_char in OPERATORS:
                first = self.current_char
                self.advance()
                temp = first + self.current_char

                if temp in [*RELATIONAL_OPERATORS, *COMMENTS]:
                    self.advance()
                    return Token(TokenType.OPERATORS, temp, self.generator_ids)

                return Token(TokenType.OPERATORS, first, self.generator_ids)
                
            result = ''     
            if self.current_char.isalpha():
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                    result += self.current_char
                    self.advance()
                if result in KEYWORDS:
                    return Token(TokenType.KEYWORD, result, self.generator_ids)
                
                if self.current_char == "'":
                    result += self.current_char
                    self.advance()

                return Token(TokenType.ID, result, self.generator_ids)


            self.error()
                


        return Token.EOF()