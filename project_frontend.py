
from tkinter import *
from tkinter import messagebox
from pubsub import pub
from pubsub import *
from project_backend import Database
from email.utils import parseaddr
import datetime
from PIL import Image,ImageTk  

BD = Database()

class Inicio():


    def __init__(self, root):

        self.window = root

        self.pagina_registo = Frame(self.window)
        self.pagina_registo.pack()

        ## Criar botões ##
        b_entrar = Button(self.window,text=" Entrar ", command = self.cruzamento, width=15)
        b_registar = Button(self.window,text="Registar-se", command = self.sub_pagina_registo, width=15)
        

        ## Criar labels ##
        l_titulo = Label(self.window, text="Entre na sua conta: ")
        l_email = Label(self.window, text="E-mail: ")
        l_password = Label(self.window, text="Password: ")

        ## Criar Input Texto ##
        self.var_email = StringVar()
        self.var_password = StringVar()
        
        self.e_email = Entry(self.window, textvariable=self.var_email)
        self.e_password = Entry(self.window,show="*", textvariable=self.var_password)
        

        ## Criar Imagem ##
        img = ImageTk.PhotoImage(Image.open('resources/disco.png').resize((420,160), Image.ANTIALIAS))
        tela = Label(self.window,image=img,height= 150, width = 420)
        tela.image = img

        ## Posicionamento ##
        tela.place(x = 0, y = 0)
        l_titulo.place(x = 15, y = 170)
        l_email.place(x = 35, y = 200)
        self.e_email.place(x = 125, y = 200)
        l_password.place(x = 35, y = 230)
        self.e_password.place(x =125, y = 230 )
        b_entrar.place(x = 150, y = 270)
        b_registar.place(x = 150, y = 300)

        ## Mensagens de outras janelas ##
        pub.subscribe(self.msm, "Close_Registro")
        pub.subscribe(self.msm, "Close_Cliente")
        pub.subscribe(self.msm, "Close_Administrador")

    
    def msm(self, arg1, arg2 = None):
        self.window.update()
        self.window.deiconify()

    def sub_pagina_registo(self):
        self.e_email.delete(0, 'end')
        self.e_password.delete(0, 'end')
        self.window.withdraw()
        self.sub_pag = Registos()

    def sub_pagina_cliente(self,nome):
        self.e_email.delete(0, 'end')
        self.e_password.delete(0, 'end')
        self.window.withdraw()
        self.sub_pag = Cliente(nome)

    def sub_pagina_admin(self,nome):
        self.e_email.delete(0, 'end')
        self.e_password.delete(0, 'end')
        self.window.withdraw()
        self.sub_pag = Administrador(nome)

    def cruzamento(self):
        ##  ESTE MÉTODO É ATIVADO QUANDO PRESSIONAR O BUTÃO "ENTRAR". É DECIDIDO SE ABRIMOS A PAGINA DO ADMIN OU CLIENTE  ##
        email =  self.var_email.get()
        password = self.var_password.get()

        if (email and password):
            if BD.verf_utilizador('cliente',email,password):
                self.sub_pagina_cliente(BD.verf_utilizador('cliente',email,password)[0])
                
                
            elif BD.verf_utilizador('administrador',email,password):
                self.sub_pagina_admin(BD.verf_utilizador('administrador',email,password)[0])

            else:
                messagebox.showinfo("Aviso","Os dados fornecidos não pertencem a uma conta existente.\nDeve criar uma nova conta.")
                self.e_email.delete(0, 'end')
                self.e_password.delete(0, 'end')
        else:
            messagebox.showinfo("Aviso","Deve registar os seus dados de conta!")
    


class Registos(Toplevel):

    def __init__(self):
        Toplevel.__init__(self)

        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (420/2)
        y = (hs/2) - (300/2)

        self.geometry("420x300"+"+%d+%d" % (x, y))
        self.resizable(0, 0)
        self.title("Registos")

        ## Criar botões ##
        b_registo = Button(self,text=" Registar ", command = self.guardar_fechar)
        b_cancelar = Button(self,text=" Cancelar ", command = self.fechar_janela)

        ## Criar labels ##
        l_slogan = Label(self, text="CRIAR UMA NOVA CONTA")
        l_nome = Label(self, text="Nome: ")
        l_email = Label(self, text="E-mail: ")
        l_password = Label(self, text="Password: ")
        l_contato = Label(self, text="Contato: ")

        ## Criar Input Texto ##
        self.var_nome = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_contato = StringVar()
        val_nome = (self.register(self.validacao_nome), '%s')
        inval_nome = (self.register(self.invalidacao_nome), '%s')
        val_email = (self.register(self.validacao_email), '%s')
        inval_email = (self.register(self.invalidacao_email), '%s')
        val_contato = (self.register(self.validacao_contato), '%s')
        inval_contato = (self.register(self.invalidacao_contato), '%s')
        
        self.e_nome = Entry(self, validate="focusout", validatecommand = val_nome, invalidcommand = inval_nome, textvariable=self.var_nome)
        self.e_email = Entry(self,validate="focusout", validatecommand = val_email, invalidcommand = inval_email, textvariable=self.var_email)
        self.e_password = Entry(self, show="*",textvariable=self.var_password)
        self.e_contato = Entry(self,validate="focusout", validatecommand = val_contato, invalidcommand = inval_contato, textvariable=self.var_contato)

        
        ## Posicionamento ##
        l_slogan.place(x = 140, y = 30)
        l_nome.place(x = 45, y = 100)
        self.e_nome.place(x = 135, y = 100)
        l_email.place(x = 45, y = 130)
        self.e_email.place(x = 135, y = 130)
        l_password.place(x = 45, y = 160)
        self.e_password.place(x =135, y = 160)
        l_contato.place(x = 45, y = 190)
        self.e_contato.place(x = 135, y = 190)
        b_registo.place(x = 240, y = 230)
        b_cancelar.place(x = 160, y = 230)


    def guardar_fechar(self):
        ##  REGISTA UM NOVO CLIENTE NA BASE DE DADOS SE TODAS AS CONDIÇÕES FOREM VERIFICADAS  ##

        nome = self.var_nome.get().title()
        email =  self.var_email.get()
        password = self.var_password.get()
        contato = self.var_contato.get()

        if contato == '':
            contato = None
        
        if not(self.validacao_contato(contato)):
            messagebox.showinfo("Aviso","Informação invalida.\nDeve escrever no formato xxxxxxxxx utilizando apenas caracteres numericos")
            self.e_contato.delete(0, 'end')
            return

        if nome and email and password:
            BD.insert_cliente(nome,email,password,contato)
            self.fechar_janela()
        else:
            messagebox.showinfo("Aviso","Deve preencher todas as informações")
        

    def validacao_nome(self,item):
        return (all(x.isalpha() or x.isspace() for x in item) or item == '')

    def invalidacao_nome(self,item):
        messagebox.showinfo("Aviso","Informação do nome invalida.")
        self.e_nome.delete(0, 'end')

    def validacao_email(self,item):
        if item == '':
            return True  
        if BD.verf_email(item)[0][0]:
            return False
        else:
            return ('@' in parseaddr(item)[1])

    def invalidacao_email(self,item):
        messagebox.showinfo("Aviso","Este e-mail de conta já existe ou é inválido. \nDeve escolher outra opção")
        self.e_email.delete(0, 'end')

    def validacao_contato(self,item):
        if item == '' or item == None:
            return True    

        if len(item) != 9:
            return False

        try:
            item = int(item)
        except:
            return False
        
        return True

    def invalidacao_contato(self,item):
        messagebox.showinfo("Aviso","Informação invalida.\nDeve escrever no formato xxxxxxxxx utilizando apenas caracteres numericos")
        self.e_contato.delete(0, 'end')

    def fechar_janela(self):
        self.destroy()
        pub.sendMessage("Close_Registro", arg1 = None)



