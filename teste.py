seq = "ATTACGGC"
complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}


complementary_sequence = ''.join(complement[base] for base in seq)
    
    # Reverter a sequência complementar
reverse_complementary_sequence = complementary_sequence[::-1]
print(seq)    
print(complementary_sequence)
print(reverse_complementary_sequence)

