import sqlite3
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DataBase:

    def __init_bd(self):
        logging.info('conectando a base de dados')
        try:
            self.conexao = sqlite3.connect(
                '../database/bancodados.db'
            )
            self.cursor = self.conexao.cursor()
        except sqlite3.OperationalError:
            raise ConnectionError('Não foi possivel conectar\n a base de dados')

    def save(self, query, valores):
        logging.info('executando a escrita')
        self.__init_bd()
        self.cursor.execute(query, valores)
        self.conexao.commit()

    def search(self, query):
        logging.info('executando a consulta')
        self.__init_bd()
        self.cursor.execute(query)

    def delete(self, query, valores):
        logging.info('executando o delete')
        self.__init_bd()
        self.cursor.execute(query, valores)
        self.conexao.commit()

    def update(self, query, valores):
        logging.info('executando o update')
        self.__init_bd()
        self.cursor.execute(query, valores)
        self.conexao.commit()

    def close(self):
        logging.info('fechando a conexão')
        self.cursor.close()
        self.conexao.close()
