
class MT:
    def __init__(self, arquivo):
        
        #inicia variaveis usadas pelo simulador
        self.opcoes=[]      #opções do usuário
        self.fita=[]        #fita da maquina
        self.cabeca=1       #posição do cabeçote
        self.cabecotes=['(',')']   #caracteres que representam o cabeçote
        self.verfArquivo=True  #verifica se a leitura do arquivo foi um sucesso
        self.blocos={}      #dicionario dos blocos, salva nome e transições
        self.transicoes=[]  #salva transições de cada bloco temporariamente
        self.keywords=['pare','retorne','*'] #palavras chaves do sistema

        cont=0
        verfBloco=0  #verifica se está lendo dentro de um bloco
        for linha in arquivo.splitlines(): #separa arquivo por linha
            cont+=1
            
            if len(linha) != 0: #se linha não for vazia

                if ';' in linha: #se existe comentario na linha
                                 
                    linha=linha.split(';')[0]#separa antes e depois do comentario

                comandos = linha.split() #separa comandos da linha

                if len(comandos)>0: #se linha não for vazia sem comentarios

                    if 'bloco' in comandos: #verifica inicio de bloco
                        
                        if verfBloco==0: #se não está dentro de um blooo
                            verfBloco=1  #muda verificador

                            if len(comandos[1])<=16:   #verifica sintaxe
                                nomeBloco=comandos[1]
                            else:
                                print(f'Erro de sintaxe: nome de bloco maior que o permitido, Linha: {cont}')
                                self.verfArquivo=False
                                return 

                            if nomeBloco in self.blocos.keys(): #não permite blocos com mesmo nome
                                print(f'Erro de sintaxe: nome de bloco repetido, Linha: {cont}')
                                self.verfArquivo=False
                                return 
                        
                            try: #verifica sintaxe
                                if comandos[2] in self.keywords or (int(comandos[2])<= 9999 and int(comandos[2])>=0):
                                    estIniBloco=int(comandos[2])
                            
                                else:
                                    print(f'Erro de sintaxe: número de estado maior que o permitido, Linha: {cont}')
                                    self.verfArquivo=False
                                    return
                            except:
                                print(f'ERRO de sintaxe: Estado não é número inteiro, Linha: {cont}')
                                self.verfArquivo=False
                                return
                        
                        else: #caso verfBloco == 1
                            print(f'Erro de sintaxe: abrindo bloco sem finalizar anterior, Linha: {cont}')
                            self.verfArquivo=False
                            return 
                    
                    elif 'fim' in comandos: #verifica fim de um bloco
                        
                        self.transicoes.append(estIniBloco) #salva estado inicial do bloco
                        self.blocos[nomeBloco]= self.transicoes.copy() #copia transições pro dicionario
                        verfBloco=0 #muda verificador
                        self.transicoes.clear() #limpa transições
                        nomeBloco='' #limpa variavel

                
                    elif verfBloco!=0: #se dentro do bloco, trata comandos

                        if len(comandos) <= 4: #chamadas de blocos
                            try:
                                
                                blocoDest=comandos[1] #nome do bloco de destino

                                if comandos[0] not in self.keywords: #trata estado atual para chamada da regra
                                    estAtual= int(comandos[0])
                                else:
                                    if comandos[0]=='*':
                                        estAtual=comandos[0]
                                    else:
                                        print(f'ERRO de sintaxe: palavra chave não pode ser atribuida a estado atual, Linha: {cont}')
                                        self.verfArquivo=False
                                        return
                                
                                if comandos[2] not in self.keywords: #trata estado de saida do bloco chamado
                                   estSaida=int(comandos[2])
                                else:
                                    if comandos[2]=='*':
                                        print(f'Erro de sintaxe: \'*\' não pode ser alocado em <estado inicial>, Linha: {cont}')
                                        self.verfArquivo=False
                                        return
                                    else: 
                                        estSaida=comandos[2]

                                if estSaida not in self.keywords and (estSaida > 9999 or estSaida<0):       #verifica número dos estados
                                    print(f'Erro de sintaxe: número de estado de saida invalido, Linha: {cont}')
                                    self.verfArquivo=False
                                    return 
                                
                                if estAtual not in self.keywords and (estAtual > 9999 or estAtual<0):     #verifica número dos estados
                                    print(f'Erro de sintaxe: número de estado atual invalido, Linha: {cont}')
                                    self.verfArquivo=False
                                    return 
                                
                                elif '!' in comandos: #verifica caso de breakpoint na linha
                                    self.transicoes.append((estAtual,blocoDest,estSaida,'!'))
                                else:
                                    self.transicoes.append((estAtual,blocoDest,estSaida))
                            
                            except:
                                print(f'ERRO de sintaxe: Estado não é número inteiro, Linha: {cont}')
                                self.verfArquivo=False
                                return
                                
                        else: #comandos normais
                            try:
                                
                                simboloAtual=comandos[1] #simbolo no cabeçote
                                novoSimbolo=comandos[3]  #simbolo que deve ser escrito
                                movimento=comandos[4]    #movimento que deve ser feito

                                if comandos[0] not in self.keywords: #trata estado atual para chamada da regra
                                    estAtual= int(comandos[0])
                                else:
                                    if comandos[0]=='*':
                                        estAtual=comandos[0]
                                    else:
                                        print(f'ERRO de sintaxe: palavra chave não pode ser atribuida a estado atual, Linha: {cont}')
                                        self.verfArquivo=False
                                        return
                                    
                                if comandos[5] not in self.keywords: #trata estado novo da maquina
                                    estNovo=int(comandos[5])
                                else:
                                    estNovo=comandos[5]

                                if estAtual not in self.keywords and (estAtual > 9999 or estAtual<0):    #verifica número dos estados
                                    print(f'Erro de sintaxe: número de estado atual invalido, Linha: {cont}')
                                    self.verfArquivo=False
                                    return 
 
                                if estNovo not in self.keywords and (estNovo > 9999 or estNovo<0):      #verifica número dos estados
                                    print(f'Erro de sintaxe: número de estado novo invalido, Linha: {cont}')
                                    self.verfArquivo=False
                                    return 
                                
                                if movimento != 'e' and movimento != 'd' and movimento != 'i':  #verifica possiveis movimentos
                                    print(f'Erro de sintaxe: movimento desconhecido, Linha: {cont}')
                                    self.verfArquivo=False
                                    return 
                                
                                intmovimento=MT.traduzMovimento(movimento) #função que traduz movimento para int
                                
                                if '!' in comandos:  #verifica caso de breakpoint na linha
                                    self.transicoes.append((estAtual,simboloAtual,novoSimbolo,intmovimento,estNovo,'!'))
                                else:
                                    self.transicoes.append((estAtual,simboloAtual,novoSimbolo,intmovimento,estNovo))
                                    
                            except:
                                print(f'ERRO de sintaxe: Estado não é número inteiro, Linha: {cont}')
                                self.verfArquivo=False
                                return
                        
                    else:
                        print(f'ERRO de sintaxe: Comandos fora de blocos, Linha: {cont}')
                        self.verfArquivo=False
                        return
                    
        if verfBloco==1:
            print(f'ERRO de sintaxe: Bloco não finalizado, Linha: {cont}')
            self.verfArquivo=False
            return
                                

        

    def traduzMovimento(movimento): #função que traduz movimento
        if movimento == 'e':
            movimento=-1
            
        elif movimento == 'i':
             movimento=0
             
        else:
             movimento=1         

        return movimento          
    

    def mudaCabecote(self,NovoCabecotes): #função que muda simbolos do cabeçote
        self.cabecotes.clear() #limpa simbolos padrões
        self.cabecotes=list(NovoCabecotes) #adiciona novos simbolos



    def criaFita(self,entrada): #função para criar fita, forma de lista
        entrada=list(entrada) #transforma entrada em lista
        
        self.fita.append('_') #adiciona _ no inicio
        self.fita.append(self.cabecotes[0]) #constrói cabeçote
        self.fita.append(entrada[0])  #simbolo no cabeçote
        self.fita.append(self.cabecotes[1])

        i=1
        while i < len(entrada): #termina de passar entrada para lista
            self.fita.append(entrada[i])
            i+=1
        
        self.fita.append('_') # adiciona _ no fim
        self.cabeca=2 #aponta posição da cabeça

    def imprimir_configuracao(self,blocoAtual, estAtual): #função para mostrar config da maquina

        estAtual=str(estAtual) #passa int para string

        if estAtual=='retorne': #muda palavra chave 'retorne' para encaixar na formatação, só no print
            estAtual='retr'

        fita_esquerda = ''.join(self.fita[:self.cabeca - 1])[-20:] #pega no máximo 20 espaços para esquerda do cabeçote 
        fita_direita = ''.join(self.fita[self.cabeca + 2:])[:20]   #pega no máximo 20 espaços para direita do cabeçote 
        cabecote = f"{self.fita[self.cabeca - 1] + self.fita[self.cabeca] + self.fita[self.cabeca + 1]}" #monta cabeçote
        
        #                 -add . antes do nome do bloco-        -formata número do estado 0000-    -add _ na esquerda da lista, se necessario-                             -add _ na direita da lista, se necessario-                -                                                
        configuracao = f"{'.'*(16-len(blocoAtual))}{blocoAtual}.{'0'*(4-len(estAtual))}{estAtual}: {'_' * (20 - len(fita_esquerda))}{fita_esquerda}{cabecote}{fita_direita}{'_' * (20 - len(fita_direita))}"
        print(configuracao) #printa

    
    def novaOpcao(self): #função para verificação de novas opções digitadas
        opcoes_validas=['-resume','-r','-verbose','-v','-step','-s'] #opções validas

        while 1: #enquanto não for valido
            self.opcoes.clear() #limpa opções antigas
            novaOpcao=input('Forneça opção (-r,-v,-s):')
            self.opcoes=novaOpcao.split() #separa opções digitadas

            if self.opcoes[0] in opcoes_validas and len(self.opcoes)<=2:   #verifica primeira posição, e maior caso posivel -s x
                if (self.opcoes[0] != '-s' or self.opcoes[0] !='-step') and len(self.opcoes)==1: #se não -s, então ou -r,ou -v , == 1
                    return
                elif (self.opcoes[0] == '-s' or self.opcoes[0] =='-step') and len(self.opcoes)==2: # se -s, então -s x == 2
                    try:
                        self.opcoes[1]=int(self.opcoes[1]) #trata número de passos
                        return 
                    except:
                        print('ERRO: Número de passos inválido')
                else:
                    print('ERRO: Opção inválida.')
            else:
                print('ERRO: Opção inválida.')
                            
            
                


    def moveCabecote(self,movimento): # função que move cabeçote
        if int(movimento) !=0: #se movimento 0 então nada acontece
            
            if self.cabeca==1 and int(movimento) == -1: #caso cabeçote esteja na primeira casa da fita e mova pra esquerda
                self.fita.insert(0,'_')     #cria casa para esquerda
                self.cabeca+=1              #acerta posição da cabeça

            elif self.cabeca == len(self.fita) -2 and int(movimento)== 1: #caso cabeçote esteja na última casa da fita e mova pra direita
                self.fita.append('_')  #cria casa para direita
        
            aux=list(self.fita[self.cabeca-1]) #cria copia do cabeçote da esquerda
            self.fita[self.cabeca-1]=self.fita[self.cabeca-1 + int(movimento)] #troca cabeçote da esquerda pela casa ao seu lado, de acordo com movimento
            self.fita[self.cabeca-1 + int(movimento)]=aux[0] #coloca cabeçote da esquerda na casa que foi movida
            
            aux=list(self.fita[self.cabeca+1]) #cria copia do cabeçote da direita
            self.fita[self.cabeca+1]=self.fita[self.cabeca+1 + int(movimento)] #troca cabeçote da direita pela casa casa ao seu lado, de acordo com movimento
            self.fita[self.cabeca+1 + int(movimento)]=aux[0] #coloca cabeçote da direita na casa que foi movida

            self.cabeca+=int(movimento) #anda posição da cabeça

            
    def programa(self, entrada): 

        MT.criaFita(self,entrada) #chama função que cria fita
        verfTransicao=False  # verifica se ocorreu alguma transição
        blocoAnterior=[]   #pilha de blocos percorridos
        estAnterior=[]     #pilha de estados para retornar
        blocoAtual='main'  #bloco atual da maquina, começa no main
        
        if blocoAtual not in self.blocos.keys(): #verifica existencia do bloco main
            print('Maquina não possui bloco main')
            return
       
        
        
        estAtual= self.blocos[blocoAtual][-1] #pega estado de inicio do bloco, sempre na ultima posição da lista de transições
        
        

        while 1:
            
            if '-verbose' in self.opcoes or '-v' in self.opcoes:   #imprime a cada loop
                MT.imprimir_configuracao(self,blocoAtual, estAtual) #função que imprime

            elif '-step' in self.opcoes or '-s'in self.opcoes:  #imprime de acordo com os passos
                MT.imprimir_configuracao(self,blocoAtual, estAtual) #função que imprime
                self.opcoes[1]=int(self.opcoes[1])-1 #diminui número de passos

                if self.opcoes[1] <= 0: #se passos == 0 chama função para nova opção
                    MT.novaOpcao(self) #função para nova opção

            
            if estAtual == 'pare':  #força parada no estado `pare`
                print('Maquina atingiu estado \'pare\'')
                break

            if estAtual=='retorne': # retorna para bloco anterior no estado `retorne`
                if len(blocoAnterior)<=0 or len(estAnterior)<=0: #se não existe bloco para retorno finaliza programa
                    print('Maquina parou, \'retorne\' para vazio')
                    break
                else:
                    estAtual=estAnterior[-1]  #pega ultimo estado
                    blocoAtual=blocoAnterior[-1] #pega ultimo bloco

                    estAnterior.pop(-1)  #remove eles das pilhas
                    blocoAnterior.pop(-1)
                    

            else: 
                simboloAtual= self.fita[self.cabeca]       #pega simbolo no cabeçote
                for transicao in self.blocos[blocoAtual]:  #for por todas transições do bloco
                    
                    if isinstance(transicao,int): # caso chegue na ultima transição, estado de inicio do bloco
                        break

                    elif len(transicao) <= 4: #chamadas de blocos           
                        if (transicao[0]==estAtual or transicao[0]=='*'): #verifica se estado da transição é compativel ou coringa
                            
                            if transicao[1] in self.blocos.keys():  #verifica se bloco chamado foi criado
                                
                                blocoAnterior.append(blocoAtual)  #adiciona bloco atual na pilha de retorno
                                estAnterior.append(transicao[2])  #adiciona estado de retorno na pilha de retorno
                                blocoAtual=transicao[1]     #muda bloco atual para o bloco da transição
                                estAtual= self.blocos[blocoAtual][-1]   #pega estado de inicio do bloco, sempre na ultima posição da lista de transições
                                verfTransicao=True  #marca transição realizada

                                if '!' in transicao:  #verificação de breakpoint
                                    self.opcoes.clear() 
                                    self.opcoes.append('-s') #substitui opções para -s 1 
                                    self.opcoes.append(1)    #dessa forma irá printar configuração da maquina e pedir nova opção

                                break
                            
                            else:
                                print('ERRO: chamada para bloco não criado')
                                return
                            
                    else: #regras normais
                        if (transicao[0]==estAtual or transicao[0]=='*') and (transicao[1] == simboloAtual or transicao[1]=='*'):
                            #verifica se estado e simbolo da transição é compativel ou coringa
                            
                            if(transicao[2]!='*'): #só muda simbolo se não for coringa
                                self.fita[self.cabeca]=transicao[2]
                            
                            if(transicao[4]!='*'): #só muda estado se não for coringa
                                estAtual=transicao[4]
                            
                            MT.moveCabecote(self,transicao[3]) #chama função para mover cabeçote
                            verfTransicao=True #marca transição realizada

                            if '!' in transicao: #verificação de breakpoint
                                    self.opcoes.clear()
                                    self.opcoes.append('-s')  #substitui opções para -s 1 
                                    self.opcoes.append(1)     #dessa forma irá printar configuração da maquina e pedir nova opção

                            break

                if  verfTransicao: #verifica se foi feita transição
                    verfTransicao=False #reinicia verificador
                else:
                    print('Maquina parou, nenhuma regra a ser seguida') #aponta parada

                    if self.opcoes[0] == '-r' or self.opcoes[0]== '-resume': #se opção -r imprime última configuração da maquina
                        MT.imprimir_configuracao(self,blocoAtual, estAtual)  
                    return
                

        if self.opcoes[0] == '-r' or self.opcoes[0]== '-resume': #se opção -r imprime última configuração da maquina
            MT.imprimir_configuracao(self,blocoAtual, estAtual)
            return