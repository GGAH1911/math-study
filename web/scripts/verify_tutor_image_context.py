import base64, json, subprocess, sys
TOK = open('/tmp/claude-1000/-home-insung-math-study/8db36fb0-c89b-4508-ba72-43f5a9235b57/scratchpad/eval_session.txt').read().strip()
IMG = '/home/insung/math-study/db/raw/2026_고1_3월모의고사/images/2026_고1_3월모의고사_단일_29.png'
data = 'data:image/png;base64,' + base64.b64encode(open(IMG,'rb').read()).decode()
SLUG = 'functions/calculus/여러가지함수의_극한/자연상수_e'

def ask(msgs):
    body = json.dumps({"slug":SLUG,"collection":"concepts","messages":msgs}, ensure_ascii=False)
    open('/tmp/_req.json','w',encoding='utf8').write(body)
    out = subprocess.run(['curl','-s','-N','--max-time','150','http://127.0.0.1:4324/api/chat',
        '-H',f'Cookie: ms_session={TOK}','-H','Content-Type: application/json',
        '-H','Origin: http://127.0.0.1:4324','--data-binary','@/tmp/_req.json'],
        capture_output=True, text=True).stdout
    txt=''; err=None
    for l in out.splitlines():
        if l.startswith('data:'):
            try: d=json.loads(l[5:])
            except: continue
            if 'text' in d: txt+=d['text']
            if 'message' in d: err=d['message']
    if err: print(f'  ⚠ 오류: {err}')
    return txt

msgs=[{"role":"user","content":"첨부한 문제 이미지를 보고 이차함수 f(x)의 식을 알려줘.","images":[data]}]
a1=ask(msgs); print(f'[1턴·이미지] {a1[:160]}'.replace('\n',' ')); msgs.append({"role":"assistant","content":a1})

for i,q in enumerate([ "그 식에서 x^2 의 계수는 뭐야?",
                       "그럼 x 의 계수는?",
                       "상수항 부분은 a 에 대한 식으로 어떻게 돼?" ], start=2):
    msgs.append({"role":"user","content":q})
    a=ask(msgs); print(f'[{i}턴·이미지없음] Q: {q}\n            A: {a[:170]}'.replace('\n',' ') if False else f'[{i}턴·이미지없음] Q:{q}\n   A: {a[:170]}')
    msgs.append({"role":"assistant","content":a})
