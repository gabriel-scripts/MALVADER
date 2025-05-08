class Usuario:
    def __init__(self, id_usuario, nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash, ):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone

    def __str__(self):
        return f"Usuario(id_usuario={self.id_usuario})"
    
    @property
    def nome(self):
        return self.nome
    
    @nome.setter    
    def nome(self, nome_novo):
        if isinstance(nome_novo, str) and nome_novo.strip():
            self.nome = nome_novo
        else:
            raise ValueError("error: invalid name")   
        
class Cliente: 
    def __init__(self, id_cliente, score_credito, id_usuario):
        self.id_cliente = id_cliente
        self.score_credito = score_credito
        self.id_usuario = id_usuario

    def __str__(self):
        return f"Usuario(id_usuario={self.id_cliente}"
    
    @property
    def nome(self):
        return self.nome
    
    @nome.setter    
    def nome(self, nome_novo):
        if isinstance(nome_novo, str) and nome_novo.strip():
            self.nome = nome_novo
        else:
            raise ValueError("error: invalid name")