class Cliente(Toplevel):

    def __init__(self, utilizador):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (730/2)
        y = (hs/2) - (650/2)

        self.geometry("730x650"+"+%d+%d" % (x, y))
        self.resizable(0, 0)

        ## Variáveis auxiliares ##
        self.id_cliente = utilizador[0]
        self.nome_cliente = utilizador[1]
        self.index_select = None
        self.lista_albuns = []
        self.lista_carrinho = []
        self.lista_msg = []
        self.modo_funcionamento = 'N'
        self.cod_carrinho = BD.cod_carrinho(self.id_cliente)
        self.id_item_selected = None
        self.msg_selecionada = None

        ## Criar botões ##
        b_logout = Button(self,text="   Logout   ", command = self.fechar_janela)
        b_adicionar_carrinho = Button(self,text="Adicionar ao carrinho", command = self.sub_pagina_adicionar_carrinho, width=16)
        b_pesquisa = Button(self,text="Pesquisar Albuns", command = self.lista_alb, width=16)
        b_detalhes = Button(self,text=" Ver Detalhes ", command = self.sub_pagina_detalhes, width=16)
        b_carrinho = Button(self,text="  Ver Carrinho  ", command = self.ver_carrinho, width=16)
        b_remover_carrinho = Button(self,text="Remover do carrinho", command = self.remover_artigo_carrinho)
        b_compra = Button(self,text="Finalizar compra", command = self.comprar_carrinho,width=16)
        b_historico_comp = Button(self,text="Histórico de Compras", command = self.sub_pagina_historico_compras, width=16) 
        b_lst_mens = Button(self,text="Lista de mensagens", command=self.ver_msg, width=16)
        b_abrir_mens = Button(self,text="  Abrir mensagem  ", command = self.sub_pagina_abrir_msg, width=16)


        ## Criar lables ##
        l_titulo = Label(self, text="Wellcome " + self.nome_cliente + "!")
        l_alb_titulo = Label(self, text="Titulo: ")
        l_alb_grupo = Label(self, text="Artista/Grupo: ")
        l_alb_data = Label(self, text="Data Edição: ")
        l_alb_preco = Label(self, text="Preço: ")
        l_pesquisa = Label(self, text="Critérios de pesquisa: ")
        l_comandos = Label(self, text="Operações: ")
        l_montante_total = Label(self, text="Valor Total: ")
        self.tipo_lista = StringVar()
        self.tipo_lista.set("RESULTADOS: ")
        l_tipo_lista = Label(self, textvariable=self.tipo_lista)

        ## Criar Menu de opçõe ##
        self.var_campo =  StringVar()
        self.var_campo.set("Escolher campo")
        opcoes_c = ('All','Titulo','Musica','Grupo/artista','Genero')
        self.op_campo = OptionMenu(self, self.var_campo,*opcoes_c)
        self.op_campo.config(width=15)
        #self.var_campo.trace("w",lambda *args: self.ativar_campo())

        self.var_tipo =  StringVar()
        self.var_tipo.set("Escolher restrição:")
        opcoes_t = ('Coleção inteira','Histórico de Compras')
        self.op_tipo = OptionMenu(self, self.var_tipo,*opcoes_t)
        self.op_tipo.config(width=15)
        #elf.var_msg.trace("w",lambda *args: self.ativar_msg())

        self.var_ord =  StringVar()
        self.var_ord.set("Critério de ordenação:")
        opcoes_o = ('Ordem Crescente','Ordem Decrescente')
        self.op_ord = OptionMenu(self, self.var_ord,*opcoes_o)
        self.op_ord.config(width=15)
        #elf.var_msg.trace("w",lambda *args: self.ativar_msg())

        ## Criar output de Texto # 
        self.var_pesquisa = StringVar()    
        self.e_alb_titulo =  Entry(self, width=17)
        self.e_alb_grupo =  Entry(self, width=17)
        self.e_alb_data =  Entry(self, width=17)
        self.e_alb_preco =  Entry(self, width=17)
        self.e_pesquisa =  Entry(self,textvariable = self.var_pesquisa, width=17)
        self.e_carrinho_montante =  Entry(self, width=7)


        ## Criar uma Listbox ##
        self.lib = Listbox(self, height=13, width=25)
        self.lib.bind('<<ListboxSelect>>', self.mostrar_item)

        ## Criar um Scrollbar ##
        self.scroll = Scrollbar(self, orient="vertical")
        
         ## Criar conecção entre o scroll e o Listbox ##
        self.lib.configure(yscrollcommand = self.scroll.set)    
        self.scroll.configure(command = self.lib.yview)   

        ## Criar Imagem ##
        img = ImageTk.PhotoImage(Image.open('resources/cliente.png').resize((730,170), Image.ANTIALIAS))
        tela = Label(self,image=img,height= 160, width = 730)
        tela.image = img

        ## Posicionamento ##
        tela.place(x = 0, y = 0)  
        l_titulo.place(x = 15, y = 180)
        self.e_alb_titulo.place(x = 115, y = 210) 
        self.e_alb_grupo.place(x = 115, y = 240) 
        self.e_alb_data.place(x = 415, y = 210) 
        self.e_alb_preco.place(x = 415, y = 240) 
        l_alb_titulo.place(x = 15, y = 210) 
        l_alb_grupo.place(x = 15, y = 240) 
        l_alb_data.place(x = 325, y = 214) 
        l_alb_preco.place(x = 325, y = 244) 
        l_tipo_lista.place(x = 55, y = 300)
        self.lib.place(x = 55, y = 330) 
        self.scroll.place(x = 295, y = 330, height=225) 

        l_pesquisa.place(x = 350 , y = 290)
        self.op_tipo.place(x=350, y = 350)
        self.op_ord.place(x=520, y = 350)
        self.op_campo.place(x = 350, y = 320) 
        self.e_pesquisa.place(x = 520, y = 320) 
        b_pesquisa.place(x = 535, y = 385)
        l_comandos.place(x = 350, y = 415)
        b_detalhes.place(x = 350, y = 445)
        b_carrinho.place(x = 520, y = 445)
        b_historico_comp.place(x = 350, y = 475) 
        b_adicionar_carrinho.place(x = 520, y = 475)
        b_lst_mens.place(x = 350, y = 505)
        b_remover_carrinho.place(x = 520, y = 505)
        b_abrir_mens.place(x = 350, y = 535)
        b_compra.place(x = 520, y = 535)
        l_montante_total.place(x = 130, y = 565)
        self.e_carrinho_montante.place(x = 210, y = 560)
        b_logout.place(x = 40, y = 600) 


    def lista_alb(self):
        ##  ESTE MÉTODO VAI MOSTRAR TODA A LISTA DE ALBUNS EXISTENTES EM FORMATO DE LISTA ("NOME" BY "ARTISTA")  ##
        ##  É TAMBÉM GUARDADA TODA A INFORMAÇÃO DOS ALBUNS NUMA VARIÁVEL (lista_albuns) AUXILIAR  ##
        self.modo_funcionamento = 'A'
        self.tipo_lista.set("LISTA DE ALBUNS: ")
        self.index_select = None
        self.id_item_selected = None
        var_list = self.criterio_pesquisa()

        if var_list == None:
            return

        self.lista_albuns = []
        self.msg_selecionada = []

        i = 1
        self.lib.delete(0, END) 
        
        for iD, ti, de, gr, da, qt, pr, cod  in var_list: 
            self.lista_albuns.append([i, iD, ti, de, gr, da, qt, pr, cod]) 
            item = str(i) + " - " + ti + " - " + gr                               
            self.lib.insert(END,item) 
            i+=1

        self.e_carrinho_montante.configure(state='normal')
        self.e_carrinho_montante.delete(0, END)
        self.e_carrinho_montante.insert(END," ")
        self.e_carrinho_montante.configure(state='readonly')


    def mostrar_item(self,select):
        ##  ESTE MÉTODO MOSTRA A INFORMAÇÃO GERAL DO ALBUM SELECIONADO NAS 4 CAIXAS DE TEXTO NA PAGINA DO ADMINSTRADOR"  ##
        try:
            w = select.widget
            lista = []
            if self.modo_funcionamento == 'C':
                lista = self.lista_carrinho
            elif self.modo_funcionamento == 'A':
                lista = self.lista_albuns
            elif self.modo_funcionamento == 'M':
                self.index_select = w.get(w.curselection())
                self.index_select = self.index_select.split(' - ')
                self.index_select = self.index_select[0]
                for item  in self.lista_msg: 
                    if str(item[0]) == self.index_select:
                        self.msg_selecionada = item
                return
                
            self.index_select = w.get(w.curselection())
            self.index_select = self.index_select.split(' - ')
            self.index_select = self.index_select[0]
            self.e_alb_titulo.configure(state='normal')
            self.e_alb_grupo.configure(state='normal')
            self.e_alb_data.configure(state='normal')
            self.e_alb_preco.configure(state='normal')
                
            for i in lista:
                if str(i[0]) == self.index_select:
                    self.id_item_selected = i[1] 
                    self.e_alb_grupo.delete(0, END)
                    self.e_alb_titulo.delete(0, END)
                    self.e_alb_data.delete(0, END)
                    self.e_alb_preco.delete(0, END)
                    self.e_alb_titulo.insert(END,i[2])
                    self.e_alb_titulo.configure(state='readonly')
                    self.e_alb_grupo.insert(END,i[4])
                    self.e_alb_grupo.configure(state='readonly')
                    self.e_alb_data.insert(END,i[5])
                    self.e_alb_data.configure(state='readonly')
                    self.e_alb_preco.insert(END,str(i[7])+'€')
                    self.e_alb_preco.configure(state='readonly')
        except:
            pass


    def ver_carrinho(self):
        self.modo_funcionamento = 'C'
        self.tipo_lista.set("CARRINHO: ")
        self.index_select = None
        self.id_item_selected = None
        self.lista_carrinho = []
        self.msg_selecionada = []
        var_list = BD.ver_artigosEmCarrinho(self.cod_carrinho)

        i = 1
        mt = 0
        aux = 0
        self.lib.delete(0, END) 
        for iD, ti, gr, da, pr, qt, mt  in var_list: 
            self.lista_carrinho.append([i, iD, ti, aux, gr, da, aux, pr, qt]) 
            item = str(i) + " - " + ti + "   QT: " + str(qt)                   
            self.lib.insert(END,item) 
            i+=1

        self.e_carrinho_montante.configure(state='normal')
        self.e_carrinho_montante.delete(0, END)
        self.e_carrinho_montante.insert(END,"{0:.2f} €".format(mt))
        self.e_carrinho_montante.configure(state='readonly')


    def ver_msg(self):
        self.modo_funcionamento = 'M'
        self.tipo_lista.set("CAIXA DE MENSAGENS: ")
        self.index_select = None
        self.id_item_selected = None
        self.lista_msg = []
        self.msg_selecionada = []
        var_list = BD.caixa_mensagens(self.id_cliente)
        self.lib.delete(0, END) 

        i = 1
        for assunto, cont, data, vis, cod in var_list: 
            self.lista_msg.append([i, assunto, cont, data, cod]) 
            item = str(i) + " - " + '[Data: '+ data.strftime("%Y-%m-%d") +']  - '+ assunto                              
            self.lib.insert(END,item) 
            if not(vis):
                self.lib.itemconfig(i-1, bg='red')
                self.lib.itemconfig(i-1, foreground="white")
            i+=1
        
        self.e_carrinho_montante.configure(state='normal')
        self.e_carrinho_montante.delete(0, END)
        self.e_carrinho_montante.insert(END," ")
        self.e_carrinho_montante.configure(state='readonly')



    def remover_artigo_carrinho(self):
        if  self.id_item_selected and self.modo_funcionamento == 'C':
            item = 0
            for i in self.lista_carrinho:
                if str(i[0]) == self.index_select:
                    item = i
            if item == 0:
                messagebox.showinfo("Aviso","Deve primeiro selecionar um album para poder eliminar do seu carrinho!")
                return
            
            montante = BD.eliminar_albumEmCarrinho(self.cod_carrinho, item[1], item[7], item[8])
            messagebox.showinfo("Aviso","O artigo selecionado foi eliminado com sucesso: \n\n MONTANTE ATUAL: "+ "{0:.2f} €".format(montante))
            self.ver_carrinho()
            
        else:
            messagebox.showinfo("Aviso","Deve primeiro selecionar um artigo para ser eliminado do carrinho!")

    def comprar_carrinho(self):
        res = BD.finalizarCompra(self.id_cliente, self.cod_carrinho)
        if res == -1:
            messagebox.showinfo("Aviso","Não foi possível finalizar esta compra! Não apresenta saldo suficiente na sua conta.")
            return

        if res:
            self.cod_carrinho = res[1]
            messagebox.showinfo("Aviso","Obrigado pela sua compra! \nO seu saldo atual é "+ "{0:.2f} €".format(res[0]))
        
        else:
            messagebox.showinfo("Aviso","O nosso sistema asinala um erro! Não foi possível concluir esta operação!")




    def criterio_pesquisa(self):
        campo = self.var_campo.get()
        tipo = self.var_tipo.get()
        ordem = self.var_ord.get()
        input_cliente = self.var_pesquisa.get().upper()
        colunas = " album.id_album, album.titulo, album.descricao, album.grupo_artista, album.data_edicao, album.quantidade, album.preco, album.generos_cod_genero "    

        if campo == "Escolher campo" and tipo == "Escolher restrição:" and ordem == "Critério de ordenação:" and input_cliente == '':
            return BD.view_albuns()

        if campo == 'All' and (tipo == "Escolher restrição:" or ordem == "Critério de ordenação:"):
            messagebox.showinfo("Aviso","Para ver toda a coleção deve definir não só o critério do campo mas também a restrição e ordenação!")
            return None
        
        if campo == 'All':
            if tipo == 'Coleção inteira':
                return BD.view_all(colunas, ordem)
            else:
                return BD.view_allCompras(colunas, ordem, self.id_cliente)

        if campo == "Escolher campo" or tipo == "Escolher restrição:" or ordem == "Critério de ordenação:" or input_cliente == '':
            messagebox.showinfo("Aviso","Deve primeiro definir todos os critérios de pesquisa!")
            return None

        if tipo == 'Coleção inteira':

            if campo == 'Titulo':
                return BD.pesquisar_PorTitulo(colunas, input_cliente, ordem)

            elif campo == 'Musica':
                return BD.pesquisar_PorMusica(colunas, input_cliente, ordem)

            elif campo == 'Grupo/artista':
                primeiro = BD.pesquisar_PorArtistaDoAlbum(colunas, input_cliente, ordem)
                segundo = BD.pesquisar_PorArtistaColaboracao(colunas, input_cliente, ordem)

                if primeiro and segundo:
                    return primeiro + segundo
                elif primeiro:
                    return primeiro
                else:
                    return segundo
 
            elif campo == 'Genero':
                return BD.pesquisar_PorGenero(colunas, input_cliente, ordem)
    
        else: 

            if campo == 'Titulo':
                return BD.pesquisar_ComprasFeitasPorTitulo(colunas, input_cliente, ordem, self.id_cliente)

            elif campo == 'Musica':
                return BD.pesquisar_ComprasFeitasPorMusica(colunas, input_cliente, ordem, self.id_cliente)

            elif campo == 'Grupo/artista':
                primeiro = BD.pesquisar_ComprasFeitasPorArtistaDoAlbum(colunas, input_cliente, ordem, self.id_cliente)  
                segundo = BD.pesquisar_ComprasFeitasPorArtistaColaboracao(colunas, input_cliente, ordem, self.id_cliente)

                if primeiro and segundo:
                    return primeiro + segundo
                elif primeiro:
                    return primeiro
                else:
                    return segundo

            elif campo == 'Genero':
                return BD.pesquisar_ComprasFeitasPorGenero(colunas, input_cliente, ordem, self.id_cliente)
        



    def sub_pagina_detalhes(self):
        aux = 0
        if self.modo_funcionamento == 'A':
            for i in self.lista_albuns:
                if str(i[0]) == self.index_select:
                    aux = i
            if aux == 0:
                messagebox.showinfo("Aviso","Deve primeiro selecionar um álbum para ver os seus detalhes!")
            else:
                self.sub_pag = Detalhes(False, aux)
        else:
            messagebox.showinfo("Aviso","Para ver os detalhes de um album deve selecionar um disco na lista de albuns!")


    def sub_pagina_adicionar_carrinho(self):
        aux = 0
        if self.modo_funcionamento == 'C':
            messagebox.showinfo("Aviso","Deve primeiro ir á lista de albuns e selecionar um album para poder adicionar ao seu carrinho!")
            return

        for i in self.lista_albuns:
            if str(i[0]) == self.index_select:
                aux = i

        if aux == 0:
            messagebox.showinfo("Aviso","Deve primeiro selecionar um album para poder adicionar ao seu carrinho!")
        else:
            self.sub_pag = Adicionar_carrinho(aux, self.id_cliente)

    def sub_pagina_abrir_msg(self):
        if self.msg_selecionada:
            self.sub_pag = Mensagem_cliente(self.msg_selecionada)
            BD.mensagem_visualizada(self.id_cliente, self.msg_selecionada[4])
            self.ver_msg()
        else:
            messagebox.showinfo("Aviso","Deve primeiro selecionar uma mensagem da sua caixa de mensagens!")


    def sub_pagina_historico_compras(self):
        self.sub_pag = Historico_compras(self.id_cliente)


    def sub_pagina_pesquisa(self):
        self.sub_pag = None


    def fechar_janela(self):
        self.destroy()
        pub.sendMessage("Close_Cliente", arg1 = None)


