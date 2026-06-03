import math

def verify():
    count = 0
    points = []
    
    # 교점의 x좌표
    sqrt5 = math.sqrt(5)
    x_min = 2 - sqrt5
    x_max = 2 + sqrt5
    
    # 정수 x에 대해 확인
    for x in range(-1, 6):
        if x_min < x < x_max:
            # 포물선 위의 점
            y_parabola = x**2 - 3*x + 1
            # 직선 위의 점
            y_line = x + 2
            
            # 도형 내부의 정수 y
            for y in range(int(y_parabola) - 1, int(y_line) + 2):
                if y_parabola < y < y_line:
                    count += 1
                    points.append((x, y))
    
    if count == 10:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {count}, expected 10')
        print(f'Points: {points}')

verify()