import Maquina

def verificar_opcoes(opcoes):

    opcoes_validas=['-resume','-r','-verbose','-v','-step','-s','-head','-h']

    # Verifica se apenas uma das opções -r, -s, -v ,-h foi fornecida
    r_option = False
    s_option = False
    v_option = False
    h_option = False
    cancelaVerf=False #usado para pular verificação de complemento ex: -s 7 -h <>, pula verificação do 7 e do <>

    for opcao in opcoes:

        if cancelaVerf:
            cancelaVerf=False

        elif opcao in ("-r", "-resume"):  
            if r_option: #caso -r ja tenha sido lida,  mostra erro
                print('ERRO: opções repetidas')
                return False
            r_option = True

        elif opcao in ("-s", "-step"):
            if s_option: #caso -s ja tenha sido lida,  mostra erro
                print('ERRO: opções repetidas')
                return False
            s_option = True

            # Verifica se o próximo elemento existe e segue a sintaxe
            index = opcoes.index(opcao)
            if index + 1 >= len(opcoes) or opcoes[index + 1] in opcoes_validas:
                print('ERRO: Número de passos inválido')
                return False
            else:
                try: #trata elemento e cancela proxima verificação
                    opcoes[index + 1] = int(opcoes[index + 1])
                    cancelaVerf=True
                except:
                    print('ERRO: ao converter passos em um inteiro')
                    return False

        elif opcao in ("-v", "-verbose"):
            if v_option: #caso -v ja tenha sido lida,  mostra erro
                print('ERRO: opções repetidas')
                return False
            v_option = True

        elif opcao in ("-h", "-head"):
            if h_option: #caso -h ja tenha sido lida,  mostra erro
                print('ERRO: opções repetidas')
                return False
            h_option = True

            # Verifica se o próximo elemento existe e segue a sintaxe
            index = opcoes.index(opcao)
            if index + 1 >= len(opcoes) or opcoes[index + 1] in opcoes_validas or len(opcoes[index+1])!=2:
                print('ERRO: Configuração de cabeçotes inválida')
                return False
            else:  #cancela proxima verificação
                cancelaVerf=True

        
        else: #caso string verificada não faça parte de opções validas retorna False
            print('ERRO: Opção inválida digitada')
            return False

    if sum([r_option, s_option, v_option]) > 1: #verifica se passaram mais uma opção de execução foi passada
        print('ERRO: Mais de um tipo de opção de execução digitada')
        return False
    
    if sum([r_option, s_option, v_option]) < 1: #verifica se não passaram uma opção de execução 
        print('ERRO: Nenhuma opção de execução')
        return False

    return True

if __name__ == '__main__':

    while 1:

        prompt = input("prompt>") #entrada do usuário

        if prompt=='exit':
            break

        modulos = prompt.split() #separa argumentos passados em Lista
    
        if modulos[0] == 'simturing': #verifica comando

            nomeArquivo=modulos[-1] #pega nome do arquivo, sempre na ultima posição
            modulos.remove('simturing')  #remove argumentos inuteis futuramente
            modulos.remove(nomeArquivo)  #comandos contém apenas as opções agora

            try:
                arquivo = open( nomeArquivo+'.txt').read() #lê arquivo
                mt=Maquina.MT(arquivo)  #chama função para tratar arquivo
            

                if mt.verfArquivo:  #se leitura foi um sucesso
                    if verificar_opcoes(modulos): #chama função para verificar opções passadas

                        if len(modulos)>2: #se lista de opções é maior que 2, obrigatoriamente existe -h na lista
                            i=0
                            while i < len(modulos): #trata -head
                                if modulos[i] =='-head' or modulos[i]=='-h':
                                    mt.mudaCabecote(modulos[i+1]) #chama função para alterar cabeçotes
                                    modulos.pop(i+1) #remove -h da lista de opções
                                    modulos.pop(i)   #remove complemento          
                                    break
                                i+=1
                        
                        mt.opcoes=modulos.copy() #copia lista de opções para opções da maquina

                        
                        print('Simulador de Máquina de Turing ver 1.0 − IFMG 2023')
                        print('Desenvolvido como trabalho prático para a disciplina de Teoria da Computação')
                        print('Autores : Thomas Santos Pollarini & Jean Claudio \n')
                            
                        entrada=input('Forneça a palavra inicial:')  #pede fita de entrada da maquina
                        mt.programa(entrada)  #chama função que roda maquina de Turing
            
            except:
                print('ERRO: Arquivo inválido')
            
        else:
            print('Erro de sintaxe, simturing expected')




