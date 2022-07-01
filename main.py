import tkinter as tk
from tkinter import ttk
from tkinter import Menu
import logging
from random import choice, randint
from tkinter.messagebox import askyesno
from tkinter.messagebox import showinfo

from views import views as vw
from controller import controller as ct
from models import models as md
from extras import Authentication
from extras import ThreadVideo


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# main
class App(tk.Tk):
    logging.info('start of program')

    def __init__(self):
        super().__init__()
        self.__settings_window()
        self.__menu_bar()
        self.__frames()
        self.__tree_view()
        self.__scrollbars()
        self.itemns()
        self.mainloop()

    def __settings_window(self):
        self.title('Portaria')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (500 / 2))
        center_y = int((screen_height / 2) - (300 / 2))
        self.geometry(f'800x600+{center_x}+{center_y}')
        self.minsize(width=800, height=600)
        self.configure(background='#ececec')

    def __menu_bar(self):
        self.menubar = Menu(self, bg='#ececec')
        self.config(menu=self.menubar)

        # criando menu
        self.opcoes_menu = Menu(self.menubar, bg='#ececec', tearoff=False)
        self.cadastro_menu = Menu(self.menubar, bg='#ececec', tearoff=False)
        self.consulta_menu = Menu(self.menubar, bg='#ececec', tearoff=False)
        self.monitor_menu = Menu(self.menubar, bg='#ececec', tearoff=False)

        # adicionando itens ao menu
        self.cadastro_menu.add_command(label='Cadastrar Visitante', command=self.window_reg_visitor)
        self.cadastro_menu.add_command(label='Cadastrar Morador', command=self.window_reg_habitant)
        self.cadastro_menu.add_command(label='Cadastrar Porteiro', command=self.window_reg_doorman)
        self.cadastro_menu.add_command(label='Cadastrar Empresa', command=self.window_reg_enterprise)
        self.consulta_menu.add_command(label='Consultar Visitante', command=self.window_search_visitor)
        self.consulta_menu.add_command(label='Consultar Morador', command=self.window_search_habitant)
        self.consulta_menu.add_command(label='Consultar Porteiro', command=self.window_search_doorman)
        self.consulta_menu.add_command(label='Consultar Empresa', command=self.window_search_enterprise)
        self.monitor_menu.add_command(label='Iniciar Monitoramento', command=self.thread_video)
        self.opcoes_menu.add_command(label='Sair', command=self.destroy)

        # adicionando o menu a menubar
        self.menubar.add_cascade(label='Opções', menu=self.opcoes_menu, underline=0)
        self.menubar.add_cascade(label='Cadastro', menu=self.cadastro_menu, underline=0)
        self.menubar.add_cascade(label='Consulta', menu=self.consulta_menu, underline=0)
        self.menubar.add_cascade(label='Monitoramento', menu=self.monitor_menu, underline=0)

    def __labels(self):
        self.lb_entrada = tk.Label(self, text='Entradas', bg='#ececec', font=('Verdana', 11))
        self.lb_entrada.place(relx=0.01, rely=0.01)
        self.lb_saida = tk.Label(self, text='Saídas', bg='#ececec', font=('Verdana', 11))
        self.lb_saida.place(relx=0.01, rely=0.50)

    def __frames(self):
        self.frame_1 = tk.Frame(self, bd=4, bg='#f8f8f8', highlightbackground='#000000',
                                highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.05, relwidth=0.96, relheight=0.43)

        self.frame_2 = tk.Frame(self, bd=4, bg='#f8f8f8', highlightbackground='#000000',
                                highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.54, relwidth=0.96, relheight=0.43)

    def __tree_view(self):
        self.tree_entrada = ttk.Treeview(self.frame_2, columns=('nome', 'hora_entrada'),
                                         show='headings')
        self.tree_entrada.heading('nome', text='Nome Visitante')
        self.tree_entrada.column('nome', width=100)
        self.tree_entrada.heading('hora_entrada', text='entrada')
        self.tree_entrada.column('hora_entrada', anchor='center', width=30)
        self.tree_entrada.place(relx=0, rely=0, relwidth=0.48, relheight=1)

        self.tree_saida = ttk.Treeview(self.frame_2, columns=('nome', 'hora_saida'),
                                       show='headings')
        self.tree_saida.heading('nome', text='Nome Visitante')
        self.tree_saida.column('nome', width=100)
        self.tree_saida.heading('hora_saida', text='saída')
        self.tree_saida.column('hora_saida', anchor='center', width=30)
        self.tree_saida.place(relx=0.49, rely=0, relwidth=0.49, relheight=1)

    def __scrollbars(self):
        # scrollbars
        # frame1
        self.scrollbar_frame_1 = ttk.Scrollbar(self.frame_2, orient=tk.VERTICAL, command=self.tree_entrada.yview)
        self.tree_entrada.configure(yscrollcommand=self.scrollbar_frame_1.set)
        self.scrollbar_frame_1.place(relx=0.47, rely=0, relwidth=0.02, relheight=1)
        # frame 2
        self.scrollbar_frame_2 = ttk.Scrollbar(self.frame_2, orient=tk.VERTICAL, command=self.tree_saida.yview)
        self.tree_saida.configure(yscrollcommand=self.scrollbar_frame_2.set)
        self.scrollbar_frame_2.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)

    def itemns(self):
        p_nomes = ['ana', 'maria', 'juliana', 'helena', 'madalena', 'carlos', 'francisco',
                   'joão', 'afonso', 'bruna', 'camila']
        s_nomes = ['barros', 'braz', 'bonfim', 'caldas', 'carvalho', 'chavier']

        itemns_1 = [(f'{choice(p_nomes)} {choice(s_nomes)}', f'{randint(1, 24)}:{randint(0,60)}') for _ in
                    range(20)]
        itemns_2 = [(f'{choice(p_nomes)} {choice(s_nomes)}', f'{randint(1, 24)}:{randint(0, 60)}') for _ in
                    range(20)]
        for item1 in itemns_1:
            self.tree_entrada.insert('', tk.END, values=item1)

        for item2 in itemns_2:
            self.tree_saida.insert('', tk.END, values=item2)

    def window_reg_habitant(self):
        logging.info('Instanciou view register habitant')
        model = md.Habitant()

        view = vw.ViewRegHabitant(self)
        view.grab_set()

        controller = ct.ControllerHabitant(model, view)
        view.set_control(controller)

    def window_reg_visitor(self):
        logging.info('Instanciou view register visitor')
        model = md.Visitor()

        view = vw.ViewRegVisitor(self)
        view.grab_set()

        controler = ct.ControllerVisitor(model, view)
        view.set_control(controler)

    def window_reg_doorman(self):
        logging.info('Instanciou view register doorman')
        model = md.Doorman()

        view = vw.ViewRegDoorman(self)
        view.grab_set()

        controler = ct.ControllerDoorman(model, view)
        view.set_control(controler)

    def window_reg_enterprise(self):
        logging.info('Instanciou view register enterprise')
        model = md.Enterprise()

        view = vw.ViewRegEnterprise(self)
        view.grab_set()

        controler = ct.ControllerEnterprise(model, view)
        view.set_control(controler)

    def window_search_visitor(self):
        logging.info('Instanciou view search visitor')
        model = md.Visitor()
        view = vw.ViewSearchVisitor(self)
        view.grab_set()

        controller = ct.ControllerVisitor(model, view)
        view.set_control(controller)

    def window_search_habitant(self):
        logging.info('Instanciou view search habitant')
        model = md.Habitant()
        view = vw.ViewSearchHabitant(self)
        view.grab_set()

        controller = ct.ControllerHabitant(model, view)
        view.set_control(controller)

    def window_search_doorman(self):
        logging.info('Instanciou view search habitant')
        model = md.Doorman()
        view = vw.ViewSearchDoorman(self)
        view.grab_set()

        controller = ct.ControllerDoorman(model, view)
        view.set_control(controller)

    def window_search_enterprise(self):
        logging.info('Instanciou view search Enterprise')
        model = md.Enterprise()
        view = vw.ViewSearchEnterprise(self)
        view.grab_set()

        controller = ct.ControllerEnterprise(model, view)
        view.set_control(controller)

    def thread_video(self):
        thread = ThreadVideo(cam=0)
        thread.start()


class ViewLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__config_window()
        self.__label()
        self.__entrys()
        self.__buttons()
        self.mainloop()

    def __config_window(self):
        self.title('Portaria')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width/2) - (500/2))
        center_y = int((screen_height/2) - (300/2))
        self.geometry(f'500x300+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(background='#ececec')

    def __label(self):
        self.label_title = tk.Label(self, text='Portaria', bg='#ececec', font=('Arial', 18))
        self.label_title.place(relx=0.5, rely=0.2, anchor='center')
        self.label_cpf = tk.Label(self, text='Cpf', bg='#ececec', font=('Arial', 12))
        self.label_cpf.place(relx=0.22, rely=0.4, anchor='center')
        self.label_senha = tk.Label(self, text='Senha', bg='#ececec', font=('Arial', 12))
        self.label_senha.place(relx=0.22, rely=0.6, anchor='center')

    def __entrys(self):
        self.senha = tk.StringVar()
        self.cpf = tk.StringVar()
        self.entry_cpf = ttk.Entry(self, textvariable=self.cpf)
        self.entry_cpf.place(relx=0.5, rely=0.4, anchor='center', relwidth=0.4)
        self.entry_senha = ttk.Entry(self, show='*', textvariable=self.senha)
        self.entry_senha.place(relx=0.5, rely=0.6, anchor='center', relwidth=0.4)

    def __buttons(self):
        self.button_login = ttk.Button(self, text='login', command=self.authentication)
        self.button_login.place(relx=0.5, rely=0.8, anchor='center', relwidth=0.2)
        self.button_recup = tk.Button(self, text='esqueci a senha', bd=0, command=self.recovery)
        self.button_recup.place(relx=0.5, rely=0.93, anchor='center', relwidth=0.3)

    def authentication(self):
        try:
            autent = Authentication(self.cpf.get(), self.senha.get())
            consulta = autent.authentication()
        except Exception as error:
            ct.MessageBox.show_error(error, parent=self)
        else:
            if consulta:
                self.destroy()
                app2 = App()
            else:
                ct.MessageBox.show_error('Senha inválida', parent=self)

    def recovery(self):
        if self.cpf.get():
            answer = askyesno(title='Recuperação', message='Resetar sua senha atual?')
            if answer:
                recovery = Authentication(self.cpf.get())
                try:
                    recovery.recovery_key()
                except ConnectionError as error:
                    ct.MessageBox.show_error(error, parent=self)
                except Exception as error:
                    ct.MessageBox.show_error(error, parent=self)
                else:
                    showinfo('info', 'Foi enviado para seu email\n uma senha temporaria')
        else:
            ct.MessageBox.show_error('Digite seu cpf')


if __name__ == '__main__':
    app = ViewLogin()
