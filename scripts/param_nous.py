"""채팅 API(Nous Portal)로 파라미터화를 돌리는 에이전트 루프.

★왜 분리했나: `claude -p` 경로와 **성질이 다른 일**이다. 저쪽은 모델이 스스로 파일을
  고치고 게이트를 돌리지만, 채팅 API 에는 그 루프가 없어 **여기서 대신 돈다**
  (파일 전체 수령 → 저장 → 게이트 실행 → 실패를 되먹임). 배치 본체는 작업목록·상태·
  게이트 판정만 맡고, 모델과 주고받는 사정은 전부 이 모듈이 안는다.
"""
from __future__ import annotations
import json, os, re, subprocess, threading, time
from pathlib import Path

VENV = os.environ.get('MS_PY', str(Path.home() / '.venvs/ms-ingest/bin/python'))
GATE_TIMEOUT_S = 180

#: 이 모듈이 쓴 토큰·비용 누계. 본체가 읽어 합산한다(순환 import 를 피하려고 여기 둔다).
USAGE = {'in': 0, 'out': 0, 'cost': 0.0, 'n': 0}
_usage_lock = threading.Lock()

# ★왜 별도 루프가 필요한가: `claude -p` 는 에이전트 루프(파일 쓰기 → 게이트 실행 →
#   실패를 읽고 고치기)를 통째로 제공한다. 채팅 API 에는 그게 없으므로 **여기서 돌린다.**
#   대신 매 콜이 솔버 파일 몇 KB 뿐이라 `claude -p` 의 거대한 시스템 프롬프트(콜당
#   캐시읽기 약 52만 토큰)를 통째로 걷어낸다. [[reference_nous_portal]]
NOUS_URL = 'https://inference-api.nousresearch.com/v1/chat/completions'
NOUS_ROUNDS = int(os.environ.get('PARAM_ROUNDS', '7'))

#: 채팅 API 는 코드를 못 돌려 본다 — 자주 밟는 지뢰를 미리 명시한다.
NOUS_HINTS = '''
## 이 방식의 주의사항 (당신은 코드를 직접 실행할 수 없습니다)
- 코드는 **그 자체로 실행 가능**해야 합니다. `comb`, `factorial`, `sqrt` 같은 함수는
  반드시 import 하세요(`from math import comb` 또는 `sympy as sp` 로 `sp.binomial`).
- 이름이 정의되지 않은 채 쓰이면 즉시 실패합니다. 제출 전 **모든 이름의 출처**를 확인하세요.
- 답을 검사할 때 `==` 는 sympy 객체에서 위험합니다. `sp.simplify(a - b) == 0` 을 쓰세요.
- 제출한 코드는 제가 실제로 돌려 **게이트 결과를 그대로 돌려드립니다.** 실패하면 고치면 됩니다.
'''


def nous_key() -> str:
    f = Path.home() / '.hermes' / '.env'
    if f.exists():
        for line in f.read_text(encoding='utf-8').splitlines():
            if line.startswith('NOUS_API_KEY='):
                return line.split('=', 1)[1].strip()
    return os.environ.get('NOUS_API_KEY', '').strip()


def _chat(model: str, messages: list[dict], key: str) -> str:
    """★스트리밍으로 받는다. 비스트리밍이면 생성이 길어질 때 게이트웨이가 유휴로 보고
    **524 로 끊는다**(max_tokens 를 16k 로 올리자마자 전건 524 였다 — 2026-08-14).
    스트림은 토큰이 계속 흘러 연결이 살아 있다."""
    import urllib.request
    body = json.dumps({'model': model, 'messages': messages,
                       'temperature': 0.2, 'max_tokens': 16000,
                       'stream': True,
                       'stream_options': {'include_usage': True}}).encode('utf-8')
    # ★User-Agent 를 반드시 준다. 기본 python-urllib UA 는 게이트웨이가 403 으로 막는다
    #   (curl 은 되는데 파이썬만 죽어서 인증 문제로 오인하기 쉽다 — 2026-08-14 실측).
    req = urllib.request.Request(NOUS_URL, data=body, headers={
        'Content-Type': 'application/json', 'Authorization': f'Bearer {key}',
        'User-Agent': 'math-study-parameterize/1.0'})
    text, usage = '', {}
    for attempt in range(3):               # 일시적 게이트웨이 오류는 재시도로 넘긴다
        try:
            text, usage = '', {}
            with urllib.request.urlopen(req, timeout=600) as r:
                for raw in r:
                    line = raw.decode('utf-8', 'replace').strip()
                    if not line.startswith('data:'):
                        continue
                    payload = line[5:].strip()
                    if payload == '[DONE]':
                        break
                    try:
                        ch = json.loads(payload)
                    except Exception:
                        continue
                    if ch.get('usage'):
                        usage = ch['usage']
                    for c in ch.get('choices') or []:
                        text += (c.get('delta') or {}).get('content') or ''
            if text.strip():
                break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))
    with _usage_lock:
        USAGE['in'] += int(usage.get('prompt_tokens') or 0)
        USAGE['out'] += int(usage.get('completion_tokens') or 0)
        USAGE['cost'] += float(usage.get('cost') or 0.0)   # 포털이 콜마다 실제 비용을 준다
        USAGE['n'] += 1
    return text


