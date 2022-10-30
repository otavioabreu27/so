from random import uniform
from time import sleep
from threading import Thread, Lock

pratos = [0, 0, 0, 0, 0]  # 0 = Não comeu, 1 = Já comeu


class Filosofo(Thread):
    execute = True  # variável para realizar a execução

    def __init__(self, nome, garfo_esquerda, garfo_direita):  # Construtor da classe Filosofo
        Thread.__init__(self)
        self.nome = nome
        self.garfo_esquerda = garfo_esquerda
        self.garfo_direita = garfo_direita

    def run(self):
        """ Sobrescrita de Thread, a função run definirá o que irá acontecer após chamar o método start() na
        instância criada. """
        while self.execute:
            print(f"\n {self.nome} está pensando")
            sleep(uniform(5, 15))
            self.comer()

    def comer(self):
        """
        Pega o garfo 1 e tenta pegar o garfo 2. Se o garfo 2 estiver livre,
        o ele janta e solta os dois garfos em seguida,senão ele desiste de
        comer e continua pensando.
        """
        garfo1, garfo2 = self.garfo_esquerda, self.garfo_direita

        while self.execute:  # enquanto tiver executando
            garfo1.acquire(True)  # tenta pegar o primeiro garfo
            locked = garfo2.acquire(False)  # verifica se o segundo garfo está livre
            if locked:
                break
            garfo1.release()  # libera o garfo1
        else:
            return  # volta a pensar

        print(f"\n {self.nome} começou a comer")
        sleep(uniform(5, 10))
        print(f"\n {self.nome} parou de comer")
        pratos[nomes.index(self.nome)] += 1  # contabiliza o número de vezes que cada filosofo comeu
        print(pratos)
        garfo1.release()  # libera o garfo1
        garfo2.release()  # libera o garfo2


nomes = ['Aristóteles', 'Platão', 'Sócrates', 'Pitágoras', 'Demócrito']  # Nomes dos filósofos
garfos = [Lock() for _ in range(5)]
mesa = [Filosofo(nomes[i], garfos[i % 5], garfos[(i + 1) % 5]) for i in range(5)]
for _ in range(50):
    Filosofo.execute = True  # Inicia a execução
    for filosofo in mesa:
        try:
            filosofo.start()  # inicia o objeto de thread criado.
            sleep(2)
        except RuntimeError:  # Se a thread já tiver sido iniciada
            pass
    sleep(uniform(5, 15))
    Filosofo.execute = False  # Para a execução