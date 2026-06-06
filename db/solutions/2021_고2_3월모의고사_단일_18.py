from itertools import combinations
math_set = {0,1,2}
all_subjects = list(range(7))
def has_math(c): return bool(set(c)&math_set)

# p = (가)
p_total=0
for cm in range(3):
    rem=[s for s in all_subjects if s!=cm]
    for ae in combinations(rem,2):
        rem_b=[s for s in rem if s not in ae]
        for be in combinations(rem_b,2):
            A=(cm,)+ae; B=(cm,)+be
            if has_math(A) and has_math(B) and len(set(A)&set(B))==1:
                p_total+=1
p=p_total//3

# q = (나)
q_total=0
for cs in range(3,7):
    rem=[s for s in all_subjects if s!=cs]
    for ae in combinations(rem,2):
        A=(cs,)+ae
        if not has_math(A): continue
        rem_b=[s for s in rem if s not in ae]
        for be in combinations(rem_b,2):
            B=(cs,)+be
            if not has_math(B): continue
            if len(set(A)&set(B))==1:
                amc=sum(1 for s in ae if s in math_set)
                bmc=sum(1 for s in be if s in math_set)
                if (amc==2 and bmc==1) or (amc==1 and bmc==2):
                    q_total+=1
q=q_total//4

print(f'p={p}, q={q}, p+q={p+q}')
if p+q==108: print('VERIFY_PASS')
else: print('VERIFY_FAIL')