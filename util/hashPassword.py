import hashlib

def generate_hash(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def verificar_senha(senha):
    pass