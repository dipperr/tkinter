import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel
from tkinter.messagebox import WARNING
from tkinter.messagebox import showinfo
import logging

from models import models as md
from controller import controller as ct
import extras


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ViewSearchPerson(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__init_window(parent)
        self.__label()
        self.__entrys()
        self.__frame()
        self.controller = None

    def __init_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (1000 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (600 / 2))
        self.geometry(f'1000x600+{center_x}+{center_y}')
        self.minsize(width=1000, height=600)
        self.configure(background='#ececec')

    def __frame(self):
        self.frame = tk.Frame(self, bd=4, bg='#f8f8f8')
        self.frame.place(x=0, rely=0.2, relwidth=1, relheight=0.8)

    def __label(self):
        self.lb_nome = tk.Label(self, text='Nome', bg='#ececec', font=('Arial', 12))
        self.lb_nome.place(x=10, y=7)

    def __entrys(self):
        self.entry_nome = ttk.Entry(self)
        self.entry_nome.place(x=10, y=30, relwidth=0.6)
        self.entry_nome.focus()


class ViewSearchDoorman(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Consultar Porteiro')
        self.__buttons()
        self.__checkbutton()
        self.__tree_view()
        self.__scrollbar()
        self.list_values = None

    def __buttons(self):
        self.button_pesquisar = ttk.Button(self, text='Pesquisar', command=self.pesquisar)
        self.button_pesquisar.place(x=10, y=70)
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.clear_tree)
        self.button_limpar.place(x=130, y=70)
        self.button_apagar = ttk.Button(self, text='Apagar', command=self.delete)
        self.button_apagar.place(x=250, y=70)
        self.button_apagar.state(['disabled'])
        self.button_editar = ttk.Button(self, text='Editar', command=self.editar)
        self.button_editar.place(x=370, y=70)
        self.button_editar.state(['disabled'])

    def __tree_view(self):
        self.tree = ttk.Treeview(self.frame, columns=('id', 'nome', 'cpf', 'telefone', 'sexo', 'email'),
                                 show='headings', displaycolumns=('nome', 'cpf', 'telefone', 'sexo', 'email'))
        self.tree.heading('nome', text='Nome')
        self.tree.heading('cpf', text='Cpf')
        self.tree.column('cpf', width=150)
        self.tree.heading('telefone', text='Telefone')
        self.tree.column('telefone', width=150)
        self.tree.heading('sexo', text='Sexo')
        self.tree.column('sexo', width=100)
        self.tree.heading('email', text='Email')
        self.tree.column('email', width=100)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(x=0, y=0, relwidth=0.98, relheight=1)

    def __scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)

    def __checkbutton(self):
        self.agreement = tk.IntVar()
        self.check = tk.Checkbutton(
            self, text='Todos Registros', command=self.agreement_changed, variable=self.agreement,
            onvalue=1, offvalue=0, bg='#ececec'
        )
        self.check.place(relx=0.85, rely=0.05)

    def pesquisar(self):
        self.clear_tree()
        if self.controller:
            self.controller.search(
                self.entry_nome.get()
            )

    def search_all(self):
        if self.controller:
            self.controller.search_all()

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?',
            icon=WARNING
        )
        if answer:
            self.controller.delete(self.list_values[0])
            showinfo(
                title='Info',
                message='Registro Apagado',
                parent=self
            )

    def editar(self):
        model = md.Doorman()
        view = ViewUpdDoorman(self)
        view.grab_set()
        controler = ct.ControllerDoorman(view, model)
        view.set_control(controler)
        view.id = self.list_values[0]
        view.entry_nome.insert('end', self.list_values[1])
        view.entry_cpf.insert('end', self.list_values[2])
        view.entry_telefone.insert('end', self.list_values[3])
        view.entry_sexo.insert('end', self.list_values[4])
        view.entry_email.insert('end', self.list_values[5])

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.check.deselect()
        self.button_apagar.state(['disabled'])
        self.button_editar.state(['disabled'])

    def agreement_changed(self):
        if self.agreement.get() == 1:
            self.search_all()

    def set_control(self, controller):
        self.controller = controller

    def item_select(self, event):
        self.button_apagar.state(['!disabled'])
        self.button_editar.state(['!disabled'])
        for selected_item in self.tree.selection():
            self.list_values = self.tree.item(selected_item, 'values')


