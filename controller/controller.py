from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror


class MessageBox:
    @staticmethod
    def show_info(parent):
        showinfo('Informação', 'Dados adicionados!!', parent=parent)

    @staticmethod
    def show_error(message, parent):
        showerror('Erro!', message, parent=parent)


class ControllerDoorman:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, cpf, nome, telefone, sexo, email, senha):
        self.model.cpf = cpf
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.sexo = sexo
        self.model.email = email
        self.model.senha = senha
        try:
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        self.model.nome = nome
        try:
            consulta = self.model.search()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            consulta = self.model.search_all()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, idd):
        self.model.id = idd
        try:
            self.model.delete()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cpf, nome, telefone, sexo, email, idd):
        self.model.cpf = cpf
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.sexo = sexo
        self.model.email = email
        self.model.id = idd
        try:
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)


class ControllerEnterprise:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, cnpj, nome, telefone, rua, numero, bairro, cidade, cep):
        self.model.cnpj = cnpj
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.endereco.rua = rua
        self.model.endereco.numero = numero
        self.model.endereco.bairro = bairro
        self.model.endereco.cidade = cidade
        self.model.endereco.cep = cep
        try:
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        self.model.nome = nome
        try:
            consulta = self.model.search()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            consulta = self.model.search_all()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, idd):
        self.model.id = idd
        try:
            self.model.delete()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cnpj, nome, telefone, rua, numero, bairro, cidade, cep, idd):
        self.model.cnpj = cnpj
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.endereco.rua = rua
        self.model.endereco.numero = numero
        self.model.endereco.bairro = bairro
        self.model.endereco.cidade = cidade
        self.model.endereco.cep = cep
        self.model.id = idd
        try:
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)


class ControllerHabitant:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, cpf, nome, telefone, residencia):
        self.model.cpf = cpf
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.residencia = residencia
        try:
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        self.model.nome = nome
        try:
            consulta = self.model.search()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            consulta = self.model.search_all()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, idd):
        self.model.id = idd
        try:
            self.model.delete()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cpf, nome, telefone, residencia, idd):
        self.model.cpf = cpf
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.residencia = residencia
        self.model.id = idd
        try:
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info()


class ControllerVisitor:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, cpf, nome, telefone, sexo, relacao):
        self.model.cpf = cpf
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.sexo = sexo
        self.model.relacao = relacao
        try:
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        self.model.nome = nome
        try:
            consulta = self.model.search()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            consulta = self.model.search_all()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, idd):
        self.model.id = idd
        try:
            self.model.delete()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cpf, nome, telefone, sexo, relacao, idd):
        self.model.cpf = cpf
        self.model.nome = nome
        self.model.telefone = telefone
        self.model.sexo = sexo
        self.model.relacao = relacao
        self.model.id = idd
        try:
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info()
