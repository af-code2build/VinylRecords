
import psycopg2
import datetime

class Database():

    ## CONSTRUTOR ##

    def __init__(self):
        self.conn = psycopg2.connect("dbname='BD' user='postgres' password='postgres' host='localhost'")
        self.curs = self.conn.cursor()

    ## REGISTO DE NOVOS CLIENTES E PORTA DE ENTRADA PARA AS PAGINAS DE ADMINISTRADOR E CLIENTE ##

    def insert_cliente(self, n, e, p, c):
        sql = """INSERT INTO cliente VALUES (nextval('utilizador_sequence'),%s, %s, %s, %s) RETURNING utilizador_id_utilizador;"""
        val = (n,e,p,c)
        self.curs.execute(sql,val)
        novo_id = self.curs.fetchall()[0][0]
        self.conn.commit()
        self.criar_carrinho(novo_id)


    def criar_carrinho(self, id_cliente):
        sql = """INSERT INTO carrinho(data_compra,montante_total,comprado, cliente_utilizador_id_utilizador) 
            VALUES(null,0,'false',%s) RETURNING cod_carrinho"""
        self.curs.execute(sql,(id_cliente,))
        self.conn.commit()
        novo_cod = self.curs.fetchall()[0][0]
        return novo_cod


    def verf_email(self, e):
        sql = """SELECT EXISTS(SELECT 1 FROM cliente WHERE utilizador_email = %s);"""
        val = (e,)
        self.curs.execute(sql,val)
        res = self.curs.fetchall()
        return res

    def verf_utilizador(self, utilizador, e, p):
        sql = "SELECT utilizador_id_utilizador, utilizador_nome FROM " + utilizador + " WHERE utilizador_email= %s and utilizador_password = %s"
        val = (e, p)
        self.curs.execute(sql,val)
        nome_utilizador = self.curs.fetchall()
        return nome_utilizador


    ## LISTAR OS ALBUNS E CLIENTES ##

    def view_tabela(self,tab):
        self.curs.execute("SELECT * from "+ tab +";")
        conteudo = self.curs.fetchall()
        return conteudo

    def view_albuns(self):
        self.curs.execute("SELECT * FROM album WHERE album.quantidade != 0 ORDER BY data_edicao desc")
        conteudo = self.curs.fetchall()
        return conteudo


    ## INSERIR ALBUNS NA PAGINA DO ADMINSTRADOR ##

    def insert_album(self, info_primaria, info_secundaria):

        self.verf_existe_e_inserir('generos','designacao',info_primaria[6])
        id_genero = self.get_id('generos','cod_genero','designacao',info_primaria[6])[0][0]

        sql1 = """ SELECT EXISTS(SELECT 1 FROM album WHERE UPPER(titulo) = %s and UPPER(grupo_artista)= %s and generos_cod_genero = %s) """
        sql2 = """ INSERT INTO album VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s) RETURNING id_album; """
        info_primaria = info_primaria[0:6] + (id_genero,)
        self.curs.execute(sql1,(info_primaria[0].upper(),info_primaria[2].upper(),info_primaria[6]))
        verif_album = self.curs.fetchall()[0][0]


        if verif_album:
            return False
            
        else:
            self.curs.execute(sql2,info_primaria)
            id_novo_album = self.curs.fetchall()[0][0]
            self.conn.commit()

            for item in info_secundaria:

                self.verf_existe_e_inserir('musicas', 'titulo', item[0])
                id_m = self.get_id('musicas','codigo_musica','titulo',item[0])[0][0]
                self.inserir_relacao('musicas_album',id_m,id_novo_album)

                if item[1]:
                    self.verf_existe_e_inserir('artista', 'nome', item[1])
                    id_a = self.get_id('artista','id_artista','nome',item[1])[0][0]
                    self.inserir_relacao('musicas_artista',id_m,id_a)

            return True


    def verf_existe_e_inserir(self, tab, coluna, valor):
        sql1 = "INSERT INTO "+tab+" ("+coluna+") SELECT %s WHERE NOT EXISTS (SELECT "+coluna+" FROM "+tab+" WHERE "+coluna+" = %s);"
        self.curs.execute(sql1,(valor,valor))
        self.conn.commit()


    def get_id(self,tab,id_tab,coluna,valor):
        sql1 = "SELECT "+id_tab+" FROM "+tab+" WHERE "+coluna+" = %s"
        self.curs.execute(sql1,(valor,))
        cod = self.curs.fetchall()
        return cod

    def inserir_relacao(self,tab, id_1, id_2):
        sql1 = "INSERT INTO "+tab+" SELECT %s, %s ON CONFLICT DO NOTHING"
        val = (id_1,id_2)
        self.curs.execute(sql1,val)
        self.conn.commit()



    ## REMOVER ALBUNS NA PAGINA DO ADMINSTRADOR ##

    def remover_album(self, id_album):

        if self.album_comprado(id_album):
            return False
        else:
            musicas = self.view_musicas(id_album)
            for musica in musicas:
                if self.n_albuns_por_musica(musica[1]):
                    artistas = self.view_artistas(musica[1])
                    for artista in artistas:
                        self.remover_relacao_musica_artista(musica[1], artista[1])
                    self.remover_relacao_musica_album(musica[1],id_album)
                    self.remover_musica(musica[1])
                else:
                    self.remover_relacao_musica_album(musica[1],id_album)

            sql1 = """ DELETE FROM updatepreco WHERE album_id_album = %s; DELETE FROM album WHERE id_album = %s;  """
            self.curs.execute(sql1,(id_album,id_album))
            self.conn.commit()

            return True


    def n_albuns_por_musica(self, id_musica):
        sql1 = """ SELECT count(*) FROM musicas_album WHERE musicas_codigo_musica = %s GROUP BY musicas_codigo_musica """
        self.curs.execute(sql1,(id_musica,))
        n = self.curs.fetchall()[0][0]
        if n > 1:
            return False   # não podes eliminar a musica
        else:
            return True    # podes eliminar a musica

    def album_comprado(self, id_album):
        sql1 = """ SELECT count(*) FROM album, artigo_carrinho, carrinho WHERE artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho
               and artigo_carrinho.album_id_album = album.id_album and album.id_album = %s and carrinho.comprado = true  """
        self.curs.execute(sql1,(id_album,))
        return bool(self.curs.fetchall()[0][0])


    def remover_relacao_musica_artista(self, id_musica, id_artista):
        sql1 = """ DELETE FROM musicas_artista WHERE musicas_codigo_musica= %s and artista_id_artista = %s;"""
        self.curs.execute(sql1,(id_musica,id_artista))
        self.conn.commit()


    def remover_relacao_musica_album(self, id_musica,id_album):
        sql1 = """ DELETE FROM musicas_album WHERE musicas_codigo_musica= %s and album_id_album = %s;  """
        self.curs.execute(sql1,(id_musica,id_album))
        self.conn.commit()


    def remover_musica(self, id_musica):
        sql1 = """ DELETE FROM musicas WHERE codigo_musica = %s;"""
        self.curs.execute(sql1,(id_musica,))
        self.conn.commit()



    ## UPDATE DAS INFORMAÇÕES DO ALBUM ##

    def view_preco(self, id_album):
        sql1 = """ SELECT preco FROM album WHERE id_album=%s """
        self.curs.execute(sql1,(id_album,))
        preco = self.curs.fetchall()[0][0]
        return preco

    def historico_preco(self, data, novo_preco, id_album,id_admin):
        sql1 = """ INSERT INTO updatepreco VALUES (DEFAULT, %s, %s, %s, %s); """
        self.curs.execute(sql1,(data,novo_preco,id_album,id_admin))

        self.conn.commit()

    def update_qt(self, nova_qt, id_album):
        sql1 = "UPDATE album SET quantidade=%s WHERE id_album = %s;"
        self.curs.execute(sql1,(nova_qt,id_album))

        self.conn.commit()

    def update_preco(self, novo_preco, id_album):
        sql1 = "UPDATE album SET preco=%s WHERE id_album = %s;"
        self.curs.execute(sql1,(novo_preco,id_album))

        self.conn.commit()


    ## OBTER INFORMAÇÃO SOBRE AS MUSICAS, ARTISTAS E GENERO MUSICAL ##

    def view_musicas(self, id_album):
        sql1 = """ SELECT musicas.titulo, musicas.codigo_musica FROM album, musicas_album, musicas WHERE musicas_album.musicas_codigo_musica = musicas.codigo_musica and
                    musicas_album.album_id_album = album.id_album and album.id_album = %s """

        self.curs.execute(sql1,(id_album,))
        musicas = self.curs.fetchall()
        return musicas


    def view_artistas(self, id_musica):
        sql1 = """ SELECT artista.nome, artista.id_artista FROM musicas, musicas_artista, artista WHERE musicas_artista.musicas_codigo_musica = musicas.codigo_musica and
                    musicas_artista.artista_id_artista = artista.id_artista and musicas.codigo_musica = %s """

        self.curs.execute(sql1,(id_musica,))
        artistas = self.curs.fetchall()
        return artistas


    def view_musicas_artistas(self, id_album):
        sql1 = """ SELECT musicas.titulo FROM album, musicas_album, musicas WHERE musicas_album.musicas_codigo_musica = musicas.codigo_musica and
                    musicas_album.album_id_album = album.id_album and album.id_album = %s """
        sql2 = """ SELECT musicas.titulo, artista.nome FROM album, musicas_album, musicas, musicas_artista, artista WHERE musicas_album.musicas_codigo_musica = musicas.codigo_musica and
                   musicas_album.album_id_album = album.id_album and musicas_artista.musicas_codigo_musica = musicas.codigo_musica and
                   musicas_artista.artista_id_artista = artista.id_artista and album.id_album = %s """

        self.curs.execute(sql1,(id_album,))
        musicas = self.curs.fetchall()
        self.curs.execute(sql2,(id_album,))
        artista_musica = self.curs.fetchall()
        return [musicas, artista_musica]


    def view_genero(self, cod):
        sql1 = """ SELECT designacao FROM generos WHERE cod_genero = %s """

        self.curs.execute(sql1,(cod,))
        conteudo = self.curs.fetchall()
        return conteudo


    ## VER HISTÓRICO DE PREÇOS ##

    def view_historico_preco(self,id_album):
        sql1 = "SELECT data_alteracao, valor_antigo FROM updatepreco WHERE album_id_album = %s ORDER BY data_alteracao ASC "
        self.curs.execute(sql1,(id_album,))
        historico = self.curs.fetchall()
        return historico


    ## INSERIR MENSAGEM ##

    def inserir_msg(self, assunto, conteudo, data, id_admin):
        try:
            sql1 = """ INSERT INTO mensagemadministrador VALUES (DEFAULT, %s, %s, %s, %s) RETURNING codigo_mensagem; """
            self.curs.execute(sql1,(assunto,conteudo,data,id_admin))
            cod = self.curs.fetchall()[0][0]
            self.conn.commit()
            return cod
        except:
            self.conn.rollback()
            return -1



    def publicar_msg(self,id_msg):
        sql1 = " SELECT utilizador_id_utilizador FROM cliente "
        sql2 = """ INSERT INTO mensagemcliente VALUES (false, %s, %s); """

        self.curs.execute(sql1)
        id_clientes = self.curs.fetchall()

        for cliente in id_clientes:
            self.curs.execute(sql2,(cliente[0],id_msg))
            self.conn.commit()


    ## INSERIR SALDO ##

    def inserir_saldo(self, saldo, id_cliente):
        sql1 = "UPDATE cliente SET saldo = %s WHERE utilizador_id_utilizador = %s"
        self.curs.execute(sql1,(saldo,id_cliente))
        self.conn.commit()

    ## CALCULAR ESTATISTICAS ##

    def total_vendas(self,ano):
        sql1 = "SELECT sum(montante_total) FROM carrinho WHERE comprado=true and data_compra >= to_date(%s,'yyyy')"
        self.curs.execute(sql1,(ano,))
        res = self.curs.fetchall()[0][0]
        return res
    
    def valor_total_stock(self):
        sql1 = "SELECT sum(quantidade*preco) FROM album"
        self.curs.execute(sql1)
        res = self.curs.fetchall()[0][0]
        return res

    def total_discos(self):
        sql1 = "SELECT sum(quantidade) FROM album"
        self.curs.execute(sql1)
        res = self.curs.fetchall()[0][0]
        return res
    
    def total_clientes(self):
        sql1 = "SELECT count(*) FROM cliente"
        self.curs.execute(sql1)
        res = self.curs.fetchall()[0][0]
        return res
    
    def total_discos_genero(self, genero):
        sql1 = "SELECT sum(album.quantidade) FROM album, generos WHERE album.generos_cod_genero=generos.cod_genero and designacao = %s"
        self.curs.execute(sql1,(genero,))
        res = self.curs.fetchall()[0][0]
        return res     


    def view_lista_genero(self):
        sql1 = "SELECT designacao FROM generos"
        self.curs.execute(sql1)
        res = self.curs.fetchall()
        res = tuple([i[0] for i in res])
        return res  

    def view_list_msg(self):   
        sql1 = "SELECT assunto FROM mensagemadministrador ORDER BY data_envio desc LIMIT 10"
        self.curs.execute(sql1)
        res = self.curs.fetchall()
        res = tuple([i[0] for i in res])
        return res   

    def proporcao_msg(self,assunto):  
        sql1 = """SELECT count(*)filter (where visualizada='true'), count(*) FROM cliente,mensagemcliente, mensagemadministrador 
                  WHERE mensagemcliente.cliente_utilizador_id_utilizador=cliente.utilizador_id_utilizador and
                  mensagemadministrador.codigo_mensagem = mensagemcliente.mensagemadministrador_codigo_mensagem and 
                  mensagemadministrador.assunto=%s"""
        self.curs.execute(sql1,(assunto,))
        res = self.curs.fetchall()[0] 
        return res

    def top_3(self): 
        sql1 = """ SELECT album.titulo,album.grupo_artista, sum(artigo_carrinho.quantidade) 
               FROM album, carrinho, artigo_carrinho WHERE artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho
               and album.id_album = artigo_carrinho.album_id_album and carrinho.comprado='true' 
               GROUP BY album.titulo, album.grupo_artista 
               ORDER BY sum(artigo_carrinho.quantidade) desc LIMIT 3"""
        self.curs.execute(sql1)
        res = self.curs.fetchall()
        return res

    ## OPERAÇÕES PARA O CARRINHO ##

    def cod_carrinho(self, id_cliente):
        sql1="""SELECT cod_carrinho FROM carrinho WHERE comprado = false and cliente_utilizador_id_utilizador =%s"""
        self.curs.execute(sql1, (id_cliente,))
        id_carrinho = self.curs.fetchall()[0][0]
        return id_carrinho

    def ver_artigosEmCarrinho(self,cod_carrinho):
        sql = """ SELECT album.id_album, album.titulo, album.grupo_artista, album.data_edicao, album.preco, artigo_carrinho.quantidade, carrinho.montante_total 
                  FROM carrinho, artigo_carrinho, album WHERE carrinho.cod_carrinho=%s
                  and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album"""
        self.curs.execute(sql, (cod_carrinho,))
        conteudo = self.curs.fetchall()
        return conteudo

    def inserir_albumEmCarrinho(self,cod_carrinho, id_album, quantidade):
        sql = """SELECT quantidade FROM album WHERE id_album=%s """
        val=(id_album,)
        self.curs.execute(sql, val)
        n_albuns = self.curs.fetchall()[0][0]

        aux=int(quantidade)
        if int(n_albuns) >= aux:
            self.curs.execute("SELECT insere_artigo_carrinho(%s,%s,%s); ", (cod_carrinho, id_album, quantidade))
            res, = self.curs.fetchall()
            self.conn.commit()
            
            if not(res):
                return 0
            else:
                return(res[0])
        else:
            return (-1)  ##Nada foi inserido!

    def eliminar_albumEmCarrinho(self,cod_carrinho, id_album, preco_album, quantidade):

        valor = preco_album * quantidade

        ##Eliminar album no Carrinho##
        sql3 = """DELETE FROM artigo_carrinho WHERE carrinho_cod_carrinho=%s and album_id_album=%s"""
        val3 = (cod_carrinho, id_album)
        self.curs.execute(sql3, val3)
        self.conn.commit()

        ##Retorna o valor do montante atual do carrinho ##
        sql5 = """SELECT carrinho.montante_total FROM carrinho, album, artigo_carrinho WHERE carrinho.cod_carrinho=%s 
                and album.id_album=artigo_carrinho.album_id_album and artigo_carrinho.carrinho_cod_carrinho=carrinho.cod_carrinho; """
        self.curs.execute(sql5, (cod_carrinho,))
        res = self.curs.fetchall()
        if  res == []:
            res = 0
        else:
            res = res[0][0]

        montante = res - valor

        if montante <= 0:
            montante = 0

        ##Atualizar o montante_total do carrinho e devolve-lo##
        sql4 = """UPDATE carrinho SET montante_total = %s WHERE cod_carrinho = %s"""
        val4 = (montante, cod_carrinho)
        self.curs.execute(sql4, val4)
        self.conn.commit()

        ##Retorna o valor do montante final do carrinho (para ser mostrado a cada operação) ##
        sql5 = """SELECT carrinho.montante_total FROM carrinho, album, artigo_carrinho WHERE carrinho.cod_carrinho=%s 
                and album.id_album=artigo_carrinho.album_id_album and artigo_carrinho.carrinho_cod_carrinho=carrinho.cod_carrinho; """
        self.curs.execute(sql5, (cod_carrinho,))
        res = self.curs.fetchall()

        if res == []:
            return 0

        res = res[0][0]
        return (res)

    ## HISTORICO DE COMPRAS DO CLIENTE ##

    def MontanteTotal_ComprasFeitas(self,id_cliente):
        sql1="""SELECT SUM(carrinho.montante_total) FROM cliente, carrinho WHERE carrinho.comprado=true and 
            carrinho.cliente_utilizador_id_utilizador=cliente.utilizador_id_utilizador and cliente.utilizador_id_utilizador=%s"""
        self.curs.execute(sql1, (id_cliente,))
        conteudo = self.curs.fetchall()
        if conteudo == []:
            return 0
        else:
            return conteudo[0][0]

    def view_compras_por_carrinho(self,id_cliente, cod_carrinho):
        sql="""SELECT album.titulo, artigo_carrinho.quantidade FROM carrinho, artigo_carrinho, album 
            WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador = %s 
            and artigo_carrinho.carrinho_cod_carrinho = %s and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho 
            and album.id_album = artigo_carrinho.album_id_album"""
        self.curs.execute(sql, (id_cliente,cod_carrinho))
        conteudo = self.curs.fetchall()
        return conteudo

    def view_carrinhos_compras(self,id_cliente):
        sql="""SELECT carrinho.data_compra, artigo_carrinho.carrinho_cod_carrinho, carrinho.montante_total FROM carrinho, artigo_carrinho, album 
            WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador = %s 
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album
            GROUP BY artigo_carrinho.carrinho_cod_carrinho, carrinho.data_compra, carrinho.montante_total
            ORDER BY carrinho.data_compra DESC"""
        self.curs.execute(sql, (id_cliente,))
        conteudo = self.curs.fetchall()
        return conteudo

    def MontateTotal_ComprasGenero(self,id_cliente,cod_genero):

        sql = """SELECT SUM(artigo_carrinho.quantidade *artigo_carrinho.preco) FROM carrinho, artigo_carrinho, album, generos WHERE carrinho.comprado = true and 
            carrinho.cliente_utilizador_id_utilizador = %s and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album
            and generos.cod_genero=album.generos_cod_genero and generos.cod_genero= %s """
        self.curs.execute(sql, (id_cliente,cod_genero))
        return self.curs.fetchall()[0][0]


    ## CAIXA DE MENSAGENS DO CLIENTE ##

    def caixa_mensagens(self,id_cliente):
        sql="""SELECT mensagemadministrador.assunto, mensagemadministrador.conteudo, mensagemadministrador.data_envio, 
        mensagemcliente.visualizada, mensagemadministrador.codigo_mensagem FROM mensagemcliente, mensagemadministrador
        WHERE mensagemcliente.cliente_utilizador_id_utilizador = %s and 
        mensagemcliente.mensagemadministrador_codigo_mensagem = mensagemadministrador.codigo_mensagem
        ORDER BY mensagemadministrador.data_envio DESC"""
        self.curs.execute(sql, (id_cliente,))
        conteudo=self.curs.fetchall()
        return conteudo

    def mensagem_visualizada(self,id_cliente, cod_mensagem):
        sql="""UPDATE mensagemcliente SET visualizada = true WHERE mensagemcliente.cliente_utilizador_id_utilizador = %s and 
        mensagemcliente.mensagemadministrador_codigo_mensagem = %s"""
        val=(id_cliente, cod_mensagem)
        self.curs.execute(sql,val)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


    ## FINALIZAR COMPRA ##

    def finalizarCompra(self,id_cliente, cod_carrinho): 

        sql= "SELECT comprado FROM carrinho WHERE cod_carrinho=%s"
        self.curs.execute(sql, (cod_carrinho,))
        estado = self.curs.fetchall()[0][0]

        if estado==True:
            return 0  #Carrinho já comprado

        else:
            sql1="SELECT saldo FROM cliente WHERE utilizador_id_utilizador=%s"
            self.curs.execute(sql1,(id_cliente,))
            saldo_inicial = self.curs.fetchall()[0][0]

            sql2 = "SELECT montante_total FROM carrinho WHERE cod_carrinho=%s"
            self.curs.execute(sql2, (cod_carrinho,))
            montante = self.curs.fetchall()[0][0]

            if saldo_inicial >= montante:
                try:
                    sql3="UPDATE cliente SET saldo = saldo - %s WHERE  utilizador_id_utilizador=%s "
                    self.curs.execute(sql3, (montante, id_cliente))
                    sql4="UPDATE carrinho SET comprado = true, data_compra=%s WHERE cod_carrinho=%s "
                    self.curs.execute(sql4, (datetime.datetime.now(),cod_carrinho))

                    self.update_quantidadeAlbuns(cod_carrinho)
                    sql4 = "SELECT saldo FROM cliente WHERE utilizador_id_utilizador=%s "
                    self.curs.execute(sql4, (id_cliente,))
                    saldo_final = self.curs.fetchall()[0][0]

                    novo_carrinho = self.criar_carrinho(id_cliente)
                    return [saldo_final, novo_carrinho]

                except psycopg2.DatabaseError as err:
                    self.conn.rollback()
                    return 0 #Erro         

            else:
                return(-1) #Sem saldo suficiente


    def update_quantidadeAlbuns(self,cod_carrinho):

        sql = """ SELECT album.id_album, artigo_carrinho.quantidade FROM carrinho, artigo_carrinho, album WHERE carrinho.cod_carrinho=%s
        and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album ORDER BY album.id_album"""
        self.curs.execute(sql, (cod_carrinho,))
        conteudo = self.curs.fetchall()

        for t in conteudo:
            id_album = t[0]
            quantidade_carrinho=t[1]
            sql1 = """UPDATE album SET quantidade=quantidade - %s WHERE id_album=%s"""
            val = (quantidade_carrinho,id_album)
            self.curs.execute(sql1, val)



     ## PESQUISAS DO CLIENTE ##

    ## Pesquisa de todos os Albuns

    def view_all(self,colunas, ordem):
        if ordem == 'Ordem Crescente':
            self.curs.execute("SELECT "+ colunas +" FROM album WHERE album.quantidade != 0 ORDER BY data_edicao ASC")
        else:
            self.curs.execute("SELECT "+ colunas +" FROM album WHERE album.quantidade != 0 ORDER BY data_edicao DESC")
        conteudo = self.curs.fetchall()
        return conteudo

    def view_allCompras(self,colunas, ordem, id_cliente):
        if ordem == 'Ordem Crescente':
            sql = """SELECT DISTINCT ON (album.titulo, album.data_edicao) """+ colunas +""" FROM carrinho, artigo_carrinho, album 
                   WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador= """ + str(id_cliente) + """ 
                   and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album 
                   ORDER BY album.data_edicao ASC """
        else:
            sql = """SELECT DISTINCT ON (album.titulo, album.data_edicao) """+ colunas +""" FROM carrinho, artigo_carrinho, album 
                   WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador= """ + str(id_cliente) + """ 
                   and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album 
                   ORDER BY album.data_edicao DESC """
        self.curs.execute(sql)
        return(self.curs.fetchall())


    ## Pesquisa por nome do Album
    def pesquisar_PorTitulo(self,colunas, input_cliente, ordem):
        if ordem == 'Ordem Crescente':
            sql = "SELECT "+ colunas +" FROM album WHERE album.quantidade != 0 and UPPER(titulo) LIKE '%" +input_cliente+ "%' ORDER BY titulo ASC"

        else:
            sql="SELECT "+ colunas +" FROM album WHERE album.quantidade != 0 and UPPER(titulo) LIKE '%" +input_cliente+ "%' ORDER BY titulo DESC"

        self.curs.execute(sql)
        conteudo=self.curs.fetchall()
        return(conteudo)


    def pesquisar_ComprasFeitasPorTitulo(self,colunas, input_cliente, ordem, id_cliente):
        if ordem == 'Ordem Crescente':
            sql = """SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM carrinho, artigo_carrinho, album WHERE carrinho.comprado = true 
                  and carrinho.cliente_utilizador_id_utilizador= """ + str(id_cliente) + """ and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho 
                  and album.id_album = artigo_carrinho.album_id_album and UPPER(album.titulo) LIKE '%""" + input_cliente + "%' ORDER BY album.titulo ASC"

        else:
            sql="""SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM carrinho, artigo_carrinho, album WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador= """ + str(id_cliente) + """ 
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album and UPPER(album.titulo) LIKE '%""" + input_cliente + "%' ORDER BY album.titulo DESC"

        self.curs.execute(sql)
        return(self.curs.fetchall())

    ## Pesquisa por género
    def pesquisar_PorGenero(self,colunas, input_cliente, ordem):
        if ordem == 'Ordem Crescente':
            sql = """SELECT """+ colunas +""" FROM album, generos WHERE album.quantidade != 0 and album.generos_cod_genero = generos.cod_genero and 
            UPPER(generos.designacao) LIKE '%"""+input_cliente+ """%' ORDER BY album.titulo ASC"""
        else:
            sql = """SELECT """+ colunas +""" FROM album, generos WHERE album.quantidade != 0 and album.generos_cod_genero = generos.cod_genero and 
            UPPER(generos.designacao) LIKE '%"""+input_cliente+ """%' ORDER BY album.titulo DESC"""

        self.curs.execute(sql)
        conteudo=self.curs.fetchall()
        return(conteudo)

    def pesquisar_ComprasFeitasPorGenero(self,colunas, input_cliente, ordem, id_cliente):
        if ordem == 'Ordem Crescente':
            sql = """SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM carrinho, artigo_carrinho, album,generos WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador = """ + str(id_cliente) + """
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album and
            album.generos_cod_genero = generos.cod_genero and UPPER(generos.designacao) LIKE '%"""+input_cliente+"""%' ORDER BY album.titulo ASC"""
        else:
            sql = """SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM carrinho, artigo_carrinho, album,generos WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador = """ + str(id_cliente) + """
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album and
            album.generos_cod_genero = generos.cod_genero and UPPER(generos.designacao) LIKE '%"""+input_cliente+"%' ORDER BY album.titulo DESC"

        self.curs.execute(sql)
        conteudo=self.curs.fetchall()
        return(conteudo)

    ## Pesquisa por Artista
    def pesquisar_PorArtistaDoAlbum(self,colunas, input_cliente, ordem):
        if ordem == 'Ordem Crescente':
            sql="SELECT "+ colunas +" FROM album WHERE album.quantidade != 0 and UPPER(grupo_artista) LIKE '%"+input_cliente+"%' ORDER BY album.titulo ASC"
        else:
            sql = "SELECT "+ colunas +" FROM album WHERE album.quantidade != 0 and UPPER(grupo_artista) LIKE '%"+input_cliente+"%' ORDER BY album.titulo DESC"

        self.curs.execute(sql)
        conteudo = self.curs.fetchall()
        return (conteudo)

    def pesquisar_PorArtistaColaboracao(self,colunas, input_cliente, ordem):
        if ordem == 'Ordem Crescente':
            sql = """SELECT DISTINCT ON (album.titulo)"""+ colunas +""" FROM album,artista, musicas_artista, musicas_album WHERE album.quantidade != 0 and musicas_artista.artista_id_artista=artista.id_artista and 
            musicas_artista.musicas_codigo_musica=musicas_album.musicas_codigo_musica and album.id_album=musicas_album.album_id_album and UPPER(artista.nome) LIKE '%"""+input_cliente+"""%'
            ORDER BY album.titulo ASC"""
        else:
            sql = """SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM album,artista, musicas_artista, musicas_album WHERE album.quantidade != 0 and musicas_artista.artista_id_artista=artista.id_artista and 
            musicas_artista.musicas_codigo_musica=musicas_album.musicas_codigo_musica and album.id_album=musicas_album.album_id_album and UPPER(artista.nome) LIKE '%"""+input_cliente+"""%'
            ORDER BY album.titulo DESC"""

        self.curs.execute(sql)
        conteudo = self.curs.fetchall()
        return (conteudo)

    def pesquisar_ComprasFeitasPorArtistaDoAlbum(self,colunas, input_cliente, ordem, id_cliente):
        if ordem == 'Ordem Crescente':
            sql= """SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM carrinho, artigo_carrinho, album WHERE carrinho.comprado = true and 
            carrinho.cliente_utilizador_id_utilizador ="""+ str(id_cliente) + """ and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and 
            album.id_album = artigo_carrinho.album_id_album and UPPER(grupo_artista) LIKE '%"""+input_cliente+"""%' ORDER BY album.titulo ASC"""
        else:
            sql = """SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM carrinho, artigo_carrinho, album WHERE carrinho.comprado = true and 
            carrinho.cliente_utilizador_id_utilizador ="""+ str(id_cliente) + """ and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and 
            album.id_album = artigo_carrinho.album_id_album and UPPER(grupo_artista) LIKE '%"""+input_cliente+"""%' ORDER BY album.titulo DESC"""

        self.curs.execute(sql)
        conteudo = self.curs.fetchall()
        return (conteudo)

    def pesquisar_ComprasFeitasPorArtistaColaboracao(self,colunas, input_cliente, ordem, id_cliente):
        if ordem == 'Ordem Crescente':
            sql="""SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM album,artista, musicas_artista, musicas_album, carrinho, artigo_carrinho WHERE 
            musicas_artista.artista_id_artista=artista.id_artista and musicas_artista.musicas_codigo_musica=musicas_album.musicas_codigo_musica and 
            album.id_album=musicas_album.album_id_album and carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador ="""+str(id_cliente)+"""
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album and UPPER(artista.nome) LIKE '%"""+input_cliente+"""%'
            ORDER BY album.titulo ASC"""
        else:
            sql ="""SELECT DISTINCT ON (album.titulo) """+ colunas +"""  FROM album,artista, musicas_artista, musicas_album, carrinho, artigo_carrinho WHERE 
            musicas_artista.artista_id_artista=artista.id_artista and musicas_artista.musicas_codigo_musica=musicas_album.musicas_codigo_musica and 
            album.id_album=musicas_album.album_id_album and carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador ="""+str(id_cliente)+"""
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album and UPPER(artista.nome) LIKE '%"""+input_cliente+"""%'
            ORDER BY album.titulo DESC"""

        self.curs.execute(sql)
        conteudo = self.curs.fetchall()
        return (conteudo)

    ## Pesquisa por musica
    def pesquisar_PorMusica(self, colunas, input_cliente, ordem):
        if ordem == 'Ordem Crescente':
            sql = """SELECT DISTINCT ON (album.titulo)  """+ colunas +"""  FROM album, musicas, musicas_album WHERE album.quantidade != 0 and musicas_album.musicas_codigo_musica = musicas.codigo_musica 
            and musicas_album.album_id_album = album.id_album and UPPER(musicas.titulo) LIKE '%"""+input_cliente+"""%' ORDER BY album.titulo ASC"""
        else:
            sql = """SELECT DISTINCT ON (album.titulo)  """+ colunas +"""  FROM album, musicas, musicas_album WHERE album.quantidade != 0 and musicas_album.musicas_codigo_musica = musicas.codigo_musica 
            and musicas_album.album_id_album = album.id_album and UPPER(musicas.titulo) LIKE '%"""+input_cliente+"""%' ORDER BY album.titulo DESC"""

        self.curs.execute(sql)
        conteudo = self.curs.fetchall()
        return(conteudo)

    def pesquisar_ComprasFeitasPorMusica(self,colunas, input_cliente, ordem, id_cliente):
        if ordem == 'Ordem Crescente':
            sql = """SELECT DISTINCT ON (album.titulo) """+ colunas +""" FROM album, musicas, musicas_album,carrinho,artigo_carrinho WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador =""" + str(id_cliente) + """
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album and
            musicas_album.musicas_codigo_musica = musicas.codigo_musica and musicas_album.album_id_album = album.id_album and UPPER(musicas.titulo) LIKE '%"""+input_cliente+"""%' ORDER BY album.titulo ASC"""
        else:
            sql = """SELECT DISTINCT ON (album.titulo) """+ colunas +"""  FROM album, musicas, musicas_album,carrinho,artigo_carrinho WHERE carrinho.comprado = true and carrinho.cliente_utilizador_id_utilizador = """ + str(id_cliente) + """
            and artigo_carrinho.carrinho_cod_carrinho = carrinho.cod_carrinho and album.id_album = artigo_carrinho.album_id_album and
            musicas_album.musicas_codigo_musica = musicas.codigo_musica and musicas_album.album_id_album = album.id_album and UPPER(musicas.titulo) LIKE '%"""+input_cliente+"""%' ORDER BY album.titulo DESC"""

        self.curs.execute(sql)
        conteudo=self.curs.fetchall()
        return(conteudo)




d = Database()



"""

    def update_album(self, info, iD):
        sql1 = "INSERT INTO generos(designacao) SELECT %s WHERE NOT EXISTS (SELECT designacao FROM generos WHERE designacao = %s);"
        sql2 = "SELECT cod_genero FROM generos WHERE designacao = %s"
        sql3 = "UPDATE album SET titulo=%s, descricao=%s,grupo_artista=%s,data_edicao=%s,quantidade=%s,preco=%s,generos_cod_genero=%s WHERE id_album = %s;"

        self.curs.execute(sql1,(info[6],info[6]))
        self.curs.execute(sql2,(info[6],))
        aux = info[0:6] + (self.curs.fetchall()[0][0],iD)
        self.curs.execute(sql3,aux)

        self.conn.commit()




"""