class Administrador(Toplevel):

    def __init__(self,utilizador):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (600/2)
        y = (hs/2) - (600/2)

        self.geometry("600x600"+"+%d+%d" % (x, y))
        self.resizable(0, 0)
        self.title("Pagina do Administrador")

        ## Variaveis auxiliares ##
        self.id_admin = utilizador[0]
        self.nome_admin = utilizador[1]
        self.lista_albuns = []
        self.index_select = None
        self.id_album_selected = None

        ## Criar botões ##
        b_logout = Button(self,text="Logout", command = self.fechar_janela, width=9)
        b_update_alb = Button(self,text="Atualizar Album", command = self.sub_pagina_update, width=17)
        b_lista_alb = Button(self,text="Lista dos Albuns", command = self.lista_alb, width=17)
        b_detalhes = Button(self,text="Ver Detalhes", command = self.sub_pagina_detalhes, width=17)
        b_remover_alb = Button(self,text="Remover Album", command = self.remover_album, width=17)
        b_adicionar_alb = Button(self,text="Adicionar Album", command = self.sub_pagina_adicionar_album, width=17)
        b_mensagem = Button(self,text="Enviar Mensagem", command = self.sub_pagina_mensagem, width=17)
        b_saldo = Button(self,text="Atualizar Saldo", command = self.sub_pagina_saldo, width=17)
        b_estatistica = Button(self,text="Ver Estatisticas", command = self.sub_pagina_estatistica, width=17)

        ## Criar labels ##
        l_titulo = Label(self, text="Wellcome " + self.nome_admin + "!")
        l_alb_titulo = Label(self, text="Titulo: ")
        l_alb_grupo = Label(self, text="Artista/Grupo: ")
        l_alb_qt = Label(self, text="Quantidade: ")
        l_alb_preco = Label(self, text="Preço: ")

        ## Criar output de Texto #     
        self.e_alb_titulo =  Entry(self, width=17)
        self.e_alb_grupo =  Entry(self, width=17)
        self.e_alb_qt =  Entry(self, width=17)
        self.e_alb_preco =  Entry(self, width=17)

        ## Criar uma Listbox ##
        self.lib = Listbox(self, height=13, width=25)
        self.lib.bind('<<ListboxSelect>>', self.mostrar_item)

        ## Criar um Scrollbar ##
        self.scroll = Scrollbar(self, orient="vertical")
        
         ## Criar conecção entre o scroll e o Listbox ##
        self.lib.configure(yscrollcommand = self.scroll.set)    
        self.scroll.configure(command = self.lib.yview)         

        ## Criar Imagem ##
        img = ImageTk.PhotoImage(Image.open('resources/admin.png').resize((600,170), Image.ANTIALIAS))
        tela = Label(self,image=img,height= 160, width = 600)
        tela.image = img

        ## Posicionamento ##
        tela.place(x = 0, y = 0)  
        l_titulo.place(x = 15, y = 180)
        self.e_alb_titulo.place(x = 115, y = 210) 
        self.e_alb_grupo.place(x = 115, y = 240) 
        self.e_alb_qt.place(x = 400, y = 210) 
        self.e_alb_preco.place(x = 400, y = 240) 
        l_alb_titulo.place(x = 15, y = 210) 
        l_alb_grupo.place(x = 15, y = 240) 
        l_alb_qt.place(x = 310, y = 214) 
        l_alb_preco.place(x = 310, y = 244) 
        self.lib.place(x = 55, y = 290) 
        self.scroll.place(x = 295, y = 290, height=225) 
        b_lista_alb.place(x = 370 , y = 290)
        b_adicionar_alb.place(x = 370, y = 320) 
        b_detalhes.place(x=370, y = 350)
        b_update_alb.place(x = 370, y = 380)
        b_remover_alb.place(x = 370, y = 410)
        b_mensagem.place(x = 370, y = 440)
        b_saldo.place(x = 370, y = 470) 
        b_estatistica.place(x = 370, y = 500)
        b_logout.place(x = 70, y = 540) 

        pub.subscribe(self.lista_alb, "Close_Update_album")



    def lista_alb(self):
        ##  ESTE MÉTODO VAI MOSTRAR TODA A LISTA DE ALBUNS EXISTENTES EM FORMATO DE LISTA ("NOME" BY "ARTISTA")  ##
        ##  É TAMBÉM GUARDADA TODA A INFORMAÇÃO DOS ALBUNS NUMA VARIÁVEL (lista_albuns) AUXILIAR  ##

        self.index_select = None
        self.id_album_selected = None
        var_list = BD.view_tabela('album')
        self.lista_albuns = []

        i = 1
        self.lib.delete(0, END) 
        
        for iD, ti, de, gr, da, qt, pr, cod  in var_list: 
            self.lista_albuns.append([ i, iD, ti, de, gr, da, qt, pr, cod]) 
            item = str(i) + " - " + ti + " - " + gr                               
            self.lib.insert(END,item) 
            i+=1


    def mostrar_item(self,select):
        ##  ESTE MÉTODO MOSTRA A INFORMAÇÃO GERAL DO ALBUM SELECIONADO NAS 4 CAIXAS DE TEXTO NA PAGINA DO ADMINSTRADOR"  ##
        try:
            w = select.widget

            self.index_select = w.get(w.curselection())
            self.index_select = self.index_select.split(' - ')
            self.index_select = self.index_select[0]
            self.e_alb_titulo.configure(state='normal')
            self.e_alb_grupo.configure(state='normal')
            self.e_alb_qt.configure(state='normal')
            self.e_alb_preco.configure(state='normal')
                
            for i in self.lista_albuns:
                if str(i[0]) == self.index_select:
                    self.id_album_selected = i[1] 
                    self.e_alb_grupo.delete(0, END)
                    self.e_alb_titulo.delete(0, END)
                    self.e_alb_qt.delete(0, END)
                    self.e_alb_preco.delete(0, END)
                    self.e_alb_titulo.insert(END,i[2])
                    self.e_alb_titulo.configure(state='readonly')
                    self.e_alb_grupo.insert(END,i[4])
                    self.e_alb_grupo.configure(state='readonly')
                    self.e_alb_qt.insert(END,i[6])
                    self.e_alb_qt.configure(state='readonly')
                    self.e_alb_preco.insert(END,str(i[7])+'€')
                    self.e_alb_preco.configure(state='readonly')
        except:
            pass



    def remover_album(self):
        if  self.id_album_selected == None:
            messagebox.showinfo("Aviso","Deve primeiro selecionar um album para ser eliminado!")
        else:
            res = BD.remover_album(self.id_album_selected)
            if res:
                messagebox.showinfo("Aviso","O álbum selecionado foi eliminado com sucesso!")
            else:
                messagebox.showinfo("Aviso","O álbum selecionado não pode ser eliminado!")


    def sub_pagina_adicionar_album(self):
        self.sub_pag = Adicionar_album()

    def sub_pagina_detalhes(self):
        aux = 0
        for i in self.lista_albuns:
            if str(i[0]) == self.index_select:
                aux = i
        if aux == 0:
            messagebox.showinfo("Aviso","Deve primeiro selecionar um album para ver os seus detalhes!")
        else:
            self.sub_pag = Detalhes(True,aux)
            

    def sub_pagina_update(self):
        aux = 0
        for i in self.lista_albuns:
            if str(i[0]) == self.index_select:
                aux = i
        if aux == 0:
            messagebox.showinfo("Aviso","Deve primeiro selecionar um album para ser atualizado!")
        else:
            self.sub_pag = Update_album(aux,self.id_admin)
    
    def sub_pagina_mensagem(self):
        self.sub_pag = Mensagem(self.id_admin)

    def sub_pagina_saldo(self):
        self.sub_pag = Saldo()

    def sub_pagina_estatistica(self):
        self.sub_pag = Estatistica()

    def fechar_janela(self):
        self.destroy()
        pub.sendMessage("Close_Administrador", arg1 = None)



