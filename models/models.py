from abc import ABC
from abc import abstractmethod
import hashlib
import logging
from pycep_correios import get_address_from_cep
from pycep_correios import WebService
from pycep_correios import exceptions

from dtbase import dtbase


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Person(ABC):
    def __init__(self, cpf, nome, telefone):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.database = dtbase.DataBase()

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def search_all(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def format_cpf(self):
        self.cpf = self.cpf.replace('.', '').replace('-', '').replace(' ', '')


class Address:
    def __init__(self, bairro=None, cidade=None, cep=None, numero=None, rua=None):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep

    def search_cep(self):
        """o formato de resposta é um objeto dict com as seguintes chaves:
           bairro, cep, cidade, logradouro, uf, complemento"""
        self.format_cep()
        try:
            endereco = get_address_from_cep(self.cep, webservice=WebService.APICEP)
        except exceptions.InvalidCEP:
            raise Exception('Cep inválido')
        except exceptions.CEPNotFound:
            raise Exception('Cep não encontrado')
        else:
            return endereco

    def non_null_validation(self):
        return all([self.rua, self.numero, self.bairro, self.cidade, self.cep])

    def format_cep(self):
        self.cep = self.cep.replace('-', '').replace(' ', '')


class Doorman(Person):
    def __init__(self, cpf=None, nome=None, telefone=None, sexo=None, email=None, senha=None, idd=None):
        super().__init__(cpf, nome, telefone)
        self.sexo = sexo
        self.email = email
        self.senha = senha
        self.id = idd

    def save(self):
        if self.non_null_validation():
            self.format_cpf()
            self.password_hash()
            self.database.save(
                """INSERT INTO portporteiro(cpf, nome, telefone, sexo, email, senha) VALUES (?, ?, ?, ?, ?, ?)""",
                (self.cpf, self.nome, self.telefone, self.sexo, self.email, self.senha)
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def search(self):
        self.database.search(
            f"""SELECT id, nome, cpf, telefone, sexo, email FROM portporteiro WHERE nome LIKE '{self.nome}%'"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def search_all(self):
        self.database.search(
            """SELECT id, nome, cpf, telefone, sexo, email FROM portporteiro"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def delete(self):
        self.database.delete(
            f"""DELETE FROM portporteiro WHERE id=:id""", {'id': self.id}
        )
        self.database.close()

    def update(self):
        logging.info('executando o update da classe visitante')
        if self.non_null_validation():
            self.database.update(
                f"""UPDATE portporteiro SET cpf=:cpf, nome=:nome, telefone=:tel, sexo=:sex,email=:email WHERE id=:id""",
                {'cpf': self.cpf, 'nome': self.nome, 'tel': self.telefone, 'sex': self.sexo,
                 'email': self.email, 'id': self.id}
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def password_hash(self):
        self.senha = hashlib.md5(self.senha.encode()).hexdigest()

    def non_null_validation(self):
        return all([self.cpf, self.nome, self.telefone, self.sexo, self.email, self.senha])


class Enterprise:
    def __init__(self, cnpj=None, nome=None, telefone=None, idd=None):
        self.endereco = Address()
        self.cnpj = cnpj
        self.nome = nome
        self.telefone = telefone
        self.id = idd
        self.database = dtbase.DataBase()

    def save(self):
        if self.non_null_validation() and self.endereco.non_null_validation():
            self.format_cnpj()
            self.endereco.format_cep()
            self.database.save(
                """INSERT INTO portempresa (cnpj, nome, telefone, rua, numero, bairro, cidade, cep)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.cnpj, self.nome, self.telefone, self.endereco.rua, self.endereco.numero, self.endereco.bairro,
                 self.endereco.cidade, self.endereco.cep)
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def search(self):
        self.database.search(
            f"""SELECT id, nome, cnpj, telefone, rua, numero, bairro, cidade, cep
            FROM portempresa WHERE nome LIKE '{self.nome}%'"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def search_all(self):
        self.database.search(
            f"""SELECT id, nome, cnpj, telefone, rua, numero, bairro, cidade, cep FROM portempresa"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def delete(self):
        self.database.delete(
            f"""DELETE FROM portempresa WHERE id=:id""", {'id': self.id}
        )
        self.database.close()

    def update(self):
        logging.info('executando o update da classe visitante')
        if self.non_null_validation() and self.endereco.non_null_validation():
            self.database.update(
                f"""UPDATE portempresa SET nome=:nome, cnpj=:cnpj, telefone=:tel, rua=:rua, numero=:num, bairro=:bairro,
                cidade=:cid, cep=:cep WHERE id=:id""",
                {'cnpj': self.cnpj, 'nome': self.nome, 'tel': self.telefone, 'rua': self.endereco.rua,
                 'num': self.endereco.numero, 'bairro': self.endereco.bairro, 'cid': self.endereco.cidade,
                 'cep': self.endereco.cep, 'id': self.id}
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.cnpj, self.nome, self.telefone])

    def format_cnpj(self):
        self.cnpj = self.cnpj.replace('.', '').replace('/', '').replace('-', '').replace(' ', '')


class Habitant(Person):
    def __init__(self, cpf=None, nome=None, telefone=None, residencia=None, idd=None):
        super().__init__(cpf, nome, telefone)
        self.residencia = residencia
        self.id = idd

    def save(self):
        if self.non_null_validation():
            self.format_cpf()
            self.database.save(
                """INSERT INTO portmorador (cpf, nome, telefone, residencia) VALUES (?, ?, ?, ?)""",
                (self.cpf, self.nome, self.telefone, self.residencia)
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def search(self):
        self.database.search(
            f"""SELECT id, nome, cpf, telefone, residencia FROM portmorador WHERE nome LIKE '{self.nome}%'"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def search_all(self):
        self.database.search(
            """SELECT id, nome, cpf, telefone, residencia FROM portmorador"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def delete(self):
        self.database.delete(
            f"""DELETE FROM portmorador WHERE id=:id""", {'id': self.id}
        )
        self.database.close()

    def update(self):
        logging.info('executando o update da classe habitant')
        if self.non_null_validation():
            self.database.update(
                f"""UPDATE portmorador SET nome=:nome, telefone=:tel, cpf=:cpf, residencia=:resid WHERE id=:id""",
                {'cpf': self.cpf, 'nome': self.nome, 'tel': self.telefone, 'resid': self.residencia, 'id': self.id}
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.cpf, self.nome, self.telefone, self.residencia])


class Visitor(Person):
    def __init__(self, cpf=None, nome=None, telefone=None, sexo=None, relacao=None, idd=None):
        super().__init__(cpf, nome, telefone)
        self.sexo = sexo
        self.relacao = relacao
        self.id = idd

    def save(self):
        if self.non_null_validation():
            self.format_cpf()
            self.database.save(
                """INSERT INTO portvisitante (cpf, nome, telefone, sexo, relacao) VALUES (?, ?, ?, ?, ?)""",
                (self.cpf, self.nome, self.telefone, self.sexo, self.relacao)
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def search(self):
        self.database.search(
            f"""SELECT id, nome, cpf, telefone, sexo, relacao FROM portvisitante WHERE nome LIKE '{self.nome}%'"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def search_all(self):
        self.database.search(
            """SELECT id, nome, cpf, telefone, sexo, relacao FROM portvisitante"""
        )
        consulta = self.database.cursor.fetchall()
        self.database.close()
        return consulta

    def delete(self):
        self.database.delete(
            f"""DELETE FROM portvisitante WHERE id=:id""", {'id': self.id}
        )
        self.database.close()

    def update(self):
        logging.info('executando o update da classe visitante')
        if self.non_null_validation():
            self.database.update(
                f"""UPDATE portvisitante SET cpf=:cpf, nome=:nome, telefone=:tel,sexo=:sex,relacao=:rel WHERE id=:id""",
                {'cpf': self.cpf, 'nome': self.nome, 'tel': self.telefone, 'sex': self.sexo,
                 'rel': self.relacao, 'id': self.id}
            )
            self.database.close()
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.cpf, self.nome, self.telefone, self.sexo, self.relacao])