def _code_of(text: str) -> str:
    """응답에서 **파일 전체**인 코드블록을 고른다.

    ★마지막 블록을 그냥 집으면 안 된다. 설명 끝에 붙은 짧은 조각이 파일을 덮어써
      '규격 미작성' 으로 떨어진다(2026-08-14 실측: 모델 탓으로 오인할 뻔했다).
      규격 요소를 다 갖춘 블록 중 **가장 긴 것**을 고른다.
    """
    blocks = [b.strip() for b in re.findall(r'```(?:python)?\s*\n(.*?)```', text, re.S)]
    full = [b for b in blocks if 'PARAMS' in b and 'def solve(' in b]
    pool = full or blocks
    return max(pool, key=len) if pool else ''


def run_nous(work: Path, model: str, spec: str, system: str) -> str:
    """게이트가 통과할 때까지 고쳐 달라고 반복한다. 최종 solver.py 내용을 남긴다."""
    key = nous_key()
    if not key:
        raise SystemExit('NOUS_API_KEY 없음 (~/.hermes/.env)')
    cur = (work / 'solver.py').read_text(encoding='utf-8', errors='replace')
    problem = (work / 'problem.txt').read_text(encoding='utf-8', errors='replace')
    msgs = [{'role': 'system', 'content': system},
            {'role': 'user', 'content':
             f'{spec}\n{NOUS_HINTS}\n\n## 원문제\n{problem}\n\n## 현재 솔버\n```python\n{cur}\n```\n\n'
             '고친 **파일 전체**를 하나의 ```python 블록으로 주세요. 설명은 짧게.'}]
    last = ''
    for _ in range(NOUS_ROUNDS):
        out = _chat(model, msgs, key)
        code = _code_of(out)
        # ★규격 요소가 없는 조각으로는 **절대 덮어쓰지 않는다.** 잘린 응답이 파일을
        #   반토막으로 만들어 '규격 미작성' 으로 떨어지던 원인이다(2026-08-14).
        if not code or 'PARAMS' not in code or 'def solve(' not in code:
            msgs += [{'role': 'assistant', 'content': out[-1500:]},
                     {'role': 'user', 'content':
                      '응답이 잘렸거나 파일 전체가 아닙니다(PARAMS/solve 누락). '
                      '설명 없이 ```python 블록 하나로 **파일 전체**를 주세요.'}]
            continue
        (work / 'solver.py').write_text(code, encoding='utf-8')
        last = code
        try:
            r = subprocess.run([VENV, str(work / 'gate.py'), '--file', str(work / 'solver.py')],
                               capture_output=True, text=True, timeout=GATE_TIMEOUT_S, cwd=str(work))
        except subprocess.TimeoutExpired:
            msgs += [{'role': 'assistant', 'content': '```python\n(생략)\n```'},
                     {'role': 'user', 'content': '실행이 너무 오래 걸립니다(180초 초과). 탐색 범위를 줄이거나 닫힌 식을 쓰세요. 파일 전체를 다시 주세요.'}]
            continue
        if r.returncode == 0:
            return last
        # ★게이트 한 줄 요약만 주면 원인을 못 짚는다. 실제 실행 트레이스백을 붙여 준다.
        try:
            run = subprocess.run([VENV, str(work / 'solver.py')], capture_output=True,
                                 text=True, timeout=60, cwd=str(work))
            trace = (run.stderr or run.stdout or '')[-1200:]
        except subprocess.TimeoutExpired:
            trace = '(실행이 60초를 넘겼습니다 — 탐색 범위를 줄이세요)'
        msgs += [{'role': 'assistant', 'content': '```python\n(직전 제출)\n```'},
                 {'role': 'user', 'content':
                  f'게이트 실패입니다:\n```\n{(r.stdout + r.stderr)[-1200:]}\n```\n'
                  + (f'\n실행 결과:\n```\n{trace}\n```\n' if trace.strip() else '')
                  + '원인을 고쳐 **파일 전체**를 다시 주세요.'}]
    return last


