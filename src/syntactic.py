from dataclasses import dataclass, field
import math
from typing import Dict, List, Tuple
from grammar import Grammar
from lexer import Lexer
from my_token import Token, TokenType
from lexer import ARITHMETIC_OPERATORS, RELATIONAL_OPERATORS, SYMBOLS, FUNCS, TYPES

@dataclass
class Syntactic:
    main_file_path: str = field(default='src/main.txt')
    grammar_file_path: str = field(default='src/grammar.txt')
    grammar: Grammar = field(init=False)
    lexer: Lexer = field(init=False)
    symbol_table: Dict[str, Token] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.grammar = Grammar(self.grammar_file_path)
        with open(self.main_file_path, 'r', encoding='utf-8') as f:
            self.lexer = Lexer(f.read())

    def get_next_token(self):
        return self.lexer.get_next_token()
    
    def clean_token(self, token):
        if token.type == TokenType.ID:
            return Token(token.type, "id")
        elif token.type == TokenType.INT:
            return Token(TokenType.KEYWORD, "numero_int")
        elif token.type == TokenType.REAL:
            return Token(TokenType.KEYWORD, "numero_real")
        else:
            return token

    def analyze(self):
        self.stack = []
        self.stack.append(self.grammar.firt_rule)
        self.stack.append(Token.EOF())
        self.read_stack_term = []
        self.read_stack_not_term = []

        token = self.get_next_token()
        token_cleaned = self.clean_token(token)
        # self.print_stack()
        while (len(self.stack) > 0 ):
            X = self.get_first_stack()
            # print(f"token = {token.value}")
            if (X == token or X.type == token_cleaned.type ):
                term = self.stack.pop(0)
                self.read_stack_term.append(term)
                token = self.get_next_token()
                token_cleaned = self.clean_token(token)
            
            elif (X.type != TokenType.NOTTERMINAL):
                raise Exception('Invalid token')

            elif (self.grammar.m_table.value[X][token_cleaned] is None):
                l = [k.value for k, t in self.grammar.m_table.value[X].items() if t is not None]
                raise Exception(f"\'{token}\' Invalid token, Expecting the following tokens: {', '.join(l)}")

            else:
                term = self.stack.pop(0)
                self.read_stack_not_term.append(term)
                exp = self.grammar.m_table.value[X][token_cleaned].value[:]
                exp_without_end = [t for t in exp if t != Token.empty()]
                self.stack = [*exp_without_end, *self.stack]

            # self.print_stack()
            

        return self.read_stack_not_term, self.read_stack_term

    def get_first_stack(self):
        return self.stack[0] if len(self.stack) > 0 else None

    def print_stack(self):
        print("________________________________________________________________________")
        for token in self.stack:
            token_formated = token.value if token.type != TokenType.NOTTERMINAL else f'<{token.value}>'
            print(f'{token_formated}', ' ', end='')
        print("")

            