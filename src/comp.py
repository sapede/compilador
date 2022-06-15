from lib2to3.pgen2 import token
from grammar import Expr, Grammar
from lexer import Lexer
from my_token import Token, TokenType

def main():
    gram = Grammar('src/grammar.txt')
    initial = True
    for non_ts, ter in gram.m_table.value.items():
        # if initial:
        #     for key, val in ter.items():
        #         print(f'    {key}    |', end='')
        #     initial = False
        #     print()

        print(non_ts, ' | ', end='')
        for key, val in ter.items():
            print(f'\'{key}\' {non_ts} -> {val} | ', end='')
        print()
    print()

    [print(f'{key} = {f}') for key, f in gram.FIRSTs().items()]
    print()
    [print(f'{key} = {f}') for key, f in gram.FOLLOWs().items()]

    exit(0)


if __name__ == '__main__':
    main()