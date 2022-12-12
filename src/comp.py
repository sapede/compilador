from grammar import Expr, Grammar
from lexer import Lexer
from my_token import Token, TokenType
from syntactic import Syntactic
import sys

def main():
    sys.stdout = open('output.txt','wt', encoding='utf-8')
    sint = Syntactic()

    sint.grammar.m_table.print_table()
    print(f'O resultado da conta é := {sint.analyze()}')

    exit(0)


if __name__ == '__main__':
    main()