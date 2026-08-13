import base64, json, subprocess, sys, os
TOK=open('/tmp/claude-1000/-home-insung-math-study/8db36fb0-c89b-4508-ba72-43f5a9235b57/scratchpad/eval_session.txt').read().strip()
PROMPT=("첨부 이미지에 인쇄된 내용을 **그대로 전사**해라. 풀지 마라. 해설하지 마라.\n"
        "- 수식은 LaTeX 로, 첨자·지수·분수를 정확히\n- 그림이 있으면 그림 안의 모든 라벨·기호를 빠짐없이 나열\n"
        "- 읽히지 않는 글자는 [?] 로 표시하고 추측하지 마라")
def call(img):
    data='data:image/png;base64,'+base64.b64encode(open(img,'rb').read()).decode()
    body=json.dumps({"slug":"functions/calculus/여러가지함수의_극한/자연상수_e","collection":"concepts",
                     "messages":[{"role":"user","content":PROMPT,"images":[data]}]},ensure_ascii=False)
    open('/tmp/_rq.json','w').write(body)
    out=subprocess.run(['curl','-s','-N','--max-time','180','http://127.0.0.1:4324/api/chat',
        '-H',f'Cookie: ms_session={TOK}','-H','Content-Type: application/json',
        '-H','Origin: http://127.0.0.1:4324','--data-binary','@/tmp/_rq.json'],capture_output=True,text=True).stdout
    t=''
    for l in out.splitlines():
        if l.startswith('data:'):
            try: d=json.loads(l[5:])
            except: continue
            if 'text' in d: t+=d['text']
            if 'message' in d: return f'__ERROR__ {d["message"]}'
    return t
res={}
for i in range(1,7):
    for sz in (512,1568):
        k=f's{i}_{sz}'
        res[k]=call(f'{k}.png')
        print(f'{k}: {len(res[k])}자 {"⚠오류" if res[k].startswith("__ERROR__") else ""}', flush=True)
json.dump(res,open('transcriptions.json','w'),ensure_ascii=False,indent=1)
