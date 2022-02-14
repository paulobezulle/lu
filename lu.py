# -*- coding: utf-8 -*-
"""lu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SHQ0hrF8RW04OUAcuVJXVIgN7OkchfZK
"""

# Commented out IPython magic to ensure Python compatibility.
""" MAT-0122 ALGEBRA LINEAR
    Prof. Walter F. Mascarenhas

    TRABALHO DE RECUPERACAO
    ALUNO: PAULO ROBERTO BEZULLE
    # USP: 10752206

    IMPLEMENTA FATORACAO LU
    E INVERSAO DE MATRIZES TRIANGULAR INFERIOR E SUPERIOR
"""

import numpy as np

def troca_linha(M, e, f):
    """
    Na matriz 'M', troca as linhas de numero 'e' e 'f' de lugar.
    SERA USADA NA FUNCAO lu() - IMPLEMENTACAO DA FATORACAO LU
    """
    M[[e,f], :] = M[[f,e], :]


def max_in_col(M, pivot_ix):
    """
    Retorna o indice do elemento com maior valor absoluto, dentre os valores
    abaixo do pivot informado.
    Parametros: M         - matriz quadrada
                pivot_ix  - indice do pivot ([pivot_ix,pivot_ix]) abaixo do
                            qual selecionar o elemento de maior valor
    Retorna:    ix        - indice do elemento com maior valor absoluto
    SERA USADA NA FUNCAO lu() - IMPLEMENTACAO DA FATORACAO LU
    """
    nlin = M.shape[0]
    ncol = M.shape[1]
    val = 0
    ix = -1
    for i in range(pivot_ix, nlin):
        if abs(M[i, pivot_ix]) > val:
            val = abs(M[i, pivot_ix])
            ix = i
    return ix


def hilbert(n):
    """
    Retorna uma matriz de Hilbert dimensao nxn
    SERÁ CHAMADA SOMENTE NOS TESTES, ISTO E, NAO FAZ PARTE DA IMPLEMENTACAO
    DAS FUNCOES DE INVERSAO DE MATRIZ REF ITENS 4, 5 OU 6.
    """
    M = np.zeros((n,n))    

    for i in range(n):
      for j in range(n):
          M[i,j] = 1 / (i + j + 1)
    return M


##########   IMPLEMENTACAO ITEM 4   ##########
def invTS(A):
    """
    Inverte a matriz triangular superior 'A', usando como técnica, a resolucao
    de sistemas AX=I, onde I eh matriz identidade, e X a inversa de A.
    A solucao do sistema para cada coluna da matriz identidade, eh armazenada na
    correspondente coluna em X.
    Cada sistema eh resolvido via simples substituicao da ultima para a
    primeira linha ("backward substitution").
    Obs.: Assume A quadrada.
    """
    nlin = A.shape[0]
    ncol = A.shape[1]
    
    I = np.identity(nlin)
    X = np.zeros((nlin, nlin))

    # Para cada coluna da matriz identidade, tomada da ultima para primeira
    for j in range(ncol-1, -1, -1):
        # Resolve-se um sistema por backward substitution
        for i in range(nlin-1, -1, -1):
            soma = 0.
            for k in range(nlin-1, i, -1):
                soma += A[i, k] * X[k, j]
                #print("-->  %.2f += %.2f * %.2f" %(soma,A[i,k],X[k,j]))

            # Cada elemento de X (x_i,j) recebe o resultado das substituicoes
            # dos elementos nas equacoes que o antecedem
            X[i, j] = (I[i, j] - soma) / A[i, i]
            #print('%.2f = (%.2f - %.2f )/%.2f' %(X[i,j],I[i,j],soma,A[i,i]))
    return X


##########   IMPLEMENTACAO ITEM 5   ##########
def invTI(A):
    """
    Inverte a matriz triangular inferior 'A', usando como técnica, a resolucao
    de sistemas AX=I, onde I eh matriz identidade, e X a inversa de A.
    A solucao do sistema para cada coluna da matriz identidade, eh armazenada na
    correspondente coluna em X.
    Cada sistema eh resolvido via simples substituicao da primeira para a
    ultima linha ("forward substitution").
    Obs.: Assume A quadrada.
    """
    nlin = A.shape[0]
    ncol = A.shape[1]
    
    I = np.identity(nlin)
    X = np.zeros((nlin, nlin))

    # Para cada coluna da matriz identidade, 
    for j in range(0, ncol, 1):
        # Resolve-se um sistema por forward substitution
        for i in range(0, nlin, 1):
            soma = 0.
            for k in range(0, i, 1):
                soma += A[i, k] * X[k, j]    
                #print("-->  %.2f += %.2f * %.2f" %(soma,A[i,k],X[k,j]))
        
            # Cada elemento de X (x_i,j) recebe o resultado das substituicoes
            # dos elementos nas equacoes que o antecedem
            #print(I[i,j],soma,A[i,i])
            X[i, j] = (I[i, j] - soma) / A[i, i]
            #print('%.2f = (%.2f - %.2f )/%.2f' %(X[i,j],I[i,j],soma,A[i,i]))
    return X