class ViewSearchEnterprise(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Consultar Empresa')
        self.__buttons()
        self.__tree_view()
        self.__scrollbar()
        self.__checkbutton()
        self.list_values = None

    def __buttons(self):
        self.button_pesquisar = ttk.Button(self, text='Pesquisar', command=self.pesquisar)
        self.button_pesquisar.place(x=10, y=70)
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.clear_tree)
        self.button_limpar.place(x=130, y=70)
        self.button_apagar = ttk.Button(self, text='Apagar', command=self.delete)
        self.button_apagar.place(x=250, y=70)
        self.button_apagar.state(['disabled'])
        self.button_editar = ttk.Button(self, text='Editar', command=self.editar)
        self.button_editar.place(x=370, y=70)
        self.button_editar.state(['disabled'])

    def __tree_view(self):
        self.tree = ttk.Treeview(self.frame, columns=('id', 'nome', 'cnpj', 'telefone', 'rua', 'numero',
                                                      'bairro', 'cidade', 'cep'),
                                 show='headings', displaycolumns=('nome', 'cnpj', 'telefone', 'rua', 'numero',
                                                                  'bairro'))
        self.tree.heading('nome', text='Nome')
        self.tree.column('nome', width=200)
        self.tree.heading('cnpj', text='Cnpj')
        self.tree.column('cnpj', width=100)
        self.tree.heading('telefone', text='Telefone')
        self.tree.column('telefone', width=100)
        self.tree.heading('rua', text='rua')
        self.tree.column('rua', width=150)
        self.tree.heading('numero', text='numero')
        self.tree.column('numero', width=50)
        self.tree.heading('bairro', text='bairro')
        self.tree.column('bairro', width=100)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(x=0, y=0, relwidth=0.98, relheight=1)

    def __scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)

    def __checkbutton(self):
        self.agreement = tk.IntVar()
        self.check = tk.Checkbutton(
            self, text='Todos Registros', command=self.agreement_changed, variable=self.agreement,
            onvalue=1, offvalue=0, bg='#ececec'
        )
        self.check.place(relx=0.85, rely=0.05)

    def pesquisar(self):
        self.clear_tree()
        if self.controller:
            self.controller.search(
                self.entry_nome.get()
            )

    def search_all(self):
        if self.controller:
            self.controller.search_all()

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?',
            icon=WARNING
        )
        if answer:
            self.controller.delete(self.list_values[0])
            showinfo(
                title='Info',
                message='Registro Apagado',
                parent=self
            )

    def editar(self):
        model = md.Enterprise()

        view = ViewUpdEnterprise(self)
        view.grab_set()

        controler = ct.ControllerEnterprise(view, model)
        view.set_control(controler)

        view.id = self.list_values[0]
        view.entry_nome.insert('end', self.list_values[1])
        view.entry_cnpj.insert('end', self.list_values[2])
        view.entry_telefone.insert('end', self.list_values[3])
        view.entry_rua.insert('end', self.list_values[4])
        view.entry_numero_imovel.insert('end', self.list_values[5])
        view.entry_bairro.insert('end', self.list_values[6])
        view.entry_cidade.insert('end', self.list_values[7])
        view.entry_cep.insert('end', self.list_values[8])

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.check.deselect()
        self.button_apagar.state(['disabled'])
        self.button_editar.state(['disabled'])

    def agreement_changed(self):
        if self.agreement.get() == 1:
            self.search_all()

    def set_control(self, controller):
        self.controller = controller

    def item_select(self, event):
        self.button_apagar.state(['!disabled'])
        self.button_editar.state(['!disabled'])
        for selected_item in self.tree.selection():
            self.list_values = self.tree.item(selected_item, 'values')


