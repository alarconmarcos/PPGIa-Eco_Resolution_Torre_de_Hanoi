import tkinter as tk
from tkinter import ttk, messagebox
from ambiente import Ambiente
from config import N_discos


class InterfaceHanoi:
    def __init__(self, root, num_discos):
        self.root = root
        self.root.title("Torre de Hanói - ECO-RESOLUÇÃO")

        # Caixa de log
        self.caixa_log = tk.Text(root, height=10, width=70)
        self.caixa_log.pack(pady=10)

        # Canvas para visualização gráfica das torres
        self.canvas = tk.Canvas(root, width=400, height=200)
        self.canvas.pack()

        # Botão para avançar um passo
        self.botao_proximo = ttk.Button(root, text="Próximo passo", command=self.proximo_passo)
        self.botao_proximo.pack(pady=10)

        # Criação do ambiente e agentes
        self.ambiente = Ambiente(num_discos=num_discos, gui=self)
        self.agentes = self.ambiente.agentes

        self.desenhar_torres()
        self.atualizar_torres(self.ambiente.torres)

    def desenhar_torres(self):
        self.canvas.delete("all")
        for i, x in enumerate([70, 200, 330]):
            self.canvas.create_rectangle(x, 50, x + 10, 150, fill="black")
            self.canvas.create_text(x + 5, 160, text=chr(ord('A') + i))

    def atualizar_torres(self, torres):
        self.desenhar_torres()
        cores = ["red", "green", "blue", "orange", "purple"]
        for idx, torre in enumerate(['A', 'B', 'C']):
            base_x = 70 + idx * 130
            for i, disco in enumerate(torres[torre]):
                largura = disco * 20
                y = 140 - i * 20
                self.canvas.create_rectangle(base_x - largura // 2 + 5, y, base_x + largura // 2 + 5, y + 15, fill=cores[disco % len(cores)])
                self.canvas.create_text(base_x + 5, y + 8, text=str(disco), fill="white")

    def atualizar_log(self, mensagem):
        self.caixa_log.insert(tk.END, mensagem + "\n")
        self.caixa_log.see(tk.END) # rola para o final

    def limpar_log(self):
        self.caixa_log.delete(1.0, tk.END)

    def proximo_passo(self):
        self.atualizar_log("\n--- Próximo passo ---\n")
        for agente in self.agentes:
            if not agente.objetivo_satisfeito():
                agente.executar()
                break

        if self.todos_os_objetivos_concluidos():
            self.atualizar_log("\n====================")
            self.atualizar_log("Todos os discos alcançaram o objetivo final.")
            
            total_movimentos = (2 ** N_discos) - 1  # Fórmula para calcular o total de movimentos
            self.atualizar_log(f"Resolução concluída com {total_movimentos} movimentos.")

            self.root.after(100, self.perguntar_reinicio)

    def todos_os_objetivos_concluidos(self):
        return all(agente.objetivo_satisfeito() for agente in self.agentes)

    def perguntar_reinicio(self):
        # Exibe janela perguntando se o usuário quer reiniciar ou encerrar
        resposta = messagebox.askyesno("Reiniciar", "Todos os discos chegaram ao destino. Deseja reiniciar?")
        if resposta:
            self.root.destroy()
            from main import main
            main()
        else:
            self.root.quit()
