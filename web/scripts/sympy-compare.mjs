#!/usr/bin/env node
// 서버 /api/sympy 와 클라이언트 pyodide worker 흐름 (Node에서 시뮬레이션)
// 의 stdout 결과를 같은 코드로 실행해 diff. 클라이언트 sympy 로 전환 후
// 도형 quality 떨어진 원인 진단.
import { loadPyodide } from 'pyodide';

const TEST_CODE = `
from sympy import symbols, solve, sqrt
x, y = symbols('x y', real=True)
# 타원과 평행선의 교점
sol = solve([x**2/16 + y**2/12 - 1, x + 2*y - 2], [x, y])
print(sol)
print("Q =", sol[0])
F_prime = (-2, 0)
Qx, Qy = sol[0]
# 직선 F'Q 와 접선 x+2y=8 교점 R
from sympy import Symbol
X, Y = symbols('X Y', real=True)
R = solve([X + 2*Y - 8, (X - F_prime[0])*Qy - (Y - F_prime[1])*(Qx - F_prime[0])], [X, Y])
print("R =", R)
print(f"R float: {float(R[X])} {float(R[Y])}")
`;

const HEADER = `
import sympy
from sympy import Symbol, symbols, solve, simplify, expand, factor, diff, integrate, limit, Sum, Product, oo, pi, E, I, sqrt, sin, cos, tan, log, ln, exp, Matrix, Rational, S
x, y, z, n, k, t, a, b, c = symbols('x y z n k t a b c')
`;

console.log('=== Server /api/sympy 호출 ===');
const sres = await fetch('http://127.0.0.1:4321/api/sympy', {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ code: TEST_CODE }),
});
const sjson = await sres.json();
console.log('ok:', sjson.ok);
console.log('stdout (server):');
console.log('---START---');
console.log(sjson.stdout);
console.log('---END---');

console.log('\n=== Pyodide (worker 시뮬레이션 + StringIO wrap) ===');
const py = await loadPyodide();
await py.loadPackage('sympy');
await py.runPythonAsync(HEADER);
py.globals.set('__user_code', TEST_CODE);
const WRAP = [
  'import sys as __sys, io as __io',
  '__stdout_buf = __io.StringIO()',
  '__stderr_buf = __io.StringIO()',
  '__old_out, __old_err = __sys.stdout, __sys.stderr',
  '__sys.stdout, __sys.stderr = __stdout_buf, __stderr_buf',
  '__err_msg = ""',
  'try:',
  '    exec(compile(__user_code, "<user>", "exec"), globals())',
  'except Exception as __e:',
  '    import traceback as __tb',
  '    __err_msg = __tb.format_exc()',
  'finally:',
  '    __sys.stdout, __sys.stderr = __old_out, __old_err',
  '__captured_stdout = __stdout_buf.getvalue()',
  '__captured_stderr = __stderr_buf.getvalue() + __err_msg',
].join('\n');
await py.runPythonAsync(WRAP);
const stdout = py.globals.get('__captured_stdout') ?? '';
const stderr = py.globals.get('__captured_stderr') ?? '';
console.log('ok:', !stderr.trim());
console.log('stdout (pyodide):');
console.log('---START---');
console.log(stdout);
console.log('---END---');

console.log('\n=== DIFF ===');
const a = sjson.stdout.trim().split('\n');
const b = stdout.trim().split('\n');
console.log(`server lines: ${a.length}, pyodide lines: ${b.length}`);
const maxLen = Math.max(a.length, b.length);
for (let i = 0; i < maxLen; i++) {
  const sl = a[i] ?? '(missing)';
  const pl = b[i] ?? '(missing)';
  if (sl === pl) console.log(`  =${i}: ${sl.slice(0, 80)}`);
  else {
    console.log(`  ✗${i}:`);
    console.log(`    server : ${sl}`);
    console.log(`    pyodide: ${pl}`);
  }
}
