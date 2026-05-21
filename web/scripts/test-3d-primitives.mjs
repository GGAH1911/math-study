#!/usr/bin/env node
// 3D primitive smoke test — Geometry3D 의 sampleSurface/sampleCurve 헬퍼 로직을
// Node 에서 재구현하고 mathjs evaluate + bbox 산출 동작 검증.

import { create, all } from 'mathjs';
const math = create(all);
const _eval = s => (typeof s === 'number' ? s : (() => { try { return math.evaluate(s); } catch { return NaN; } })());

function sampleSurface({ x, y, z, uRange, vRange, uSamples = 16, vSamples = 16 }) {
  const u0 = _eval(uRange[0]), u1 = _eval(uRange[1]);
  const v0 = _eval(vRange[0]), v1 = _eval(vRange[1]);
  if (![u0, u1, v0, v1].every(Number.isFinite)) return [];
  let xN, yN, zN;
  try { xN = math.parse(x).compile(); yN = math.parse(y).compile(); zN = math.parse(z).compile(); } catch { return []; }
  const out = [];
  for (let i = 0; i <= uSamples; i++) for (let j = 0; j <= vSamples; j++) {
    const u = u0 + (u1 - u0) * i / uSamples;
    const v = v0 + (v1 - v0) * j / vSamples;
    try {
      const xv = xN.evaluate({ u, v }), yv = yN.evaluate({ u, v }), zv = zN.evaluate({ u, v });
      if (Number.isFinite(xv) && Number.isFinite(yv) && Number.isFinite(zv)) out.push([xv, yv, zv]);
    } catch { /* skip */ }
  }
  return out;
}

function sampleCurve({ x, y, z, tRange, samples = 200 }) {
  const t0 = _eval(tRange[0]), t1 = _eval(tRange[1]);
  if (!Number.isFinite(t0) || !Number.isFinite(t1) || t1 <= t0) return [];
  let xN, yN, zN;
  try { xN = math.parse(x).compile(); yN = math.parse(y).compile(); zN = math.parse(z).compile(); } catch { return []; }
  const out = [];
  for (let i = 0; i <= samples; i++) {
    const t = t0 + (t1 - t0) * i / samples;
    try {
      const xv = xN.evaluate({ t }), yv = yN.evaluate({ t }), zv = zN.evaluate({ t });
      if (Number.isFinite(xv) && Number.isFinite(yv) && Number.isFinite(zv)) out.push([xv, yv, zv]);
    } catch { /* skip */ }
  }
  return out;
}

function bbox(pts) {
  if (pts.length === 0) return null;
  const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]), zs = pts.map(p => p[2]);
  return {
    xMin: Math.min(...xs), xMax: Math.max(...xs),
    yMin: Math.min(...ys), yMax: Math.max(...ys),
    zMin: Math.min(...zs), zMax: Math.max(...zs),
    n: pts.length,
  };
}

const tests = [
  {
    name: '구면 (반지름 1)',
    fn: () => sampleSurface({ x: 'sin(u)*cos(v)', y: 'sin(u)*sin(v)', z: 'cos(u)', uRange: [0, 'pi'], vRange: [0, '2*pi'] }),
    check: b => Math.abs(b.xMin + 1) < 0.05 && Math.abs(b.xMax - 1) < 0.05 && Math.abs(b.zMin + 1) < 0.05 && Math.abs(b.zMax - 1) < 0.05,
  },
  {
    name: '회전체 y=x² (x ∈ [0,1])',
    fn: () => sampleSurface({ x: 'u', y: 'u^2*cos(v)', z: 'u^2*sin(v)', uRange: [0, 1], vRange: [0, '2*pi'] }),
    check: b => b.xMin >= -0.01 && b.xMax <= 1.01 && Math.abs(b.yMin + 1) < 0.05 && Math.abs(b.yMax - 1) < 0.05,
  },
  {
    name: 'helix (헬릭스)',
    fn: () => sampleCurve({ x: 'cos(t)', y: 'sin(t)', z: 't/(2*pi)', tRange: [0, '4*pi'] }),
    check: b => b.zMin >= -0.01 && b.zMax <= 2.01,
  },
  {
    name: '원기둥 surface',
    fn: () => sampleSurface({ x: 'cos(v)', y: 'sin(v)', z: 'u', uRange: [0, 2], vRange: [0, '2*pi'] }),
    check: b => Math.abs(b.xMin + 1) < 0.05 && Math.abs(b.xMax - 1) < 0.05 && b.zMin >= -0.01 && b.zMax <= 2.01,
  },
  {
    name: 'bad surface expr — empty',
    fn: () => sampleSurface({ x: 'bad(', y: 'v', z: 'u', uRange: [0, 1], vRange: [0, 1] }),
    check: () => true,
    raw: pts => pts.length === 0,
  },
  {
    name: 'invalid tRange (t1<t0)',
    fn: () => sampleCurve({ x: 't', y: 't', z: 't', tRange: [1, 0] }),
    check: () => true,
    raw: pts => pts.length === 0,
  },
];

let pass = 0, fail = 0;
for (const t of tests) {
  try {
    const pts = t.fn();
    if (t.raw) {
      if (t.raw(pts)) { console.log(`  ✓ ${t.name}`); pass++; }
      else { console.log(`  ✗ ${t.name} — got ${pts.length} pts`); fail++; }
      continue;
    }
    const b = bbox(pts);
    if (b && t.check(b)) { console.log(`  ✓ ${t.name} (n=${b.n})`); pass++; }
    else {
      console.log(`  ✗ ${t.name}`);
      console.log(`    bbox: ${JSON.stringify(b)}`);
      fail++;
    }
  } catch (e) {
    console.log(`  ✗ ${t.name} — threw: ${e.message}`);
    fail++;
  }
}
console.log(`\n${pass}/${tests.length} passed (${fail} failed)`);
process.exit(fail === 0 ? 0 : 1);
