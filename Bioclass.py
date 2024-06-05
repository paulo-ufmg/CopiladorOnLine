# Trabalho.
#
# Este arquivo faz parte do trabalho da disciplina de Ambintes de Computação do dpto de 
# pós graduação da Ciência da Computação da  UFMG
import importlib.util
import re
import sys

class Bioprof:
    """Bioprof - Trabalho da disciplina de Ambientes de Computação DCC-PPGCC.UFMG(2024)
    Leitura de arquivo de sequencia .FASTA e manipulação de sequências
    Disciplina: Ambientes de Computação
    Local: UFMG, 2024
    Professor:  Diego .
    Alunos:
     - Fredy Ernesto Villena Patiño (fredyvp@ufmg.br)
     - Paulo Rocha (paulo-rocha@ufmg.br)
     - Rodrigo Jereissati Martins (rod.jereissati@gmail.com)

    Link do github: https://github.com/paulo-ufmg/Bioprof
    """
    
    def __init__(self):
       self.__version__ = "0.05"
       self.id = "" #string que contém o nome(identificação da sequencia)
       self.ids = [] #Lista de id's das sequências referenciadas pelo index da lista
       self.info ={} #Dicionario que armazena um comentario da sequência
       self.composicao_DNA_RNA_PROTEINA = {} #nucleotideos ou aminoácidos presente na sequencia DNA-RNA ou de Proteina
       #self.nucleotideo = {} #nucleotideos ou aminoácidos presente na sequencia DNA-RNA ou de Proteina
       self.composicao_total = [] #Totalização de nucleotídeos na sequencia  {"C":0,"G":0,"T":0,"U":0}
       self.sequencia = [] # Lista de string contendo a sequencia de DNA,RNA ou Proteina
       self.alerta = True
       self.codons = {
            "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L","CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L","AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M","GUU": "V",
            "GUC": "V", "GUA": "V", "GUG": "V","UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S","CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P","ACU": "T", "ACC": "T",
            "ACA": "T", "ACG": "T","GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A","UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*","CAU": "H", "CAC": "H", "CAA": "Q",
            "CAG": "Q","AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K","GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E","UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",
            "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R","AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R","GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"           
        }
       self.aux_chaining = "" #usando para armazenar sequencia em utilização de métodos em cascata

    def verificar_biblioteca(self,biblioteca):
        if importlib.util.find_spec(biblioteca) is None:
            print(f"A biblioteca '{biblioteca}' não está instalada.")
            print(f"Por favor, instale-a usando: pip install {biblioteca}")
            return False
        return True

    def message_view(self,mensagem,interrupt=False):
        """Exibir mensagem de alerta"""
        if(self.alerta): print(mensagem)
        if(interrupt): exit()        
        

    def seq_existe (self,arg):
       """Retorna verdadeiro se a sequencia identificada em argumento está registrada"""
       if(isinstance(arg, int)): return True if 0 <= arg < len(self.ids) else False #procura por um indice presente na Lista de identificação de sequencias (ids)
       else: return True if(arg in self.ids) else False  #procura pela identificação da sequencia na Lista de identificação de sequencias (ids)
    
    def get_seqs(self):
        """Retorna a lista de sequencias registradas"""
        return  self.ids
    
    def get_info(self,arg):
        """Retorna comentário da sequencia"""
        busca = self.ids[arg] if (isinstance(arg, int)) else arg #busca irá manter o id
        if busca in self.info:
            return self.info[busca]
        else: self.message_view("Sequencia não possui comentário!")   
        return []
        
        
    def get_tamanho_sequencia(self,arg): #permite receber como paramentro um inteiro que é o indice ou uma string id que é a identificação da sequencia
        """Soma a quantidade nucleotideos ou aminoácidos de uma sequencia"""
        busca = arg if (isinstance(arg, int)) else self.ids.index(arg)
        tamanho = 0
        if((len(self.composicao_total) < busca) or not isinstance(busca, int)): 
            self.message_view("Sequencia não encontrada!")
            return 0
        for n in self.composicao_total[busca]:
            tamanho += self.composicao_total[busca][n]
        return tamanho

    def nova_sequencia(self,id): #id é a identificação da sequência a ser armazenada
       """Insere uma nova sequencia na lista ids"""
       if not(self.seq_existe(id)):
          self.ids.append(id)
          self.composicao_total.append(dict(self.composicao_DNA_RNA_PROTEINA)) #Expressão dict faz uma copia do dicionario
          self.sequencia.append("") #Inicializa uma string na lista para aramazenar a sequencia
          return True 
       else:
          self.message_view("Sequencia já inserida!")   
          return False
       
    def get_sequencia(self,arg):
        """ Retorna a sequencia armazenada com seus nucleotídeos (DNA e RNA) ou dos aminoácidos (Proteina)"""
        indice = arg if (isinstance(arg, int)) else self.ids.index(arg)
        return None if not(self.seq_existe(arg)) else self.sequencia[ indice ]
    
    def get_composicao_seq(self,arg):
        """ Retorna a composição da sequência com os totais de nucleotídeos (DNA e RNA) ou dos aminoácidos (Proteina) """
        if (self.seq_existe(arg)):
            indice = arg if (isinstance(arg, int)) else self.ids.index(arg)
            temp = f"T({self.get_tamanho_sequencia(indice)}): "
            for chave, valor in self.composicao_total[ indice ].items():
                temp +=  chave +'('+str(valor)+')'+','
            return temp
        self.message_view("Sequencia não encontrada!")   

    def get_tipo_seq(self,arg,sequencia = None):
        """Identifica uma sequencia se é de DNA, RNA ou PROTEINA"""
        seq = self.get_sequencia(arg) if(sequencia == None) else sequencia
        if(seq.find("U") != -1):  
            return "RNA"
        return "DNA" if(len(re.findall(r'[^ACGT]', seq)) == 0) else "Proteina" #Se sequencia contém somente ACGT é um DNA
    
    def get_percentual_GC(self,arg):
        """Retorna a percentual(%) de Guanina e Citosina na sequência."""
        if (self.seq_existe(arg)):
            indice = arg if isinstance(arg, int) else self.ids.index(arg) 
            G = self.composicao_total[indice]['G'] if('G' in self.composicao_total[indice]) else 0
            C = self.composicao_total[indice]['C'] if('C' in self.composicao_total[indice]) else 0
            GC = ( G + C ) / self.get_tamanho_sequencia(indice) if(self.get_tamanho_sequencia(indice) > 0) else 0
            return GC*100
        self.message_view("Sequencia não encontrada!")
        return None



    def insert_comment(self,arg,info):
       """Armazena o comentário da sequência"""
       if (self.seq_existe(arg) and info is not None):
            busca = self.ids.index(arg) if isinstance(arg, int) else arg
            self.info[ busca ] = info
     
    def add_item(self,id,item):
        """Adciona um somatório de nucleotídos ou aminoácidos da sequência"""
        if(re.sub(r'[\t\n\r\f\v\b\0\a\s]', '',item)==""):
            return 
        if(self.seq_existe(id)): 
            if("ACGTUDEFHIKLMNPQRSVWY".find(item) != -1): #ACGTU (Nucleotídeos presentes no DNA ou RNA) | ACDEFGHIKLMNPQRSTVWY (Aminoácidos presentes na Proteina)
                indice = self.ids.index(id)
                if(item in self.composicao_total[ indice ]):
                    self.composicao_total[ indice ][item] += 1
                else:
                    self.composicao_total[ indice ][item] = 1    
                self.sequencia[ indice ] += item    
            else:
               self.message_view(f"Um nucleotídeo ou aminoácido não reconhecido na sequencia[{id}]!{item}",True)
        else:
            self.message_view(f"-Identificação de sequência não encontrada!{id}")
                    
    def ver_info_seq(self,arg):
        """Exibe dados de uma sequência"""
        if(self.seq_existe(arg)):
            indice = arg if (isinstance(arg, int)) else self.ids.index(arg)
            print("Informações da sequência:")
            print("=========================")
            print(f"Id: {self.ids[indice]}")
            print(f"Sequencia de {self.get_tipo_seq(arg)}")
            if(indice in self.info ):
                print(f"Info: {self.info[indice]}")
            print(f"Composição: {self.get_composicao_seq(arg)}")
                #print(f"Q(n): A({self.composicao_total[indice]['A']}),C({self.composicao_total[indice]['C']}),G({self.composicao_total[indice]['G']}),T({self.composicao_total[indice]['T']}),U({self.composicao_total[indice]['U']})")
            print(f"Tamanho sequencia: {self.get_tamanho_sequencia(indice)}")
            print("Percentual de GC: {:.2f} %".format(self.get_percentual_GC(indice)))
            
            #if(("G" in self.composicao_total[indice])and("C" in self.composicao_total[indice])):
            #    GC = (self.composicao_total[indice]['G']+self.composicao_total[indice]['C'])/self.get_tamanho_sequencia(indice)
            #    print("GC: {:.2f} %".format(GC*100))


        else:
            self.message_view("Sequencia não encontrada!")   
        return ""
    def identifica_id(self,line):
        """Retorna a string de identificação da sequência (id)"""
        match = re.match(r'^>(\S+)', line)
        if match:
            return match.group(1)
        else:
            return None

    def identifica_info(self,line):
        """Retorna a string de comentário da sequência (id)"""
        match = re.match(r'^>[\w\|]+ (.+)', line)
        if match:
            return match.group(1)
        else:
           return None
        
    def leiaArquivoFasta(self,nome_arquivo):
        """ Lê  todas as sequências de um arquivo Fasta """    
        with open (nome_arquivo, "r") as arq:
            while True:
                self.line = arq.readline()
                if not self.line: break #interrompe ao final do arquivo
                if self.line.strip() == "": continue  # Ignorar linhas em branco
                if self.line.strip()[0]==";": continue # ignora linhas de comentário

                if(self.line.find('>') >= 0): #Identificado nova sequencia
                    self.id = self.identifica_id(self.line)
                    if(self.nova_sequencia(self.id)):
                        comment = self.identifica_info(self.line)
                        self.insert_comment(self.id,comment)
                    else: self.id = None    
                else:    #compilando a sequencia
                    if(self.id != None):
                        for i in [*self.line]:
                            self.add_item(self.id,i)    

    def adiciona_seq(self,n1,n2,n3):
        """Insere uma sequência através de código"""
        #n1 - string com a identificação da sequência
        #n2 - string com informações sobre a sequência
        #n3 - srting da seqUencia
        if(self.nova_sequencia(n1)):
            self.insert_comment(n1,n2)
            for n in n3:
                self.add_item(n1,n) 
        else:
            self.message_view("Erro ao adicionar ou sequência já inserida!")   
    
    def remove_seq(self,arg):
        """Remove uma sequência usando o id da sequencia o index armazenado em ids"""
        if (self.seq_existe(arg)):
            indice = arg if isinstance(arg, int) else self.ids.index(arg) 
            self.info.pop( self.ids[ indice ]) #primeiro remove a info da sequencia se existir 
            self.sequencia.pop(indice) #remove a sequencia do id removido (as referencias se ajustam)
            self.ids.pop(indice) #remove a identificação da sequencia armazenada
            return True
        else: return False


    # Calcula a distância de Hamming (dH) entre duas sequências
    def dH(self,id1,id2):
        """Distãncia de Hamming (dH) entre duas sequências de DNA ou RNA"""
        if(self.seq_existe(id1) and self.seq_existe(id2)):
            if([self.get_tipo_seq(id1),self.get_tipo_seq(id2)] == ['DNA','DNA'] or [self.get_tipo_seq(id1),self.get_tipo_seq(id2)] == ['RNA','RNA']):
                if(self.get_tamanho_sequencia(id1)==self.get_tamanho_sequencia(id2)):
                    seq1 = self.get_sequencia(id1)
                    seq2 = self.get_sequencia(id2)
                    dist =0 
                    for n1, n2 in zip(seq1, seq2):
                        if(n1 != n2):
                            dist += 1
                    return dist       
                else: self.message_view("As sequências têm comprimentos diferentes.")       
            else: self.message_view("Para calcular a distância de hamming as sequências devem ser de DNA ou de RNA.")       
        else: self.message_view("Identificação das sequências não encontrada!")       
        return False
    
    def rna2proteina(self,arg):
        proteina = []
        if(self.seq_existe(arg)):
            
            if(self.get_tipo_seq(arg) == "RNA"):
                mRNA = self.get_sequencia(arg)
                for i in range(0, len(mRNA), 3):
                    codon = mRNA[i:i+3]  # Extrai o códon de 3 nucleotídeos
                    aminoacido = self.codons.get(codon, 'X')  # Obtém o aminoácido correspondente ao códon
                    proteina.append(aminoacido)  # Adiciona o aminoácido à lista
                # Junta os aminoácidos em uma única string
                return ''.join(proteina) 
            else: 
                self.message_view("Sequência para transcrição não é um RNA!")              
                print(self.get_sequencia(arg))
                exit()
        else: self.message_view("Identificação das sequências não encontrada!")              
        return None
    
    def transc_dna2rna(self,arg):
        """Transcrição de uma sequência de DNA em um mRNA -Substitui todas as ocorrências de 'T' por 'U' """
        if(self.seq_existe(arg)):
            if(self.get_tipo_seq(arg) != "Proteina"):
                DNA = self.get_sequencia(arg)
                mRNA =  DNA.replace('T', 'U')
                return mRNA
            else: self.message_view("Sequência para transcrição já é uma Proteina!")              
        else: self.message_view("Identificação das sequências não encontrada!")              
        return None


    def get_kmers(self,arg,k):
        """Retorna uma lista de sequencias k da janela deslizante da sequência
        :param sequencia: A sequência de entrada (string)
        :param k: O comprimento dos k-mers (inteiro)
        :return: Uma lista de k-mers
        """
        if(self.seq_existe(arg)):
            if(k <= self.get_tamanho_sequencia(arg)):
                sequencia = self.get_sequencia(arg)
                kmers = []
                for i in range(len(sequencia) - k + 1):
                    kmers.append(sequencia[i:i + k])
                return kmers
            else: self.message_view("Comprimento k (k-mers) maior que a sequência!")                  
        else: self.message_view("Identificação das sequências não encontrada!")  
        return None                
    
    def get_assembly_kmers(self):
        """Assembly, monta um genoma a partir dos kmers (conjunto de todas as sequencias do objeto)"""
        if(len(self.ids) > 1):
            genoma = ""
            for i in range(len(self.ids)-1):
                genoma += self.sequencia[i][0]
            genoma += self.sequencia[len(self.ids)-1]
            return genoma
        if (len(self.ids) == 1): return self.ids[0]
        else: self.message_view("Não existe Mers suficientes para construir uma estrutura de sequência!")                  
        return None
    
    #--------------------------------------------------------------------------    
    #______________________________________________________________  
    #def matriz_d(self, filename):
    def matriz_d(self):
        """Calcula a matriz de distância para sequências de proteínas."""
        bibliotecas = ['numpy', 'blosum','matplotlib.pyplot','seaborn','scipy.cluster.hierarchy'] # Lista de bibliotecas necessárias
        for biblioteca in bibliotecas: # Verificar cada biblioteca
            if not self.verificar_biblioteca(biblioteca):
                sys.exit(1)  # Sair do script se alguma biblioteca não estiver instalada

        import numpy as np
        import blosum as bl
        import matplotlib.pyplot as plt
        import seaborn as sns
        import scipy.cluster.hierarchy as sch

        self.blosum_matrix = bl.BLOSUM(62) # Define um atributo de instância

        #sequences = self.get_fasta_sequences(filename)
        #num_sequences = len(sequences)
        num_sequences = len(self.ids)

        # Verifica se todas as sequencias são de proteínas
        for i in range(num_sequences):
            # Verifica se o tipo da sequencia é DNA ou RNA
            if self.get_tipo_seq(i) != 'Proteina':
                self.message_view("Erro: Não é uma sequência de proteínas!", True) 
                return # Sai da função se encontrar uma sequência que não seja de proteína

        # Inicializar matriz de distância
        distance_matrix = np.zeros((num_sequences, num_sequences))

        # Execute alinhamentos aos pares e preencha a matriz de distância

        for i, seq1 in enumerate(self.ids):
            for j, seq2 in enumerate(self.ids):
                if self.ids[i] != self.ids[j]: #se as identificações das sequencias são iguais
                    #  recebe as sequências self.sequencia[i] e self.sequencia[j] e retorna informações sobre o alinhamento
                    rx_indices, ry_indices, rx_alignment, ry_alignment, scoring_matrix, num_gaps = self.needleman_wunsch_2(self.sequencia[i], self.sequencia[j])
                    # pega a última linha e última coluna da matriz de score (scoring_matrix).
                    distance_matrix[i,j] = -scoring_matrix[-1,-1]  # Executar alinhamentos aos pares e preencher a matriz de distância
                    
                    # Optional: Imprimir alinhamentos
                    #print(f"Alignment between {name1} and {name2}:")
                    #print(f"Alignment between {self.ids[i]} and {self.ids[j]}:")
                    print(".",end="")
                    print(rx_alignment)
                    #print(ry_alignment)
                    #plot_scoring_matrix(scoring_matrix, rx_indices, ry_indices)  # Optional: Individual plots

        # agrupando os dados de acordo com suas distâncias
        linkage_matrix = sch.linkage(distance_matrix, method='ward')
        # cria um mapa de calor (heatmap) e dendrogramas (diagramas de árvores)
        clustermap = sns.clustermap(distance_matrix, cmap='coolwarm', row_linkage=linkage_matrix, col_linkage=linkage_matrix)
        plt.show()  

        #  alinhea duas sequências de aminoácidos, retornando o alinhamento ótimo, a matriz de pontuação e gaps
    def needleman_wunsch_2(self, x, y, gap=1):
        bibliotecas = ['numpy', 'blosum','matplotlib.pyplot','seaborn','scipy.cluster.hierarchy'] # Lista de bibliotecas necessárias
        for biblioteca in bibliotecas: # Verificar cada biblioteca
            if not self.verificar_biblioteca(biblioteca):
                sys.exit(1)  # Sair do script se alguma biblioteca não estiver instalada
        import numpy as np
        import blosum as bl
        import matplotlib.pyplot as plt
        import seaborn as sns
        import scipy.cluster.hierarchy as sch
        scoring_matrix = self.calculate_scoring_matrix_2(x, y, gap) # calcula a matriz de pontuação para o alinhamento de sequências
        rx_indices, ry_indices, num_gaps = self.traceback_2(scoring_matrix, x, y,gap) #  para encontrar o alinhamento ótimo.

        rx_alignment = ''.join([x[i - 1] if i > 0 else '-' for i in rx_indices]) # Constrói o alinhamento para a primeira sequência (x) 
        ry_alignment = ''.join([y[j - 1] if j > 0 else '-' for j in ry_indices]) # Constrói o alinhamento para a segunda sequência (y)

        return rx_indices, ry_indices, rx_alignment, ry_alignment, scoring_matrix, num_gaps # A função retorna os resultados do alinhamento

        # traceback_2: retorna os índices do alinhamento e a contagem de gaps (Use scoring_matrix)
    def traceback_2(self, scoring_matrix, x, y, gap=1):  
        import numpy as np
        import blosum as bl
        import matplotlib.pyplot as plt
        import seaborn as sns
        import scipy.cluster.hierarchy as sch
        

        i, j = len(x), len(y)
        rx, ry = [], []
        gap_count = 0
        while i > 0 or j > 0: # itera até que todas as posições das sequências tenham sido processadas
            # aminoácidos correspondentes aos índices i e j das sequências
            amino_acid_x = x[i - 1]
            amino_acid_y = y[j - 1]
            #Verifica se o valor atual na matriz de pontuação (scoring_matrix) obtida da matriz self.blosum_matrix.
            #  aminoácidos estão alinhados
            if i > 0 and j > 0 and scoring_matrix[i, j] == scoring_matrix[i - 1, j - 1] + (self.blosum_matrix[amino_acid_x][amino_acid_y]): # Use self.blosum_matrix
                rx.append(i)
                ry.append(j)
                i -= 1
                j -= 1
            elif i > 0 and scoring_matrix[i, j] == scoring_matrix[i - 1, j] - gap: # inclui um gap na sequência
                rx.append(i)
                ry.append(0) # um gap foi introduzido na sequência y
                i -= 1
                gap_count += 1
            else: 
                rx.append(0) # gap foi introduzido na sequência x
                ry.append(j)
                j -= 1
                gap_count += 1

        return rx[::-1], ry[::-1], gap_count  # índices do alinhamento ótimo, e a contagem de gaps, após inverter as listas para obter a ordem correta

        #  calculate_scoring_matrix_2: calcula a matriz de pontuação para o alinhamento das sequências, usando a matriz BLOSUM
    def calculate_scoring_matrix_2(self, x, y, gap=1):  # calcula a matriz de pontuação para o alinhamento de duas sequências
        import numpy as np
        import blosum as bl
        import matplotlib.pyplot as plt
        import seaborn as sns
        import scipy.cluster.hierarchy as sch

        nx = len(x)
        ny = len(y)
        # Cria uma matriz de zeros de tamanho (nx + 1, ny + 1) para armazenar a matriz de pontuação
        # As linhas e colunas extras (nx + 1 e ny + 1) são para gaps 
        scoring_matrix = np.zeros((nx + 1, ny + 1))
        # Inicializa a primeira coluna e a primeira linha da matriz de pontuação (penalidades por gaps)
        scoring_matrix[:, 0] = np.linspace(0, -nx * gap, nx + 1)
        scoring_matrix[0, :] = np.linspace(0, -ny * gap, ny + 1)
        # iterar sobre cada posição na matriz de pontuação
        for i in range(1, nx + 1):
            for j in range(1, ny + 1):
              amino_acid_x = x[i - 1]
              amino_acid_y = y[j - 1]

              if x[i - 1] == y[j - 1]:
                # definida como a soma da pontuação da posição anterior na diagonal + blosum_matrix
                  scoring_matrix[i, j] = scoring_matrix[i - 1, j - 1] + self.blosum_matrix[amino_acid_x][amino_acid_y] # Use self.blosum_matrix
                # posição atual é definida como o máximo entre três valores:
              else: 
                  scoring_matrix[i, j] = max(scoring_matrix[i - 1, j] - gap,
                                              scoring_matrix[i, j - 1] - gap,
                                              scoring_matrix[i - 1, j - 1] + self.blosum_matrix[amino_acid_x][amino_acid_y]) # Use self.blosum_matrix

        return scoring_matrix

