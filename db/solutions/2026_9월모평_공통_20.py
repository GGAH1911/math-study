from sympy import sqrt, symbols, Rational, simplify, solve

CANDIDATE = 12

# Given conditions from problem
# PB : PC : BC = 7 : 5 : √14
# AD = 4√13
# ∠BPC = θ where cos(θ) = 6/7
# AB : CD = 1 : 3
# △BPC ~ △DPA (from cyclic quadrilateral property)

k = symbols('k', positive=True, real=True)
l = symbols('l', positive=True, real=True)

# Define lengths in terms of k
PB = 7 * k
PC = 5 * k
BC = sqrt(14) * k
AD = 4 * sqrt(13)

# ============================================
# STEP 1: Verify cos(∠BPC) = 6/7 from cosine rule
# ============================================
# BC² = PB² + PC² - 2·PB·PC·cos(∠BPC)
# cos(∠BPC) = (PB² + PC² - BC²) / (2·PB·PC)

cos_BPC_calculated = (PB**2 + PC**2 - BC**2) / (2 * PB * PC)
cos_BPC_calculated = simplify(cos_BPC_calculated)

assert cos_BPC_calculated == Rational(6, 7), f"Cosine check failed: {cos_BPC_calculated}"
print(f"✓ Step 1: cos(∠BPC) = {cos_BPC_calculated} (verified)")

# ============================================
# STEP 2: Find (가) = coefficient linking l and k
# ============================================
# From similarity △BPC ~ △DPA:
# Corresponding sides: PB/PD = PC/PA
# With P-B-A collinear (PA = PB + AB) and P-C-D collinear (PD = PC + CD)
# where AB = l and CD = 3l
#
# 7k / (5k + 3l) = 5k / (7k + l)
# 7k(7k + l) = 5k(5k + 3l)
# 49k² + 7kl = 25k² + 15kl
# 24k² = 8kl
# l = 3k

eq_similarity = 7*k*(7*k + l) - 5*k*(5*k + 3*l)
l_solutions = solve(eq_similarity, l)
l_value = l_solutions[0]

assert simplify(l_value / k) == 3, f"l should be 3k"
print(f"✓ Step 2: l = {l_value} = 3k  →  (가) = 3")
p = 3

# ============================================
# STEP 3: Find (나) = similarity ratio denominator
# ============================================
# With l = 3k:
# PD = PC + CD = 5k + 3(3k) = 14k
# PA = PB + AB = 7k + 3k = 10k
# Similarity ratio: PB/PD = PC/PA = BC/AD
# 7k / 14k = 5k / 10k = 1/2
#
# Therefore BC/AD = 1/2, so (나) = 2 (ratio 1:(나))

l_val_num = 3 * k
PD = PC + 3*l_val_num  # PC + CD where CD = 3l
PA = PB + l_val_num     # PB + AB where AB = l

PD_simplified = simplify(PD)
PA_simplified = simplify(PA)
similarity_ratio = simplify(PB / PD_simplified)

assert similarity_ratio == Rational(1, 2), f"Similarity ratio check failed: {similarity_ratio}"
print(f"✓ Step 3: PD = {PD_simplified}, PA = {PA_simplified}")
print(f"         Similarity ratio PB/PD = {similarity_ratio} = 1/2  →  (나) = 2")
q = 2

# ============================================
# STEP 4: Verify consistency with AD = 4√13
# ============================================
# From BC/AD = 1/2 and BC = √14·k:
# √14·k / (4√13) = 1/2
# k = 2√13 / √14

k_value = 2 * sqrt(13) / sqrt(14)
BC_computed = sqrt(14) * k_value
BC_computed = simplify(BC_computed)

assert BC_computed == 2*sqrt(13), f"BC computation failed: {BC_computed}"
print(f"✓ Step 4: k = {simplify(k_value)}")
print(f"         BC = {BC_computed} (consistent with AD/2)")

# ============================================
# STEP 5: Calculate (다) = circumradius
# ============================================
# sin(∠BPC) = √(1 - cos²(∠BPC))
# cos(∠BPC) = 6/7 → sin²(∠BPC) = 1 - 36/49 = 13/49
# sin(∠BPC) = √13/7
#
# Circumradius formula: R = BC / (2·sin(∠BPC))
# R = 2√13 / (2·√13/7) = 2√13 · 7/(2√13) = 7

cos_val = Rational(6, 7)
sin_BPC = sqrt(1 - cos_val**2)
sin_BPC = simplify(sin_BPC)

R = BC_computed / (2 * sin_BPC)
R = simplify(R)

assert R == 7, f"Circumradius calculation failed: {R}"
print(f"✓ Step 5: sin(∠BPC) = {sin_BPC}")
print(f"         R = {BC_computed} / (2·{sin_BPC}) = {R}  →  (다) = 7")
r = 7

# ============================================
# FINAL ANSWER
# ============================================
answer = p + q + r

print(f"\n{'='*50}")
print(f"Final: p = {p}, q = {q}, r = {r}")
print(f"p + q + r = {answer}")
print(f"{'='*50}")

if answer == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")