class ViewSearchHabitant(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Consultar Morador')
        self.__buttons()
        self.__checkbutton()
        self.__tree_view()
        self.__scrollbar()
        self.list_values = None

    def __buttons(self):
        self.button_pesquisar = ttk.Button(self, text='Pesquisar', command=self.pesquisar)
        self.button_pesquisar.place(x=10, y=70)
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.clear_tree)
        self.button_limpar.place(x=130, y=70)
        self.button_apagar = ttk.Button(self, text='Apagar', command=self.delete)
        self.button_apagar.place(x=250, y=70)
        self.button_apagar.state(['disabled'])
        self.button_editar = ttk.Button(self, text='Editar', command=self.editar)
        self.button_editar.place(x=370, y=70)
        self.button_editar.state(['disabled'])

    def __tree_view(self):
        self.tree = ttk.Treeview(self.frame, columns=('id', 'nome', 'cpf', 'telefone', 'residencia'),
                                 show='headings', displaycolumns=('nome', 'cpf', 'telefone', 'residencia'))
        self.tree.heading('nome', text='Nome')
        self.tree.heading('cpf', text='Cpf')
        self.tree.column('cpf', width=150)
        self.tree.heading('telefone', text='Telefone')
        self.tree.column('telefone', width=150)
        self.tree.heading('residencia', text='Residência')
        self.tree.column('residencia', width=100)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(x=0, y=0, relwidth=0.98, relheight=1)

    def __scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)

    def __checkbutton(self):
        self.agreement = tk.IntVar()
        self.check = tk.Checkbutton(
            self, text='Todos Registros', command=self.agreement_changed, variable=self.agreement,
            onvalue=1, offvalue=0, bg='#ececec'
        )
        self.check.place(relx=0.85, rely=0.05)

    def pesquisar(self):
        self.clear_tree()
        if self.controller:
            self.controller.search(
                self.entry_nome.get()
            )

    def search_all(self):
        if self.controller:
            self.controller.search_all()

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?',
            icon=WARNING
        )
        if answer:
            self.controller.delete(self.list_values[0])
            showinfo(
                title='Info',
                message='Registro Apagado',
                parent=self
            )

    def editar(self):
        model = md.Habitant()
        view = ViewUpdHabitant(self)
        view.grab_set()
        controler = ct.ControllerHabitant(model, view)
        view.set_control(controler)
        view.id = self.list_values[0]
        view.entry_nome.insert('end', self.list_values[1])
        view.entry_cpf.insert('end', self.list_values[2])
        view.entry_telefone.insert('end', self.list_values[3])
        view.entry_residencia.insert('end', self.list_values[4])

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.check.deselect()
        self.button_apagar.state(['disabled'])
        self.button_editar.state(['disabled'])

    def agreement_changed(self):
        if self.agreement.get() == 1:
            self.search_all()

    def set_control(self, controller):
        self.controller = controller

    def item_select(self, event):
        self.button_apagar.state(['!disabled'])
        self.button_editar.state(['!disabled'])
        for selected_item in self.tree.selection():
            self.list_values = self.tree.item(selected_item, 'values')


