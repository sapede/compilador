from grammar import Expr, Grammar
from lexer import Lexer
from my_token import Token, TokenType
from syntactic import Syntactic
from semantic import Semantic
import sys

def main():
    sys.stdout = open('output.txt','wt', encoding='utf-8')

    sint = Syntactic()

    # sint.grammar.m_table.print_table()

    # print("FIRST")
    # ret = sint.grammar.FIRSTs()
    # for t, rule in ret.items():
    #     print(f"{t} = {[i for i in rule]}")
  
    # print("FOLLOW")
    # ret = sint.grammar.FOLLOWs()
    # for t, rule in ret.items():
    #     print(f"{t} = {[i for i in rule]}")
    teste = sint.analyze()
    print([f'{t.value}' for t in teste[0]])
    print([f'{t.value}' for t in teste[1]])
    semantic = Semantic()
    language = semantic.createLanguages(teste[1])
    print(language)

    exit(0)


if __name__ == '__main__':
    main()