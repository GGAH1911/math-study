import numpy as np
from scipy.optimize import fsolve
import warnings
warnings.filterwarnings('ignore')

def verify_conditions(a, b):
    # 조건 (나) 검증: g(f(x)) = 3이 [0,6]에서 정확히 3개 해
    def f(x):
        return (3/a) * abs(x - 3) - b
    
    def equation(x):
        return np.sin((np.pi/b) * f(x))
    
    # [0,6] 범위에서 해 찾기
    solutions = []
    for start in np.linspace(0, 6, 25):
        try:
            sol = fsolve(equation, start, full_output=True)
            if sol[2] == 1 and 0 <= sol[0][0] <= 6:
                x_val = sol[0][0]
                if abs(equation(x_val)) < 1e-6:
                    # 중복 제거
                    is_new = True
                    for s in solutions:
                        if abs(x_val - s) < 1e-4:
                            is_new = False
                            break
                    if is_new:
                        solutions.append(x_val)
        except:
            pass
    
    num_intersections = len(solutions)
    
    if num_intersections == 3 and 4.5 < a*b <= 9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

# 최솟값 검증
verify_conditions(2, 3)

# 최댓값 검증  
verify_conditions(9, 1)