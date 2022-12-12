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

    def analyze(self):
        self.stack = []
        self.stack.append(self.grammar.firt_rule)
        self.stack.append(Token.EOF())

        self.read_stack = []
        self.read_stack_id = []
        self.read_stack_op = []
        self.terminator_stack = []

        last_token_exp = None
        token = self.get_next_token()
        self.print_stack()
        while (len(self.stack) > 0 ):
            X = self.get_first_stack()

            terminal = None
            if (token.type == TokenType.INT or token.type == TokenType.REAL or token.type == TokenType.ID):
                terminal = Token(TokenType.KEYWORD, token.type.name.lower())
            else:
                terminal = token

            # TO DEBUG
            print(f'ID  == {[t for t in self.read_stack_id]}')
            print(f'OP  == {[t.value for t in self.read_stack_op]}')
            print(f'TER  == {[t.value for t in self.terminator_stack]}')
            print('------------------------------------------------')
            if (X == terminal):
                self.stack.pop(0)
                if (terminal.type == TokenType.KEYWORD):
                    if (terminal.value in FUNCS):
                        self.read_stack_op.insert(0, token)
                        self.terminator_stack.insert(0, last_token_exp)
                    elif (terminal.value in TYPES):
                        self.read_stack_id.insert(0, token.value)
                elif (terminal.type == TokenType.OPERATORS):
                    if (len(self.terminator_stack) > 0 and token.value == self.terminator_stack[0].value):
                        op = self.read_stack_op.pop(0)
                        self.terminator_stack.pop(0)
                        self.calc_ops(op.value)
                            
                    elif (terminal.value in ARITHMETIC_OPERATORS):
                        self.read_stack_op.insert(0, token)
                        self.terminator_stack.insert(0, last_token_exp)
                
                self.read_stack.append(token) 
                token = self.get_next_token()
            
            elif (X.type != TokenType.NOTTERMINAL):
                raise Exception('Invalid token')

            elif (self.grammar.m_table.value[X][terminal] is None):
                l = [k.value for k, t in self.grammar.m_table.value[X].items() if t is not None]
                raise Exception(f"\'{terminal}\' Invalid token, Expecting the following tokens: {', '.join(l)}")

            else:
                term = self.stack.pop(0)

                if (len(self.terminator_stack) > 0 and term.value_id == self.terminator_stack[0].value_id):
                    op = self.read_stack_op.pop(0)
                    self.terminator_stack.pop(0)

                    self.calc_ops(op.value)

                exp = self.grammar.m_table.value[X][terminal].value[:]
                exp_without_end = [t for t in exp if t != Token.empty()]

                if len(exp_without_end) > 0 :
                    last_token_exp = exp_without_end[-1] 
                self.stack = [*exp_without_end, *self.stack]

            self.print_stack()
            X = self.get_first_stack()
        # print([t.value for t in self.read_stack])

        if (len(self.read_stack_id) > 0):
            return self.read_stack_id[0]
            # print(f'O Resultado da conta é := {self.read_stack_id[0]}')

        return 0

    def get_first_stack(self):
        return self.stack[0] if len(self.stack) > 0 else None

    def get_values(self, n) -> Tuple[float] | float:
        if n == 1:
            return self.read_stack_id.pop(0)
        return tuple([float(self.read_stack_id.pop(0)) for i in range(n)])

    def calc_ops(self, value):
        match (value):
            case '+':
                val2, val1 = self.get_values(2)
                self.read_stack_id.insert(0, val1 + val2)
            case '-':
                val2, val1 = self.get_values(2)
                self.read_stack_id.insert(0, val1 - val2)
            case '*':
                val2, val1 = self.get_values(2)
                self.read_stack_id.insert(0, val1 * val2)
            case '/':
                val2, val1 = self.get_values(2)
                self.read_stack_id.insert(0, val1 / val2)
            case '^':
                val2, val1 = self.get_values(2)
                self.read_stack_id.insert(0, val1 ** val2)
            case 'exp':
                val1 = self.get_values(1)
                self.read_stack_id.insert(0, math.e ** val1)
            # case '%':
            #     self.read_stack_id.insert(0, val1 % val2)
            # case '==':
            #     self.read_stack_id.insert(0, val1 == val2)
            # case '!=':
            #     self.read_stack_id.insert(0, val1 != val2)
            # case '<':
            #     self.read_stack_id.insert(0, val1 < val2)
            # case '>':
            #     self.read_stack_id.insert(0, val1 > val2)
            # case '<=':
            #     self.read_stack_id.insert(0, val1 <= val2)
            # case '>=':
            #     self.read_stack_id.insert(0, val1 >= val2)

    def print_stack(self):
        for token in self.stack:
            print(f'{token.value}◉' if (token.value_id in [t.value_id for t in self.terminator_stack]) else token.value , ' ', end='')
        print()

            