class Adicionar_carrinho(Toplevel):

    def __init__(self, info_album, id_cliente):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.grab_set()

        self.geometry("330x300")
        self.resizable(0, 0)
        self.title("Novo artigo")

        ## Variáveis auxiliares ##
        self.id_cliente = id_cliente
        self.cod_carrinho = BD.cod_carrinho(self.id_cliente)
        _,self.iD, self.ti, _, self.gr, _, _, self.pr, _ = info_album

        ## Criar botões ##
        b_submeter = Button(self,text=" Submeter ", command = self.inserir_artigo)
        b_cancelar = Button(self,text="  Cancelar  ", command = self.fechar_janela)

        ## Criar labels ##
        l_titulo = Label(self, text="Adicionar o seguinte produto ao carrinho: ")
        l_nome = Label(self, text=" TITULO: "+ self.ti)
        l_grupo = Label(self, text=" GRUPO/ARTISTA: " + self.gr)
        l_genero = Label(self, text=" PREÇO: " + str(self.pr)+ '€')
        l_parametros = Label(self, text="Defina o seguinte parâmetro: ")
        l_quantidade = Label(self, text="Quantidade: ")
        
        ## Criar Input Texto ##
        self.var_qt = StringVar()
        self.e_qt = Entry(self, textvariable=self.var_qt)


        ## Posicionamento ##
        l_titulo.place(x = 10, y = 30)
        l_nome.place(x = 20, y = 65)
        l_grupo.place(x = 20, y = 95)
        l_genero.place(x = 20, y = 125)
        l_parametros.place(x = 10, y = 170)
        l_quantidade.place(x = 20, y = 200)
        self.e_qt.place(x = 120, y = 200, width=100)
        b_submeter.place(x = 180, y = 250)
        b_cancelar.place(x = 80, y = 250)


    def inserir_artigo(self):
        quantidade = self.var_qt.get()

        if quantidade == '':
            messagebox.showinfo("Aviso","Não é possível inserir este artigo sem a quantidade!")
            return 

        try:
            quantidade = int(quantidade)
        except:
            messagebox.showinfo("Aviso","Existe algum erro na informação!")
            self.e_qt.delete(0, 'end')
            return 
        
        if quantidade < 0:
            messagebox.showinfo("Aviso","Existe algum erro na informação!")
            self.e_qt.delete(0, 'end')
            return 

        montante = BD.inserir_albumEmCarrinho(self.cod_carrinho, self.iD, quantidade)

        if montante == -1:
            messagebox.showinfo("Aviso","Não foi possível inserir este artigo ao seu carrinho de compras. \n\nNão existe a quantidade pedida de exemplares em stock")
        else:
            messagebox.showinfo("Aviso","Um novo artigo foi inserido no seu carrinho: \n\n MONTANTE ATUAL: "+ "{0:.2f} €".format(montante))
            self.fechar_janela()


    def fechar_janela(self):
        self.grab_release()
        self.destroy()


