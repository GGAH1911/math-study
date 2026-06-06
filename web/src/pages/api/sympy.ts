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

  return new Promise<Response>((resolveResp) => {
    const child = spawn(VENV_PYTHON, ['-c', HEADER + code], {
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
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
