from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple, TypeVar
from lexer import Lexer
from my_token import Token, TokenType
from ordered_set import OrderedSet

T = TypeVar("T")

class MySet(OrderedSet):
    def __init__(self, iterable: Optional[Iterable[T]] = None):
        super().__init__(iterable)
    def __str__(self) -> str:
        return '{' + ', '.join(map(str, self)) + '}'

@dataclass
class Expr(object):
    value: List[Token] = field(default_factory=list)
    
    def __hash__(self) -> int:
        return hash(tuple(self.value))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Expr):
            return False

        for i in range(len(self.value)):
            if self.value[i] != other.value[i]:
                return False
        return True

@dataclass
class Rule(object):
    name: str = ''
    value: List[Expr] = field(default_factory=list)

@dataclass
class TokenFirstFollow(object):
    def __init__(self, token: Token, expr: Expr):
        self.token = token
        self.expr = expr

    def __hash__(self) -> int:
        temp = [self.token.__hash__(), self.expr.__hash__()]
        return hash(tuple(temp))

    def __eq__(self, other) -> bool:
        if not isinstance(other, TokenFirstFollow):
            return False
        return self.token == other.token and self.expr == other.expr

    def __str__(self) -> str:
        return f'\'{self.token.value}\''

    def __repr__(self) -> str:
        return self.__str__()

    def to_string(self) -> str:
        return f'{self.token} -> {self.expr}'

    def __lt__(self, other):
        return self.token < other.token

class M_Table(object):
    def __init__(self, grammar: Dict[Token, Rule], non_terminals: Set[Token], terminals:Set[Token], firsts: Dict[Token, Set[TokenFirstFollow]], follows: Dict[Token,Set[TokenFirstFollow]], value: Dict[Token, Dict[Token, Expr]] = {}):
        self.grammar = grammar
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.terminals.remove(Token.end_of_rule())
        self.terminals.add(Token.EOF())
        self.firts = firsts
        self.follows = follows
        self.value = value
        self.create_m_table()
        self.fill_table()

    def create_m_table(self):
        self.value = {}
        for non_terminal in self.non_terminals:
            self.value[non_terminal] = {}
            for terminal in self.terminals:
                self.value[non_terminal][terminal] = None   

    def set_m_table(self, non_terminal: Token, terminal: Token, expr: Expr):
        self.value[non_terminal][terminal] = expr

    def get_m_table(self, non_terminal: Token, terminal: Token):
        return self.value[non_terminal][terminal]
    
    def fill_table(self):
        for key, _ in self.grammar.items():
            first = self.firts[key]
            for tok in first:
                if tok.token == Token.end_of_rule():
                    for elem_f in self.follows[key]:
                        self.set_m_table(key, elem_f.token, tok.expr)
                else:
                    self.set_m_table(key, tok.token, tok.expr)

    def print_table(self):
        print(''.rjust(14," "), end='')
        for terminal in self.terminals:
            print(f'{terminal.value}'.center(14," "), end='')
        print()
        print('_'*500)
        for key, rule in self.grammar.items():
            print(f'{key.value} ->'.center(14," "), end='')
            for terminal in self.terminals:
                if self.value[key][terminal] is not None:
                    print(f'{key.value} -> { " ".join([t.value for t in self.value[key][terminal].value])}'.center(14," "), end='')
                else:
                    print(f'None'.center(14," "), end='')
            print('')

                    

