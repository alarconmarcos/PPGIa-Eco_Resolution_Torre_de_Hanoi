import tkinter as tk
from interface import InterfaceHanoi

discos = 3

def main():
    root = tk.Tk()
    gui = InterfaceHanoi(root, num_discos=discos)
    
    root.mainloop()

if __name__ == "__main__":
    main()