class Adicionar_album(Toplevel):

    data_correta = ''

    def __init__(self):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        self.grab_set()

        self.geometry("400x600")
        self.resizable(0, 0)
        self.title("Informação do Album")

        ## Variável auxiliar ##
        self.index_select = ''

        ## Criar botões ##
        b_submeter = Button(self,text=" Submeter ", command = self.guardar_info)
        b_remove = Button(self,text=" Remover ", command = self.remove_musica)
        b_cancelar = Button(self,text=" Cancelar ", command = self.fechar_janela)
        b_add = Button(self,text=" Acrescentar ", command = self.add_musica)

        ## Criar labels ##
        l_intro = Label(self, text="Registo do Album: ")
        l_titulo = Label(self, text="Titulo: ")
        l_des = Label(self, text="Descrição: ")
        l_grupo = Label(self, text="Grupo/Artista: ")
        l_genero = Label(self, text="Genero: ")
        l_data = Label(self, text="Data de Edição: ")
        l_qt = Label(self, text="Quantidade: ")
        l_preco = Label(self, text="Preço: ")
        l_intro_musicas = Label(self, text="Adicione a lista de musicas desse album: ")
        l_musica = Label(self, text="Musica: ")
        self.colab_artista = StringVar()
        self.colab_artista.set("Artista: ")
        l_artista = Label(self, textvariable=self.colab_artista)


        ## Criar Input Texto ##
        self.var_titulo =  StringVar()
        self.var_des =  StringVar()
        self.var_grupo =  StringVar()
        self.var_genero =  StringVar()
        self.var_data =  StringVar()
        self.var_qt =  StringVar()
        self.var_preco =  StringVar()
        self.var_musica =  StringVar()
        self.var_artista =  StringVar()
        val_preco = (self.register(self.validacao_preco), '%s')
        inval_preco = (self.register(self.invalidacao_preco), '%s')
        val_data = (self.register(self.validacao_data), '%s')
        inval_data = (self.register(self.invalidacao_data), '%s')
        val_qt = (self.register(self.validacao_qt), '%s')
        inval_qt = (self.register(self.invalidacao_qt), '%s')
        val_artista = (self.register(self.validacao_artista), '%s')
        inval_artista = (self.register(self.invalidacao_artista), '%s')
        
        self.e_titulo =  Entry(self, textvariable=self.var_titulo)
        self.e_des =  Entry(self, textvariable=self.var_des)
        self.e_grupo =  Entry(self, textvariable=self.var_grupo)
        self.e_grupo.configure(state='disabled')
        self.e_genero =  Entry(self, textvariable=self.var_genero)
        self.e_data =  Entry(self, validate="focusout", validatecommand = val_data, invalidcommand = inval_data, textvariable=self.var_data)
        self.e_qt =  Entry(self, validate="focusout", validatecommand = val_qt, invalidcommand = inval_qt, textvariable=self.var_qt)
        self.e_preco =  Entry(self,validate="focusout", validatecommand = val_preco, invalidcommand = inval_preco, textvariable=self.var_preco)
        self.e_musica =  Entry(self, textvariable=self.var_musica)
        self.e_musica.configure(state='disabled')
        self.e_artista =  Entry(self, validate="focusout", validatecommand = val_artista, invalidcommand = inval_artista, textvariable=self.var_artista)
        self.e_artista.configure(state='disabled')

        ## Criar um Menu de opçõe ##
        self.var_tipo =  StringVar()
        self.var_tipo.set("Tipo de album")
        self.op_tipo = OptionMenu(self, self.var_tipo,"Coletanea","Individual")
        self.var_tipo.trace("w",lambda *args: self.ativar_grupo())

        ## Criar uma Listbox ##
        self.lib = Listbox(self, height=5, width=20)
        self.lib.bind('<<ListboxSelect>>', self.musica_selecionada)

        ## Criar um Scrollbar ##
        self.scroll = Scrollbar(self, orient="vertical")
        
         ## Criar conecção entre o scroll e o Listbox ##
        self.lib.configure(yscrollcommand = self.scroll.set)    
        self.scroll.configure(command = self.lib.yview)   

        ## Posicionamento ##
        l_intro.place(x = 15, y = 30)
        l_titulo.place(x = 15, y = 90)
        l_des.place(x = 15, y = 120)
        l_grupo.place(x = 15, y = 150)
        self.op_tipo.place(x = 135, y = 150)
        l_genero.place(x = 15, y = 210)
        l_data.place(x = 15, y = 240)
        l_qt.place(x = 15, y = 270)
        l_preco.place(x = 15, y = 300)
        self.e_titulo.place(x = 135, y = 90)
        self.e_des.place(x = 135, y = 120)
        self.e_grupo.place(x = 135, y = 180)
        self.e_genero.place(x = 135, y = 210)
        self.e_data.place(x = 135, y = 240)
        self.e_qt.place(x = 135, y = 270)
        self.e_preco.place(x = 135, y = 300)
        l_intro_musicas.place(x = 15, y = 345)
        l_musica.place(x = 15, y = 380)
        l_artista.place(x = 15, y = 410)
        self.e_musica.place(x = 135, y = 380)
        self.e_artista.place(x = 135, y = 410)
        b_add.place(x = 15, y = 455)
        b_remove.place(x = 15, y = 485)
        self.lib.place(x = 138, y = 450)
        self.scroll.place(x = 330, y = 450, height = 87)
        b_cancelar.place(x = 120, y = 560)
        b_submeter.place(x = 200, y = 560)


    def guardar_info(self):
        
        if self.var_tipo.get() == 'Individual':
            grupo = self.var_grupo.get().title()
        elif self.var_tipo.get() == 'Coletanea':
            grupo = 'Coletanea'
        else:
            grupo = ''

        top_info = (self.var_titulo.get().title(),
        self.var_des.get(),
        grupo,
        self.data_correta,
        self.var_qt.get(),
        self.var_preco.get(),
        self.var_genero.get().title())

        second_info = []
        aux = []
        res = False
        for i in self.lib.get(0, END):
            try:
                aux = i.split(" - ")
                aux[1]=aux[1].title()
            except:
                aux.append('')

            aux[0]=aux[0].title()        
            second_info.append(aux)

        if all(top_info) and any(second_info):
            res = BD.insert_album(top_info, second_info)
            if not(res):
                messagebox.showinfo("Aviso","O album que procura submeter já existe na base de dados!")
            self.fechar_janela()
        else:
            messagebox.showinfo("Aviso","Falta preencher alguma informação antes de poder submeter.")


    def ativar_grupo(self):
        if self.var_tipo.get() == 'Individual':
            self.e_grupo.configure(state='normal')
            self.colab_artista.set("Colaboração: ")
        else:
            self.e_grupo.configure(state='disabled')
            self.colab_artista.set("Artista: ")

        self.e_musica.configure(state='normal')
        self.e_artista.configure(state='normal')
        self.lib.delete(0,END)

    def add_musica(self):
        if not(self.validacao_artista()):
            self.invalidacao_artista()

        musica = self.var_musica.get()
        artista = self.var_artista.get()

        if self.var_tipo.get() == "Coletanea" and musica and artista:
            item = musica + ' - ' + artista
            self.lib.insert(END,item) 
            self.e_musica.delete(0, END)
            self.e_artista.delete(0, END)

        if self.var_tipo.get() == 'Individual' and musica:
            if artista:
                item = musica + ' - ' + artista
            else:
                item = musica
            self.lib.insert(END,item) 
            self.e_musica.delete(0, END)
            self.e_artista.delete(0, END)


    def remove_musica(self):
        if self.index_select:
            self.lib.delete(self.index_select)


    def musica_selecionada(self,select):
        try:
            w = select.widget
            self.index_select = w.curselection()
        except:
            pass

    
    def validacao_data(self,item):
        if item == '':
            return True
        try:
            self.data_correta = datetime.datetime.strptime(item, '%Y-%m-%d')
        except:
            return False

        if self.data_correta > datetime.datetime.now():
            return False
        
        return True
        

    def invalidacao_data(self,item):
        messagebox.showinfo("Aviso","Algo está errado com a informação da data.\nEsta deve ser apresentada como o formato YYYY-MM-DD")
        self.e_data.delete(0, 'end')


    def validacao_preco(self,item):
        if item == '':
            return True
        try:
            item = float(item)
        except:
            return False

        if item < 0:
            return False

        return True
 

    def invalidacao_preco(self,item):
        messagebox.showinfo("Aviso","Algo está errado com a informação do preço.\nEste deve ser um número")
        self.e_preco.delete(0, 'end')
    

    def validacao_qt(self,item):
        if item == '':
            return True
        try:
            item = int(item)
        except:
            return False
        
        if item < 0:
            return False

        return True
 

    def invalidacao_qt(self,item):
        messagebox.showinfo("Aviso","Algo está errado com a informação da quantidade. Esta deve ser um número inteiro positivo")
        self.e_qt.delete(0, 'end')


    def validacao_artista(self,item=None):
        if self.var_artista.get().title() == '':
            return True

        if self.var_grupo.get().title() == self.var_artista.get().title():
            return False
        else:
            return True


    def invalidacao_artista(self,item=None):
        messagebox.showinfo("Aviso","Apenas deve registar colaborações com outros artistas e não o grupo/artista que lançou o disco")
        self.e_artista.delete(0, 'end')


    def fechar_janela(self):
        self.grab_release()
        self.destroy()


