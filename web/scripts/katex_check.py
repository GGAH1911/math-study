#!/usr/bin/env python3
# 풀이 step을 **우리 실제 렌더러 SSOT**(src/lib/katex-normalize.mjs renderMathSegments)로 검증.
# SolutionPanel 경로 그대로: '**' 제거 → '\n' 분리 → 각 줄을 renderMathSegments(line, katex, {display:true}).
# renderMathSegments는 throwOnError시 원본 `$...$`로 폴백 → 출력에 '$'가 남으면 = 페이지에 raw 누출(렌더실패).
import glob, re, yaml, json, subprocess
REPO = '/home/insung/Projects/math-study'
steps = []
for md in glob.glob(f'{REPO}/docs/problems/**/*.md', recursive=True):
    t = open(md, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', t, re.S)
    if not m:
        continue
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception:
        continue
    if not fm or not fm.get('solution'):
        continue
    slug = md.split('/')[-1][:-3]
    for i, s in enumerate(fm['solution'].get('steps') or []):
        if isinstance(s, str) and '$' in s:
            steps.append({'slug': slug, 'i': i, 's': s})
json.dump(steps, open('/tmp/steps.json', 'w'), ensure_ascii=False)
NODE = r'''
import { renderMathSegments } from '%s/web/src/lib/katex-normalize.mjs';
import katex from 'katex';
import fs from 'fs';
const steps = JSON.parse(fs.readFileSync('/tmp/steps.json'));
const fails = [];
for (const x of steps) {
  const lines = x.s.replace(/\*\*(.+?)\*\*/g, '$1').split('\n').filter(l => l.trim());
  for (const line of lines) {
    let out;
    try { out = renderMathSegments(line, katex, { display: true }); }
    catch (e) { fails.push({ slug: x.slug, i: x.i, line: line.slice(0, 60), err: 'throw:' + e.message.slice(0, 40) }); continue; }
    if (out.includes('$')) fails.push({ slug: x.slug, i: x.i, line: line.slice(0, 70), err: 'fallback(raw 누출)' });
  }
}
console.log('SSOT 검증: ' + steps.length + ' step($포함) · 렌더실패(raw 누출) ' + fails.length);
for (const f of fails.slice(0, 40)) console.log('  [' + f.slug + '][step' + f.i + '] ' + f.line + ' → ' + f.err);
fs.writeFileSync('/tmp/ssot_fails.json', JSON.stringify(fails));
''' % REPO
subprocess.run(['node', '--input-type=module', '-e', NODE], cwd=f'{REPO}/web')
