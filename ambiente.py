import threading
import time
from queue import Queue
from agente import Agente
from config import Torre_Origem, Torre_Destino, Torre_Auxiliar


# === CLASSE AMBIENTE (Controle Lógico da Torre) ===
class Ambiente:
    def __init__(self, num_discos, gui):
        self.num_discos = num_discos
        self.torre_objetivo = Torre_Destino
        self.gui = gui
        self.inicializar_ambiente()

    def inicializar_ambiente(self):
        # Define as torres e cria os agentes
        torres_iniciais = {
        'A': {'A': list(range(self.num_discos, 0, -1)), 'B': [], 'C': []},
        'B': {'A': [], 'B': list(range(self.num_discos, 0, -1)), 'C': []},
        'C': {'A': [], 'B': [], 'C': list(range(self.num_discos, 0, -1))}
        }
        self.torres = torres_iniciais[Torre_Origem]  # Inicializa a torre de origem
        
        self.movimentos = Queue()
        self.lock = threading.Lock()
        self.mensagens_log = []
        self.agentes = [Agente(f"Disco {i}", self.torre_objetivo, self) for i in range(1, self.num_discos + 1)]
        self.resolver(self.num_discos, Torre_Origem, Torre_Destino, Torre_Auxiliar)

    def reiniciar(self):
        self.gui.limpar_log()
        self.inicializar_ambiente()
        self.gui.agentes = self.agentes
        self.gui.atualizar_torres(self.torres)
        self.registrar("[Ambiente]: Torre de Hanói reiniciada.")

    def resolver(self, n, origem, destino, auxiliar):
        # Gera a sequência de movimentos da Torre de Hanói
        if n == 1:
            self.movimentos.put((n, origem, destino)) 
        else:
            self.resolver(n-1, origem, auxiliar, destino)
            self.movimentos.put((n, origem, destino))
            self.resolver(n-1, auxiliar, destino, origem)

    def mover_disco(self, agente):
        with self.lock:
            if self.movimentos.empty(): # Verifica se há movimentos pendentes
                return True, None

            disco, origem, destino = self.movimentos.queue[0] # Obtém o próximo movimento

            # Verifica se é o disco correto e se ele está no topo da torre
            if int(agente.nome.split()[1]) != disco:
                return False, self.encontrar_agente_por_disco(disco)

            if self.torres[origem][-1] != disco:
                return False, self.encontrar_agente_por_disco(self.torres[origem][-1]) # Disco não está no topo

            # Realiza o movimento
            self.torres[origem].pop() # Remove o disco da torre de origem
            self.torres[destino].append(disco) # Adiciona o disco à torre de destino
            self.movimentos.get() # Remove o movimento da fila
            self.gui.atualizar_torres(self.torres) # Atualiza a interface gráfica
            time.sleep(0.2)  # pequena pausa para visualização
            self.registrar(f"[Ambiente]: {agente.nome} moveu o disco {disco} de {origem} para {destino}") # Log do movimento
            return True, None

    def fugir(self, agente):
        return self.mover_disco(agente)

    def encontrar_agente_por_disco(self, disco):
        for agente in self.agentes:
            if agente.nome == f"Disco {disco}":
                return agente
        return None

    def verificar_objetivo(self, agente):
        # Verifica se o disco está corretamente empilhado na torre final
        disco = int(agente.nome.split()[1])
        torre_final = self.torres[self.torre_objetivo]
        return torre_final == list(range(self.num_discos, 0, -1)) and disco in torre_final

    def registrar(self, mensagem):
        self.mensagens_log.append(mensagem)
        self.gui.atualizar_log(mensagem)
