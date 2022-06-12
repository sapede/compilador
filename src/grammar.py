
from dataclasses import dataclass, field
from typing import List, Tuple
from lexer import Lexer
from my_token import Token, TokenType

@dataclass
class Expr(object):
    value: List[Token] = field(default_factory=list)

@dataclass
class Rule(object):
    name: str = ''
    value: List[Expr] = field(default_factory=list)

class Grammar(object):
    def __init__(self, grammar_file):
        self.grammar_file = grammar_file
        self.grammar = self.read_grammar()

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
        ...

    def FOLLOW(self, non_terminal):
        ...
