import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from random import choice, randint


class WindowCliente(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # janela
        self.title('Cadastro Visitante')
        self.geometry('700x400')
        self.minsize(width=700, height=400)
        self.resizable(False, False)
        self.configure(background='#f9f9f9')

        # labels
        self.lb_nome = ttk.Label(self, text='Nome')
        self.lb_cpf = ttk.Label(self, text='Cpf')
        self.lb_telefone = ttk.Label(self, text='Telefone')
        self.lb_sexo = ttk.Label(self, text='Sexo')
        self.lb_rel_morador = ttk.Label(self, text='Relação com Morador')

        # entrys
        self.entry_nome = ttk.Entry(self)
        self.entry_cpf = ttk.Entry(self)
        self.entry_telefone = ttk.Entry(self)
        self.entry_sexo = ttk.Entry(self)
        self.entry_rel_morador = ttk.Entry(self)

        # buttons
        self.button_limpar = ttk.Button(self, text='Limpar')

        # separator
        self.separator = ttk.Separator(self, orient='horizontal')

        # style
        self.style = ttk.Style(self)

        # inicializa
        self.inicializar()

    def inicializar(self):
        self.lb_nome.place(relx=0.01, rely=0.03)
        self.lb_cpf.place(relx=0.65, rely=0.03)
        self.lb_telefone.place(relx=0.01, rely=0.2)
        self.lb_sexo.place(relx=0.25, rely=0.2)
        self.lb_rel_morador.place(relx=0.5, rely=0.2)

        # entrys
        self.entry_nome.place(relx=0.01, rely=0.08, relwidth=0.6)
        self.entry_cpf.place(relx=0.65, rely=0.08, relwidth=0.25)
        self.entry_telefone.place(relx=0.01, rely=0.25, relwidth=0.20)
        self.entry_sexo.place(relx=0.25, rely=0.25, relwidth=0.20)
        self.entry_rel_morador.place(relx=0.5, rely=0.25, relwidth=0.4)

        # buttons
        self.button_limpar.place(relx=0.02, rely=0.45)

        # separator
        self.separator.place(relx=0, rely=0.4, relwidth=1)

        # configure style
        self.style.configure('TLabel', font=('Arial', 13), background='#f9f9f9')
        self.style.configure('TButton', font=('Arial', 13), background='#d9d9d9')


class WindowEmpresa(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # janela
        self.title('Cadastro Empresa')
        self.geometry('700x400')
        self.minsize(width=700, height=400)
        self.resizable(False, False)

        # labels
        self.lb_nome = ttk.Label(self, text='Nome Fantasia')
        self.lb_cnpj = ttk.Label(self, text='Cnpj')
        self.lb_telefone = ttk.Label(self, text='Telefone')
        self.lb_rua = ttk.Label(self, text='Rua')
        self.lb_cep = ttk.Label(self, text='Cep')
        self.lb_bairro = ttk.Label(self, text='Bairro')
        self.lb_numero_imovel = ttk.Label(self, text='Número')
        self.lb_numero_imovel = ttk.Label(self, text='Cidade')

        # entrys
        self.entry_nome = ttk.Entry(self)
        self.entry_cnpj = ttk.Entry(self)
        self.entry_telefone = ttk.Entry(self)
        self.entry_rua = ttk.Entry(self)
        self.entry_cep = ttk.Entry(self)
        self.entry_bairro = ttk.Entry(self)
        self.entry_numero_imovel = ttk.Entry(self)
        self.entry_cidade = ttk.Entry(self)

        # separator
        self.separator = ttk.Separator(self, orient='horizontal')

        # style
        self.style = ttk.Style(self)

        # inicializa
        self.inicializar()

    def inicializar(self):
        # labels
        self.lb_nome.place(relx=0.01, rely=0.03)
        self.lb_cnpj.place(relx=0.65, rely=0.035)
        self.lb_telefone.place(relx=0.01, rely=0.15)
        self.lb_rua.place(relx=0.01, rely=0.4)
        self.lb_cep.place(relx=0.65, rely=0.4)
        self.lb_bairro.place(relx=0.01, rely=0.55)
        self.lb_numero_imovel.place(relx=0.55, rely=0.55)
        self.lb_numero_imovel.place(relx=0.70, rely=0.55)

        # entrys
        self.entry_nome.place(relx=0.01, rely=0.08, relwidth=0.6)
        self.entry_cnpj.place(relx=0.65, rely=0.08, relwidth=0.25)
        self.entry_telefone.place(relx=0.01, rely=0.20, relwidth=0.25)
        self.entry_rua.place(relx=0.01, rely=0.45, relwidth=0.60)
        self.entry_cep.place(relx=0.65, rely=0.45, relwidth=0.25)
        self.entry_bairro.place(relx=0.01, rely=0.60, relwidth=0.50)
        self.entry_numero_imovel.place(relx=0.55, rely=0.60, relwidth=0.09)
        self.entry_cidade.place(relx=0.70, rely=0.60, relwidth=0.25)

        # separator
        self.separator.place(relx=0, rely=0.35, relwidth=1)

        # configure style
        self.style.configure('Tlabel', font=('Arial', 13))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # janela
        self.title('Portaria')
        self.geometry('700x600')
        self.minsize(width=700, height=600)
        self.configure(background='#f9f9f9')

        # menubar
        self.menubar = Menu(self, bg='#f2f2f2')

        # criando menu
        self.opcoes_menu = Menu(self.menubar, bg='#f8f8f8', tearoff=False)

        # labels
        self.lb_entrada = tk.Label(self, text='Entradas', bg='#f9f9f9', font=('Verdana', 11))
        self.lb_saida = tk.Label(self, text='Saídas', bg='#f9f9f9', font=('Verdana', 11))

        # frames
        self.frame_1 = tk.Frame(self, bd=4, bg='#ffffff')

        self.frame_2 = tk.Frame(self, bd=4, bg='#ffffff')

        # treeview
        self.tree_frame_1 = ttk.Treeview(self.frame_1, columns=('nome', 'relacao_morador', 'hora_entrada'),
                                         show='headings')

        self.tree_frame_2 = ttk.Treeview(self.frame_2, columns=('nome', 'relacao_morador', 'hora_saida'),
                                         show='headings')

        # scrollbars
        # --frame1
        self.scrollbar_frame_1 = ttk.Scrollbar(self.frame_1, orient=tk.VERTICAL, command=self.tree_frame_1.yview)
        # --frame 2
        self.scrollbar_frame_2 = ttk.Scrollbar(self.frame_2, orient=tk.VERTICAL, command=self.tree_frame_2.yview)

        # inicializa
        self.inicializar()
        # preenche as lista
        self.itemns()

    def inicializar(self):
        # menu
        self.config(menu=self.menubar)
        # adicionando itens ao menu
        self.opcoes_menu.add_command(label='Cadastrar Visitante', command=self.window_cad_visitante)
        self.opcoes_menu.add_command(label='Cadastrar Empresa', command=self.window_cad_empresa)
        self.opcoes_menu.add_command(label='Sair', command=self.destroy)

        # adicionando o menu a menubar
        self.menubar.add_cascade(label='Opções', menu=self.opcoes_menu)

        # labels
        self.lb_entrada.place(relx=0.01, rely=0.01)
        self.lb_saida.place(relx=0.01, rely=0.50)

        # frames
        self.frame_1.place(relx=0.02, rely=0.06, relwidth=0.96, relheight=0.43)
        self.frame_2.place(relx=0.02, rely=0.55, relwidth=0.96, relheight=0.43)

        # treeviews
        # --frame1
        self.tree_frame_1.column('nome', anchor='center')
        self.tree_frame_1.column('relacao_morador', anchor='center')
        self.tree_frame_1.column('hora_entrada', anchor='center')
        self.tree_frame_1.heading('nome', text='Nome Visitante')
        self.tree_frame_1.heading('relacao_morador', text='Relação com morador')
        self.tree_frame_1.heading('hora_entrada', text='Hora da entrada')
        self.tree_frame_1.place(relx=0, rely=0, relwidth=0.95, relheight=1)
        # --frame2
        self.tree_frame_2.column('nome', anchor='center')
        self.tree_frame_2.column('relacao_morador', anchor='center')
        self.tree_frame_2.column('hora_saida', anchor='center')
        self.tree_frame_2.heading('nome', text='Nome Visitante')
        self.tree_frame_2.heading('relacao_morador', text='Relação com morador')
        self.tree_frame_2.heading('hora_saida', text='Hora da saída')
        self.tree_frame_2.place(relx=0, rely=0, relwidth=1, relheight=1)

        # scrollbars
        # -- frame1
        self.tree_frame_1.configure(yscrollcommand=self.scrollbar_frame_1.set)
        self.scrollbar_frame_1.place(relx=0.95, rely=0, relwidth=0.05, relheight=1)
        # --frame2
        self.tree_frame_2.configure(yscrollcommand=self.scrollbar_frame_2.set)
        self.scrollbar_frame_2.place(relx=0.95, rely=0, relwidth=0.05, relheight=1)

    def itemns(self):
        p_nomes = ['ana', 'maria', 'juliana', 'helena', 'madalena', 'carlos', 'francisco',
                   'joão', 'afonso', 'bruna', 'camila']
        s_nomes = ['barros', 'braz', 'bonfim', 'caldas', 'carvalho', 'chavier']

        itemns_1 = [(f'{choice(p_nomes)} {choice(s_nomes)}', 'Amigo', f'{randint(1, 24)}:{randint(0,60)}') for _ in
                    range(20)]
        itemns_2 = [(f'{choice(p_nomes)} {choice(s_nomes)}', 'Amigo', f'{randint(1, 24)}:{randint(0, 60)}') for _ in
                    range(20)]
        for item1 in itemns_1:
            self.tree_frame_1.insert('', tk.END, values=item1)

        for item2 in itemns_2:
            self.tree_frame_2.insert('', tk.END, values=item2)

    def window_cad_visitante(self):
        window_cad_visitante = WindowCliente(self)
        window_cad_visitante.grab_set()

    def window_cad_empresa(self):
        window_cad_empresa = WindowEmpresa(self)
        window_cad_empresa.grab_set()


if __name__ == '__main__':
    app = App()
    app.mainloop()