#_____________________________________________________________________________________________  
    #===========================================================================================
    def compara_genomas(self,id1,id2):
        """Compara dois genomas e retorna a porcentagem de diferenças"""
        if(self.seq_existe(id1) and self.seq_existe(id2)):
            if([self.get_tipo_seq(id1),self.get_tipo_seq(id2)] == ['DNA','DNA']):
                if(self.get_tamanho_sequencia(id1)==self.get_tamanho_sequencia(id2)):
                    genoma1 = self.get_sequencia(id1)
                    genoma2 = self.get_sequencia(id2)
                    print(id1," : ", self.get_sequencia(id1) )
                    print(id2," : ", self.get_sequencia(id1) )
                    Num_Dif = 0
                    for i in range(len(genoma1)):
                        if genoma1[i] != genoma2[i]:
                            Num_Dif += 1
                    Dif_Percentual = (Num_Dif / len(genoma1)) * 100
                    return "{:.2f}%".format(Dif_Percentual)      
                else: self.message_view("As sequências têm comprimentos diferentes.")       
            else: self.message_view("Para comparar os genomas as sequências devem ser de DNA.")       
        else: self.message_view("Identificação das sequências não encontrada!")       
        return False
    
    def reverso_complementar(self,arg):
        """Retorna o reverso complementar de uma sequência de DNA')"""
        dic_reverse = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}  # Dicionário
        nova_seq = []                                           # Cria uma lista auxiliar que será preenchida com valores do Dicionário
        if(self.seq_existe(arg)):                                # Verifica se a sequência foi carregada
            if(self.get_tipo_seq(arg)=="DNA"):                   # Verifica se a sequência é um DNA
                seq = self.get_sequencia(arg)                    # Atribui a string da sequência à variável seq
                seq = seq[::-1]                                 # Inverte a sequência
                for i in range(len(seq)):                       # Percorre a sequência invertida do início ao final
                    nova_seq.append(dic_reverse[seq[i]])        # Alimenta a lista auxiliar com valores do Dicionário
                                                                # alternativa seria [nova_seq = ''.join(complemento[base] for base in seq)]
                return ''.join(nova_seq)                        # Retorna a lista auxiliar em formato de string
            else: self.message_view(f"A sequencia informada não é um DNA![{self.get_tipo_seq(id)}]")
        else: self.message_view("A sequencia para o Reverso Complentar não foi encontrada!")
        return None
    #=============================================================================================

    def __encontra_codificante_sequencia(self,sequencia,codon_start): #recebe uma sequencia qualquer e devolve uma janela de sequencia codificante
        stop = ['TAA','TAG','TGA'] if self.get_tipo_seq("",sequencia) == "DNA" else ['UAA','UAG','UGA'] #códons de stop para geração da da proteing
        cds = [] #armazena os segmentos codificantes
        #pos_cds = [] #armazena uma lista de tuplas com posição inicial e final das sequencias codificantes
        pos_i = 0 #determina a posicao inicial do segmento
        finais = [0,0,0] #encontra três possibilidades de encerramento da sequência codificante
        for cd in range(sequencia.count(codon_start)-1):
            pos_i = sequencia.find(codon_start,pos_i) #recebe a primeira posição de uma sequencia codificante
            pos_f = pos_i + 3 #busca o códon de stop a partir do códon de start
            finais = [sequencia.find(stop[0],pos_f),sequencia.find(stop[1],pos_f),sequencia.find(stop[2],pos_f)] #encontra até 3 possíveis condições de stop
            pos_f = min([n for n in finais if n>=0])+3 if(len([n for n in finais if n>=0]) > 0) else -1 #Seleciona a posição mais próxima
            if pos_f < 0: break #se não encontrar mais posicao de stop, interrompe a busca
            cds.append(sequencia[pos_i:pos_f]) #armazena a sequencia codificante
            #pos_cds.append((pos_i,pos_f)) #armazena tuplas de início e fim das sequencias codificantes no genoma
            pos_i = pos_f #reinicia a busca da posição final da última sequenciapass
        return cds    
    def __traduz_janelas_codificantes(self,exons): #exons é uma lista de string cds
        proteina = []
        for e in exons: #primeira janela
            proteina.append(self.dna("",e).transcreve().traduz().get())
        for e in exons: #segunda janela   
            proteina.append(self.dna("",e[1:]).transcreve().traduz().get())
        for e in exons: #terceira janela       
            proteina.append(self.dna("",e[2:]).transcreve().traduz().get())
        return proteina    


    def busca_cds(self,arg,codon_start):
        """Busca na squẽncias os segmentos codificantes no genoma que inicia pelo codon_start, se a fita é um DNA, encontra também no reverso complementar
           traduz todos o exons em proteina
        """
        if(self.seq_existe(arg)):
            #indice = arg if isinstance(arg, int) else self.ids.index(arg) 
            proteina = []
            if(self.get_tipo_seq(arg) != "Proteina"):
                exons = self.__encontra_codificante_sequencia(self.get_sequencia(arg),codon_start) #busca os exons em uma fita
                #Traduz usando a Sequência Original (5' -> 3'): 3 janelas de codificação
                proteina = self.__traduz_janelas_codificantes(exons) 
                if(self.get_tipo_seq(arg)=="DNA"): #obtêm as proteinas do reverso complementar da fita 
                    proteina.extend(self.__traduz_janelas_codificantes(self.__encontra_codificante_sequencia(self.reverso_complementar(arg),codon_start)))
                return proteina
            else: self.message_view("A sequência informada é uma Proteína!")             
        else: self.message_view("Identificação das sequências não encontrada!")       
        return []
    
    #***************************************************************
    # Modelamento de métodos em cascada ( chanining)
    #***************************************************************
    def dna(self,arg,sequencia = None):
        if self.seq_existe(arg) or sequencia != None: #prossegue para uma sequencia válida
            self.aux_chaining = self.get_sequencia(arg) if(sequencia == None) else sequencia
        else: self.message_view("Sequencia não encontrada!",True)   
        return self

    def rm_introns(self,*args):
        for arg in args:
            if isinstance(arg, str):
                self.aux_chaining = re.sub(arg, "", self.aux_chaining)
        return self
    
    def transcreve(self):
        if(len(self.aux_chaining)>0): #processa se somente de existir uma sequencia
            self.adiciona_seq("Transcricao00x2","Sequencia armazenada de forma temporária para calculo de transcrição",self.aux_chaining)
            self.aux_chaining = self.transc_dna2rna("Transcricao00x2")
            self.remove_seq("Transcricao00x2")
        return self
    
    def traduz(self):
        if(len(self.aux_chaining)>0): #processa se somente de existir uma sequencia
            self.adiciona_seq("Traducao00x1","Sequencia armazenada de forma temporária para calculo de transcrição",self.aux_chaining)
            self.aux_chaining = self.rna2proteina("Traducao00x1")
            self.remove_seq("Traducao00x1")
        return self

    def imprime(self):
        print(self.aux_chaining)
        return self

    def get(self):
        return self.aux_chaining


