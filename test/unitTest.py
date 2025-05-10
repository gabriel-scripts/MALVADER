# tests/test_repositories.py
from testBase import TestBase

from models.Usuario import Usuario
from dao.UserRepository import UserRepository

from datetime import date
import unittest

class TestUsuarioRepository(TestBase):
    def setUp(self):

        super().setUp()
        self.repo = UserRepository(self.session)
        
        self.usuario_data = {
            "nome": "Repositório Teste",
            "cpf": "11122233344",
            "data_nascimento": date(1995, 5, 5),
            "telefone": "11777777777",
            "tipo_usuario": "cliente",
            "senha_hash": "hash789"
        }

    def test_create_usuario(self):
        usuario = self.repo.create(self.usuario_data)
        
        self.assertIsNotNone(usuario.id_usuario)
        self.assertEqual(usuario.nome, "Repositório Teste")
        
        db_usuario = self.session.query(Usuario).get(usuario.id_usuario)
        self.assertEqual(db_usuario.cpf, "11122233344")

if __name__ == '__main__':
    unittest.main()