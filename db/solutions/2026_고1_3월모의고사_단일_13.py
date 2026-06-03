# 요금제 A와 B의 비용 함수
def cost_A(n):
    return 15000

def cost_B(n):
    if n <= 50:
        return 10000
    else:
        return 10000 + 150 * (n - 50)

# n = 84일 때 A < B 확인
n = 84
a_cost = cost_A(n)
b_cost = cost_B(n)

print(f'n={n}: A={a_cost}, B={b_cost}')
if a_cost < b_cost:
    # n = 83일 때도 확인
    a_cost_83 = cost_A(83)
    b_cost_83 = cost_B(83)
    print(f'n=83: A={a_cost_83}, B={b_cost_83}')
    if a_cost_83 >= b_cost_83 and a_cost < b_cost:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')