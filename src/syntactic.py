from dataclasses import dataclass, field
from typing import Dict
from grammar import Grammar
from lexer import Lexer
from my_token import Token, TokenType

@dataclass
class Syntactic:
    main_file_path: str = field(default='src/main.txt')
    grammar_file_path: str = field(default='src/grammar.txt')
    grammar: Grammar = field(init=False)
    lexer: Lexer = field(init=False)
    symbol_table: Dict[str, Token] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.grammar = Grammar(self.grammar_file_path)
        with open(self.main_file_path, 'r') as f:
            self.lexer = Lexer(f.read())

    def get_next_token(self):
        return self.lexer.get_next_token()

    def analyze(self):
        self.stack = []
        self.stack.append(self.grammar.firt_rule)
        self.stack.append(Token.EOF())

        token = self.get_next_token()
        self.print_stack()
        while (len(self.stack) > 0 ):
            X = self.get_first_stack()

            terminal = None
            if (token.type == TokenType.INT or token.type == TokenType.REAL or token.type == TokenType.ID):
                terminal = Token(TokenType.KEYWORD, token.type.name.lower())
            else:
                terminal = token


            if (X == terminal):
                self.stack.pop(0)
                token = self.get_next_token()
            
            elif (X.type != TokenType.NOTTERMINAL):
                raise Exception('Invalid token')

            elif (self.grammar.m_table.value[X][terminal] is None):
                l = [k for k, t in self.grammar.m_table.value[X].items() if t is not None]
                raise Exception(f"\'{terminal}\' Invalid token, Expecting the following tokens: {', '.join(l)}")

            else:
                self.stack.pop(0)
                exp = self.grammar.m_table.value[X][terminal].value[:]
                self.stack = [*[t for t in exp if t != Token.end_of_rule()], *self.stack]

            self.print_stack()
            X = self.get_first_stack()

    def get_first_stack(self):
        return self.stack[0] if len(self.stack) > 0 else None

    def print_stack(self):
        for token in self.stack:
            print(token.value, ' ', end='')
        print()

            