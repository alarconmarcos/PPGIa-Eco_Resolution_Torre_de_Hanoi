class Agente:
    def __init__(self, nome, objetivo, ambiente):
        self.nome = nome
        self.objetivo = objetivo  # Torre de destino (normalmente 'C')
        self.ambiente = ambiente  # Referência ao ambiente para interações
        self.estado = None
        self.bloqueado_por = None  # Outro agente que impede sua ação

    def executar(self):
        # Tenta satisfazer o objetivo; se não conseguir, tenta agredir o bloqueador
        if self.objetivo_satisfeito():
            self.ambiente.registrar(f"[Agente {self.nome}]: Objetivo já satisfeito.")
            return False

        sucesso = self.tentar_satisfazer()
        if sucesso:
            return True

        if self.bloqueado_por:
            self.ambiente.registrar(f"[Agente {self.nome}]: Bloqueado por {self.bloqueado_por.nome}. Iniciando agressão.")
            return self.agredir(self.bloqueado_por)

        return False

    def objetivo_satisfeito(self):
        return self.ambiente.verificar_objetivo(self)

    def tentar_satisfazer(self):
        # Pede ao ambiente para tentar mover o disco
     #   self.ambiente.registrar(f"[Agente {self.nome}]: Tentando mover para {self.objetivo}.")
        sucesso, bloqueador = self.ambiente.mover_disco(self)
        self.bloqueado_por = bloqueador
        return sucesso

    def agredir(self, bloqueador):
        # Tenta forçar o outro a se mover
        if bloqueador:
            self.ambiente.registrar(f"[Agente {self.nome}]: Agressão bem-sucedida contra {bloqueador.nome}.")
        
            return bloqueador.fugir(self)
        return False

    def fugir(self, agressor):
        # Tenta se mover para liberar o caminho
        self.ambiente.registrar(f"[Agente {self.nome}]: Agredido por {agressor.nome}. Tentando fugir...")
        self.ambiente.registrar(f"[Agente {self.nome}]: Fuga bem-sucedida.")
        sucesso, bloqueador = self.ambiente.fugir(self)
        if sucesso:
            return True
        if bloqueador:
            self.ambiente.registrar(f"[Agente {self.nome}]: Fuga bloqueada por {bloqueador.nome}. Contra-agressão!")
            return self.agredir(bloqueador)
        return False