class ViewSearchVisitor(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Consultar Visitantes')
        self.__buttons()
        self.__checkbutton()
        self.__tree_view()
        self.__scrollbar()
        self.list_values = None

    def __buttons(self):
        self.button_pesquisar = ttk.Button(self, text='Pesquisar', command=self.pesquisar)
        self.button_pesquisar.place(x=10, y=70)
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.clear_tree)
        self.button_limpar.place(x=130, y=70)
        self.button_apagar = ttk.Button(self, text='Apagar', command=self.delete)
        self.button_apagar.place(x=250, y=70)
        self.button_apagar.state(['disabled'])
        self.button_editar = ttk.Button(self, text='Editar', command=self.editar)
        self.button_editar.place(x=370, y=70)
        self.button_editar.state(['disabled'])

    def __tree_view(self):
        self.tree = ttk.Treeview(self.frame, columns=('id', 'nome', 'cpf', 'telefone', 'sexo', 'relacao'),
                                 show='headings', displaycolumns=('nome', 'cpf', 'telefone', 'sexo', 'relacao'))
        self.tree.heading('nome', text='Nome')
        self.tree.column('nome', width=200)
        self.tree.heading('cpf', text='Cpf')
        self.tree.column('cpf', width=150)
        self.tree.heading('telefone', text='Telefone')
        self.tree.column('telefone', width=150)
        self.tree.heading('sexo', text='Sexo')
        self.tree.column('sexo', width=100)
        self.tree.heading('relacao', text='Relação')
        self.tree.column('relacao', width=150)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(x=0, y=0, relwidth=0.98, relheight=1)

    def __scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)

    def __checkbutton(self):
        self.agreement = tk.IntVar()
        self.check = tk.Checkbutton(
            self, text='Todos Registros', command=self.agreement_changed, variable=self.agreement,
            onvalue=1, offvalue=0, bg='#ececec'
        )
        self.check.place(relx=0.85, rely=0.05)

    def set_control(self, controller):
        self.controller = controller

    def pesquisar(self):
        self.clear_tree()
        if self.controller:
            self.controller.search(
                self.entry_nome.get()
            )

    def search_all(self):
        if self.controller:
            self.controller.search_all()

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?',
            icon=WARNING
        )
        if answer:
            self.controller.delete(self.list_values[0])
            showinfo(
                title='Info',
                message='Registro Apagado',
                parent=self
            )

    def editar(self):
        model = md.Visitor()
        view = ViewUpdVisitor(self)
        view.grab_set()
        controler = ct.ControllerVisitor(model, view)
        view.set_control(controler)
        view.id = self.list_values[0]
        view.entry_nome.insert('end', self.list_values[1])
        view.entry_cpf.insert('end', self.list_values[2])
        view.entry_telefone.insert('end', self.list_values[3])
        view.entry_sexo.insert('end', self.list_values[4])
        view.entry_rel_morador.insert('end', self.list_values[5])

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.check.deselect()
        self.button_apagar.state(['disabled'])
        self.button_editar.state(['disabled'])

    def agreement_changed(self):
        if self.agreement.get() == 1:
            self.search_all()

    def item_select(self, event):
        self.button_apagar.state(['!disabled'])
        self.button_editar.state(['!disabled'])
        for selected_item in self.tree.selection():
            self.list_values = self.tree.item(selected_item, 'values')