##########   IMPLEMENTACAO ITEM 6   ##########
def lu(A):
    """
    Fatora a matriz quadrada 'A' nas matrizes:
    - L - triangular inferior
    - U - triangular superior
    - P - matrix de permutacoes
    tal que     PA = LU
    Retorna:    P, L, U   (legenda acima)
    CHAMA AS FUNCOES max_in_col() E troca_linha() DEFINIDAS ACIMA
    Obs.: Assume que a matriz de entrada eh QUADRADA
    """
    nlin = A.shape[0]
    ncol = A.shape[1]
    I = np.identity(nlin)
    
    # inicializa P como matriz identidade,
    #            L como matriz quadrada com zeros
    #              (diagonal de 1s adicionada só no fim para simplificar permutacoes)
    #            U como copia da matriz de entrada
    P = np.copy(I)
    L = np.zeros((nlin, nlin))
    U = np.copy(A)

    # Para cada coluna da matriz
    for j in range(0, ncol):
        # encontra o elemento de maior valor absoluto abaixo do pivot
        # e troca sua linha de lugar com a linha do pivot, se necessario
        ix_max = max_in_col(U, j)
        if ix_max != j:
            troca_linha(U, j, ix_max)
            troca_linha(P, j, ix_max)
            troca_linha(L, j, ix_max)

        pivot = U[j, j]
        # Subtrai, de cada linha abaixo do pivot, um multiplo da linha pivot,
        # tal que o elemento cabeca da linha seja zerado
        for i in range(j+1, nlin):
            cabeca = U[i, j]
            for k in range(j, ncol):
                U[i, k] -= U[j, k] * cabeca/pivot
            # Atualiza triangular inferior L com o inverso da subtracao
            L[i, j] = cabeca/pivot

    # Adiciona a diagonal de 1's na triangular inferior L
    L += I

    return P, L, U


def inverte(A):
    """
    Inverte a matriz quadrada 'A', usando o seguinte algoritmo:
    - fatora A na forma PA = LU
    - inverte L e U
    - retorna o resultado A^-1 = U^-1 @ L^-1 @ P
    CHAMA AS FUNCOES lu(), invTS() e invTI() DEFINIDAS ACIMA
    Obs.: Assume que a matriz de entrada eh QUADRADA
    """
    # Fatora A na forma PA = LU
    (P, L, U) = lu(A)
    # Inverte L (triangular inferior) e U (triangular superior)
    Ui = invTS(U)
    Li = invTI(L)

    # Retorna a inversa de A => A^-1 = U^-1 @ L^-1 @ P
    return Ui @ Li @ P

def main():
    """
    Nesta funcao main(), está o código usado para testar as implementacoes
    referentes aos itens 4., 5. e 6. 
    """

    #######################################################################
    # TESTA ITEM 4. (INVERSAO DA TRIANGULAR SUPERIOR)
    # M = np.triu(np.random.rand(1000,1000))
    
    # myM_i = invTS(M)         # inversao implementada por mim
    # npM_i = np.linalg.inv(M) # inversao pelo numpy para comparar
    
    # print(np.allclose(myM_i, npM_i)) # compara com limite tolerancia
    # print(np.linalg.cond(M))
    # print(M@myM_i)


    #######################################################################
    # TESTA ITEM 5. (INVERSAO TRIANGULAR INFERIOR) 
    # M = np.tril(1000*np.random.rand(50,50))
    
    # myM_i = invTI(M)         # inversao implementada por mim
    # npM_i = np.linalg.inv(M) # inversao pelo numpy para comparar
    
    # print(np.allclose(myM_i, npM_i)) # compara com limite tolerancia
    # print(np.linalg.cond(M))
    # print(M@myM_i)


    #######################################################################
    # TESTA ITEM 6. COM MATRIZ ALEATORIA (INVERSAO DE QUADRADA NxN) 
    # n = 1000
    # M = np.random.rand(n, n)

    # Mi = inverte(M)

    # print(np.allclose(Mi @ M, np.identity(n)))
    # print(Mi @ M)

    
    #######################################################################
    # TESTA ITEM 6. COM HILBERT (INVERSAO DE QUADRADA NxN)
    n = 50
    H = hilbert(n)
    Hi = inverte(H)
    npHi = np.linalg.inv(H) # inversao feita pelo numpy

    print('Condition number %f' %(np.linalg.cond(H)))
    print('Inversa: nossa = do Numpy? %s' 
#                                    %(np.allclose(Hi, npHi)))
    print('H @ Hi = I? %s' %(np.allclose(H @ Hi, np.identity(n))))
    print(H @ Hi)


main()

M=np.random.rand(100,100)

(P, L, U) = lu(M)

Li = invTI(L)
Ui = invTS(U)

print(Ui@Li@P)
print(np.linalg.inv(M))
print(np.allclose(Ui@Li@P, np.linalg.inv(M)))