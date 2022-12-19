
class Interpreter:
    def __init__(self):
        self.lines = []
        self.stack = []
        self.loc = -1
        with open('output.txt', 'r') as f:
            for line in f:
                lineSplited = []
                word = ''
                for letter in line:
                    if letter != ' ' and letter != '\n' and letter != '\t':
                        word += letter
                    else:
                        lineSplited.append(word)
                        word = ''
                if word != '':
                    lineSplited.append(word)
                self.lines.append(lineSplited)


    def readLanguages(self):
        for i in self.lines:
            if i[0] == 'INPP':
                self.stack = []
            elif i[0] == 'CRCT':
                self.CRCT(i[1])
            elif i[0] == 'CRVL':
                self.CRVL(i[1])
            elif i[0] == 'SOMA':
                self.SOMA()
            elif i[0] == 'SUBT':
                self.SUBT()
            elif i[0] == 'MULT':
                self.MULT()
            elif i[0] == 'DIVI':
                self.DIVI()
            elif i[0] == 'INVE':
                self.INVE()
            elif i[0] == 'CONJ':
                self.CONJ()
            elif i[0] == 'DISJ':
                self.DISJ()
            elif i[0] == 'NEGA':
                self.NEGA()
            elif i[0] == 'CPME':
                self.CPME()
            elif i[0] == 'CPMA':
                self.CPMA()
            elif i[0] == 'CPIG':
                self.CPIG()
            elif i[0] == 'CDES':
                self.CDES()
            elif i[0] == 'CPMI':
                self.CPMI()
            elif i[0] == 'CMAI':
                self.CMAI()
            elif i[0] == 'ARMZ':
                self.ARMZ(i[1])
            elif i[0] == 'LEIT':
                self.LEIT()
            elif i[0] == 'IMPR':
                self.IMPR()
            elif i[0] == 'ALME':
                self.ALME(i[1])

    def CRCT(self, k):
        """
            :param k: element

            Carrega constante k no topo da pilha D
            """
        self.loc += 1
        self.stack.append(float(k))

    def CRVL(self, n):
        """
        :param n: endereço

        Carrega valor de endereço n no topo da pilha D
        """
        self.loc += 1
        self.stack.append(self.stack[int(n)])

    def SOMA(self):
        """
        Soma o elemento antecessor com o topo da pilha; desempilha os dois e empilha o resultado
        """
        self.stack[self.loc - 1] = self.stack[self.loc - 1] + self.stack[self.loc]
        self.loc -= 1
        self.stack.pop()

    def SUBT(self):
        """
        Subtrai o antecessor pelo elemento do topo
        """
        self.stack[self.loc - 1] = self.stack[self.loc - 1] - self.stack[self.loc]
        self.loc -= 1
        self.stack.pop()

    def MULT(self):
        """
        Multiplica elemento antecessor pelo elemento do topo
        """
        self.stack[self.loc - 1] = self.stack[self.loc - 1] * self.stack[self.loc]
        self.loc -= 1
        self.stack.pop()

    def DIVI(self):
        """
        Divide o elemento antecessor pelo elemento do topo
        """
        self.stack[self.loc - 1] = self.stack[self.loc - 1] / self.stack[self.loc]
        self.loc -= 1
        self.stack.pop()

    def INVE(self):
        """
        Inverte sinal do topo
        """
        self.stack[self.loc] = -1 * self.stack[self.loc]

    def CONJ(self):
        """
        Conjunção de valores lógicos. F=0; V=1
        """
        if self.stack[self.loc - 1] == 1 and self.stack[self.loc] == 1:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def DISJ(self):
        """
        Disjunção de valores lógicos
        """
        if self.stack[self.loc - 1] == 1 or self.stack[self.loc] == 1:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def NEGA(self):
        """
        Negação lógica
        """
        self.stack[self.loc] = -1 * self.stack[self.loc]

    def CPME(self):
        """
        Comparação de menor entre o antecessor e o topo
        """
        if self.stack[self.loc - 1] < self.stack[self.loc]:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def CPMA(self):
        """
        Comparação de maior
        """
        if self.stack[self.loc - 1] > self.stack[self.loc]:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def CPIG(self):
        """
        Comparação de igualdade
        """
        if self.stack[self.loc - 1] == self.stack[self.loc]:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def CDES(self):
        """
        Comparação de desigualdade
        """
        if self.stack[self.loc - 1] != self.stack[self.loc]:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def CPMI(self):
        """
        Comparação menor-igual
        """
        if self.stack[self.loc - 1] <= self.stack[self.loc]:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def CMAI(self):
        """
        Comparação maior-igual
        """
        if self.stack[self.loc - 1] >= self.stack[self.loc]:
            self.stack[self.loc - 1] = 1
        else:
            self.stack[self.loc - 1] = 0

        self.loc -= 1
        self.stack.pop()

    def ARMZ(self, n):
        """
        :param n: Endereço
        Armazena o topo da pilha no endereço n de D
        """
        self.stack[int(n)] = self.stack[self.loc]

    def DSVI(self, p):
        """
        Desvio incondicional para a instrucao de endereco p
        """
        self.i = p - 1

    def DSVF(self, p):
        """
        Desvio condicional para a instrucao de endereco p
        O desvio sera executado caso a condicao resultante seja falsa
        O valor da condicao esta no topo
        """

        if self.stack[self.loc] == 0:
            self.i = p - 1

        self.loc -= 1
        self.stack.pop()

    def LEIT(self):
        """
        Lê um dado de entrada para o topo da pilha
        """
        self.stack.append(float(input()))
        self.loc += 1

    def IMPR(self):
        """
        Imprime valor o valor do topo da pilha na saída
        """
        print(self.stack[self.loc])
        self.loc -= 1
        self.stack.pop()

    def ALME(self, m):
        """
        Imprime valor o valor do topo da pilha na saída
        """
        self.stack.append(None)
        self.loc += int(m)
