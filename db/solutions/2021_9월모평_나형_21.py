from fractions import Fraction

def compute_sequence(a1, a2, n_terms):
    seq = [a1, a2]
    for i in range(len(seq), n_terms):
        a_n, a_n1 = seq[i-2], seq[i-1]
        if a_n <= a_n1:
            a_n2 = 2 * a_n + a_n1
        else:
            a_n2 = a_n + a_n1
        seq.append(a_n2)
    return seq

# Test a1 = 1/4
a1_val = Fraction(1, 4)
a2_val = 2 - 2 * a1_val  # a2 = 3/2
seq1 = compute_sequence(a1_val, a2_val, 6)
check1 = (seq1[2] == 2 and seq1[5] == 19)

# Test a1 = -1/2
a1_val = Fraction(-1, 2)
a2_val = 2 - 2 * a1_val  # a2 = 3
seq2 = compute_sequence(a1_val, a2_val, 6)
check2 = (seq2[2] == 2 and seq2[5] == 19)

if check1 and check2:
    sum_a1 = Fraction(1, 4) + Fraction(-1, 2)
    if sum_a1 == Fraction(-1, 4):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')