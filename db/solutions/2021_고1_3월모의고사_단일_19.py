from sympy import symbols, solve, Integer

# Problem parameters
# n x n grid filling square ABCD
# Colored tiles: boundary + diagonal tiles
# White tiles = 168
# Find colored tiles

# For even n:
# white = (n-2)*(n-4)
# colored = 6n - 8

n = 16  # candidate

# Verify white tile count
boundary = 4*(n-1)

# Main diagonal: (i,i) for i=1..n -> n tiles
# Anti-diagonal: (i, n+1-i) for i=1..n -> n tiles
# Overlap check: i=i and i=n+1-i => 2i=n+1 => i=(n+1)/2=8.5 (not integer for n=16) -> no overlap
main_diag = n
anti_diag = n
diag_overlap = 0  # no shared interior tile for even n
total_diag_tiles = main_diag + anti_diag - diag_overlap  # 32

# Corner tiles are on both boundary and diagonal: (1,1),(n,n),(1,n),(n,1) -> 4 tiles
corner_on_diag = 4
pure_diag = total_diag_tiles - corner_on_diag  # 28

colored = boundary + pure_diag  # 60 + 28 = 88
total = n * n  # 256
white = total - colored  # 168

if white == 168 and colored == 88:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: white={white}, colored={colored}')
