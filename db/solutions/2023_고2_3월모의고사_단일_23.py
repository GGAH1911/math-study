from sympy import Eq, simplify

def solve(f1=4, f2=1, f3=2, f4=3, a=1, b=1):
    """
    일반화된 함수 합성·역함수 문제 솔버
    
    Parameters:
    - f1, f2, f3, f4: f(1), f(2), f(3), f(4) 값
    - a: (f∘f)(a) 계산 대상 (기본: 1)
    - b: f^(-1)(b) 계산 대상 (기본: 1)
    
    Returns:
    (f∘f)(a) + f^(-1)(b) 값
    """
    # 함수 맵 구성
    f_map = {1: f1, 2: f2, 3: f3, 4: f4}
    
    # 역함수 맵 구성
    f_inv_map = {v: k for k, v in f_map.items()}
    
    # (f∘f)(a) = f(f(a))
    ff_a = f_map[f_map[a]]
    
    # f^(-1)(b)
    f_inv_b = f_inv_map[b]
    
    # 최종 관계식: (f∘f)(a) + f^(-1)(b)
    result = ff_a + f_inv_b
    
    return result

CANDIDATE = 5
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')