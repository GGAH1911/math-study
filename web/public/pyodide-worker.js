// 클라이언트 sympy 실행기. Pyodide 를 main thread 와 분리된 worker 에서
// init + sympy 로드. UI block 없음. 첫 init ~3-5초 (이후 캐시 재사용).
//
// 사용: lib/pyodide-client.ts 의 runSympyLocal() 이 이 worker 에 메시지 보냄.

const PYODIDE_VERSION = '0.27.0';
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js`;

let pyodideReady = null;

async function init() {
  if (pyodideReady) return pyodideReady;
  importScripts(PYODIDE_URL);
  const py = await loadPyodide({ indexURL: `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/` });
  await py.loadPackage('sympy');
  // HEADER inject — 자주 쓰는 sympy 심볼 자동 import (서버 /api/sympy 와 동일)
  await py.runPythonAsync(`
import sympy
from sympy import Symbol, symbols, solve, simplify, expand, factor, diff, integrate, limit, Sum, Product, oo, pi, E, I, sqrt, sin, cos, tan, log, ln, exp, Matrix, Rational, S, Point, Line, Segment, Ray, nsimplify
x, y, z, n, k, t, a, b, c = symbols('x y z n k t a b c')

# --- geom helpers — 작도 검증·교점·이등분선 표준화 (서버 /api/sympy 와 동일) ---
def L(p1, p2):
    return Line(Point(*p1), Point(*p2))

def intersect(o1, o2):
    return o1.intersection(o2)

def angle_bisector_dir(vertex, a, b):
    va = Matrix(a) - Matrix(vertex)
    vb = Matrix(b) - Matrix(vertex)
    na = va.norm(); nb = vb.norm()
    if na == 0 or nb == 0:
        raise ValueError("angle_bisector_dir: degenerate ray")
    d = va / na + vb / nb
    nd = d.norm()
    if nd == 0:
        raise ValueError("angle_bisector_dir: rays opposite")
    d = d / nd
    return (d[0], d[1])

def _close(value, target=0, tol=1e-9):
    try:
        s = simplify(value - target)
        if s == 0:
            return True
        return abs(float(s)) < tol
    except Exception:
        try:
            return abs(float(value) - float(target)) < tol
        except Exception:
            return False

def assert_on_line(point, p1, p2, tag):
    line = L(p1, p2)
    P = Point(*point)
    d = line.distance(P)
    if _close(d):
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            dval = float(d)
        except Exception:
            dval = d
        print(f"[VERIFY FAIL] {tag}: point {tuple(point)} not on line {tuple(p1)}-{tuple(p2)} (dist={dval})")

def assert_on_circle(point, center, radius, tag):
    d = sqrt((point[0]-center[0])**2 + (point[1]-center[1])**2)
    if _close(d, radius):
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            dval = float(d); rval = float(radius)
        except Exception:
            dval, rval = d, radius
        print(f"[VERIFY FAIL] {tag}: dist={dval} != r={rval}")

def assert_distance(p1, p2, expected, tag):
    d = sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    if _close(d, expected):
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            dval = float(d); eval_ = float(expected)
        except Exception:
            dval, eval_ = d, expected
        print(f"[VERIFY FAIL] {tag}: |{p1}-{p2}|={dval} != {eval_}")

def assert_angle(vertex, a, b, expected, tag):
    """∠a-vertex-b 가 expected (radian) 인지. 부호·사분면 오류 직격 검증."""
    from sympy import acos
    va = Matrix(a) - Matrix(vertex)
    vb = Matrix(b) - Matrix(vertex)
    na = va.norm(); nb = vb.norm()
    if na == 0 or nb == 0:
        print(f"[VERIFY FAIL] {tag}: degenerate ray (zero-length vector)")
        return
    cosv = (va.dot(vb)) / (na * nb)
    try:
        cv = float(cosv)
        if cv > 1: cv = 1
        elif cv < -1: cv = -1
        ang_val = float(acos(cv))
    except Exception:
        ang_val = acos(cosv)
    if _close(ang_val, expected):
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            eval_ = float(expected)
        except Exception:
            eval_ = expected
        print(f"[VERIFY FAIL] {tag}: angle={ang_val} != {eval_}")
`);
  pyodideReady = py;
  return py;
}

// 사용자 코드를 wrap — io.StringIO 로 sys.stdout/stderr 캡처.
// setStdout({batched}) 가 print() 의 줄바꿈을 보존 안 해서 모든 줄이 한 줄로
// 합쳐지는 버그 회피. buffer 값은 pyodide globals 로 노출 후 worker 가 추출.
function wrapForCapture(userCode) {
  // userCode 안에 triple-quoted string 충돌 방지 — exec(compile()) 패턴.
  // userCode 가 import, def, class 등 어떤 구문이든 동작하려면 dedent 그대로.
  return [
    'import sys as __sys',
    'import io as __io',
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
}

self.onmessage = async (e) => {
  const { id, type, code } = e.data;
  if (type === 'ping') {
    self.postMessage({ id, type: 'pong', ready: !!pyodideReady });
    return;
  }
  if (type !== 'run') return;
  try {
    const py = await init();
    py.globals.set('__user_code', code);
    try {
      await py.runPythonAsync(wrapForCapture());
      let stdout = py.globals.get('__captured_stdout') ?? '';
      let stderr = py.globals.get('__captured_stderr') ?? '';
      if (stdout.length > 4096) stdout = stdout.slice(0, 4096);
      const ok = !stderr.trim();
      self.postMessage({ id, ok, stdout, stderr });
    } catch (err) {
      self.postMessage({ id, ok: false, stderr: String(err.message ?? err) });
    }
  } catch (err) {
    self.postMessage({ id, ok: false, stderr: `[pyodide init] ${err.message ?? err}` });
  }
};