class Detalhes(Toplevel):

    def __init__(self, admin, info_album):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        self.grab_set()

        self.geometry("390x360")
        self.resizable(0, 0)
        self.title("Detalhes do Artigo")


        ## Criar botões ##
        b_ok = Button(self,text="     Ok      ", command = self.fechar_janela)

        ## Criar output de Texto ##
        info = Text(self, height=17, width=45)

        ## Criar um Scrollbar ##
        scroll = Scrollbar(self, orient="vertical")
        
         ## Criar conexão entre o scroll e o Listbox ##
        info.configure(yscrollcommand = scroll.set)    
        scroll.configure(command = info.yview) 

        ## Posicionamento ##
        info.place(x = 15, y = 35)
        b_ok.place(x = 165 , y = 310)
        scroll.place(x=355, y = 70, height=215)

        ## APRESENTAÇÃO DE TODA A INFORMAÇÃO DETALHADA DO ALBUM QUE FOI SELECIONADO ##
        _,iD, ti, de, gr, da, qt, pr, cod = info_album

        texto = "TITULO: " + ti + "\n\nARTISTA / GRUPO: " + gr + "\n\nDESCRIÇÃO:\n" + de + "\n\nDATA EDIÇÃO: " + da.strftime("%d/%m/%Y") + "\n\nGENERO: " + BD.view_genero(cod)[0][0] 
        if admin:
            texto = texto + "\n\nQUANTIDADE: " + str(qt) 
        texto = texto + "\n\nPREÇO: " + str(pr) + ' €' + "\n\nMUSICAS:\n\n"

        mix = BD.view_musicas_artistas(iD)
    
        aux = ''
        if gr == 'Coletanea':
            aux = 'Artista: '
        else:
            aux = 'Em colaboração: '

        for i in mix[0]:  
            flag = True
            texto = texto + ' -> ' + i[0]
            for j in mix[1]:
                if i[0] == j[0]:
                    if flag:
                        texto = texto + '\n    '+ aux + j[1]
                        flag = False
                    else:
                        texto = texto + ', ' + j[1]
            texto = texto + '\n\n'
        

        if admin:
            texto = texto + "\nHISTORICO DE PREÇOS:\n\n"
            data_anterior = ''
            historico = BD.view_historico_preco(iD)

            if historico == []:
                texto = texto + '(sem histórico de atualizações)\n\n'

            for index, item in enumerate(historico):
                if index == 0:
                    data_anterior = item[0].strftime("%m/%d/%Y %H:%M:%S")
                    texto = texto + '[inicio até ' + data_anterior + ']\n'
                    texto = texto + ' -> ' + str(item[1]) +'€'+'\n\n'
                else:
                    texto = texto + '[' + data_anterior + ' até ' + item[0].strftime("%m/%d/%Y %H:%M:%S") + ']\n'
                    texto = texto + ' -> ' + str(item[1]) +'€'+ '\n\n'
                    data_anterior = item[0].strftime("%m/%d/%Y %H:%M:%S")

        info.insert(END,texto)
        info.config(wrap=WORD)

        info.config(state=DISABLED)


    def fechar_janela(self):
        self.grab_release()
        self.destroy()
    


class Update_album(Toplevel):

    def __init__(self, info_album,id_utilizador):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        self.grab_set()

        self.geometry("350x300")
        self.resizable(0, 0)
        self.title("Informação do Album")

        ## Variáveis auxiliares ##
        _, self.info_iD, self.info_titulo, _, self.info_grupo, _, self.info_qt, self.info_preco, _ = info_album
        self.id_admin = id_utilizador

        ## Criar botões ##
        b_submeter = Button(self,text=" Submeter ", command = self.guardar_info)
        b_cancelar = Button(self,text=" Cancelar ", command = self.fechar_janela)


        ## Criar labels ##
        l_intro = Label(self, text="Atualização das quantidades e preços do album: ")
        self.titulo = StringVar()
        self.grupo = StringVar()
        self.titulo.set("Titulo: " + self.info_titulo)
        self.grupo.set("Grupo/Artista: " + self.info_grupo)
        l_titulo = Label(self, textvariable=self.titulo)
        l_grupo = Label(self, textvariable=self.grupo)
        l_qt = Label(self, text="Quantidade: ")
        l_preco = Label(self, text="Preço: ")


        ## Criar Input Texto ##
        self.var_qt =  StringVar()
        self.var_preco =  StringVar()

        val_preco = (self.register(self.validacao_preco), '%s')
        inval_preco = (self.register(self.invalidacao_preco), '%s')
        val_qt = (self.register(self.validacao_qt), '%s')
        inval_qt = (self.register(self.invalidacao_qt), '%s')

        self.e_qt =  Entry(self, validate="focusout", validatecommand = val_qt, invalidcommand = inval_qt, textvariable=self.var_qt)
        self.e_preco =  Entry(self,validate="focusout", validatecommand = val_preco, invalidcommand = inval_preco, textvariable=self.var_preco)
        self.e_qt.insert(END,self.info_qt)
        self.e_preco.insert(END,self.info_preco)


        ## Posicionamento ##
        l_intro.place(x = 15, y = 30)
        l_titulo.place(x = 15, y = 70)
        l_grupo.place(x = 15, y = 100)
        l_qt.place(x = 15, y = 160)
        l_preco.place(x = 15, y = 190)
        self.e_qt.place(x = 135, y = 160)
        self.e_preco.place(x = 135, y = 190)
        b_cancelar.place(x = 90, y = 250)
        b_submeter.place(x = 170, y = 250)


    def guardar_info(self):
        
        nova_qt = self.var_qt.get()
        novo_preco = self.var_preco.get()
        antigo_preco = str(self.info_preco)
        antiga_qt = str(self.info_qt)

        if nova_qt == '' or novo_preco == '':
            messagebox.showinfo("Aviso","Falta preencher alguma informação antes de poder submeter")

        elif novo_preco != antigo_preco:
            self.historico_precos(antigo_preco,self.info_iD,self.id_admin)
            BD.update_preco(novo_preco, self.info_iD)
            self.fechar_janela()

        elif nova_qt != antiga_qt:
            BD.update_qt(nova_qt, self.info_iD)
            self.fechar_janela()    

        else:
            self.fechar_janela()
            

    def historico_precos(self,preco_atual,id_album,id_admin):
        preco = BD.view_preco(id_album)
        if preco == preco_atual or preco_atual == None:
            return
        else:
            BD.historico_preco(datetime.datetime.now(),preco_atual,id_album,id_admin)



    def validacao_preco(self,item):
        if item == '':
            return True
        try:
            item = float(item)
        except:
            return False

        if item < 0:
            return False

        return True
 

    def invalidacao_preco(self,item):
        messagebox.showinfo("Aviso","Algo está errado com a informação do preço.\nEste deve ser um número")
        self.e_preco.delete(0, 'end')
    

    def validacao_qt(self,item):
        if item == '':
            return True
        try:
            item = int(item)
        except:
            return False
        
        if item < 0:
            return False

        return True
 

    def invalidacao_qt(self,item):
        messagebox.showinfo("Aviso","Algo está errado com a informação da quantidade. Esta deve ser um número inteiro positivo")
        self.e_qt.delete(0, 'end')



    def fechar_janela(self):
        self.grab_release()
        self.destroy()
        pub.sendMessage("Close_Update_album")




