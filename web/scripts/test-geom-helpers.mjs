#!/usr/bin/env node
// geom helper smoke test — /api/sympy 가 작도 헬퍼 (L, intersect, angle_bisector_dir,
// assert_on_line, assert_on_circle, assert_distance) 를 자동 주입했는지 확인.
//
// 사용: web/ 디렉토리에서 `node scripts/test-geom-helpers.mjs`
// (dev 서버가 127.0.0.1:4321 에 떠 있어야 함)

const BASE = process.env.SYMPY_BASE ?? 'http://127.0.0.1:4321';

const cases = [
  {
    name: 'angle_bisector_dir 직각 (1,0)·(0,1) → (√2/2, √2/2)',
    code: `bd = angle_bisector_dir((0,0), (1,0), (0,1))
print("bd =", (float(bd[0]), float(bd[1])))`,
    expect: /bd = \(0\.7071[0-9]+, 0\.7071[0-9]+\)/,
  },
  {
    name: 'assert_on_line OK',
    code: `assert_on_line((0.5, 0.5), (0,0), (1,1), "diag")`,
    expect: /\[VERIFY OK\] diag/,
  },
  {
    name: 'assert_on_line FAIL',
    code: `assert_on_line((0.5, 0.6), (0,0), (1,1), "diag2")`,
    expect: /\[VERIFY FAIL\] diag2/,
  },
  {
    name: 'assert_on_circle OK (unit circle)',
    code: `from sympy import cos, sin, pi
P = (float(cos(pi/4)), float(sin(pi/4)))
assert_on_circle(P, (0,0), 1, "P unit")`,
    expect: /\[VERIFY OK\] P unit/,
  },
  {
    name: 'intersect(L, L)',
    code: `pts = intersect(L((0,0),(2,2)), L((0,2),(2,0)))
print("X =", (float(pts[0].x), float(pts[0].y)))`,
    expect: /X = \(1\.0, 1\.0\)/,
  },
  {
    name: 'assert_distance OK',
    code: `assert_distance((0,0), (3,4), 5, "3-4-5")`,
    expect: /\[VERIFY OK\] 3-4-5/,
  },
];

let pass = 0, fail = 0;
for (const c of cases) {
  try {
    const res = await fetch(`${BASE}/api/sympy`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: c.code }),
    });
    const json = await res.json();
    const out = (json.stdout ?? '') + '\n' + (json.stderr ?? '');
    if (c.expect.test(out)) {
      console.log(`  ✓ ${c.name}`);
      pass++;
    } else {
      console.log(`  ✗ ${c.name}`);
      console.log(`    expected ${c.expect}`);
      console.log(`    got:\n${out.split('\n').map(l => '      ' + l).join('\n')}`);
      fail++;
    }
  } catch (e) {
    console.log(`  ✗ ${c.name} — fetch failed: ${e.message}`);
    fail++;
  }
}

console.log(`\n${pass}/${cases.length} passed (${fail} failed)`);
process.exit(fail === 0 ? 0 : 1);
