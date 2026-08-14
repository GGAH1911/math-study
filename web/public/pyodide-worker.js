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
  // HEADER inject — 자주 쓰는 sympy 심볼 자동 import
// ★★이 헤더는 `web/src/pages/api/sympy.ts` 의 **복사본**이다. 한쪽만 고치면 브라우저와
//   서버가 다른 함수를 갖게 되고, 브라우저가 1차이므로 **서버만 고치면 사용자에겐 아무
//   변화가 없다**(2026-08-14 실제로 그랬다 — 3D 작도가 여전히 막혀 있었다).
//   둘의 동기화는 `scripts/ops/verify_sympy_header_sync.py` 가 검사한다.
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

def _dist(p1, p2):
    """차원 무관 거리. ★2D 식으로 3D 점을 재면 z 가 버려져 **거리가 0 으로 나온다**
    (2026-08-14 실측: |(0,0,4)-(0,0,1)| 이 0.0). 그래서 짧은 쪽에 맞춰 전 성분을 쓴다."""
    n = min(len(p1), len(p2))
    return sqrt(sum((p1[i]-p2[i])**2 for i in range(n)))

def assert_distance(p1, p2, expected, tag):
    d = _dist(p1, p2)
    if _close(d, expected):
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            dval = float(d); eval_ = float(expected)
        except Exception:
            dval, eval_ = d, expected
        print(f"[VERIFY FAIL] {tag}: |{p1}-{p2}|={dval} != {eval_}")

def _seg(p1, p2):
    return Segment(Point(*p1), Point(*p2))

def assert_segments_cross(p1, p2, q1, q2, tag):
    """선분 p1p2 와 q1q2 가 실제로 만나는지 — "~가 ~와 만나도록" 조건 검증."""
    if _seg(p1, p2).intersection(_seg(q1, q2)):
        print(f"[VERIFY OK] {tag}")
    else:
        print(f"[VERIFY FAIL] {tag}: segments {tuple(p1)}-{tuple(p2)} & {tuple(q1)}-{tuple(q2)} do NOT meet")

def assert_segments_disjoint(p1, p2, q1, q2, tag):
    """선분 p1p2 와 q1q2 가 안 만나는지 — "~가 ~와 만나지 않도록" 조건 검증.
    등비급수 자기닮음 도형에서 새 단계 직사각형의 방향(부호)을 직격으로 잡는다."""
    inter = _seg(p1, p2).intersection(_seg(q1, q2))
    if not inter:
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            where = [(float(o.x), float(o.y)) for o in inter if hasattr(o, 'x')] or inter
        except Exception:
            where = inter
        print(f"[VERIFY FAIL] {tag}: segments {tuple(p1)}-{tuple(p2)} & {tuple(q1)}-{tuple(q2)} MEET at {where}")
\`;

type RunRequest = { code: string };

export const POST: APIRoute = async ({ request }) => {
  let body: RunRequest;
  try { body = await request.json(); }
  catch { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400 }); }

  const code = (body.code ?? '').trim();
  if (!code) return new Response(JSON.stringify({ error: 'empty code' }), { status: 400 });
  if (code.length > 4000) return new Response(JSON.stringify({ error: 'code too long' }), { status: 400 });

  // ★샌드박싱(2026-06): sympy 계산 외 위험 토큰 차단 — 임의 코드실행·파일/네트워크/내부 접근 방지.
  //   HEADER가 필요한 심볼·헬퍼를 모두 제공하므로 사용자 코드엔 import·시스템 접근이 불필요하다.
  if (/__|\b(import|os|sys|subprocess|socket|shutil|importlib|pickle|marshal|ctypes|eval|exec|compile|open|input|globals|locals|getattr|setattr|delattr|breakpoint|exit|quit)\b/.test(code)) {
    return new Response(JSON.stringify({ error: 'disallowed token (sympy 계산만 허용)' }), { status: 400 });
  }

  return new Promise<Response>((resolveResp) => {
    const child = spawn(VENV_PYTHON, ['-c', HEADER + code], {
      // ★최소 env — process.env(DATABASE_URL·세션시크릿·OAuth토큰) 상속 금지(코드가 os.environ 못 읽게 이중방어).
      env: { PYTHONIOENCODING: 'utf-8', PATH: '/usr/bin:/bin', HOME: '/tmp', LANG: 'C.UTF-8' },
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let stdout = '';
    let stderr = '';
    let truncated = false;
    const onChunk = (s: string) => (chunk: Buffer) => {
      const t = chunk.toString('utf-8');
      if (s === 'out') {
        if (stdout.length + t.length > MAX_OUTPUT) { stdout += t.slice(0, MAX_OUTPUT - stdout.length); truncated = true; }
        else stdout += t;
      } else {
        if (stderr.length + t.length > MAX_OUTPUT) { stderr += t.slice(0, MAX_OUTPUT - stderr.length); truncated = true; }
        else stderr += t;
      }
    };
    child.stdout.on('data', onChunk('out'));
    child.stderr.on('data', onChunk('err'));

    const killer = setTimeout(() => { child.kill('SIGKILL'); }, TIMEOUT_MS);

    child.on('close', (code) => {
      clearTimeout(killer);
      resolveResp(new Response(JSON.stringify({
        ok: code === 0,
        exit_code: code,
        stdout: stdout.trim(),
        stderr: stderr.trim(),
        truncated,
      }), { status: 200, headers: { 'Content-Type': 'application/json' } }));
    });
    child.on('error', (e) => {
      clearTimeout(killer);
      resolveResp(new Response(JSON.stringify({ ok: false, error: e.message }), { status: 500 }));
    });
  });
};

def assert_distance3d(p1, p2, expected, tag):
    """3D 거리 검증. 튜터 프롬프트(geometry3d STEP B)가 이 이름을 쓰라고 지시한다."""
    assert_distance(p1, p2, expected, tag)

def assert_coplanar(pts, tag):
    """네 점 이상이 한 평면에 있는지. 공간도형 밑면·단면이 뒤틀리는 사고를 잡는다."""
    if len(pts) < 4:
        print(f"[VERIFY OK] {tag}"); return
    o = Matrix(pts[0])
    v1 = Matrix(pts[1]) - o; v2 = Matrix(pts[2]) - o
    n = v1.cross(v2)
    if n.norm() == 0:
        print(f"[VERIFY FAIL] {tag}: 처음 세 점이 일직선"); return
    for q in pts[3:]:
        if not _close(n.dot(Matrix(q) - o), 0):
            print(f"[VERIFY FAIL] {tag}: {q} 가 평면 밖"); return
    print(f"[VERIFY OK] {tag}")

def assert_perpendicular(p1, p2, q1, q2, tag):
    """두 선분(또는 벡터)이 수직인지 — 2D·3D 공통."""
    u = Matrix(p2) - Matrix(p1); v = Matrix(q2) - Matrix(q1)
    if u.norm() == 0 or v.norm() == 0:
        print(f"[VERIFY FAIL] {tag}: 길이 0 벡터"); return
    print(f"[VERIFY OK] {tag}" if _close(u.dot(v), 0)
          else f"[VERIFY FAIL] {tag}: 내적={float(u.dot(v))} != 0")

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
