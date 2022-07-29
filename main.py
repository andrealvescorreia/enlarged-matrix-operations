# Objetivo: resolver equações lineares usando matriz ampliada, por meio do escalonamento.

# from decimal import Decimal
from fractions import Fraction
from dataclasses import dataclass

import os
import platform

os_name = platform.system()
if os_name == 'Linux':
    clear = lambda: os.system('clear')
else:
    clear = lambda: os.system('cls')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if (j < len(matriz[0]) - 1):
                s = ', '
            else:
                s = '\n'
            print(matriz[i][j], end=s)


def criar_matriz(linhas, colunas):
    m = [[0 for x in range(colunas)] for y in range(linhas)]
    return m


def matriz_input():
    clear()

    s_cmd = '-s'

    print('Lines: ')
    try:
        linhas = int(input())
    except:
        return False
    if (linhas < 1): return False
    print('Rows:  ')
    try:
        colunas = int(input())
    except:
        return False
    if (colunas < 1): return False

    clear()

    m = criar_matriz(linhas, colunas)

    for i in range(linhas):
        for j in range(colunas):
            print('type', s_cmd, 'at any moment to stop.\n')
            for k in range(len(m)):
                for l in range(len(m[0])):
                    if (l < len(m[0]) - 1):
                        s = ', '
                    else:
                        s = '\n'

                    if (k == i and l == j):
                        print(bcolors.OKGREEN + '_' + bcolors.ENDC, end=s)
                    else:
                        print(m[k][l], end=s)

            print('\n[' + str(i) + '][' + str(j) + ']:')

            inp = input()
            if inp == s_cmd:
                clear()
                return False
            else:
                try:
                    m[i][j] = int(inp)
                except:
                    return False
            clear()

    return m


def matriz_fracoes(matriz):
    m = criar_matriz(len(matriz), len(matriz[0]))
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            m[i][j] = Fraction(matriz[i][j])
    return m


# ____________________CLASSE


@dataclass
class OperacaoParametros:

    tipo: str
    linha_a: str
    linha_b: str
    multiplicador_linha_a: str
    multiplicador_linha_b: str
    operacao: str


