#!/usr/bin/env python3
# 풀이 step LaTeX 변환 적용 — /tmp/conversions.json([{slug,i,latex}])을 읽어 해당 step 교체.
# steps 블록만 재직렬화(json.dumps 이스케이프), yaml 재파싱 검증 후 기록.
import glob, re, yaml, json, sys
REPO='/home/insung/Projects/math-study'
conv=json.load(open('/tmp/conversions.json'))
by_slug={}
for c in conv: by_slug.setdefault(c['slug'],{})[c['i']]=c['latex']
done=0; failed=[]
for slug,fixes in by_slug.items():
    g=glob.glob(f'{REPO}/docs/problems/**/{slug}.md',recursive=True)
    if not g: failed.append((slug,'NF')); continue
    md=g[0]; raw=open(md,encoding='utf-8').read()
    try: fm=yaml.safe_load(re.match(r'^---\n(.*?)\n---',raw,re.S).group(1))
    except Exception as e: failed.append((slug,'yaml')); continue
    steps=fm['solution']['steps']
    for i,latex in fixes.items():
        if 0<=i<len(steps): steps[i]=latex
    nb='  steps:\n'+''.join('    - '+json.dumps(s,ensure_ascii=False)+'\n' for s in steps)
    raw2=re.sub(r'  steps:\n(?:    - .*\n)+', lambda m: nb, raw, count=1)
    try:
        yaml.safe_load(re.match(r'^---\n(.*?)\n---',raw2,re.S).group(1))
    except Exception as e:
        failed.append((slug,'reparse')); continue
    open(md,'w',encoding='utf-8').write(raw2); done+=1
print(f'적용: {done}문제 · 실패 {len(failed)}: {failed[:5]}')
