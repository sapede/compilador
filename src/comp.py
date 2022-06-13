from grammar import Grammar
from lexer import Lexer
from my_token import Token, TokenType

def main():
    # lex = Lexer("<T'> -> <F> | &, <F> -> <F'>,")
    # while True:
    #     token = lex.get_next_token()
    #     if token.type == TokenType.EOF:
    #         break
    #     print(token)

    gram = Grammar('src/grammar.txt')
    initial = True
    for non_ts, ter in gram.m_table.value.items():
        if initial:
            for key, val in ter.items():
                print(f'    {key}    |', end='')
            initial = False
            print()

        print(non_ts, ' | ', end='')
        for key, val in ter.items():
            print(f'{non_ts} -> {val} | ', end='')
        print()
    # print(gram.m_table.value)
    exit(0)


if __name__ == '__main__':
    main()