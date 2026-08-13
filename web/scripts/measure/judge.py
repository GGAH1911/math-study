import json, random, subprocess, os, re
random.seed(11)
tr=json.load(open('transcriptions.json'))
out=[]
env=dict(os.environ, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS='1')
for i in range(1,7):
    a_is_512 = random.random()<0.5
    A = tr[f's{i}_{512 if a_is_512 else 1568}']; B = tr[f's{i}_{1568 if a_is_512 else 512}']
    img=os.path.abspath(f's{i}_native.png')
    p=f"""Read the image at {img}. It is a printed Korean math exam problem.

Below are two transcriptions of that image, produced by a vision model. Judge them AGAINST THE IMAGE ONLY — do not assume either is correct.

Count, for each: how many **factual reading errors** it makes (wrong digit, wrong subscript/superscript, wrong variable, missing condition, missing or invented figure label, wrong relation). Ignore formatting/LaTeX-style differences and ignore differences in verbosity. Missing content counts as an error only if it is content actually present in the image.

=== TRANSCRIPTION A ===
{A}

=== TRANSCRIPTION B ===
{B}

Reply with ONLY a JSON object:
{{"A_errors": <int>, "B_errors": <int>, "winner": "A"|"B"|"tie", "worst_error": "<one sentence naming the single most serious error and which side made it, or 'none'>"}}"""
    r=subprocess.run(['claude','-p',p,'--allowedTools','Read'],capture_output=True,text=True,cwd='/tmp/resize_test',env=env,timeout=600,stdin=subprocess.DEVNULL)
    m=re.search(r'\{.*\}', r.stdout, re.S)
    if not m: print(f's{i}: 심판 파싱 실패 {r.stdout[:120]} {r.stderr[:120]}'); continue
    d=json.loads(m.group(0))
    e512 = d['A_errors'] if a_is_512 else d['B_errors']
    e1568= d['B_errors'] if a_is_512 else d['A_errors']
    win = d['winner']
    winner = 'tie' if win=='tie' else (('512' if a_is_512 else '1568') if win=='A' else ('1568' if a_is_512 else '512'))
    out.append({'s':i,'e512':e512,'e1568':e1568,'winner':winner,'worst':d['worst_error'],'A_was':'512' if a_is_512 else '1568'})
    print(f"s{i}: 512={e512}오류 1568={e1568}오류 승={winner} | {d['worst_error'][:90]}", flush=True)
json.dump(out,open('judgement.json','w'),ensure_ascii=False,indent=1)
t512=sum(o['e512'] for o in out); t1568=sum(o['e1568'] for o in out)
print(f"\n합계  512px: {t512}오류  |  1568px: {t1568}오류  (n={len(out)})")
print("승패 ", {k:sum(1 for o in out if o['winner']==k) for k in ('512','1568','tie')})
