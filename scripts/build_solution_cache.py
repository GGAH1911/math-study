#!/usr/bin/env python3
"""Offline verified-solution cache builder.

For each problem: Sonnet reads the problem image, solves it, and emits BOTH a
solution (steps) AND a self-contained back-substitution verifier. We then run
that verifier locally. A solution is cached into the problem's frontmatter
ONLY when (a) Sonnet's answer_choice == the official gold choice AND (b) the
verifier prints VERIFY_PASS. Anything else is retried, then flagged — never
cached. The live Haiku tutor later reads the cached `solution.steps` as a
trusted reference path (Socratic rules unchanged — it knows but never reveals).

WHY this is safe even though Sonnet errs sometimes:
  - The gate checks the answer against the PROBLEM'S OWN conditions
    (back-substitution), not against Sonnet's narrative.
  - Cache only on pass → fail-loud-offline, never fail-silent-live.
  - generated_by/verified are recorded so a later audit can re-check.

Usage:
  python scripts/build_solution_cache.py --slug 2024_6월모평_미적분_28   # one problem
  python scripts/build_solution_cache.py --sample 20                    # 20 killer/준킬러 pilot
  python scripts/build_solution_cache.py --list a,b,c
Env: ANTHROPIC_API_KEY (claude CLI auth). Verifiers run via the repo venv.
"""
from __future__ import annotations
import re, sys, json, glob, subprocess, tempfile, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
VENV_PY = Path('/home/insung/Projects/math-study/.venv/bin/python')
VERIFIER_DIR = ROOT / 'db' / 'solutions'
MODEL = 'sonnet'

sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402  세로 긴 문제 → 원해상도 타일
MAX_RETRIES = 3
# 모델 호출 타임아웃(초). FLAG 회복 시 SOLVE_TIMEOUT=1200 등으로 늘려 재시도.
TIMEOUT_S = int(os.environ.get('SOLVE_TIMEOUT', '480'))
# 난이도 사다리: (model, effort), 모델별 1회 (blind 풀이).
# blind = 정답을 프롬프트에 안 줌 → 모델이 스스로 푼 답이 공식 gold 와 일치해야 통과.
#   · 단답형(0-999): gold 정수 일치 자체가 강한 검증 → 검증기 불필요.
#   · 5지선다: gold 가 1/5 이라 약함 → 원본식 역대입 검증기까지 통과해야.
# tier-gate: 킬러는 Haiku 스킵(외운-답+어설픈-풀이 방지) → Sonnet 부터.
# tesseract/DeepSeek 안 씀 — 모든 문제를 '풀이 성공'으로 해결하고 점수는 거기 올라탄다.
LADDER_DEFAULT = [('haiku', 'high'), ('sonnet', 'max'), ('opus', 'max')]   # early / mid
LADDER_KILLER  = [('sonnet', 'max'), ('opus', 'max')]                       # killer: Haiku 스킵
# verifier 안전: 파일/네트워크/시스템 접근 금지 — 순수 수학만 허용
FORBIDDEN = re.compile(r'\b(os|subprocess|socket|shutil|requests|httpx|urllib|open|eval|exec|__import__|pathlib|Path)\b')
# 검증기-코딩 누명 회복: ans==gold인데 검증기만 실패하면 같은 모델에 '에러 힌트' 주고 재시도.
# 검증기 작성은 확률적이라(금지import·크래시·로직버그) 재롤하면 깨끗이 나옴 → 불필요한 escalation/FLAG 흡수.
VERIFY_RETRIES = int(os.environ.get('VERIFY_RETRIES', '2'))
# 풀이/검증기 분리 — 구제(salvage): 사다리가 다 떨어져도(검증기 *코딩*이 병목인 킬러) 검증기 없이
# '답만' 받아 gold 일치 시 solved(verified:false)로 캐시. SALVAGE_ONLY=1 → 사다리 건너뛰고 바로 구제(알려진 FLAG 재시도용).
SALVAGE_ONLY = os.environ.get('SALVAGE_ONLY') == '1'
# 관측성: 단일 모델콜은 capture_output로 끝까지 묵음(헤드리스 claude -p는 transcript도 안 남김).
# parallel==1(단일/디버깅) 실행에서 HEARTBEAT_S 마다 '작업중' 하트비트를 로그에 찍어 진행을 보이게 한다.
HEARTBEAT = False
HEARTBEAT_S = int(os.environ.get('HEARTBEAT_S', '60'))
# 최종 티어: 자동 사다리·구제가 verified:true 를 못 만든 hard 문제(도형·이산 런어웨이, 검증기 병목)를
# 전체 도구(Read·Bash·Write) 에이전트가 '직접 풀이' — 코드로 계산하고 검증기까지 작성. 비용 커서 마지막에만.
AGENT_TIER = os.environ.get('AGENT_TIER', '1') == '1'        # 끄려면 AGENT_TIER=0 (빠른 모드: 인플레이스 구제)
AGENT_TIMEOUT = int(os.environ.get('AGENT_TIMEOUT', '900'))

SYSTEM = """당신은 한국 수능 수학 문제를 정확히 푸는 전문가입니다. 첨부된 문제 이미지를 Read 도구로 먼저 본 뒤 풀이하세요. 도형·조건·보기 값은 모두 이미지에서 확인합니다. 추측 금지."""


