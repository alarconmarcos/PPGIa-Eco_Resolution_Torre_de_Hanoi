import tkinter as tk
from interface import InterfaceHanoi

discos = 3  # Número de discos para a Torre de Hanói

def main():
    root = tk.Tk() # Cria a janela principal
    gui = InterfaceHanoi(root, num_discos=discos) # Cria a interface gráfica
    gui.atualizar_log("Iniciando a Torre de Hanói com {} discos.".format(discos)) # Atualiza o log inicial
    gui.atualizar_log("Pressione 'Próximo passo' para avançar.") # Instrução inicial    
    root.mainloop() # Inicia o loop principal da interface gráfica

if __name__ == "__main__":
    main()
