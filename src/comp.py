from lib2to3.pgen2 import grammar
from grammar import Grammar
from lexer import Lexer, TokenType
from my_token import Token

def main():
    # lex = Lexer("<T'> -> <F> | &, <F> -> <F'>,")
    # while True:
    #     token = lex.get_next_token()
    #     if token.type == TokenType.EOF:
    #         break
    #     print(token)

    gram = Grammar('src/grammar.txt')
    print(gram.FIRSTs().items())
    exit(0)


if __name__ == '__main__':
    main()