def build_prompt(img_paths: list[str], fmt: str, meta: str, hint: str = '', with_verifier: bool = True) -> str:
    use_verifier = with_verifier   # 솔버는 객관식·단답 모두 필수(유사문제 재생성+정답표 독립검증). 구제모드만 생략
    lines = ['  "answer": <네가 푼 보기 번호 1-5 정수>,' if fmt == 'choice'
             else '  "answer": <네가 푼 단답형 정답 정수(0-999)>,']
    lines.append('  "answer_value": "<최종 답의 값만, 설명·중간식 없이. 예: -7/64 또는 163>",')
    lines.append('  "score": <2|3|4 정수, 이미지 상단의 "[N점]" 배점 그대로>,')
    if use_verifier:
        lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."],')
        lines.append('  "verifier_python": "<자기완결 파이썬 검산기. **맨 윗줄에 `CANDIDATE = <네가 구한 답>` 정의**. 그 아래에서 **이미지에 주어진 원래 함수·방정식·조건을 코드로 표현**하고 CANDIDATE 를 역대입/대조해 만족하는지 sympy·numpy 로 확인(근사식·중간식 금지, 원식 그대로; 필요시 수치 root-find). \'if CANDIDATE==답\' 같은 자기비교 금지 — CANDIDATE 를 틀린 값으로 바꾸면 반드시 VERIFY_FAIL 이 나오게. 통과 시 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print. 파일·네트워크·os 금지, 수학 라이브러리만.>"')
    else:
        lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."]')
    body = '\n'.join(lines)
    if len(img_paths) == 1:
        img_intro = f"문제 이미지: {img_paths[0]}\n{meta}\n\n위 이미지를 Read 로 연 뒤"
    else:
        listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(img_paths))
        img_intro = (
            f"문제 이미지 — 세로로 길어 위→아래 {len(img_paths)}장으로 나눴고 경계가 약간 겹칩니다:\n"
            f"{listing}\n{meta}\n\n"
            f"위 {len(img_paths)}장을 **모두** Read 로 열어 **하나의 문제로 이어 붙여** 본 뒤"
        )
    return f"""{img_intro} 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** **마지막 메시지에 오직 하나의 ```json 블록**만 출력 (설명 산문 금지):

```json
{{
{body}
}}
```{(chr(10) + chr(10) + hint) if hint else ''}"""


def _anonymize(img_paths: list[str]) -> tuple[list[str], str]:
    """정체 누출 차단(future-leak) — 파일명(연도·시험·번호)이 모델에 안 보이게 타일을 중립이름 임시폴더로 복사."""
    import shutil, tempfile
    d = tempfile.mkdtemp(prefix='sol_')
    out = []
    for i, p in enumerate(img_paths):
        o = Path(d) / f'p_{i + 1}.png'
        shutil.copy(p, o)
        out.append(str(o))
    return out, d


