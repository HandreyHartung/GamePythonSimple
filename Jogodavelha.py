import random

def linhas():
    return [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def mostrar(b):
    g = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    for i,x in enumerate(b):
        g[i] = x if x else " "
    r = f"\n {g[0]} │ {g[1]} │ {g[2]}\n───┼───┼───\n {g[3]} │ {g[4]} │ {g[5]}\n───┼───┼───\n {g[6]} │ {g[7]} │ {g[8]}\n"
    print(r)

def vencedor(b,p):
    for a,c,d in linhas():
        if b[a]==b[c]==b[d]==p:
            return True
    return False

def vazios(b):
    return [i for i,x in enumerate(b) if not x]

def jogar(b,i,p):
    nb=b[:]
    nb[i]=p
    return nb

def pode_vencer(b,p):
    for i in vazios(b):
        if vencedor(jogar(b,i,p),p):
            return i
    return None

def count_wins_proximas(b,p):
    c=0
    for i in vazios(b):
        if vencedor(jogar(b,i,p),p):
            c+=1
    return c

def eh_fork(b,p,i):
    nb=jogar(b,i,p)
    return count_wins_proximas(nb,p)>=2

def movimentos_fork(b,p):
    return [i for i in vazios(b) if eh_fork(b,p,i)]

def centro(b):
    return 4 if not b[4] else None

def cantos():
    return [0,2,6,8]

def lados():
    return [1,3,5,7]

def oposto(i):
    return {0:8,2:6,6:2,8:0}.get(i,None)

def canto_oposto_livre(b,p_op):
    for i in cantos():
        j=oposto(i)
        if b[i]==p_op and j is not None and not b[j]:
            return j
    return None

def escolher_entre(b,ops):
    m=[i for i in ops if not b[i]]
    return random.choice(m) if m else None

def evita_forks(b,eu,op):
    melhores=[]
    for i in vazios(b):
        nb=jogar(b,i,eu)
        forks_op=movimentos_fork(nb,op)
        if not forks_op:
            melhores.append(i)
    return melhores

def melhor_jogada(b,eu,op):
    j=pode_vencer(b,eu)
    if j is not None:
        return j
    j=pode_vencer(b,op)
    if j is not None:
        return j
    forks=movimentos_fork(b,eu)
    if forks:
        return random.choice(forks)
    forks_op=movimentos_fork(b,op)
    if len(forks_op)==1:
        return forks_op[0]
    if len(forks_op)>=2:
        e=centro(b)
        if e is not None:
            return e
        for i in lados():
            nb=jogar(b,i,eu)
            if pode_vencer(nb,eu) is not None:
                return i
        boas=evita_forks(b,eu,op)
        if boas:
            return random.choice(boas)
    e=centro(b)
    if e is not None:
        return e
    j=canto_oposto_livre(b,op)
    if j is not None:
        return j
    j=escolher_entre(b,cantos())
    if j is not None:
        return j
    j=escolher_entre(b,lados())
    if j is not None:
        return j
    return random.choice(vazios(b))

def acabou(b):
    if vencedor(b,"X") or vencedor(b,"O") or not vazios(b):
        return True
    return False

def status(b):
    if vencedor(b,"X"):
        return "X"
    if vencedor(b,"O"):
        return "O"
    if not vazios(b):
        return "E"
    return None

def input_humano(b):
    while True:
        try:
            s=input("Sua jogada (1-9): ").strip()
            if s.lower() in ("q","sair","exit"):
                return None
            i=int(s)-1
            if i in range(9) and not b[i]:
                return i
        except:
            pass
        print("Entrada inválida.")

def cabecalho():
    print("Jogo da Velha • Você é X, IA é O")
    print("Posições:\n 1 │ 2 │ 3\n───┼───┼───\n 4 │ 5 │ 6\n───┼───┼───\n 7 │ 8 │ 9\n")

def jogo():
    random.seed()
    b=[None]*9
    cabecalho()
    mostrar(b)
    while True:
        i=input_humano(b)
        if i is None:
            print("Encerrado.")
            return
        b[i]="X"
        mostrar(b)
        if acabou(b):
            break
        j=melhor_jogada(b,"O","X")
        b[j]="O"
        print("IA jogou em",j+1)
        mostrar(b)
        if acabou(b):
            break
    r=status(b)
    if r=="X":
        print("Você venceu.")
    elif r=="O":
        print("IA venceu.")
    else:
        print("Empate.")

if __name__=="__main__":
    jogo()
