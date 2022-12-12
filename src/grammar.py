from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple, TypeVar
from lexer import Lexer
from my_token import Token, TokenType
from ordered_set import OrderedSet

T = TypeVar("T")
QTD_LTS = 50
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

class MySet(OrderedSet):
    def __init__(self, iterable: Optional[Iterable[TokenFirstFollow]] = None):
        super().__init__(iterable)
    def __str__(self) -> str:
        return '{' + ', '.join(map(str, self)) + '}'
    def remove(self, value) -> None:
        for it in self:
            if it.token == value:
                del it
                return
        raise ValueError(f'{value} not in set')
class M_Table(object):
    def __init__(self, grammar: Dict[Token, Rule], non_terminals: Set[Token], terminals:Set[Token], firsts: Dict[Token, Set[TokenFirstFollow]], follows: Dict[Token,Set[TokenFirstFollow]], value: Dict[Token, Dict[Token, Expr]] = {}):
        self.grammar = grammar
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.terminals.remove(Token.empty())
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
                if tok.token == Token.empty():
                    for elem_f in self.follows[key]:
                        self.set_m_table(key, elem_f.token, tok.expr)
                else:
                    self.set_m_table(key, tok.token, tok.expr)

    def print_table(self):
        print(''.rjust(QTD_LTS," "), end='')
        for terminal in self.terminals:
            print(f'{terminal.value}'.center(QTD_LTS," "), end='')
        print()
        print('_'*500)
        for key, rule in self.grammar.items():
            print(f'{key.value} ->'.center(QTD_LTS," "), end='')
            for terminal in self.terminals:
                if self.value[key][terminal] is not None:
                    print(f'{key.value} -> { " ".join([t.value for t in self.value[key][terminal].value])}'.center(QTD_LTS," "), end='')
                else:
                    print(f'None'.center(QTD_LTS," "), end='')
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

        with open(self.grammar_file, 'r', encoding='utf-8') as f:
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

        while (token := self.lex.get_next_token(with_end_line=True)).value not in ['\n', '|']:
            if token.type == TokenType.OPERATORS and token.value == '<':
                new_token = self.lex.get_next_token(with_space=True, with_end_line=True)
                if new_token.type == TokenType.SPACE or new_token.type == TokenType.NEW_LINE:
                    expr.value.append(token)
                    self.terminals.add(token)
                    if new_token.type == TokenType.NEW_LINE:
                        return (expr, True)
                    continue

                if new_token.type == TokenType.ID:
                    new_token.type = TokenType.NOTTERMINAL
                    expr.value.append(new_token)

                    _ = self.lex.get_next_token()
                    continue
                
                if new_token.value == '|':
                    break

            elif token.type == TokenType.OPERATORS or token.type == TokenType.KEYWORD or token.type == TokenType.ID:
                expr.value.append(token)
                self.terminals.add(token)
        
        if token == Token(TokenType.NEW_LINE, '\n'):
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

    def FIRST(self, non_terminal) -> MySet[TokenFirstFollow]:
        first = MySet()
        for expr in self.grammar[non_terminal].value:
            first_elem = expr.value[0]
            if first_elem.type == TokenType.NOTTERMINAL:
                ret = self.FIRST(first_elem)
                first.update(ret)
                i = 1
                while i < len(expr.value) and Token.empty() in [tok.token for tok in ret]:
                    if expr.value[i].type == TokenType.NOTTERMINAL:
                        ret = self.FIRST(expr.value[i])
                        first.update(ret)
                        i += 1
                    else:
                        first.add(TokenFirstFollow(expr.value[i], expr))
                        break
            else:
                first.add(TokenFirstFollow(expr.value[0], expr))
        return first


    def FOLLOWs(self) -> Dict[Token, MySet[TokenFirstFollow]]:
        follows = dict()
        for key, _ in self.grammar.items():
            follows[key] = self.FOLLOW(key)
        return follows

    def FOLLOW(self, non_terminal, visited = []) -> MySet[TokenFirstFollow]:
        follow = MySet()
        follow.add(TokenFirstFollow(Token.EOF(), Expr([Token.EOF()])))
        visited.append(non_terminal)

        for key, rule in self.grammar.items():
            for expr in rule.value:
                for i, token in enumerate(expr.value):
                    if token == non_terminal:
                        if i+1 == len(expr.value) :
                            if key != non_terminal and key not in visited:
                                follow.update(self.FOLLOW(key, visited))
                          
                        elif expr.value[i+1].type != TokenType.NOTTERMINAL:
                            follow.add( TokenFirstFollow(expr.value[i+1], expr))

                        else:
                            first = self.FIRST(expr.value[i+1])
                            if Token.empty() in [tok.token for tok in first]:
                                first.remove(Token.empty())
                                follow.update(first)
                                if key != non_terminal and key not in visited: 
                                    follow.update(self.FOLLOW(key, visited))
                            else:
                                follow.update(first)
                        break

        return follow

    def create_m_table(self):
        m_table = M_Table(grammar=self.grammar, firsts=self.FIRSTs(), follows=self.FOLLOWs(), terminals=self.terminals, non_terminals=self.non_terminals)
        return m_table
        


