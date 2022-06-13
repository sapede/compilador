from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple
from lexer import Lexer
from my_token import Token, TokenType

@dataclass
class Expr(object):
    value: List[Token] = field(default_factory=list)

@dataclass
class Rule(object):
    name: str = ''
    value: List[Expr] = field(default_factory=list)

class M_Table(object):
    def __init__(self, grammar: Dict[str, Rule], non_terminals: Set[str], terminals:Set[str], firsts: Dict[str, Set[str]], follows: Dict[str,Set[str]], value: Dict[str, Dict[str, Expr]] = {}):
        self.grammar = grammar
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.terminals.remove('&')
        self.terminals.add('$')
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

    def set_m_table(self, non_terminal: str, terminal: str, expr: Expr):
        self.value[non_terminal][terminal] = expr

    def get_m_table(self, non_terminal: str, terminal: str):
        return self.value[non_terminal][terminal]
    
    def fill_table(self):
        for key, rule in self.grammar.items():
            first = self.firts[key]
            for expr in rule.value:
                for token in expr.value:
                    if token.type != TokenType.NOTTERMINAL and token.value in first:
                        for elem in first:
                            if elem != '&':
                                self.set_m_table(key, elem, expr)
                            else:
                                for elem_f in self.follows[key]:
                                    self.set_m_table(key, elem_f, expr)

class Grammar(object):
    def __init__(self, grammar_file):
        self.grammar_file = grammar_file
        self.terminals = set()
        self.non_terminals = set()
        self.grammar = self.read_grammar()
        self.m_table = self.create_m_table()


    def read_grammar(self):

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
                    self.non_terminals.add(non_terminal.value)
                    last_non_terminal = non_terminal

                    _ = self.lex.get_next_token()
                    continue

                if token.type == TokenType.OPERATORS and token.value == '-':
                    _ = self.lex.get_next_token()
                    rule = self.scan_rule()
                    rule.name = last_non_terminal.value
                    grammar[last_non_terminal.value] = rule
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
                self.terminals.add(token.value)
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

    def FIRSTs(self):
        firsts = dict()
        for key, _ in self.grammar.items():
            firsts[key] = self.FIRST(key)
        return firsts

    def FIRST(self, non_terminal):
        first = set()
        for key, rules in self.grammar.items():
            if key == non_terminal:
                for rule in rules.value:
                    if rule.value[0].type == TokenType.NOTTERMINAL:
                        first.update(self.FIRST(rule.value[0].value))
                    else:
                        first.add(rule.value[0].value)
        return first

    def FOLLOWs(self):
        follows = dict()
        for key, _ in self.grammar.items():
            follows[key] = self.FOLLOW(key)
        return follows

    def FOLLOW(self, non_terminal):
        follow = set()
        initial = True
        for key , rule in self.grammar.items():
            if initial == True:
                follow.add('$')
                initial = False
            for expr in rule.value:
                for i, token in enumerate(expr.value):
                    if token.type == TokenType.NOTTERMINAL and token.value == non_terminal:
                        if i+1 == len(expr.value) :
                            if key != non_terminal:
                                follow.update(self.FOLLOW(key))
                            break
                        
                        if expr.value[i+1].type != TokenType.NOTTERMINAL:
                            follow.add(expr.value[i+1].value)

                        if expr.value[i+1].type == TokenType.NOTTERMINAL and expr.value[i+1].value != non_terminal:
                            first = self.FIRST(expr.value[i+1].value)
                            if '&' in first:
                                first.remove('&')
                                follow.update(first)
                                follow.update(self.FOLLOW(key))
                            else:
                                follow.update(first)

        return follow

    def create_m_table(self):
        m_table = M_Table(grammar=self.grammar, firsts=self.FIRSTs(), follows=self.FOLLOWs(), terminals=self.terminals, non_terminals=self.non_terminals)
        return m_table
        


