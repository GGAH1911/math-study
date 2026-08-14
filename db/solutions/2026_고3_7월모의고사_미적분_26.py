# y=e^x 가 y=t, y=t+2 와 만나는 x 좌표는 ln t, ln(t+2) → f(t)=ln(t+2)-ln t.
import sympy as sp

t = sp.symbols('t', positive=True)
f = sp.log(t + 2) - sp.log(t)
val = sp.simplify(sp.integrate(f/t**2, (t, sp.Rational(2, 3), 2)))
choices = {1: -1 + 3*sp.log(2), 2: -1 + 4*sp.log(2), 3: 4*sp.log(2),
           4: 1 + 3*sp.log(2), 5: 1 + 4*sp.log(2)}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [1] else 'VERIFY_FAIL')