class Mensagem(Toplevel):

    def __init__(self,iD):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
  
        self.grab_set()

        self.geometry("500x400")
        self.resizable(0, 0)
        self.title("Caixa de Mensagens")



        ## Variável auxiliar ##
        self.id_admin = iD

        ## Criar botões ##
        b_enviar = Button(self,text="  Enviar  ", command = self.enviar_msg)
        b_cancelar = Button(self,text="Cancelar", command = self.fechar_janela)

        ## Criar labels ##
        l_intro = Label(self, text="Escrever mensagem: ")
        l_assunto = Label(self, text="Assunto: ")
        l_conteudo = Label(self, text="Conteudo: ")


        ## Criar Input Texto ##
        self.var_assunto =  StringVar()
        self.e_assunto =  Entry(self, textvariable=self.var_assunto)
        self.e_assunto.configure(state='normal')
        

        ## Criar output de Texto ##
        self.corpo = Text(self, height=14, width=60)
        self.corpo.insert(END, "Escrever aqui...")
        self.corpo.configure(state='normal')
        

        ## Posicionamento ##
        l_intro.place(x = 20, y = 30)
        l_assunto.place(x = 20, y = 65)
        l_conteudo.place(x = 20, y = 95)
        self.e_assunto.place(x = 105, y = 63)
        self.corpo.place(x = 25, y = 125)
        b_enviar.place(x = 395, y = 350)
        b_cancelar.place(x = 325, y = 350)


    def enviar_msg(self):
        info_assunto = self.e_assunto.get()
        info_conteudo = self.corpo.get("1.0",END)

        if info_assunto and info_conteudo:
            id_msg = BD.inserir_msg(info_assunto, info_conteudo, datetime.datetime.now(), self.id_admin)
            if id_msg == -1:
                messagebox.showinfo("Aviso","A mensagem apresenta demasiados caracteres!")
                return
            BD.publicar_msg(id_msg)
            self.fechar_janela()
        else:
            messagebox.showinfo("Aviso","Deve preencher todos os parâmetros da mensagem!")
        

    def fechar_janela(self):
        self.grab_release()
        self.destroy()

    
class Saldo(Toplevel):

    def __init__(self):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.grab_set()

        self.geometry("350x400")
        self.resizable(0, 0)
        self.title("Alteração do Saldo")

        ## Variáveis auxiliares ##
        self.lista_cliente = []
        self.id_cliente = None
        self.saldo_cliente = None

        ## Criar botões ##
        b_atualizar = Button(self,text="  Update  ", command = self.atualiza_saldo, width=7)
        b_cancelar = Button(self,text="  Close  ", command = self.fechar_janela, width=7)

        ## Criar labels ##
        l_intro = Label(self, text="Atualizar o saldo do cliente: ")
        l_nome = Label(self, text="Nome: ")
        l_saldo = Label(self, text="Saldo: ")
        l_clientes = Label(self, text="Escolha um cliente da lista: ")

        ## Criar Input Texto ##
        self.var_nome =  StringVar()
        self.var_saldo =  StringVar()
        val_saldo = (self.register(self.validacao_saldo), '%s')
        inval_saldo = (self.register(self.invalidacao_saldo), '%s')
        
        self.e_nome =  Entry(self, textvariable=self.var_nome)
        self.e_saldo =  Entry(self, validate="focusout", validatecommand = val_saldo, invalidcommand = inval_saldo, textvariable=self.var_saldo)
        self.e_nome.configure(state='readonly')
        self.e_saldo.configure(state='readonly')

        ## Criar uma Listbox ##
        self.lib = Listbox(self, height=8, width=30)
        self.lib.bind('<<ListboxSelect>>', self.seleciona_cliente)

        ## Criar um Scrollbar ##
        scroll = Scrollbar(self)
        
         ## Criar conecção entre o scroll e o Listbox ##
        self.lib.configure(yscrollcommand = scroll.set)    
        scroll.configure(command = self.lib.yview)  

        ## Posicionamento ##
        l_intro.place(x = 15, y = 30)
        l_nome.place(x = 15, y = 70)
        l_saldo.place(x = 15, y = 100)
        l_clientes.place(x = 15, y = 150) 
        self.e_nome.place(x = 125, y = 70)
        self.e_saldo.place(x = 125, y = 100)
        self.lib.place(x = 15, y = 180) 
        scroll.place(x = 300, y = 180, height = 140) 
        b_atualizar.place(x = 240, y = 350)
        b_cancelar.place(x = 160, y = 350)

        self.listar_clientes()

        
    def listar_clientes(self):   
        self.id_cliente = None 
        self.saldo_cliente = None
        list_total = BD.view_tabela('cliente')
        self.lista_cliente = []
        self.lib.delete(0,END)
        self.e_nome.configure(state='normal')
        self.e_nome.delete(0, END)
        self.e_nome.configure(state='readonly')
        self.e_saldo.delete(0, END)

        i = 1
        aux = ''
        for iD, nome, _, _, _, saldo  in list_total: 
            self.lista_cliente.append([i, iD, nome, saldo]) 
            if saldo == 0:
                aux = 'SALDO NULO'
            elif saldo < 20:
                aux = 'SALDO BAIXO'
            else:
                aux = ''
            item = str(i) + " - " + nome + "        " + aux  
            self.lib.insert(END,item) 
            if aux:     
                self.lib.itemconfig(i-1, bg='red')
                self.lib.itemconfig(i-1, foreground="white")                        
            i+=1


    def seleciona_cliente(self,opcao):
        try:
            w = opcao.widget
            index_select = w.get(w.curselection())
            index_select = index_select.split(' - ')
            index_select = index_select[0]
            self.e_nome.configure(state='normal')
            self.e_saldo.configure(state='normal')
            
            for i in self.lista_cliente:
                if str(i[0]) == index_select:
                    self.id_cliente = i[1] 
                    self.saldo_cliente = i[3]
                    self.e_nome.delete(0, END)
                    self.e_saldo.delete(0, END)
                    self.e_nome.insert(END,i[2])
                    self.e_nome.configure(state='readonly')
                    self.e_saldo.insert(END,"{0:.2f} €".format(i[3]))
        except:
            pass

    def atualiza_saldo(self):

        saldo = self.var_saldo.get()

        saldo = self.validacao_saldo(saldo)

        if self.id_cliente and saldo: 
            if saldo != str(self.saldo_cliente):
                BD.inserir_saldo(saldo, self.id_cliente)
                messagebox.showinfo("Aviso","O saldo do cliente foi atualizado com sucesso!")
                self.listar_clientes()
            else:
                messagebox.showinfo("Aviso","Deve colocar a nova informação sobre o novo saldo do cliente!")
        else:
            messagebox.showinfo("Aviso","Deve primeiro selecionar um cliente para poder atualizar o seu saldo!")


    def validacao_saldo(self,item):
        if item == '':
            return item
        try:
            item = float(item)
        except:
            try:
                item = item.replace(" ", "")
                item = item.rstrip('€')
                item = float(item)
                return item
            except:
                return False
        
        if item < 0:
            return False

        return item
 

    def invalidacao_saldo(self,item):
        messagebox.showinfo("Aviso","Algo está errado com a informação do saldo. Este deve ser um número positivo")
        self.e_saldo.delete(0, 'end')

    def fechar_janela(self):
        self.grab_release()
        self.destroy()

    

