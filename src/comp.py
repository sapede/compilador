from grammar import Expr, Grammar
from lexer import Lexer
from my_token import Token, TokenType
from syntactic import Syntactic

def main():
    sint = Syntactic()

    sint.analyze()

    exit(0)


if __name__ == '__main__':
    main()