class Grammar(object):
    def __init__(self, grammar_file):
        self.grammar_file = grammar_file
        self.terminals = set()
        self.non_terminals = set()
        self.grammar = self.read_grammar()
        self.m_table = self.create_m_table()


    def read_grammar(self) -> Dict[Token, Rule]:

        init = True

        with open(self.grammar_file, 'r') as f:
            self.lex = Lexer(f.read())
            grammar = dict()
            last_non_terminal = None

            while (token := self.lex.get_next_token()).type != TokenType.EOF:
                if token.type == TokenType.OPERATORS and token.value == '<':
                    non_terminal = self.lex.get_next_token()
                    if non_terminal.type != TokenType.ID:
                        raise Exception('Invalid non-terminal')

                    non_terminal.type = TokenType.NOTTERMINAL

                    if init:
                        self.firt_rule = non_terminal
                        init = False

                    self.non_terminals.add(non_terminal)
                    last_non_terminal = non_terminal

                    _ = self.lex.get_next_token()
                    continue

                if token.type == TokenType.OPERATORS and token.value == '-':
                    _ = self.lex.get_next_token()
                    rule = self.scan_rule()
                    rule.name = last_non_terminal.value
                    grammar[last_non_terminal] = rule
                    continue

                raise Exception('Invalid Rule')
        return grammar



    def scan_expr(self) -> Tuple[Expr, bool]:
        expr = Expr()

        while (token := self.lex.get_next_token()).value not in  [',', '|']:
            if token.type == TokenType.OPERATORS and token.value == '<':
                non_terminal = self.lex.get_next_token()
                if non_terminal.type != TokenType.ID:
                    raise Exception('Invalid non-terminal')

                non_terminal.type = TokenType.NOTTERMINAL
                expr.value.append(non_terminal)

                _ = self.lex.get_next_token()
                continue
                
            if token.type == TokenType.OPERATORS or token.type == TokenType.KEYWORD or token.type == TokenType.ID:
                expr.value.append(token)
                self.terminals.add(token)
                continue
        
        if token == Token(TokenType.OPERATORS, ','):
            return (expr, True)

        return (expr, False)
        
            
    def scan_rule(self):
        rule = Rule()

        while (ret := self.scan_expr())[1] != True:
            rule.value.append(ret[0])
        
        rule.value.append(ret[0])
        return rule

    def FIRSTs(self) -> Dict[str, MySet[TokenFirstFollow]]:
        firsts = dict()
        for key, _ in self.grammar.items():
            firsts[key] = self.FIRST(key)
        return firsts

    def FIRST(self, non_terminal, expr=None) -> MySet[TokenFirstFollow]:
        first = MySet()
        for key, rules in self.grammar.items():
            if key == non_terminal:
                for rule in rules.value:
                    if rule.value[0].type == TokenType.NOTTERMINAL:
                        if expr == None:
                            first.update(self.FIRST(rule.value[0], rule))
                        else:
                            first.update(self.FIRST(rule.value[0], expr))
                    else:
                        if expr == None:
                            first.add(TokenFirstFollow(rule.value[0], rule))
                        else:
                            first.add(TokenFirstFollow(rule.value[0], expr))
        return first

    def FOLLOWs(self) -> Dict[Token, MySet[TokenFirstFollow]]:
        follows = dict()
        for key, _ in self.grammar.items():
            follows[key] = self.FOLLOW(key)
        return follows

    def FOLLOW(self, non_terminal) -> MySet[TokenFirstFollow]:
        follow = MySet()
        initial = True
        for key , rule in self.grammar.items():
            if initial == True:
                follow.add(TokenFirstFollow(Token.EOF(), Expr([Token.EOF()])))
                initial = False
            for expr in rule.value:
                for i, token in enumerate(expr.value):
                    if token == non_terminal:
                        if i+1 == len(expr.value) :
                            if key != non_terminal:
                                follow.update(self.FOLLOW(key))
                            break
                        
                        if expr.value[i+1].type != TokenType.NOTTERMINAL:
                            follow.add( TokenFirstFollow(expr.value[i+1], expr))

                        if expr.value[i+1] != non_terminal:
                            first = self.FIRST(expr.value[i+1])
                            for tok in first:
                                if tok.token == Token.end_of_rule():
                                    first.remove(tok)
                                    follow.update(first)
                                    follow.update(self.FOLLOW(key))
                                    break
                            else:
                                follow.update(first)

        return follow

    def create_m_table(self):
        m_table = M_Table(grammar=self.grammar, firsts=self.FIRSTs(), follows=self.FOLLOWs(), terminals=self.terminals, non_terminals=self.non_terminals)
        return m_table
        


