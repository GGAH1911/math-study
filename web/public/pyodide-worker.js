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
    return tuple(d)   # ★2D 성분만 돌려주면 3D 이등분선이 조용히 납작해진다

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

def assert_on_circle(point, center, radius, tag, normal=None):
    """원 위인지. 3D 면 normal(평면 법선)을 같이 줘라.

    ★2D 식으로 3D 점을 재면 z 가 통째로 버려져 **조용히 틀린 [VERIFY OK]** 가 난다.
      2026-08-14 3D 기출 전수조사에서 2024 9월모평 기하 28·2025 수능 기하 27 두 건에서
      실제로 걸렸다(assert_distance 는 그날 고쳤는데 이 함수는 남아 있었다).
    ★3D 에서 '원' 은 중심·반지름만으로 정해지지 않는다 — 그 중심을 지나는 구면 전체가
      후보다. normal 을 주면 평면까지 함께 보고, 안 주면 거리만 본다."""
    d = _dist(point, center)
    if normal is not None and _close(d, radius):
        n = Matrix(list(normal))
        if not _close(n.dot(Matrix(list(point)) - Matrix(list(center))), 0):
            print(f"[VERIFY FAIL] {tag}: 반지름은 맞지만 원의 평면 밖")
            return
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

def assert_on_plane(point, plane_pts, tag):
    """point 가 plane_pts(세 점) 가 정하는 평면 위인지. 3D 작도에서 가장 자주 쓰는 검증이라
    ★따로 둔다 — 없으면 튜터가 이름을 지어내 NameError 로 계산이 통째로 날아간다."""
    assert_coplanar([plane_pts[0], plane_pts[1], plane_pts[2], point], tag)

def assert_perpendicular(p1, p2, q1, q2, tag):
    """두 선분(또는 벡터)이 수직인지 — 2D·3D 공통."""
    u = Matrix(p2) - Matrix(p1); v = Matrix(q2) - Matrix(q1)
    if u.norm() == 0 or v.norm() == 0:
        print(f"[VERIFY FAIL] {tag}: 길이 0 벡터"); return
    print(f"[VERIFY OK] {tag}" if _close(u.dot(v), 0)
          else f"[VERIFY FAIL] {tag}: 내적={float(u.dot(v))} != 0")

def assert_on_sphere(point, center, radius, tag):
    """점이 구면 위인지. assert_on_circle 과 헷갈리지 않게 이름을 따로 둔다."""
    assert_distance(point, center, radius, tag)

def _plane_normal(pts):
    o = Matrix(list(pts[0]))
    n = (Matrix(list(pts[1])) - o).cross(Matrix(list(pts[2])) - o)
    if n.norm() == 0:
        raise ValueError("_plane_normal: 세 점이 일직선")
    return o, n

def point_plane_distance(point, plane_pts):
    """점에서 평면(세 점)까지 거리 — 값을 그대로 돌려준다(print 안 함)."""
    o, n = _plane_normal(plane_pts)
    return abs(n.dot(Matrix(list(point)) - o)) / n.norm()

def assert_point_plane_distance(point, plane_pts, expected, tag):
    d = point_plane_distance(point, plane_pts)
    if _close(d, expected):
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            print(f"[VERIFY FAIL] {tag}: dist={float(d)} != {float(expected)}")
        except Exception:
            print(f"[VERIFY FAIL] {tag}: dist={d} != {expected}")

def assert_tangent_plane(center, radius, plane_pts, tag):
    """구(center, radius)가 평면에 **접하는지**. 공간도형에서 가장 자주 쓰는 조건인데
    없어서 매번 손으로 법선을 외적하던 것."""
    assert_point_plane_distance(center, plane_pts, radius, tag)

def assert_planes_perpendicular(plane1_pts, plane2_pts, tag):
    """두 평면이 수직인지(법선끼리 수직). '평면 ABH 와 평면 BCD 는 서로 수직' 같은 조건."""
    _, n1 = _plane_normal(plane1_pts)
    _, n2 = _plane_normal(plane2_pts)
    if _close(n1.dot(n2), 0):
        print(f"[VERIFY OK] {tag}")
    else:
        print(f"[VERIFY FAIL] {tag}: 법선 내적={float(n1.dot(n2))} != 0")

def point_line_distance(point, p1, p2):
    """점에서 직선까지 거리 — 2D·3D 공통(sympy Line 은 3D 도 받는다)."""
    return L(p1, p2).distance(Point(*point))

def assert_point_line_distance(point, p1, p2, expected, tag):
    d = point_line_distance(point, p1, p2)
    if _close(d, expected):
        print(f"[VERIFY OK] {tag}")
    else:
        try:
            print(f"[VERIFY FAIL] {tag}: dist={float(d)} != {float(expected)}")
        except Exception:
            print(f"[VERIFY FAIL] {tag}: dist={d} != {expected}")

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
