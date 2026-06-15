import sympy as sp
m_var = sp.Symbol('m', integer=True, positive=True)
f = -10*m_var**2 + 222*m_var + 460
f11 = f.subs(m_var, 11)
f12 = f.subs(m_var, 12)
f10 = f.subs(m_var, 10)
results = {'f(10)': f10, 'f(11)': f11, 'f(12)': f12}
max_m = max(results.items(), key=lambda x: x[1])[0]
max_value = results[max_m]
print(f'f(10)={f10}, f(11)={f11}, f(12)={f12}')
print('VERIFY_PASS' if max_m == 'f(11)' else 'VERIFY_FAIL')