def call_model(img_paths: list[str], fmt: str, meta: str, model: str, effort: str,
               add_dir: str, hint: str = '', with_verifier: bool = True) -> dict | None:
    import shutil
    anon_paths, anon_dir = _anonymize(img_paths)   # ← 파일명 정체 누출 차단
    prompt = build_prompt(anon_paths, fmt, meta, hint, with_verifier)
    args = ['claude', '-p', '--model', model, '--effort', effort,
            '--allowedTools', 'Read', '--add-dir', anon_dir,
            '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '14', '--system-prompt', SYSTEM, '--', prompt]
    import threading                              # 하트비트: 단일콜이 capture_output로 묵음 → 살아있음 주기 로그
    stop = threading.Event()
    def _hb():
        s = 0
        while not stop.wait(HEARTBEAT_S):
            s += HEARTBEAT_S
            print(f'      · {model} 작업중 {s}s… (타임아웃 {TIMEOUT_S}s)', flush=True)
    if HEARTBEAT:
        threading.Thread(target=_hb, daemon=True).start()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None
    finally:
        stop.set()
        shutil.rmtree(anon_dir, ignore_errors=True)
    out = r.stdout
    blocks = re.findall(r'```json\s*(.*?)```', out, re.DOTALL)
    if not blocks:
        blocks = re.findall(r'(\{.*"verifier_python".*\})', out, re.DOTALL)
    for b in reversed(blocks):
        try:
            return json.loads(b.strip())
        except Exception:
            continue
    return None


SYSTEM_TEXT = ("당신은 한국 수능 수학 문제를 정확히 푸는 전문가입니다. 주어진 문제 텍스트를 읽고 끝까지 "
               "풀이하세요. 조건·식·보기 값은 모두 텍스트에서 확인합니다. 추측 금지.")


def extract_searchable(md_text: str) -> str:
    m = re.search(r'^searchable_text:\s*[|>][-+]?\s*\n(.*?)(?=^\S|\Z)', md_text, re.M | re.S)
    return m.group(1).strip() if m else ''


def build_text_prompt(problem_text: str, fmt: str, meta: str) -> str:
    lines = ['  "answer": <네가 푼 보기 번호 1-5 정수>,' if fmt == 'choice'
             else '  "answer": <네가 푼 단답형 정답 정수(0-999)>,']
    lines.append('  "answer_value": "<최종 답의 값만, 설명·중간식 없이. 예: -7/64 또는 163>",')
    lines.append('  "score": <2|3|4 정수, 배점이 보이면 그대로, 없으면 4>,')
    lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."],')
    lines.append('  "verifier_python": "<자기완결 파이썬 검산기. **맨 윗줄에 `CANDIDATE = <네가 구한 답>` 정의**. 그 아래에서 **문제에 주어진 원래 함수·방정식·조건을 코드로 표현**하고 CANDIDATE 를 역대입/대조해 만족하는지 sympy·numpy 로 확인(근사식·중간식 금지, 원식 그대로; 필요시 수치 root-find). \'if CANDIDATE==답\' 같은 자기비교 금지 — CANDIDATE 를 틀린 값으로 바꾸면 반드시 VERIFY_FAIL 이 나오게. 통과 시 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print. 파일·네트워크·os 금지, 수학 라이브러리만.>"')
    body = '\n'.join(lines)
    return (f"다음은 한국 수능 수학 문제다 (텍스트):\n\n{problem_text}\n\n{meta}\n\n"
            f"위 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** "
            f"**마지막 메시지에 오직 하나의 ```json 블록**만 출력 (설명 산문 금지):\n\n"
            f"```json\n{{\n{body}\n}}\n```")


def call_model_text(problem_text: str, fmt: str, meta: str, model: str, effort: str) -> dict | None:
    """식-텍스트 우회 — 이미지 없이 searchable_text만으로 풀이(도구 없음). vision 누명 제거용."""
    prompt = build_text_prompt(problem_text, fmt, meta)
    args = ['claude', '-p', '--model', model, '--effort', effort,
            '--disallowedTools', 'Read,Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '6', '--system-prompt', SYSTEM_TEXT, '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None
    blocks = re.findall(r'```json\s*(.*?)```', r.stdout, re.DOTALL)
    if not blocks:
        blocks = re.findall(r'(\{.*"answer".*\})', r.stdout, re.DOTALL)
    for b in reversed(blocks):
        try:
            return json.loads(b.strip())
        except Exception:
            continue
    return None


def verify_hint(log: str) -> str:
    """검증기 실패 사유별 맞춤 힌트 — 재시도 프롬프트에 덧붙여 같은 실수 반복 방지."""
    if 'mutation-pass' in log:
        return ('⚠ 직전 검증기가 *틀린 답*에도 VERIFY_PASS 를 냈다(하드코딩 의심). 맨 위 CANDIDATE 를 '
                '원래 문제의 식·조건에 실제로 대입/풀이해서, CANDIDATE 가 틀린 값이면 반드시 VERIFY_FAIL 이 '
                '나오도록 다시 작성하라.')
    if 'no-realmath' in log:
        return ('⚠ 직전 검증기에 실제 수식 풀이(sympy solve/Eq/subs/isclose 등)가 없다. 원래 문제의 식을 '
                '코드로 표현하고 CANDIDATE 를 대입해 판정하라.')
    if 'self-compare' in log:
        return ('⚠ 직전 검증기가 답을 자기 자신과 직접 비교(if CANDIDATE == 정답)했다. 금지다. 원래 문제의 '
                '식에 대입한 결과로만 판정하라.')
    if 'no-CANDIDATE' in log:
        return '⚠ 맨 윗줄에 CANDIDATE = <답> 정의가 없다. 반드시 그렇게 시작하고 그 값으로 원식을 검증하라.'
    if 'forbidden-import' in log:
        return ('⚠ 직전 검증기가 금지어(os·open·Path·pathlib·subprocess·shutil 등)를 사용해 거부됐다. '
                '아무것도 파일/시스템 접근하지 말고 sympy·numpy·math·fractions 만 써서 verifier_python 을 다시 작성하라.')
    if 'timeout' in log:
        return ('⚠ 직전 검증기가 시간초과로 죽었다. 무한루프·과도한 기호연산을 피하고 '
                '가능하면 수치(numpy)로 가볍게 역대입 검사하도록 verifier_python 을 다시 작성하라.')
    if 'Traceback' in log or 'Error' in log:
        return (f'⚠ 직전 검증기가 실행 중 에러로 죽었다: {log[:140]} ... '
                '문법·변수명·인덱스·심볼정의를 점검하고 sympy·numpy 로 안전하게 verifier_python 을 다시 작성하라.')
    return ('⚠ 직전 검증기가 VERIFY_FAIL 을 냈다. 네 답 자체는 정답(gold)과 일치하니 *검증기 코드의 버그*다. '
            '원래 문제의 식·조건에 네 답을 역대입하는 로직을 처음부터 재검토해 verifier_python 을 다시 작성하라.')


def run_verifier(code: str) -> tuple[bool, str]:
    if FORBIDDEN.search(code):
        return False, 'forbidden-import'
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write(code); tmp = f.name
    try:
        r = subprocess.run([str(VENV_PY), tmp], capture_output=True, text=True, timeout=40)
        ok = 'VERIFY_PASS' in r.stdout and 'VERIFY_FAIL' not in r.stdout
        return ok, (r.stdout[-300:] + r.stderr[-300:]).strip()
    except subprocess.TimeoutExpired:
        return False, 'verifier-timeout'
    finally:
        try: os.unlink(tmp)
        except Exception: pass


# ───────────────────────── open-book 솔버 작성 (정답+풀이 제공) ─────────────────────────
def build_openbook_prompt(problem_text: str, gold: str, fmt: str, steps_text: str = '') -> str:
    """정답과 검증된 풀이단계를 주고, 원래 식에 역대입하는 검산기를 쓰게 하는 프롬프트."""
    kind = '객관식(보기 번호 1-5)' if fmt == 'choice' else '단답형(정수)'
    steps_block = (f"\n[검증된 풀이 단계 — 이 논리를 코드로 옮겨라]\n{steps_text}\n"
                   if steps_text else '')
    return (
        f"다음은 한국 수능 수학 문제다 (텍스트):\n\n{problem_text}\n\n"
        f"이 문제의 정답은 이미 검증돼 있다: **정답 = {gold}** ({kind}).{steps_block}\n"
        f"임무: 이 정답이 옳음을 **원래 문제의 식·조건으로 직접 확인**하는 자기완결 파이썬 검산기를 작성하라.\n\n"
        f"엄격 규칙:\n"
        f"1. 맨 윗줄에 검사할 답을 정확히 이렇게 정의: CANDIDATE = {gold}\n"
        f"2. 그 아래에서 **문제에 주어진 원래 함수·방정식·조건을 코드로 인코딩**하고, CANDIDATE 를 그 식에 "
        f"대입/대조해 만족하는지 sympy·numpy·math·fractions 로 확인하라. 문제에 나온 계수·상수를 코드에 그대로 써라.\n"
        f"3. 'if CANDIDATE == {gold}' 처럼 답을 자기 자신(또는 같은 상수)과 직접 비교하지 마라. "
        f"반드시 원래 식을 풀거나 대입한 결과로 판정하라.\n"
        f"4. CANDIDATE 를 틀린 값으로 바꾸면 반드시 VERIFY_FAIL 이 나오게, 진짜 문제 조건에 의존시켜라.\n"
        f"5. 통과 시 정확히 VERIFY_PASS, 아니면 VERIFY_FAIL 를 print. 파일·네트워크·os 금지(sympy·numpy·math·fractions 만).\n\n"
        f"**마지막 메시지에 오직 하나의 ```json 블록**만 출력 (산문 금지):\n"
        f"```json\n{{\n  \"verifier_python\": \"<자기완결 파이썬 검산기 (CANDIDATE 로 시작)>\"\n}}\n```"
    )


def call_openbook(problem_text: str, gold: str, fmt: str, steps_text: str,
                  model: str, effort: str, hint: str = '') -> dict | None:
    """Open-book: 정답+풀이단계를 주고 역대입 검산기를 작성하게 함 (이미지 없음)."""
    prompt = build_openbook_prompt(problem_text, gold, fmt, steps_text)
    if hint:
        prompt += f"\n\n{hint}"
    args = ['claude', '-p', '--model', model, '--effort', effort,
            '--disallowedTools', 'Read,Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '6', '--system-prompt', SYSTEM_TEXT, '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None
    blocks = re.findall(r'```json\s*(.*?)```', r.stdout, re.DOTALL)
    if not blocks:
        blocks = re.findall(r'(\{.*"verifier_python".*\})', r.stdout, re.DOTALL)
    for b in reversed(blocks):
        try:
            return json.loads(b.strip())
        except Exception:
            continue
    return None


_REALMATH = re.compile(r'\b(solve|solveset|linsolve|nsolve|roots|Eq|subs|isclose|allclose|'
                       r'integrate|diff|limit|Poly|simplify|expand|factor|Matrix|det|Rational)\b')


def _set_candidate(code: str, val: str) -> str:
    return re.sub(r'(?m)^CANDIDATE\s*=.*$', f'CANDIDATE = {val}', code, count=1)


def hardcode_gate(code: str, gold: str, fmt: str) -> tuple[bool, str]:
    """역대입 검산기 진위 판정 — 변이테스트로 하드코딩 차단.
    반환 (통과, 사유). 통과 = 원래 문제식에 실제로 의존하는 검산기."""
    from fractions import Fraction
    if not re.search(r'(?m)^CANDIDATE\s*=', code):
        return False, 'no-CANDIDATE'
    gq = re.escape(str(gold))
    if re.search(rf'CANDIDATE\s*==\s*{gq}\b', code) or re.search(rf'{gq}\s*==\s*CANDIDATE', code):
        return False, 'self-compare'                      # 답을 자기 자신과 직접 비교
    if not _REALMATH.search(code):
        return False, 'no-realmath'                       # 실제 수식 풀이 흔적 없음
    ok, _ = run_verifier(code)
    if not ok:
        return False, 'orig-fail'                         # 원본이 통과 못 함
    if fmt == 'choice':
        muts = [str(x) for x in range(1, 6) if str(x) != str(gold)]
    else:
        try:
            g = Fraction(str(gold)); muts = [str(g + 1), str(g - 1), str(g + 2)]
        except Exception:
            muts = [f'(({gold})+1)', f'(({gold})-1)']
    for mv in muts:
        passed, _ = run_verifier(_set_candidate(code, mv))
        if passed:
            return False, f'mutation-pass:{mv}'           # 틀린 답이 통과 → 하드코딩
    return True, 'ok'


def accept_verifier(vp: str, gold: str, fmt: str) -> tuple[bool, str]:
    """검산기 수용 판정 — 단순 VERIFY_PASS 가 아니라 하드코딩 게이트(변이테스트)까지 통과해야 채택.
    인제스트·백필 공통 진입점. 실패 시 사유를 로그로 반환해 재시도 힌트에 사용."""
    if not vp:
        return False, 'no-verifier'
    return hardcode_gate(vp, gold, fmt)


def try_write_verifier(p: Path, vp: str, gold: str, fmt: str) -> str:
    """단답형 additive 검산기: 게이트 통과 시 db/solutions 에 기록하고 경로 반환, 아니면 'gold-match'.
    정수 일치로 이미 verified:true 이므로 검산기는 유사문제 재생성용 부가물 — 실패해도 무손상."""
    if vp:
        ok, _ = accept_verifier(vp, gold, fmt)
        if ok:
            VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
            (VERIFIER_DIR / f'{p.stem}.py').write_text(vp, encoding='utf-8')
            return f'db/solutions/{p.stem}.py'
    return 'gold-match'


def gold_answer(md_text: str) -> str | None:
    """choice → 보기번호(1-5), numeric → 정수. 중첩 따옴표 제거."""
    m = re.search(r'^answer:\s*(.+?)\s*$', md_text, re.M)
    return m.group(1).strip().strip('\'"') if m else None


def already_cached(md_text: str) -> bool:
    return bool(re.search(r'^solution:\s*$', md_text, re.M))


def write_solution(p: Path, sol: dict, verifier_rel: str, model: str = MODEL,
                   solved_by: str | None = None, trace: list | None = None,
                   source: str | None = None, verified: bool = True):
    t = p.read_text(encoding='utf-8')
    if re.search(r'^solution:', t, re.M):
        return  # 동시 실행 레이스 방어 — 이미 solution 블록 있으면 중복 삽입 안 함

    steps = '\n'.join(f'    - {json.dumps(s, ensure_ascii=False)}' for s in sol['solution_steps'])
    # solved_by = 최초로 답 맞힌 모델(난이도). escalation = 그 전에 탈락한 모델·사유.
    fails = [(m, r) for (m, r) in (trace or []) if r != 'pass']
    extra = ''
    if solved_by:
        extra += f"  solved_by: {solved_by}\n"
    if source:                                  # 'text' = searchable_text만으로 검증 통과(튜터 게이트 신호)
        extra += f"  source: {source}\n"
    if fails:
        extra += "  escalation:\n" + ''.join(
            f"    - {{model: {m}, reason: {r}}}\n" for m, r in fails)
    block = (f"solution:\n"
             f"  answer_value: {json.dumps(str(sol.get('answer_value','')), ensure_ascii=False)}\n"
             f"  verified: {'true' if verified else 'false'}\n"
             f"  generated_by: {model}\n"
             f"{extra}"
             f"  verifier: {verifier_rel}\n"
             f"  steps:\n{steps}\n")
    # frontmatter 닫는 --- 앞에 삽입
    parts = t.split('---\n', 2)
    if len(parts) >= 3:
        parts[1] = parts[1] + block
        p.write_text('---\n' + parts[1] + '---\n' + parts[2], encoding='utf-8')
    else:
        print(f'    [warn] {p.name}: frontmatter 형식 예외, 스킵')


def fix_score(p: Path, new: str):
    """Correct frontmatter `score:` + body `# [...] N점` from Sonnet's image read."""
    if new not in ('2', '3', '4'):
        return
    t = p.read_text(encoding='utf-8')
    t2 = re.sub(r'^(\s*score:\s*)\d+', rf'\g<1>{new}', t, count=1, flags=re.M)
    t2 = re.sub(r'^(#\s*\[[^\n\]]*\])\s*\d+\s*점', rf'\g<1> {new}점', t2, count=1, flags=re.M)
    if t2 != t:
        p.write_text(t2, encoding='utf-8')


def _agent_prompt(img_paths: list[str], fmt: str, meta: str) -> str:
    listing = '\n'.join(f'    {i + 1}. {pp}' for i, pp in enumerate(img_paths))
    intro = (f"문제 이미지 — 세로로 길어 위→아래 {len(img_paths)}장 타일(경계 약간 겹침):\n{listing}"
             if len(img_paths) > 1 else f"문제 이미지: {img_paths[0]}")
    lines = ['  "answer": <보기 번호 1-5 정수>,' if fmt == 'choice' else '  "answer": <단답형 정답 정수(0-999)>,',
             '  "answer_value": "<최종 값만, 설명 없이>",', '  "score": <2|3|4 정수, 이미지 상단 [N점]>,']
    lines.append('  "solution_steps": ["<핵심 단계, 한국어 KaTeX $...$ 허용>", "..."],')
    lines.append('  "verifier_python": "<자기완결 파이썬 검산기. **맨 윗줄에 `CANDIDATE = <네가 구한 답>` 정의** 후 **원래 문제의 조건/식에 CANDIDATE 를 역대입·재계산**해 검사. \'if CANDIDATE==답\' 자기비교 금지 — CANDIDATE 를 틀린 값으로 바꾸면 VERIFY_FAIL 이 나오게. sympy/numpy/math/fractions 만, 파일·os·네트워크 금지. 통과 시 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print.>"')
    body = '\n'.join(lines)
    return f"""{intro}
{meta}

위 문제를 **도구(Read·Bash·Write)를 적극 활용해** 끝까지 풀어라. 정답은 주어지지 않는다.
1. 이미지를 Read 로 정밀히 읽어 조건을 파악하라(도형이면 좌표로 옮겨라).
2. **경우의 수·도형 넓이·무한급수·방정식 등 이산/수치 계산은 암산하지 말고, Python 을 작성해 Bash(`python3 -c …` 또는 Write 로 파일 저장 후 실행)로 돌려** 정확히 구하라.
3. 답을 확정한 뒤 검증기를 작성하라(객관식이면 필수).

작업이 끝나면 **마지막 메시지에 오직 하나의 ```json 블록**만 출력(설명 산문 금지):
```json
{{
{body}
}}
```"""


def _agent_solve(p: Path, tiles, fmt, meta, img_dir, gold, solved_by, trace):
    """최종 티어 — 전체 도구(Read·Bash·Write) 에이전트가 '직접 풀이'(코드로 계산·검증기 작성).
    자동 사다리가 verified:true 를 못 만든 hard 문제(도형·이산 런어웨이, 검증기 병목)용.
    → verified:true(CACHED@A) 목표, 답만 맞으면 verified:false(CACHED@A~)."""
    import shutil, threading
    anon_paths, anon_dir = _anonymize(tiles)
    args = ['claude', '-p', '--model', 'opus', '--effort', 'high',
            '--allowedTools', 'Read,Bash,Write', '--add-dir', anon_dir,
            '--disallowedTools', 'WebFetch,WebSearch,Edit', '--max-turns', '30',
            '--system-prompt', SYSTEM, '--', _agent_prompt(anon_paths, fmt, meta)]
    stop = threading.Event()
    if HEARTBEAT:
        def _hb():
            s = 0
            while not stop.wait(HEARTBEAT_S):
                s += HEARTBEAT_S; print(f'      · agent 직접풀이 {s}s… (타임아웃 {AGENT_TIMEOUT}s)', flush=True)
        threading.Thread(target=_hb, daemon=True).start()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=AGENT_TIMEOUT)
    except subprocess.TimeoutExpired:
        trace.append(('agent', 'timeout')); return None
    finally:
        stop.set(); shutil.rmtree(anon_dir, ignore_errors=True)
    sol = None
    for b in reversed(re.findall(r'```json\s*(.*?)```', r.stdout, re.DOTALL)):
        try: sol = json.loads(b.strip()); break
        except Exception: continue
    if not sol:
        trace.append(('agent', 'gen-fail')); return None
    if str(sol.get('answer')).strip().strip('\'"') != gold:
        trace.append(('agent', 'ans-wrong')); return None
    by = solved_by or 'agent'
    if fmt == 'choice':
        ok, vlog = accept_verifier(sol.get('verifier_python', ''), gold, fmt)
        if ok:
            VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
            (VERIFIER_DIR / f'{p.stem}.py').write_text(sol['verifier_python'], encoding='utf-8')
            trace.append(('agent', 'verified'))
            write_solution(p, sol, f'db/solutions/{p.stem}.py', 'agent', by, trace)
            fix_score(p, str(sol.get('score', ''))); return 'CACHED@A'
        trace.append(('agent', f'verify-fail:{vlog[:20]}'))
        write_solution(p, sol, 'unverified', 'agent', by, trace, verified=False)
        fix_score(p, str(sol.get('score', ''))); return 'CACHED@A~'    # 답 맞음·검증기만 실패
    trace.append(('agent', 'pass'))
    write_solution(p, sol, try_write_verifier(p, sol.get('verifier_python', ''), gold, fmt), 'agent', by, trace)
    fix_score(p, str(sol.get('score', ''))); return 'CACHED@A'


def _salvage(p: Path, tiles, fmt, meta, img_dir, gold, solved_by, trace):
    """검증기 분리·구제 — 검증기 없이 '답만' 받아 gold 일치 시 캐시(verified:false).
    킬러는 검증기 *코딩*이 병목 → 답·풀이는 살리고 python 역대입 검증만 보류(미검증 표시)."""
    sal_model, _ = LADDER_KILLER[-1]                 # 가장 강한 모델(opus/max)
    sol = call_model(tiles, fmt, meta, sal_model, 'max', img_dir, with_verifier=False)
    if not sol:
        trace.append((sal_model, 'salvage-gen-fail')); return None
    ans = str(sol.get('answer')).strip().strip('\'"')
    if ans != gold:
        trace.append((sal_model, 'salvage-ans≠gold')); return None
    trace.append((sal_model, 'salvage-pass(미검증)'))
    write_solution(p, sol, 'unverified', sal_model, solved_by or sal_model, trace, verified=False)
    fix_score(p, str(sol.get('score', '')))
    return f'CACHED@{sal_model[0]}~'                  # '~' = 미검증 구제(답만, python 역대입 보류)


def build_one(p: Path) -> str:
    t = p.read_text(encoding='utf-8')
    if already_cached(t):
        return 'skip-cached'
    gold = gold_answer(t)
    img = IMGDIR / (p.stem + '.png')
    if not gold or not img.exists():
        return 'skip-no-gold-or-img'
    fm = re.search(r'^format:\s*(\w+)', t, re.M)
    fmt = fm.group(1) if fm else 'choice'
    tier = (re.search(r'^killer_tier:\s*(\w+)', t, re.M) or [None, None])[1]
    ladder = LADDER_KILLER if tier == 'killer' else LADDER_DEFAULT   # 킬러는 Haiku 스킵
    meta = f"문항 형식: {'객관식 5지선다' if fmt == 'choice' else '단답형(정수 정답)'}"
    real_img = img.resolve()                        # 심링크 → 실제 db/raw 원본
    tiles = [str(t) for t in tile_for_vision(real_img)]  # 세로 길면 원해상도 N타일(tiles/ 하위)
    img_dir = str(real_img.parent)                  # 단일 이미지·tiles/ 둘 다 이 dir 아래
    last = ''
    trace = []           # 모델별 결과 (escalation 사유 기록)
    solved_by = None     # 최초로 답(ans==gold)을 맞힌 모델 = 난이도 신호 (검증기 통과와 무관)

    if SALVAGE_ONLY:     # 사다리 건너뛰고 바로 구제(알려진 FLAG 재시도) — 검증기 없이 답만
        return _salvage(p, tiles, fmt, meta, img_dir, gold, solved_by, trace) or 'FLAG(salvage-fail)'

    # ── 0) 식-텍스트 우회: searchable_text로 Haiku 먼저 (vision 누명 제거 · 검증 게이트가 안전망) ──
    # 텍스트로 ans==gold + (객관식이면 검증기까지) 통과 → 싼 Haiku로 끝. 실패 시 이미지 사다리로 폴백.
    stext = extract_searchable(t)
    if stext and len(stext) > 40:
        solt = call_model_text(stext, fmt, meta, 'haiku', 'high')
        if solt and str(solt.get('answer')).strip().strip('\'"') == gold:
            okt, vref_t = True, 'gold-match'
            if fmt == 'choice':
                okt, _ = accept_verifier(solt.get('verifier_python', ''), gold, fmt)
                if okt:
                    VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
                    (VERIFIER_DIR / f'{p.stem}.py').write_text(solt['verifier_python'], encoding='utf-8')
                    vref_t = f'db/solutions/{p.stem}.py'
            else:                                 # 단답형 additive 검산기(게이트 통과 시만)
                vref_t = try_write_verifier(p, solt.get('verifier_python', ''), gold, fmt)
            if okt:                               # 텍스트만으로 검증 통과 → 난이도=haiku, 끝
                write_solution(p, solt, vref_t, 'haiku', 'haiku', [('haiku-text', 'pass')], source='text')
                return 'CACHED@T'
        trace.append(('haiku-text', 'text-fail'))  # 텍스트 실패 → 이미지 사다리 폴백

    for model, effort in ladder:                  # 모델별 1회 (blind)
        sol = call_model(tiles, fmt, meta, model, effort, img_dir)
        if not sol:
            last = f'{model}:gen-fail'; trace.append((model, 'gen-fail')); continue
        ans = str(sol.get('answer')).strip().strip('\'"')
        if ans != gold:                           # blind 답이 공식 gold 와 불일치 → escalate
            last = f'{model}:ans{ans}≠{gold}'; trace.append((model, 'ans-wrong')); continue
        if solved_by is None:                     # 답 맞힌 첫 모델 — 이게 '난이도'다
            solved_by = model
        # 단답형: gold 정수 일치로 충분. 5지선다: 원본식 역대입 검증기까지.
        vtry = 0
        if fmt == 'choice':
            ok, log = accept_verifier(sol.get('verifier_python', ''), gold, fmt)
            while not ok and vtry < VERIFY_RETRIES:   # 검증기-코딩은 확률적 → 같은 모델에 에러힌트 주고 재시도
                vtry += 1                              # (escalation/FLAG의 상당수가 이 '검증기 누명' → 같은 티어서 흡수)
                sol2 = call_model(tiles, fmt, meta, model, effort, img_dir, verify_hint(log))
                if sol2 and str(sol2.get('answer')).strip().strip('\'"') == gold:
                    ok2, log2 = accept_verifier(sol2.get('verifier_python', ''), gold, fmt)
                    if ok2:
                        sol, ok, log = sol2, True, log2   # 새(깨끗한) 검증기 통과 → 채택
            if not ok:                            # 재시도까지 실패 (답은 gold 일치, 검증기만 못 짬)
                last = f'{model}:verify-fail:{log[:30]}'; trace.append((model, f'verify-fail×{1 + vtry}'))
                if AGENT_TIER:
                    break                          # 답 맞음 → 사다리 그라인딩 멈추고 에이전트가 verified:true 마무리
                # (빠른 모드) 비킬러면 즉시 verified:false 인플레이스 구제(추가 콜 0); 킬러/haiku는 escalate
                if tier != 'killer' and model != 'haiku':
                    trace.append((model, 'salvage-inplace(미검증)'))
                    write_solution(p, sol, 'unverified', model, solved_by, trace, verified=False)
                    fix_score(p, str(sol.get('score', '')))
                    return f'CACHED@{model[0]}~'
                continue                          # 킬러/haiku → 상위 모델로 escalate
            VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
            (VERIFIER_DIR / f'{p.stem}.py').write_text(sol['verifier_python'], encoding='utf-8')
            vref = f'db/solutions/{p.stem}.py'
        else:
            vref = try_write_verifier(p, sol.get('verifier_python', ''), gold, fmt)  # 단답형 additive 검산기(게이트 통과 시만, 아니면 gold-match)
        trace.append((model, f'pass(retry×{vtry})' if vtry else 'pass'))
        write_solution(p, sol, vref, model, solved_by, trace)
        fix_score(p, str(sol.get('score', '')))   # 같은 이미지 읽기로 배점도 교정
        return f'CACHED@{model[0]}'
    # 사다리 전멸(또는 verify-fail에서 break) →
    if AGENT_TIER:        # ① 전체도구 에이전트 직접 풀이(코드+검증기) — verified:true 목표
        r = _agent_solve(p, tiles, fmt, meta, img_dir, gold, solved_by, trace)
        if r:
            return r
    # ② 답만이라도 구제(verified:false) → 그것도 안 되면 FLAG
    return _salvage(p, tiles, fmt, meta, img_dir, gold, solved_by, trace) or f'FLAG({last})'


def find(slug: str) -> Path | None:
    m = glob.glob(str(ROOT / 'docs' / 'problems' / '**' / f'{slug}.md'), recursive=True)
    return Path(m[0]) if m else None


_TIER = {'killer': 0, 'mid': 1, 'early': 2}


def difficulty_key(p: Path):
    """난이도 내림차순 정렬 키: killer > mid > early, 그 안에서 배점↓, 문제번호↓."""
    t = p.read_text(encoding='utf-8')
    g = lambda k: (re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M) or [None, None])[1]
    tier = _TIER.get(g('killer_tier'), 3)
    try: sc = -int(g('score') or 0)
    except Exception: sc = 0
    try: num = -int(g('number') or 0)
    except Exception: num = 0
    return (tier, sc, num)


def all_by_difficulty() -> list[Path]:
    fs = [Path(f) for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)
          if 'README' not in f]
    return sorted(fs, key=difficulty_key)


