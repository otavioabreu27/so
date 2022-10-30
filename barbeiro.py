import threading
from time import sleep as sp
import random

#semáforos
clientes = threading.Semaphore(0) # mantém fila de clientes
barbeiros = threading.Semaphore(0) # diz se o barbeiro está disponível ou não
mutex = threading.Semaphore(1) # para exclusão mútua

#variáveis
dormir = 0 # diz se o barbeiro está dormindo ou não (1 - dormindo, 0 - acordado)
esperando = 0 #número de clientes esperando nos acentos
total = 0 # total de clientes presentes atualmente (incluindo quem está recebendo o corte)
lista_esperando = [ ] # nome dos clientes esperando na fila
cliente_cortando_cabelo = '' # nome do cliente recebendo o corte

#funções
def barbeiro():
    global total, esperando, dormir, lista_esperando, cliente_cortando_cabelo
    while True:
        print("Barbeiro esperando mais clientes, total de clientes esperando:",esperando,"\n")
        if (len(lista_esperando) > 0): # se alguém estiver esperando
            print('Clientes esperando são: ',lista_esperando)
        if (esperando == 0 and total == 0):# se nenhum cliente estiver presente, barbeiro dorme
            print("Barbeiro dorme")
            dormir = 1
        clientes.acquire() # wait (clientes)
        mutex.acquire() # wait (mutex)
        if (esperando > 0): # se o cliente estiver esperando
            esperando -= 1 # decrementa número de clientes na fila
        barbeiros.release () # signal (barbeiro)
        mutex.release() # signal (mutex)
        sp(1) # esperando por 1 segundo
        cortando_cabelo() # barbeiro vai cortar o cabelo
        sp(4) # cortando por 4 segundos
        print (f"Barbeiro terminou o corte de {cliente_cortando_cabelo}\n")
        if (len(lista_esperando) > 0 and cliente_cortando_cabelo in lista_esperando):# remove o cliente
            lista_esperando.remove(cliente_cortando_cabelo)
        cliente_cortando_cabelo = ""
        total -= 1 # decrementa total
            
def customer(name):
    global cadeiras, esperando, cliente_cortando_cabelo, dormir, lista_esperando, total
    mutex.acquire() # wait (mutex)
    if (esperando < cadeiras or total == 0):
        if (total == 0):
            total += 1 # incrementa total
            print (f"cliente: {name} entrou na barbearia\n")
        else:
            total += 1
            esperando += 1 # incrementa número de clientes esperando
            lista_esperando.append(name) # adiciona nome do cliente na lista de esperando
            print (f"cliente: {name} entrou na sala de esperando, total de clientes esperando :", esperando, "\n")
            
        clientes.release () # signal (clientes)
        mutex.release () # signal (mutex)
        barbeiros.acquire () # wait (barbeiro)
        
        if (dormir == 1): # se o barbeiro estiver dormindo, ele acorda
            print(f"cliente: {name} está acordando o barbeiro \n")
            dormir = 0 # barbeiro está acordado
            
        cliente_cortando_cabelo = name
        cortar_cabelo (name)     
    else: # se não houver mais acentos disponíveis
        mutex.release () # signal (mutex)
        sair (name) # deixar a loja
        
def cortar_cabelo (name):
    ''' Requerir um corte de cabelo '''
    print (f'Cliente: {name} chamou cortar_cabelo\n')
    return

def cortando_cabelo ():
    ''' Cortar o cabelo '''
    print (f"Barbeiro cortando o cabelo de {cliente_cortando_cabelo}\n")
    return

def sair (name):
    ''' Sair da loja '''
    print (f'Cliente: {name} está tentando entrar na sala de esperando\nloja cheia, chamando sair para {name} \n')

#threads e outras variáveis
barbeiro_thread = threading.Thread (name="Barbeiro", target=barbeiro) # inicializa thread para o barbeiro
barbeiro_thread.start() # começa a thread do barbeiro
custs = [ 'Mr. a', 'Mr. b', 'Mr. c', 'Mr. d', 'Mr. e', 'Mr. f', 'Mr. g', 'Mr. h' ]
cust_threads = [] # todas as threads de clientes

while True:
    global cadeiras
    if (len(cust_threads)): # se houverem threads em cust_threads
        for t in cust_threads:
            t.join () # executa os seguintes códigos somente quando todas as threads de clientes terminam suas execuções
    if (esperando == 0 and not (cliente_cortando_cabelo)): # se nenhum cliente estiver esperando ou recebendo corte
        print (f'Cliente recebendo o corte: {cliente_cortando_cabelo},lista_esperando: {lista_esperando}')
        n_cust = int (input ("quantos clientes você quer?\n")) # receber entrada do número de clientes
        cadeiras = int (input ("quantos acentos de esperando você quer?\n")) # receber entrada do número de clientes
        if (n_cust > 11): # se o usuário quiser criar mais de 11 clientes
            for i in range (12, n_cust +1): # cria mais exemplos de clientes
                custs.append (f'Customer{i}')
        print ("gerando clientes...")
        for index, cust in enumerate (custs [:n_cust]):# para todos os exemplos, inicializar e começar as threads
            sp(1) # esperando 1 segundo
            customer_thread = threading.Thread (name = "Customer", 
            target=customer, args=[f'{cust} ({str(index +1)})'])
            customer_thread.start()
            cust_threads.append(customer_thread)
            sp (random.randint (0,3)) # esperando por um número aleatório entre 0 e 3 segundos