class Encadear(Bioprof):
    """ Classe demonstra técnica de modelamento de métodos em cascada ( chanining)"""

    def __init__(self):
        super().__init__()
        self.aux_chaining = ""

    def dna(self,arg,sequencia = None):
        """Armazena uma sequẽncia para operação de encadeamento"""
        if self.seq_existe(arg) or sequencia != None: #prossegue para uma sequencia válida
            self.aux_chaining = self.get_sequencia(arg) if(sequencia == None) else sequencia
        else: self.message_view("Sequencia não encontrada!",True)   
        return self
      

    def rm_introns(self,*args):
        for arg in args:
            if isinstance(arg, str):
                self.aux_chaining = re.sub(arg, "", self.aux_chaining)
        return self
    
    def transcreve(self):
        self.adiciona_seq("Transcricao00x2","Sequencia armazenada de forma temporária para calculo de transcrição",self.aux_chaining)
        self.aux_chaining = self.transc_dna2rna("Transcricao00x2")
        self.remove_seq("Transcricao00x2")
        return self
    
    def traduz(self):
        self.adiciona_seq("Traducao00x1","Sequencia armazenada de forma temporária para calculo de transcrição",self.aux_chaining)
        self.aux_chaining = self.rna2proteina("Traducao00x1")
        self.remove_seq("Traducao00x1")
        return self

    def imprime(self):
        print(self.aux_chaining)
        return self

    def get(self):
        return self.aux_chaining
