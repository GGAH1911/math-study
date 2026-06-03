import math

theta_candidates = []
for k in range(-100, 100):
    candidates = [
        math.asin(3/5) + math.pi/2 + 2*math.pi*k,
        math.pi - math.asin(3/5) + math.pi/2 + 2*math.pi*k
    ]
    for t in candidates:
        if math.pi < t < 1.5*math.pi:
            theta_candidates.append(t)

if not theta_candidates:
    print('VERIFY_FAIL: no theta found in range')
else:
    theta = theta_candidates[0]
    cond1 = abs(math.sin(theta - math.pi/2) - 3/5) < 1e-9
    cond2 = math.pi < theta < 1.5*math.pi
    sin_val = math.sin(theta)
    cond3 = abs(sin_val - (-4/5)) < 1e-9
    if cond1 and cond2 and cond3:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: sin(theta)={sin_val}, cond1={cond1}, cond2={cond2}')
