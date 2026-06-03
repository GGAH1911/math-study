from itertools import permutations
from fractions import Fraction

students = ['1a','1b','2a','2b','3a','3b','3c']
grade = {'1a':1,'1b':1,'2a':2,'2b':2,'3a':3,'3b':3,'3c':3}

def check_cond_ga(perm):
    # perm[0..2] -> A1,A2,A3
    A = perm[:3]
    grades_A = set(grade[s] for s in A)
    if len(grades_A) != 2:
        return False
    # same-grade pair must be adjacent (|i-j|==1)
    for i in range(3):
        for j in range(i+1, 3):
            if grade[A[i]] == grade[A[j]]:
                if abs(i-j) != 1:
                    return False
    return True

def check_cond_na(perm):
    # perm[3..6] -> B1,B2,B3,B4
    B = perm[3:]
    for i in range(4):
        for j in range(i+1, 4):
            if grade[B[i]] == grade[B[j]] and abs(i-j)==1:
                return False
    return True

total = 0
fav = 0
for p in permutations(students):
    total += 1
    if check_cond_ga(p) and check_cond_na(p):
        fav += 1

prob = Fraction(fav, total)
if prob == Fraction(16, 105):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}')
