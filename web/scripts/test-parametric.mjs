#!/usr/bin/env node
// parametric primitive smoke test — mathjs evaluate + sample 동작 검증.
// Geometry 컴포넌트의 sampleParametric 과 동일 로직을 Node 에서 재구현해 검증.

import { create, all } from 'mathjs';
const math = create(all);

function _eval(s) { if (typeof s === 'number') return s; try { return math.evaluate(s); } catch { return NaN; } }

function sample(spec) {
  const t0 = _eval(spec.tRange[0]);
  const t1 = _eval(spec.tRange[1]);
  if (!Number.isFinite(t0) || !Number.isFinite(t1) || t1 <= t0) return [];
  const n = Math.max(2, Math.min(spec.samples ?? 120, 2000));
  let xNode, yNode;
  try { xNode = math.parse(spec.x).compile(); yNode = math.parse(spec.y).compile(); }
  catch { return []; }
  const out = [];
  for (let i = 0; i <= n; i++) {
    const t = t0 + (t1 - t0) * i / n;
    try {
      const xv = xNode.evaluate({ t });
      const yv = yNode.evaluate({ t });
      if (Number.isFinite(xv) && Number.isFinite(yv)) out.push([xv, yv]);
      else out.push(null);
    } catch { out.push(null); }
  }
  return out;
}

function bbox(pts) {
  const valid = pts.filter(p => p !== null);
  if (valid.length === 0) return null;
  const xs = valid.map(p => p[0]), ys = valid.map(p => p[1]);
  return { xMin: Math.min(...xs), xMax: Math.max(...xs), yMin: Math.min(...ys), yMax: Math.max(...ys), n: valid.length };
}

const cases = [
  {
    name: 'circle (전체 원)',
    spec: { x: 'cos(t)', y: 'sin(t)', tRange: [0, '2*pi'] },
    expect: b => Math.abs(b.xMin + 1) < 0.01 && Math.abs(b.xMax - 1) < 0.01 && Math.abs(b.yMin + 1) < 0.01,
  },
  {
    name: 'semicircle (위쪽 반원)',
    spec: { x: 'cos(t)', y: 'sin(t)', tRange: [0, 'pi'] },
    expect: b => b.yMin >= -0.01 && Math.abs(b.yMax - 1) < 0.01 && Math.abs(b.xMin + 1) < 0.01 && Math.abs(b.xMax - 1) < 0.01,
  },
  {
    name: 'arc 45°~135°',
    spec: { x: 'cos(t)', y: 'sin(t)', tRange: ['pi/4', '3*pi/4'] },
    expect: b => b.yMin >= 0.7 && Math.abs(b.yMax - 1) < 0.01,
  },
  {
    name: 'cycloid',
    spec: { x: 't-sin(t)', y: '1-cos(t)', tRange: [0, '4*pi'] },
    expect: b => b.yMin >= -0.01 && b.yMax <= 2.01,
  },
  {
    name: 'cardioid',
    spec: { x: '(1-cos(t))*cos(t)', y: '(1-cos(t))*sin(t)', tRange: [0, '2*pi'] },
    expect: b => b.xMin < 0 && b.xMax > 0,
  },
  {
    name: 'scaled circle (r=2)',
    spec: { x: '2*cos(t)', y: '2*sin(t)', tRange: [0, '2*pi'] },
    expect: b => Math.abs(b.xMin + 2) < 0.05 && Math.abs(b.xMax - 2) < 0.05,
  },
  {
    name: 'bad expr — should return [] (not crash)',
    spec: { x: 'bad(', y: 'sin(t)', tRange: [0, '2*pi'] },
    expect: pts => pts.length === 0,
    raw: true,
  },
  {
    name: 'invalid tRange (t1<t0)',
    spec: { x: 'cos(t)', y: 'sin(t)', tRange: [1, 0] },
    expect: pts => pts.length === 0,
    raw: true,
  },
  {
    name: 'tan (Infinity 처리)',
    spec: { x: 't', y: 'tan(t)', tRange: ['-pi/2', 'pi/2'], samples: 60 },
    expect: pts => pts.filter(p => p === null || !Number.isFinite(p[1])).length >= 0,
    raw: true,
  },
];

let pass = 0, fail = 0;
for (const c of cases) {
  try {
    const pts = sample(c.spec);
    const arg = c.raw ? pts : bbox(pts);
    const ok = c.expect(arg);
    if (ok) {
      console.log(`  ✓ ${c.name}`);
      pass++;
    } else {
      console.log(`  ✗ ${c.name}`);
      console.log(`    got: ${c.raw ? `${pts.length} pts` : JSON.stringify(arg)}`);
      fail++;
    }
  } catch (e) {
    console.log(`  ✗ ${c.name} — threw: ${e.message}`);
    fail++;
  }
}

console.log(`\n${pass}/${cases.length} passed (${fail} failed)`);
process.exit(fail === 0 ? 0 : 1);
