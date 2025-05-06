class Funcionario:
    def __init__(self, id_funcionario, nome, codigo_funcionario, data_nascimento, cargo, id_supervisor, senha_hash, ):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self.codigo_funcionario = codigo_funcionario
        self.data_nascimento = data_nascimento
        self.cargo = cargo
        self.id_supervisor = id_supervisor

    def __str__(self):
        return f"Usuario(id_funcionario={self.id_funcionario}, nome={self.nombre}, codigo_funcionario={self.correo})"
    
    @property
    def nome(self):
        return self.nome
    
    @nome.setter    
    def nome(self, nome_novo):
        if isinstance(nome_novo, str) and nome_novo.strip():
            self.nome = nome_novo
        else:
            raise ValueError("error: invalid name")   