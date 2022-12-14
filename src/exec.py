class Interpretador():

    D = []
    i = 0
    s = -1

    def __init__(self, C):
        self.C = C

    def executar(self):

        while self.i < len(self.C):
            palavras = self.C[self.i].split()
            comando = ""
            parametro = ""
            if len(palavras) == 2:
                comando, parametro = palavras[0], int(palavras[1])
                funcao = getattr(Interpretador, comando)
                funcao(self, parametro)
            else:
                comando = palavras[0]
                funcao = getattr(Interpretador, comando)
                funcao(self)

            self.i += 1

    def CRVL(self, n):
        # Carrega valor de endereco n no topo da pilha D
        self.s += 1
        self.D.append(self.D[n])

    def CRCT(self, k):
        # Carrega constante k no topo da pilha D
        self.s += 1
        self.D.append(k)

    def SOMA(self):
        # Soma o elemento antecessor com o elemento do topo
        # Desempilha os dois e empilha o resultado
        self.D[self.s-1] = self.D[self.s-1] + self.D[self.s]
        self.D.pop()
        self.s -= 1

    def SUBT(self):
        # Subtrai o elemento antecessor pelo elemento do topo
        # Desempilha os dois e empilha o resultado
        self.D[self.s-1] = self.D[self.s-1] - self.D[self.s]
        self.D.pop()
        self.s -= 1

    def MULT(self):
        # Multiplica o elemento antecessor pelo elemento do topo
        # Desempilha os dois e empilha o resultado
        self.D[self.s-1] = self.D[self.s-1] * self.D[self.s]
        self.D.pop()
        self.s -= 1

    def DIVI(self):
        # Divide o elemento antecessor pelo elemento do topo
        # Desempilha os dois e empilha o resultado
        self.D[self.s-1] = self.D[self.s-1] / self.D[self.s]
        self.D.pop()
        self.s -= 1

    def INVE(self):
        # Inverte o elemento no topo da pilha D
        self.D[self.s] = -self.D[self.s]

    def CONJ(self):
        # Conjuncao de valores logicos
        if self.D[self.s-1] == 1 and self.D[self.s] == 1:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def DISJ(self):
        # Disjuncao de valores logicos
        if self.D[self.s-1] == 1 or  self.D[self.s] == 1:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def NEGA(self):
        # Negacao logica
        self.D[self.s] = 1 - self.D[self.s]

    def CPME(self):
        # Comparacao de menor entre o antecessor e o topo
        if self.D[self.s-1] < self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CPMA(self):
        # Comparacao de maior entre o antecessor e o topo
        if self.D[self.s-1] > self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CPIG(self):
        # Comparacao de igualdade entre o antecessor e o topo
        if self.D[self.s-1] == self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CDES(self):
        # Comparacao de desigualdade entre o antecessor e o topo
        if self.D[self.s-1] != self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CPMI(self):
        # Comparacao de menor-igual entre o antecessor e o topo
        if self.D[self.s-1] <= self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CMAI(self):
        # Comparacao de maior-igual entre o antecessor e o topo
        if self.D[self.s-1] >= self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def ARMZ(self, n):
        # Armazena o topo da pilha no endereco n de D
        self.D[n] = self.D[self.s]
        self.D.pop()
        self.s -= 1

    def DSVI(self, p):
        # Desvio incondicional para a instrucao de endereco p
        self.i = p - 1

    def DSVF(self, p):
        # Desvio condicional para a instrucao de endereco p
        # O desvio sera executado caso a condicao resultante seja falsa
        # O valor da condicao esta no topo
        if self.D[self.s] == 0:
            self.i = p - 1

        self.s -= 1
        self.D.pop()

    def LEIT(self):
        # Le um dado de entrada para o topo da pilha
        self.s += 1
        entrada = float(input())
        self.D.append(entrada)

    def IMPR(self):
        # Imprime o valor do topo da pilha
        print(f"{self.D[self.s]}")
        self.D.pop()
        self.s -= 1

    def ALME(self, m):
        # Reserva m posições na pilha D
        # m depende do tipo da variavel (???)
        for _ in range(m):
            self.s += 1
            self.D.append(None)

    def INPP(self):
        # Inicia o programa
        return

    def PARA(self):
        # Termina a execucao do programa
        return
