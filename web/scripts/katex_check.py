#!/usr/bin/env python3
# 모든 풀이 step의 $-세그먼트를 실제 KaTeX 엔진으로 렌더 검증. 실패분 리포트(/tmp/katex_fails.json).
# LaTeX 문법만으론 부족 — KaTeX는 부분집합이라 ½/¼·_\min 같은 건 LaTeX OK여도 KaTeX 실패.
import glob, re, yaml, json, subprocess
REPO = '/home/insung/Projects/math-study'
segs = []
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
        if not isinstance(s, str) or '$' not in s:
            continue
        disp = re.findall(r'\$\$(.+?)\$\$', s, re.S)
        inl = re.findall(r'\$([^$]+)\$', re.sub(r'\$\$.+?\$\$', '', s, flags=re.S))
        for seg in disp + inl:
            if seg.strip():
                segs.append({'slug': slug, 'i': i, 'seg': seg})
json.dump(segs, open('/tmp/katex_segs.json', 'w'), ensure_ascii=False)
NODE = r'''
const katex=require('katex'),fs=require('fs');
const segs=JSON.parse(fs.readFileSync('/tmp/katex_segs.json'));
let w=[];const o=console.warn;console.warn=(m)=>w.push(String(m).slice(0,50));
const fails=[];
for(const x of segs){try{katex.renderToString(x.seg,{throwOnError:true,strict:false});}catch(e){fails.push({...x,err:e.message.split('\n')[0].replace('KaTeX parse error: ','').slice(0,60)});}}
console.warn=o;
console.log('KaTeX 검증: '+segs.length+'세그 · 하드실패 '+fails.length+' · 경고 '+[...new Set(w)].length);
for(const f of fails.slice(0,40)) console.log('  FAIL ['+f.slug+'][step'+f.i+'] '+f.seg.slice(0,55)+' → '+f.err);
fs.writeFileSync('/tmp/katex_fails.json',JSON.stringify(fails));
'''
subprocess.run(['node', '-e', NODE], cwd=f'{REPO}/web')