class Estatistica(Toplevel):

    def __init__(self):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.grab_set()

        self.geometry("420x530")
        self.resizable(0, 0)
        self.title("Estatisticas do Negócio")


        ## Criar variáveis auxiliares ##
        self.total_clientes = None
        self.total_discos = None     
        self.total_stock = None  
        self.total_vendas = None
        self.total_genero = None
        self.total_msg = None
        self.top_3 = None

        ## Criar botões ##
        b_ok = Button(self,text="     Ok     ", command = self.fechar_janela)


        ## Criar labels ##
        l_vendas = Label(self, text="Total de vendas anual: ")
        l_n_clientes = Label(self, text="Número total de clientes: ")
        l_n_discos = Label(self, text="Número total de discos: ")
        l_stock = Label(self, text="Valor total em stock: ")
        l_intro_genero = Label(self, text="Número total de discos por género musical: ")
        l_intro_msg = Label(self, text="Percentagem de clientes que viram as mensagens enviadas (escolha uma das 10 mais recentes): ",wraplength=380)

        ## Criar Input Texto ##
        self.e_vendas =  Entry(self)
        self.e_n_clientes =  Entry(self)  
        self.e_n_discos =  Entry(self)  
        self.e_stock =  Entry(self)  
        self.e_genero =  Entry(self)  
        self.e_msg =  Entry(self)  


        ## Criar Menu de opçõe ##
        self.var_genero =  StringVar()
        self.var_genero.set("Escolha do genero")
        opcoes_g = BD.view_lista_genero()
        self.op_genero = OptionMenu(self, self.var_genero,*opcoes_g)
        self.op_genero.config(width=15)
        self.var_genero.trace("w",lambda *args: self.ativar_genero())

        self.var_msg =  StringVar()
        self.var_msg.set("Escolha da mensagem")
        opcoes_m = BD.view_list_msg()
        self.op_msg = OptionMenu(self, self.var_msg,*opcoes_m)
        self.op_msg.config(width=16)
        self.var_msg.trace("w",lambda *args: self.ativar_msg())

        ## Criar output de Texto ##
        top_3_info = Text(self, height=7, width=45)

        ## Criar um Scrollbar ##
        scroll = Scrollbar(self, orient="vertical")
        
         ## Criar conexão entre o scroll e o Listbox ##
        top_3_info.configure(yscrollcommand = scroll.set)    
        scroll.configure(command = top_3_info.yview) 

        ## Posicionamento ##
        l_vendas.place(x = 15, y = 35)
        l_n_clientes.place(x = 15, y = 65)
        l_n_discos.place(x = 15, y = 95)
        l_stock.place(x = 15, y = 125)
        l_intro_genero.place(x = 15, y = 170)
        l_intro_msg.place(x = 15, y = 235)
        self.e_vendas.place(x = 200, y = 35)
        self.e_n_clientes.place(x = 200, y = 65)
        self.e_n_discos.place(x = 200, y = 95)
        self.e_stock.place(x = 200, y = 125)
        self.op_genero.place(x = 15, y = 200)
        self.op_msg.place(x = 15, y = 285)
        self.e_genero.place(x = 200, y = 200) 
        self.e_msg.place(x = 200, y = 285)
        top_3_info.place(x = 35, y = 335)
        scroll.place(x = 370, y = 335, height=110)
        b_ok.place(x = 170 , y = 480)
        


        ## APRESENTAÇÃO DE TODA A INFORMAÇÃO ESTATISTICA ##
        self.e_genero.configure(state="readonly")
        self.e_msg.configure(state="readonly")
        self.calcular_info()
        self.e_vendas.insert(END,self.total_vendas)
        self.e_n_clientes.insert(END,self.total_clientes)
        self.e_n_discos.insert(END,self.total_discos)
        self.e_stock.insert(END,self.total_stock)   
        self.e_vendas.configure(state="readonly")
        self.e_n_clientes.configure(state="readonly")
        self.e_n_discos.configure(state="readonly")
        self.e_stock.configure(state="readonly")

        info = BD.top_3()
        texto = "OS TRÊS ALBUNS MAIS VENDIDOS: \n\n" 
        for item in info:
            titulo,grupo,qt = item
            texto = texto + "    -> " + titulo + ' - ' + grupo + "\n       TOTAL DE VENDAS: " + str(qt) + '\n\n'

        top_3_info.insert(END,texto)
        top_3_info.config(wrap=WORD)
        top_3_info.config(state=DISABLED)
        

    
    def calcular_info(self):
        now = datetime.datetime.now()
        ano = now.strftime("%Y")
        self.total_vendas = BD.total_vendas(ano) 
        self.total_stock = BD.valor_total_stock()
        self.total_discos = BD.total_discos()
        self.total_clientes = BD.total_clientes()

        if not(self.total_vendas):
            self.total_vendas = 0
        if not(self.total_stock):
            self.total_stock=0
        if not(self.total_discos):
            self.total_discos=0
        if not(self.total_clientes):
            self.total_clientes = 0

        self.total_vendas = "{0:.2f} €".format(self.total_vendas)
        self.total_stock = "{0:.2f} €".format(self.total_stock)


    def ativar_genero(self):
        self.e_genero.configure(state='normal')
        self.e_genero.delete(0,END)
        self.total_genero = BD.total_discos_genero(self.var_genero.get())
        if not(self.total_genero):
            self.total_genero = 0
        self.e_genero.insert(END,self.total_genero)
        self.e_genero.configure(state="readonly")



    def ativar_msg(self):
        self.e_msg.configure(state='normal')
        self.e_msg.delete(0,END)
        aux= BD.proporcao_msg(self.var_msg.get())
        if all(aux):
            self.total_msg = (aux[0]/aux[1])*100
            self.total_msg = "{0:.2f} %".format(self.total_msg)
        else:
            self.total_msg = '0 %'
        self.e_msg.insert(END,self.total_msg)
        self.e_msg.configure(state="readonly")


    def fechar_janela(self):
        self.grab_release()
        self.destroy()


class Historico_compras(Toplevel):

    def __init__(self, iD):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.grab_set()

        self.geometry("400x400")
        self.resizable(0, 0)
        self.title("Historico de Compras")


        ## Criar variáveis auxiliares ##
        self.total = BD.MontanteTotal_ComprasFeitas(iD)
        if not(self.total):
            self.total = 0
        self.valor_total = "{0:.2f} €".format(self.total) 
        self.id_cliente = iD

        ## Criar botões ##
        b_ok = Button(self,text="    Ok     ", command = self.fechar_janela)


        ## Criar labels ##
        l_valor_total = Label(self, text="Valor total gasto: ")

        ## Criar Input Texto ##
        self.e_valor_total =  Entry(self)
        self.e_valor_genero =  Entry(self)  

        ## Criar um Menu de opçõe ##
        self.var_genero =  StringVar()
        self.var_genero.set("Valor gasto por genero: ")
        opcoes_g = BD.view_lista_genero()
        self.op_genero = OptionMenu(self, self.var_genero,*opcoes_g)
        self.op_genero.config(width=17)
        self.var_genero.trace("w",lambda *args: self.ativar_genero())

        ## Criar output de Texto ##
        info = Text(self, height=15, width=45)

        ## Criar um Scrollbar ##
        scroll = Scrollbar(self, orient="vertical")
        
         ## Criar conexão entre o scroll e o Listbox ##
        info.configure(yscrollcommand = scroll.set)    
        scroll.configure(command = info.yview) 

        ## Posicionamento ##
        info.place(x = 30, y = 35)
        scroll.place(x = 365, y = 35, height=210)
        l_valor_total.place(x = 30, y = 290)
        self.e_valor_total.place(x = 220, y = 290, width=100)
        self.op_genero.place(x = 30, y = 320)
        self.e_valor_genero.place(x = 220, y = 320, width=100)
        b_ok.place(x = 170 , y = 360)
        

        ## APRESENTAÇÃO DA INFORMAÇÃO ##
        self.e_valor_genero.configure(state="readonly")
        self.e_valor_total.insert(END,self.valor_total)
        self.e_valor_total.configure(state="readonly")
        
        texto = "REGISTO DO SEU HISTÓRICO DE COMPRAS: \n______________________________________\n\n" 

        if self.total:
            for carrinho in BD.view_carrinhos_compras(self.id_cliente):
                texto = texto + "DATA DA COMPRA: " + carrinho[0].strftime("%Y-%m-%d %H:%M") + '\n\n'
                for artigo in BD.view_compras_por_carrinho(self.id_cliente,carrinho[1]):
                    texto = texto + "     -> Qt: " + str(artigo[1]) + ' - '+ artigo[0] + '\n'
                texto = texto + "\nTOTAL DE COMPRA: " + str(carrinho[2]) + "\n\n___________________________________________\n\n" 
        else:
            texto = texto + "  << o seu histórico está vazio! >>   \n\n"

        info.insert(END,texto)
        info.config(wrap=WORD)
        #info.config(state=DISABLED)


    def ativar_genero(self):
        self.e_valor_genero.configure(state='normal')
        self.e_valor_genero.delete(0,END)
        cod = BD.get_id('generos','cod_genero','designacao',self.var_genero.get())[0][0]
        self.total_genero = BD.MontateTotal_ComprasGenero(self.id_cliente,cod)
        if not(self.total_genero):
            self.total_genero = 0
        self.total_genero = "{0:.2f} €".format(self.total_genero)
        self.e_valor_genero.insert(END,self.total_genero)
        self.e_valor_genero.configure(state="readonly")


    def fechar_janela(self):
        self.grab_release()
        self.destroy()



class Mensagem_cliente(Toplevel):

    def __init__(self,m):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
  
        self.grab_set()

        self.geometry("460x380")
        self.resizable(0, 0)
        self.title("Mensagem")

        ## Variável auxiliar ##
        self.msg = m

        ## Criar botões ##
        b_ok = Button(self,text="    Ok     ", command = self.fechar_janela)

        ## Criar labels ##
        l_assunto = Label(self, text="ASSUNTO:  "+self.msg[1],wraplength=330)
        l_conteudo = Label(self, text="CONTEUDO: ")
        

        ## Criar output de Texto ##
        self.corpo = Text(self, height=12, width=55)
        self.corpo.insert(END, self.msg[2])
        self.corpo.config(wrap=WORD)
        self.corpo.config(state=DISABLED)

        ## Criar um Scrollbar ##
        self.scroll = Scrollbar(self, orient="vertical")
        
         ## Criar conecção entre o scroll e o Listbox ##
        self.corpo.configure(yscrollcommand = self.scroll.set)    
        self.scroll.configure(command = self.corpo.yview) 
        

        ## Posicionamento ##
        l_assunto.place(x = 20, y = 30)
        l_conteudo.place(x = 20, y = 95)
        self.corpo.place(x = 25, y = 125)
        self.scroll.place(x = 425, y = 125, height=190)
        b_ok.place(x = 190, y = 335)

        

    def fechar_janela(self):
        self.grab_release()
        self.destroy()



login = Tk()
login.title('Loja de Discos Vinil')
ws = login.winfo_screenwidth()
hs = login.winfo_screenheight()
x = (ws/2) - (425/2)
y = (hs/2) - (340/2)

login.geometry("425x340"+"+%d+%d" % (x, y))
login.resizable(0, 0)
           

App = Inicio(login)

login.mainloop() 