class MatrizAmpliada:

    conteudo = []
    linhas = 0
    colunas = 0

    def __init__(self, conteudo):
        self.conteudo = matriz_fracoes(conteudo)
        self.linhas = len(conteudo)
        self.colunas = len(conteudo[0])

    # funcao auxiliar.
    def linha_int_format(linha):
        if (isinstance(linha, str)):
            if (linha[0] != 'L' and linha[0] != 'l'): return False
            try:
                l = int(linha[1:])
                return l
            except:
                print('ERROr')
                return False
        elif (isinstance(linha, int)):
            if linha < 1: return False
            return linha
        else:
            return False

    def trocar_linhas(self, linha_a, linha_b):
        # se for uma string 'Ln', pega o numero n.

        linha_a = MatrizAmpliada.linha_int_format(linha_a)
        if (linha_a == False): return False

        linha_b = MatrizAmpliada.linha_int_format(linha_b)
        if (linha_b == False): return False

        if (linha_a > self.linhas or linha_b > self.linhas or linha_a < 1
                or linha_b < 1):
            print('erro ao trocar linhas', linha_a, 'e', linha_b,
                  ': valor invalido.')
            return False

        aux = self.conteudo[linha_a - 1]
        self.conteudo[linha_a - 1] = self.conteudo[linha_b - 1]
        self.conteudo[linha_b - 1] = aux

    # funcao que pode mudar o conteudo.
    def multiplicar_linha(self, linha_a, multiplicador_linha_a):

        linha_a = MatrizAmpliada.linha_int_format(linha_a)
        if (linha_a == False): return

        if linha_a > self.linhas or linha_a < 1: return False

        if (multiplicador_linha_a == 0 or multiplicador_linha_a == '0'):
            return False

        mult = Fraction(multiplicador_linha_a)

        for j in range(self.colunas):
            self.conteudo[linha_a - 1][j] *= mult

    # funcao que pode mudar o conteudo.
    def operacao_entre_linhas(self, linha_a, operacao, multiplicador_linha_b,
                              linha_b):

        if (multiplicador_linha_b == 0 or multiplicador_linha_b == '0'):
            return False

        linha_a = MatrizAmpliada.linha_int_format(linha_a)
        if (linha_a == False): return False

        linha_b = MatrizAmpliada.linha_int_format(linha_b)
        if (linha_b == False): return False

        if (linha_a == linha_b): return False

        if (linha_a > self.linhas or linha_b > self.linhas): return False

        if (linha_a < 1 or linha_b < 1): return False

        aux = []
        for j in range(self.colunas):
            aux.append(self.conteudo[linha_b - 1][j])

        mult = Fraction(multiplicador_linha_b)

        for j in range(self.colunas):
            aux[j] *= mult

        if (operacao == '+'):
            for j in range(self.colunas):
                self.conteudo[linha_a - 1][j] += aux[j]
        elif (operacao == '-'):
            for j in range(self.colunas):
                self.conteudo[linha_a - 1][j] -= aux[j]
        else:
            #print('OPERACAO invalida')
            return False

    # funcao de codigo 'feio' que verifica se uma operacao de matriz em formato string é valida (ex: L1 -> 2*L1), alem de formatar para parametros que podem ser usados.
    def string_op_format(inp):
        if inp == '': return False

        op = OperacaoParametros('', '', '', '', '', '')
        op.linha_a = ''
        op.multiplicador_linha_a = ''
        op.linha_b = ''
        op.multiplicador_linha_b = ''

        op.operacao = ''

        op.tipo = ''  # multiplicar_linha, operacao_entre_linhas, trocar_linhas

        spl = inp.split()

        op.linha_a = MatrizAmpliada.linha_int_format(spl[0])
        if op.linha_a == False: return False

        if spl[1] == '<->':
            op.tipo = 'trocar_linhas'
            op.linha_b = MatrizAmpliada.linha_int_format(spl[2])
            if op.linha_b == False: return False
            # FINISH

        elif len(spl) == 3:
            op.tipo = 'multiplicar_linha'
            aux = spl[2].split('*')
            op.multiplicador_linha_a = aux[0]

            if MatrizAmpliada.linha_int_format(aux[1]) != op.linha_a:
                return False
            # FINISH
        elif len(spl) == 5:
            op.tipo = 'operacao_entre_linhas'
            if MatrizAmpliada.linha_int_format(spl[2]) != op.linha_a:
                return False
            op.operacao = spl[3]

            if '*' in spl[4]:
                aux = spl[4].split('*')
                op.multiplicador_linha_b = aux[0]
                op.linha_b = MatrizAmpliada.linha_int_format(aux[1])
                if op.linha_b == False: return False
                #FINISH
            else:
                op.linha_b = MatrizAmpliada.linha_int_format(spl[4])
                if op.linha_b == False: return False

                # FINISH

        else:
            return False
        '''
    print('tipo:',op.tipo)
    print('linha_a:',op.linha_a)
    print('linha_b:',op.linha_b)
    print('multiplicador_linha_a:',op.multiplicador_linha_a)
    print('multiplicador_linha_b:',op.multiplicador_linha_b)
    print('operacao:',op.operacao)'''

        if op.linha_a == op.linha_b: return False

        if op.multiplicador_linha_a == '0' or op.multiplicador_linha_b == '0':
            return False

        if op.tipo == 'operacao_entre_linhas':
            if op.operacao != '-' and op.operacao != '+': return False

            if (op.multiplicador_linha_b != ''):
                try:
                    Fraction(op.multiplicador_linha_b)
                except:
                    return False
            else:
                op.multiplicador_linha_b = '1'

        if op.tipo == 'multiplicar_linha':
            try:
                Fraction(op.multiplicador_linha_a)
            except:
                return False

        return op

    def operacao_por_string(self, string):
        op = OperacaoParametros('', '', '', '', '', '')
        op = MatrizAmpliada.string_op_format(string)

        if op == False:
            print('ERROr: bad format')
            return False
        elif op.tipo == 'multiplicar_linha':
            if self.multiplicar_linha(op.linha_a,
                                      op.multiplicador_linha_a) == False:
                return False
        elif op.tipo == 'operacao_entre_linhas':
            if self.operacao_entre_linhas(op.linha_a, op.operacao,
                                          op.multiplicador_linha_b,
                                          op.linha_b) == False:
                return False
        elif op.tipo == 'trocar_linhas':
            if self.trocar_linhas(op.linha_a, op.linha_b) == False:
                return False


#________________________MAIN______________________________


def op_loop(matrizAmpliada):

    s_cmd = '-s'
    h_cmd = '-h'
    print('type', s_cmd, 'at any moment to stop.\n')
    inp = ''
    print(
        'Type the operation you want to realise onto the Augmented Matrix . (-h for help)'
    )
    while inp != s_cmd:
        #clear()
        print_matriz(matrizAmpliada.conteudo)
        print()
        inp = input()
        if (inp == h_cmd):
            clear()
            print('__Examples:\n')
            print('L1 -> 1/2*L1')
            print('"Line1 is equals to itself times 1/2"\n')

            print('L3 -> L3 + -1*L2')
            print('"Line3 is equals to itself plus Line2 times -1."\n')

            print('L3 -> L3 - L2')
            print('"Line3 is equals to itself minus Line2."\n')

            print('L1 <-> L4')
            print('"Line1 and Line4 change places."\n')
            input('press ENTER')
        elif (inp == s_cmd):
            return
        else:
            if matrizAmpliada.operacao_por_string(inp) == False:
                print('Invalid Operation.', 'press ENTER.')
                input()


def run():
    m = matriz_input()
    if m == False: return

    ma = MatrizAmpliada(m)
    if ma == False: return False
    op_loop(ma)


def main():

    e_cmd = '-e'
    r_cmd = '-r'

    op = ''

    while op != e_cmd:
        clear()
        print('type', r_cmd, 'to run.')
        print('type', e_cmd, 'to exit.')

        op = input()

        if (op == r_cmd):
            run()
        elif (op == e_cmd):
            return


def test():

    ma = MatrizAmpliada([[1, 3, 2, 1], [2, 2, 0, 1], [3, 0, 0, 1]])
    op_loop(ma)


main()
#test()

