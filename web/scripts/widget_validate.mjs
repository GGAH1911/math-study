#!/usr/bin/env node
// InteractiveSpec 검증기 (블루프린트 §3 ③수학게이트의 린치핀).
//   입력: spec(JSON) + recipe { samples:[{param:val}], invariants:["식≈0"], oracle:[{params,expect:{var:val}}], tol }
//   방식: 샘플 슬라이더값에서 spec.scope 평가 → ① 모든 readout·shape 좌표 finite ② 불변식 ≈0 ③ 오라클 대조.
//   하나라도 어긋나면 reject(정답의 hard-stop). gemma 아닌 결정적 수치 검증 — LLM 노이즈 0.
//   ★카나리아: --canary 로 정답spec 통과 & 깨진spec reject 확인(검증기 자가진단). 실패=검증기 고장.
// 사용: node web/scripts/widget_validate.mjs <specFile> <recipeFile>   |   --canary
import { readFileSync } from 'node:fs';
import { create, all } from 'mathjs';
const math = create(all);

// "=expr" 또는 expr 문자열을 scope로 평가. 배열/객체는 재귀. 일반값은 그대로.
function resolve(v, scope) {
  if (typeof v === 'string' && v.startsWith('=')) { try { return math.evaluate(v.slice(1), scope); } catch { return NaN; } }
  if (Array.isArray(v)) return v.map((x) => resolve(x, scope));
  if (v && typeof v === 'object') { const o = {}; for (const [k, x] of Object.entries(v)) o[k] = resolve(x, scope); return o; }
  return v;
}
function allFinite(v) {
  if (typeof v === 'number') return Number.isFinite(v);
  if (Array.isArray(v)) return v.every(allFinite);
  if (v && typeof v === 'object') return Object.values(v).every(allFinite);
  return true; // 비수치(문자열 라벨 등)는 통과
}

export function validate(spec, recipe) {
  const fails = [];
  const tol = recipe.tol ?? 1e-6;
  const samples = (recipe.samples && recipe.samples.length) ? recipe.samples : [{}];
  for (const sample of samples) {
    const tag = JSON.stringify(sample);
    const scope = {};
    for (const p of spec.params || []) scope[p.name] = sample[p.name] ?? p.init;
    // scope preamble
    for (const stmt of (spec.scope || '').split(';')) { const s = stmt.trim(); if (!s) continue; try { math.evaluate(s, scope); } catch (e) { fails.push(`scope '${s}' @${tag}: ${e.message}`); } }
    // readout finite
    for (const r of spec.readout || []) { try { const val = math.evaluate(r.expr, scope); if (!Number.isFinite(val)) fails.push(`readout '${r.label}'=${val} @${tag}`); } catch (e) { fails.push(`readout '${r.label}' @${tag}: ${e.message}`); } }
    // geometry/plot/3d shape 좌표 finite
    for (const blk of [spec.geometry, spec.geometry3d]) {
      for (const sh of blk?.shapes || []) { const r = resolve(sh, scope); if (!allFinite(r)) fails.push(`shape ${sh.type || '?'} non-finite @${tag}`); }
    }
    // 불변식 ≈ 0
    for (const inv of recipe.invariants || []) { try { const val = math.evaluate(inv, scope); if (!Number.isFinite(val) || Math.abs(val) > tol) fails.push(`불변식 |${inv}|=${val} > ${tol} @${tag}`); } catch (e) { fails.push(`불변식 '${inv}' @${tag}: ${e.message}`); } }
    // 오라클(독립 유도값) 대조
    for (const o of recipe.oracle || []) {
      const s2 = {}; for (const p of spec.params || []) s2[p.name] = (o.params || {})[p.name] ?? p.init;
      for (const stmt of (spec.scope || '').split(';')) { const s = stmt.trim(); if (s) try { math.evaluate(s, s2); } catch {} }
      for (const [v, exp] of Object.entries(o.expect || {})) { try { const got = math.evaluate(v, s2); if (!Number.isFinite(got) || Math.abs(got - exp) > tol) fails.push(`오라클 ${v}=${got} ≠ ${exp} @${JSON.stringify(o.params)}`); } catch (e) { fails.push(`오라클 '${v}': ${e.message}`); } }
    }
  }
  return { ok: fails.length === 0, fails };
}

// ── 카나리아: 검증기 자가진단 ──
const GOOD = { params: [{ name: 'theta', type: 'slider', min: 0, max: 360, init: 30, step: 1 }], scope: 'rad = theta*pi/180; cx = cos(rad); sy = sin(rad)', geometry: { shapes: [{ type: 'point', at: ['=cx', '=sy'] }, { type: 'segment', from: [0, 0], to: ['=cx', '=sy'] }] }, readout: [{ label: 'sin', expr: 'sy' }, { label: 'cos', expr: 'cx' }] };
const BROKEN = { ...GOOD, scope: 'rad = theta*pi/180; cx = cos(rad); sy = 2*sin(rad)' }; // sy 2배 → 단위원 이탈
const RECIPE = { samples: [{ theta: 30 }, { theta: 135 }, { theta: 200 }, { theta: 312 }], invariants: ['cx^2 + sy^2 - 1'], oracle: [{ params: { theta: 30 }, expect: { sy: 0.5 } }, { params: { theta: 90 }, expect: { sy: 1, cx: 0 } }], tol: 1e-6 };

function canary() {
  const g = validate(GOOD, RECIPE), b = validate(BROKEN, RECIPE);
  const pass = g.ok && !b.ok;
  console.log(`카나리아: 정답spec ${g.ok ? '✓통과' : '✗실패(' + g.fails[0] + ')'} · 깨진spec ${!b.ok ? '✓reject(' + b.fails[0].slice(0, 50) + ')' : '✗오통과!'}`);
  console.log(pass ? '✅ 검증기 정상 — 큐 처리 가능' : '🛑 검증기 고장 — HALT (큐 처리 금지)');
  process.exit(pass ? 0 : 1);
}

const argv = process.argv.slice(2);
if (argv[0] === '--canary') canary();
else if (argv.length >= 2) {
  const r = validate(JSON.parse(readFileSync(argv[0], 'utf8')), JSON.parse(readFileSync(argv[1], 'utf8')));
  console.log(r.ok ? '✓ PASS' : '✗ FAIL\n' + r.fails.map((f) => '  - ' + f).join('\n'));
  process.exit(r.ok ? 0 : 1);
} else { console.log('사용: --canary | <specFile> <recipeFile>'); process.exit(2); }
