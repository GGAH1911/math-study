#!/usr/bin/env python3
"""고친 위젯 스펙이 **실제로 움직이고 깨지지 않는지** 결정적으로 검증한다.

★LLM 이 고친 것을 LLM 이 채점하면 같은 착각을 공유한다. 여기서는 계산으로만 판정한다.
사용: python3 scripts/ops/verify_widget_fix.py <file.json>   (exit 0=통과)
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/ops'))
from audit_widget_params import audit_one            # noqa: E402

NODE = r'''
const { readFileSync } = require('node:fs');
const math = require('/app/web/node_modules/mathjs');
const d = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const spec = d.spec, rec = d.recipe || {};
const res = (v, s) => (typeof v === 'string' && v.startsWith('='))
  ? math.evaluate(v.slice(1), s) : Array.isArray(v) ? v.map(x => res(x, s))
  : (v && typeof v === 'object') ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, res(x, s)])) : v;
const run = (params) => {
  const s = { ...params };
  for (const st of (spec.scope || '').split(';').map(x => x.trim()).filter(Boolean)) math.evaluate(st, s);
  return s;
};
const out = { errors: [], visualVaries: {} };
// ① 샘플·오라클에서 scope 가 터지지 않는가
const samples = (rec.samples && rec.samples.length ? rec.samples
  : [Object.fromEntries((spec.params || []).map(p => [p.name, p.init]))]);
for (const smp of samples) { try { run(smp); } catch (e) { out.errors.push('scope: ' + e.message); } }
// ② 오라클 일치
for (const o of (rec.oracle || [])) {
  try { const s = run(o.params);
    for (const [k, want] of Object.entries(o.expect || {}))
      if (Math.abs(Number(s[k]) - Number(want)) > (rec.tol ?? 1e-6)) out.errors.push(`oracle ${k}: ${s[k]} != ${want}`);
  } catch (e) { out.errors.push('oracle: ' + e.message); }
}
// ③ ★각 파라미터를 흔들면 **그림 산출물**이 실제로 달라지는가
const base = Object.fromEntries((spec.params || []).map(p => [p.name, p.init]));
// ★fns 의 식은 `=` 접두사가 없다 — function-plot 에 scope 를 주입해 평가된다.
//   문자열 그대로 비교하면 파라미터가 곡선을 움직여도 "안 변했다" 로 나온다(거짓 실패).
//   그래서 **여러 x 에서 실제로 값을 계산해** 비교한다.
const SAMPLE_X = [-2.5, -1.3, -0.4, 0.35, 1.1, 2.2, 3.7];
const visualOf = (params) => {
  const s = run(params);
  const v = {};
  for (const k of ['plot', 'geometry', 'geometry3d']) if (spec[k]) v[k] = res(spec[k], s);
  const curves = [];
  for (const f of (spec.plot?.fns || [])) {
    const row = [];
    for (const x of SAMPLE_X) {
      let y; try { y = math.evaluate(String(f.fn), { ...s, x }); } catch { y = 'ERR'; }
      row.push(typeof y === 'number' && Number.isFinite(y) ? Math.round(y * 1e6) / 1e6 : String(y));
    }
    curves.push(row);
  }
  return JSON.stringify({ v, curves });
};
let ref; try { ref = visualOf(base); } catch (e) { out.errors.push('visual: ' + e.message); }
for (const p of (spec.params || [])) {
  // ★한 값만 흔들면 **우연히 같은 결과**가 나올 수 있다(실측: 1/2+1/2 와 1/2÷1/2 가 둘 다 1
  //   이라 op 를 1→4 로 바꿔도 그림이 같았다). 여러 값을 시도해 하나라도 달라지면 살아 있다.
  const lo = p.min ?? -1, hi = p.max ?? 1, st = p.step || (hi - lo) / 8 || 1;
  const cand = [];
  for (let v = lo; v <= hi + 1e-9; v += st) { cand.push(v); if (cand.length > 40) break; }
  if (!cand.length) cand.push(lo, hi);
  let varies = false;
  for (const v of cand) {
    if (v === base[p.name]) continue;
    try { if (visualOf({ ...base, [p.name]: v }) !== ref) { varies = true; break; } }
    catch (e) { out.errors.push(`visual(${p.name}): ${e.message}`); break; }
  }
  out.visualVaries[p.name] = varies;
}
console.log(JSON.stringify(out));
'''


def main() -> int:
    f = Path(sys.argv[1]).resolve()
    (ROOT / 'web/scripts/_wverify.cjs').write_text(NODE, encoding='utf-8')
    rel = '/app/' + str(f.relative_to(ROOT))
    r = subprocess.run(['docker', 'compose', '-f', str(ROOT / 'deploy/docker-compose.yml'),
                        'exec', '-T', 'web', 'node', 'scripts/_wverify.cjs', rel],
                       capture_output=True, text=True, cwd=ROOT, stdin=subprocess.DEVNULL, timeout=120)
    try:
        out = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        print(f'❌ 실행 실패: {r.stdout[:120]} {r.stderr[:200]}'); return 1
    still = audit_one(f)
    ok = True
    if out['errors']:
        ok = False; [print('  ❌', e) for e in out['errors'][:5]]
    dead = [p for p, v in out['visualVaries'].items() if not v]
    if dead:
        ok = False; print(f'  ❌ 그림이 안 변하는 파라미터: {dead}')
    if still and still.get('blind'):
        ok = False; print(f"  ❌ 정적 감사 잔존: {still['blind']}")
    print('✅ 통과' if ok else '🔴 실패')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