def _bucket(r: str) -> str:
    if r.startswith('CACHED'): return 'CACHED'
    if r.startswith('skip'): return 'skip'
    if r.startswith('ERROR'): return 'ERROR'
    return 'FLAG'


if __name__ == '__main__':
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from collections import Counter
    args = sys.argv[1:]
    parallel = 1
    if '--parallel' in args:
        i = args.index('--parallel'); parallel = int(args[i + 1]); del args[i:i + 2]
    easy_first = '--easy-first' in args   # 복구: 싼 문제(early/mid) 먼저 → 한도 재충돌 시 손실 최소
    if easy_first: args.remove('--easy-first')
    if args and args[0] == '--slug':
        targets = [x for x in [find(args[1])] if x]
    elif args and args[0] == '--list':
        targets = [q for s in args[1].split(',') if (q := find(s.strip()))]
    elif args and args[0] == '--sample':
        targets = all_by_difficulty()[:int(args[1])]
    elif args and args[0] == '--all':
        targets = all_by_difficulty()
    else:
        targets = all_by_difficulty()[:1]

    targets = sorted(targets, key=difficulty_key)   # 킬러-먼저: 느린 문제 먼저 출발 → straggler/makespan 최소화 (--list 인제스트 경로 포함)
    if easy_first: targets = targets[::-1]
    print(f'대상 {len(targets)}문제 · 병렬 {parallel} · {"쉬운순" if easy_first else "난이도순"}\n', flush=True)
    if parallel == 1:
        globals()['HEARTBEAT'] = True       # 단일/디버깅 실행 → HEARTBEAT_S 마다 진행 하트비트(묵음 해소)
    res = Counter(); flags = []; t0 = time.time(); done = 0
    # circuit-breaker: 연속 N개 실패면 API 한도/장애로 보고 중단 (죽은 API에 헛 FLAG 방지).
    # CACHED 가 나오면 리셋, skip(이미 캐시)은 무시.
    consec_fail = 0; ABORT_AFTER = 8; aborted = False
    def _timed(p):                       # 문항별 실측 소요시간(워커 점유~완료) → 느린 문항 식별
        _s = time.time()
        try: return build_one(p), time.time() - _s
        except Exception as e: return f'ERROR:{type(e).__name__}', time.time() - _s
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        futs = {ex.submit(_timed, p): p for p in targets}
        for fut in as_completed(futs):
            p = futs[fut]; done += 1
            r, dt = fut.result()
            cat = _bucket(r)
            res[cat] += 1
            if cat in ('FLAG', 'ERROR'):
                flags.append(f'{p.stem}: {r}')
                # breaker 는 API 장애 신호(gen-fail/ERROR)만 카운트. ans≠gold·verify-fail 은
                # 개별 데이터/검증 문제라 연속돼도 API 죽음 아님 → 리셋(false-trip 방지).
                consec_fail = consec_fail + 1 if ('gen-fail' in r or cat == 'ERROR') else 0
            elif cat == 'CACHED':
                consec_fail = 0
            print(f'[{done}/{len(targets)}] {p.stem}  →  {r}  ({dt:.0f}s)', flush=True)
            if consec_fail >= ABORT_AFTER:
                aborted = True
                print(f'\n⚠ {ABORT_AFTER}연속 실패 — API 한도/장애 의심. 중단 (캐시된 건 보존). 회복 후 재실행.', flush=True)
                ex.shutdown(wait=False, cancel_futures=True)
                break
    dt = time.time() - t0
    print(f'\n=== 요약 ({dt:.0f}s, 병렬 {parallel}) ===')
    for k, v in res.most_common():
        print(f'  {k}: {v}')
    if targets:
        print(f'  통과율: {res["CACHED"]}/{len(targets)} = {100*res["CACHED"]//max(1,len(targets))}%')
    if flags:
        print('\n실패/플래그:')
        for f in flags: print(f'  - {f}')