class ViewRegPerson(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__config_window(parent)
        self.__base_labels()
        self.__base_entrys()
        self.controller = None

    def __config_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width()/2)) - (700/2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (400/2))
        self.geometry(f'700x400+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(background='#ececec')

    def __base_labels(self):
        self.lb_nome = tk.Label(self, text='Nome', bg='#ececec', font=('Arial', 12))
        self.lb_nome.place(relx=0.01, rely=0.01)
        self.lb_cpf = tk.Label(self, text='Cpf', bg='#ececec', font=('Arial', 12))
        self.lb_cpf.place(relx=0.65, rely=0.03)
        self.lb_telefone = tk.Label(self, text='Telefone', bg='#ececec', font=('Arial', 12))
        self.lb_telefone.place(relx=0.01, rely=0.2)

    def __base_entrys(self):
        self.entry_nome = ttk.Entry(self)
        self.entry_nome.place(relx=0.01, rely=0.08, relwidth=0.6)
        self.entry_nome.focus()
        self.entry_cpf = ttk.Entry(self)
        self.entry_cpf.place(relx=0.65, rely=0.08, relwidth=0.25)
        self.entry_telefone = ttk.Entry(self)
        self.entry_telefone.place(relx=0.01, rely=0.25, relwidth=0.20)


# Janela para cadastros
class ViewRegDoorman(ViewRegPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Cadastrar Porteiro')
        self.__labels()
        self.__entrys()
        self.__buttons()

    def __labels(self):
        self.lb_sexo = tk.Label(self, text='Sexo', bg='#ececec', font=('Arial', 12))
        self.lb_sexo.place(relx=0.25, rely=0.2)
        self.lb_email = tk.Label(self, text='Email', bg='#ececec', font=('Arial', 12))
        self.lb_email.place(relx=0.01, rely=0.35)
        self.lb_senha = tk.Label(self, text='Senha', bg='#ececec', font=('Arial', 12))
        self.lb_senha.place(relx=0.65, rely=0.35)

    def __entrys(self):
        self.entry_sexo = ttk.Entry(self)
        self.entry_sexo.place(relx=0.25, rely=0.25, relwidth=0.20)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(relx=0.01, rely=0.40, relwidth=0.60)
        self.entry_senha = ttk.Entry(self)
        self.entry_senha.place(relx=0.65, rely=0.40, relwidth=0.30)

    def __buttons(self):
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.limpar_tela)
        self.button_limpar.place(relx=0.02, rely=0.7, relwidth=0.13)
        self.button_add = ttk.Button(self, text='Salvar', command=self.save_button)
        self.button_add.place(relx=0.18, rely=0.7, relwidth=0.13)

    def limpar_tela(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_sexo.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

    def set_control(self, controller):
        self.controller = controller

    def save_button(self):
        if self.controller:
            self.controller.save(
                self.entry_cpf.get(), self.entry_nome.get(), self.entry_telefone.get(),
                self.entry_sexo.get(), self.entry_email.get(), self.entry_senha.get()
            )


class ViewRegEnterprise(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Cadastrar Empresa')
        self.__config_window(parent)
        self.__labals()
        self.__entrys()
        self.__buttons()
        self.__add_settings()
        self.controller = None

    def __config_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (700 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (400 / 2))
        self.geometry(f'700x400+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(background='#ececec')

    def __labals(self):
        self.lb_nome = tk.Label(self, text='Nome Fantasia', bg='#ececec', font=('Arial', 12))
        self.lb_nome.place(relx=0.01, rely=0.03)
        self.lb_cnpj = tk.Label(self, text='Cnpj', bg='#ececec', font=('Arial', 12))
        self.lb_cnpj.place(relx=0.65, rely=0.035)
        self.lb_telefone = tk.Label(self, text='Telefone', bg='#ececec', font=('Arial', 12))
        self.lb_telefone.place(relx=0.01, rely=0.15)
        self.lb_rua = tk.Label(self, text='Rua', bg='#ececec', font=('Arial', 12))
        self.lb_rua.place(relx=0.01, rely=0.4)
        self.lb_cep = tk.Label(self, text='Cep', bg='#ececec', font=('Arial', 12))
        self.lb_cep.place(relx=0.65, rely=0.4)
        self.lb_bairro = tk.Label(self, text='Bairro', bg='#ececec', font=('Arial', 12))
        self.lb_bairro.place(relx=0.01, rely=0.55)
        self.lb_numero_imovel = tk.Label(self, text='Número', bg='#ececec', font=('Arial', 12))
        self.lb_numero_imovel.place(relx=0.55, rely=0.55)
        self.lb_numero_imovel = tk.Label(self, text='Cidade', bg='#ececec', font=('Arial', 12))
        self.lb_numero_imovel.place(relx=0.70, rely=0.55)

    def __entrys(self):
        self.entry_nome = ttk.Entry(self)
        self.entry_nome.place(relx=0.01, rely=0.08, relwidth=0.6)
        self.entry_nome.focus()
        self.entry_cnpj = ttk.Entry(self)
        self.entry_cnpj.place(relx=0.65, rely=0.08, relwidth=0.25)
        self.entry_telefone = ttk.Entry(self)
        self.entry_telefone.place(relx=0.01, rely=0.20, relwidth=0.25)
        self.entry_rua = ttk.Entry(self)
        self.entry_rua.place(relx=0.01, rely=0.45, relwidth=0.60)
        self.entry_cep = ttk.Entry(self)
        self.entry_cep.place(relx=0.65, rely=0.45, relwidth=0.20)
        self.entry_bairro = ttk.Entry(self)
        self.entry_bairro.place(relx=0.01, rely=0.60, relwidth=0.50)
        self.entry_numero_imovel = ttk.Entry(self)
        self.entry_numero_imovel.place(relx=0.55, rely=0.60, relwidth=0.09)
        self.entry_cidade = ttk.Entry(self)
        self.entry_cidade.place(relx=0.70, rely=0.60, relwidth=0.25)

    def __buttons(self):
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.limpar_tela)
        self.button_limpar.place(relx=0.02, rely=0.75, relwidth=0.13)
        self.button_add = ttk.Button(self, text='Salvar', command=self.save_button)
        self.button_add.place(relx=0.18, rely=0.75, relwidth=0.13)
        self.button_add = ttk.Button(self, text='pesquisar', command=self.search_cep)
        self.button_add.place(relx=0.86, rely=0.44, relwidth=0.13, height=30)

    def __add_settings(self):
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.place(relx=0, rely=0.35, relwidth=1)
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Arial', 13), background='#d9d9d9')

    def limpar_tela(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cnpj.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_rua.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_numero_imovel.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)

    def set_control(self, controller):
        self.controller = controller

    def save_button(self):
        if self.controller:
            self.controller.save(
                self.entry_cnpj.get(), self.entry_nome.get(), self.entry_telefone.get(), self.entry_rua.get(),
                self.entry_numero_imovel.get(), self.entry_bairro.get(), self.entry_cidade.get(), self.entry_cep.get()
            )

    def search_cep(self):
        cep_object = md.Address(cep=self.entry_cep.get())

        try:
            endereco = cep_object.search_cep()
        except Exception as error:
            ct.MessageBox.show_error(error)
        else:
            self.entry_bairro.insert('end', endereco['bairro'])
            self.entry_cidade.insert('end', endereco['cidade'])
            self.entry_rua.insert('end', endereco['logradouro'])


class ViewRegHabitant(ViewRegPerson):

    def __init__(self, parent):
        super().__init__(parent)
        self.title('Cadastrar Morador')
        self.__labels()
        self.__entrys()
        self.__buttons()

    def __labels(self):
        self.lb_residencia = tk.Label(self, text='N° Apt', bg='#ececec', font=('Arial', 12))
        self.lb_residencia.place(relx=0.30, rely=0.2)

    def __entrys(self):
        self.entry_residencia = ttk.Entry(self)
        self.entry_residencia.place(relx=0.30, rely=0.25, relwidth=0.08)

    def __buttons(self):
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.limpar_tela)
        self.button_limpar.place(relx=0.02, rely=0.5, relwidth=0.13)
        self.button_add = ttk.Button(self, text='Salvar', command=self.save_button)
        self.button_add.place(relx=0.18, rely=0.5, relwidth=0.13)

    def limpar_tela(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_residencia.delete(0, tk.END)

    def set_control(self, controller):
        self.controller = controller

    def save_button(self):
        if self.controller:
            self.controller.save(
                self.entry_cpf.get(), self.entry_nome.get(), self.entry_telefone.get(),
                self.entry_residencia.get()
            )


# Janela para cadastrar visitante
class ViewRegVisitor(ViewRegPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Cadastrar Visitante')
        self.__labels()
        self.__entrys()
        self.__buttons()
        self.__add_settings()

    def __labels(self):
        self.lb_sexo = tk.Label(self, text='Sexo', bg='#ececec', font=('Arial', 12))
        self.lb_sexo.place(relx=0.25, rely=0.2)
        self.lb_rel_morador = tk.Label(self, text='Relação com Morador', bg='#ececec', font=('Arial', 12))
        self.lb_rel_morador.place(relx=0.5, rely=0.2)

    def __entrys(self):
        self.entry_sexo = ttk.Entry(self)
        self.entry_sexo.place(relx=0.25, rely=0.25, relwidth=0.20)
        self.entry_rel_morador = ttk.Entry(self)
        self.entry_rel_morador.place(relx=0.5, rely=0.25, relwidth=0.4)

    def __buttons(self):
        self.button_limpar = ttk.Button(self, text='Limpar', command=self.limpar_tela)
        self.button_limpar.place(relx=0.02, rely=0.5, relwidth=0.13)
        self.button_add = ttk.Button(self, text='Salvar', command=self.save_button)
        self.button_add.place(relx=0.18, rely=0.5, relwidth=0.13)

    def __add_settings(self):
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.place(relx=0, rely=0.6, relwidth=1)
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Arial', 13), background='#d9d9d9')

    def limpar_tela(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_sexo.delete(0, tk.END)
        self.entry_rel_morador.delete(0, tk.END)

    def set_control(self, controller):
        self.controller = controller

    def save_button(self):
        if self.controller:
            self.controller.save(
                self.entry_cpf.get(), self.entry_nome.get(), self.entry_telefone.get(),
                self.entry_sexo.get(), self.entry_rel_morador.get()
            )


# Janela para atualizar informações
class ViewUpdDoorman(ViewRegDoorman):
    def __init__(self, parent):
        super().__init__(parent)
        self.id = None
        self.entry_senha.config(state='disabled')

    def save_button(self):
        view_autent = ViewAuthentication(self, self.controller, self.entry_cpf.get(),
                                         self.entry_nome.get(), self.entry_telefone.get(),
                                         self.entry_sexo.get(), self.entry_email.get(),
                                         self.id
                                         )


class ViewUpdEnterprise(ViewRegEnterprise):
    def __init__(self, parent):
        super().__init__(parent)
        self.id = None

    def save_button(self):
        if self.controller:
            self.controller.update(
                self.entry_cnpj.get(), self.entry_nome.get(), self.entry_telefone.get(), self.entry_rua.get(),
                self.entry_numero_imovel.get(), self.entry_bairro.get(), self.entry_cidade.get(), self.entry_cep.get(),
                self.id
            )


class ViewUpdHabitant(ViewRegHabitant):
    def __init__(self, parent):
        super().__init__(parent)
        self.id = None

    def save_button(self):
        if self.controller:
            self.controller.update(
                self.entry_cpf.get(), self.entry_nome.get(), self.entry_telefone.get(),
                self.entry_residencia.get(), self.id
            )


class ViewUpdVisitor(ViewRegVisitor):
    def __init__(self, parent):
        super().__init__(parent)
        self.id = None

    def save_button(self):
        if self.controller:
            self.controller.update(
                self.entry_cpf.get(), self.entry_nome.get(), self.entry_telefone.get(),
                self.entry_sexo.get(), self.entry_rel_morador.get(), self.id
            )


class ViewAuthentication(tk.Toplevel):
    def __init__(self, parent, controler, *args):
        super().__init__(parent)
        self.__config_window(parent)
        self.__labels()
        self.__entrys()
        self.__buttons()
        self.controler = controler
        self.args = args

    def __config_window(self, parent):
        self.title('Autenticação')
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (300 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (100 / 2))
        self.geometry(f'300x100+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(background='#ececec')

    def __labels(self):
        self.label_senha = tk.Label(self, text='Senha', bg='#ececec', font=('Arial', 12))
        self.label_senha.place(relx=0.22, rely=0.4, anchor='center')

    def __entrys(self):
        self.senha = tk.StringVar()
        self.entry_senha = ttk.Entry(self, show='*', textvariable=self.senha)
        self.entry_senha.place(relx=0.5, rely=0.4, anchor='center', relwidth=0.4)

    def __buttons(self):
        self.button_login = ttk.Button(self, text='alterar', command=self.__authentication)
        self.button_login.place(relx=0.5, rely=0.8, anchor='center', relwidth=0.4)

    def __authentication(self):
        try:
            autent = extras.Authentication(self.args[0], self.senha.get())
            consulta = autent.authentication()
        except Exception as error:
            ct.MessageBox.show_error(error, parent=self)
        else:
            if consulta:
                self.controler.update(self.args[0], self.args[1], self.args[2], self.args[3], self.args[4],
                                      self.args[5])
                self.destroy()
            else:
                ct.MessageBox.show_error('Senha invalida', parent=self)
