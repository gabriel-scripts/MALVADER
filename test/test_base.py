# tests/test_setup.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dao.config.database import Base

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('mysql+pymysql://root:verysecret@localhost:33789/test_db')
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Remove todas as tabelas
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        # Nova sessão para cada teste
        self.session = self.Session()
        self.session.begin_nested()

    def tearDown(self):
        # Rollback após cada teste
        self.session.rollback()
        self.session.close()