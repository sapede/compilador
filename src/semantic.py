
from lexer import KEYWORDS


class Semantic:
    def __init__(self):
        self.stack = []
        self.C = []
        self.loc = 0
        self.input = ''
        self.reservedWord = KEYWORDS
        self.adress = -1
        self.tableSymbol = {}


    def createLanguages(self, stack):
        self.input = stack
        self.programa()
        with open('output.txt', 'w') as f:
            for i in self.C:
                f.write(i + '\n')
        return self.C

    def programa(self):
        self.C.append('INPP')
        self.loc += 1
        self.loc += 1
        self.corpo()
        self.loc += 1
        self.C.append('PARA')

    def corpo(self):
        self.dc()
        self.loc += 1
        self.comandos()
        self.loc += 1

    def dc(self):
        if self.input[self.loc].value in ['real', 'integer']:
            self.dc_v()
            self.mais_dc()

    def mais_dc(self):
        if self.input[self.loc].value == ';':
            self.loc += 1
            self.dc()

    def dc_v(self):
        type_var = self.tipo_var()
        self.loc += 1
        self.variaveis(type_var)

    def tipo_var(self):
        self.loc += 1
        if self.input[self.loc].value == 'real':
            return 'real'
        else:
            return 'integer'

    def variaveis(self, type_var):
        if self.input[self.loc] not in self.reservedWord:
            self.C.append('ALME 1')
            self.adress += 1
            self.tableSymbol[self.input[self.loc].value] = [type_var, [self.input[self.loc].value], self.adress]
            self.loc += 1
            self.mais_var(type_var)

    def mais_var(self, type_var):
        if self.input[self.loc].value == ',':
            self.loc += 1
            self.variaveis(type_var)

    def comandos(self):
        self.comando()
        self.mais_comandos()

    def mais_comandos(self):
        if self.input[self.loc].value == ';':
            self.loc += 1
            self.comandos()

    def comando(self):
        if self.input[self.loc].value in ['read', 'write']:
            a = self.input[self.loc].value
            self.loc += 1
            self.loc += 1
            if self.input[self.loc].value not in self.reservedWord and self.input[self.loc].value in self.tableSymbol.keys():
                if a == 'read':
                    self.C.append('LEIT')
                    self.adress += 1
                    self.C.append(f'ARMZ {self.tableSymbol[self.input[self.loc].value][2]}')
                else:
                    self.C.append(f'CRVL {self.tableSymbol[self.input[self.loc].value][2]}')
                    self.adress += 1
                    self.C.append('IMPR')
                self.loc += 1
                self.loc += 1

        else:
            if self.input[self.loc].value not in self.reservedWord and self.input[self.loc].value in self.tableSymbol.keys():
                a = self.input[self.loc].value
                self.loc += 1
                self.loc += 1
                self.expressao()
                self.C.append(f'ARMZ {self.tableSymbol[a][2]}')

    def expressao(self):
        self.termo()
        self.outros_termos()

    def termo(self):
        op_un = self.op_un()
        self.fator(op_un)
        self.mais_fatores()

    def op_un(self):
        if self.input[self.loc].value == '-':
            self.loc += 1
            return '-'

    def fator(self, op_un):
        if self.input[self.loc].value == '(':
            self.loc += 1
            self.expressao()
            if op_un:
                self.C.append('INVE')
            self.loc += 1
        else:
            if self.input[self.loc].value == 'ident':
                if self.input[self.loc].value not in self.reservedWord and self.input[self.loc].value in \
                        self.tableSymbol.keys():
                    self.C.append(f'CRVL {self.tableSymbol[self.input[self.loc].value][2]}')
                else:
                    try:
                        a = float(self.input[self.loc].value)
                        self.C.append(f'CRCT {a}')
                    except:
                        self.C.append(f'CRVL {self.input[self.loc].value}')
                if op_un:
                    self.C.append('INVE')
                self.loc += 1

    def outros_termos(self):
        if self.input[self.loc].value in ['+', '-']:
            op_ad = self.op_ad()
            self.termo()
            if op_ad == '+':
                self.C.append('SOMA')
            else:
                self.C.append('SUBT')
            self.outros_termos()

    def op_ad(self):
        op = self.input[self.loc].value
        self.loc += 1
        return op

    def mais_fatores(self):
        if self.input[self.loc].value in ['*', '/']:
            op_mul = self.op_mul()
            self.fator(None)
            if op_mul == '*':
                self.C.append('MULT')
            else:
                self.C.append('DIVI')
            self.mais_fatores()

    def op_mul(self):
        op = self.input[self.loc].value
        self.loc += 1
        return op
