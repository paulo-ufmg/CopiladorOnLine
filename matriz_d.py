from Bioclass import Bioprof
obj = Bioprof()
obj.leiaArquivoFasta('sequencia_proteina.fasta')
print(obj.get_seqs())
obj.matriz_d()