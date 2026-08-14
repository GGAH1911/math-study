import type { APIRoute } from 'astro';
import { spawn } from 'node:child_process';
import { resolve } from 'node:path';

export const prerender = false;

const VENV_PYTHON = resolve(process.cwd(), '..', '.venv', 'bin', 'python');
const MAX_OUTPUT = 4096;
const TIMEOUT_MS = 10_000;

const HEADER = `import sympy
from sympy import Symbol, symbols, solve, simplify, expand, factor, diff, integrate, limit, Sum, Product, oo, pi, E, I, sqrt, sin, cos, tan, log, ln, exp, Matrix, Rational, S, Point, Line, Segment, Ray, nsimplify
x, y, z, n, k, t, a, b, c = symbols('x y z n k t a b c')

# --- geom helpers — 작도 검증·교점·이등분선 표준화 ---
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

def assert_distance3d(p1, p2, expected, tag):
    """3D 거리 검증. 이름만 다르고 assert_distance 와 동작이 같다 —
    튜터 프롬프트(geometry3d STEP B)가 이 이름을 쓰라고 지시하기 때문에 존재해야 한다."""
    assert_distance(p1, p2, expected, tag)

def assert_coplanar(pts, tag):
    """네 점 이상이 한 평면에 있는지. 공간도형 작도에서 밑면·단면이 뒤틀리는 사고를 잡는다."""
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
    # clamp numerical noise
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
`;

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
