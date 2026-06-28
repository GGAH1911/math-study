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
from solve_prompts import build_prompt, build_text_prompt, build_openbook_prompt, build_promote_prompt

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
VENV_PY = Path('/home/insung/Projects/math-study/.venv/bin/python')
VERIFIER_DIR = ROOT / 'db' / 'solutions'
MODEL = 'sonnet'
# ★claude -p 캐시 친화: 레포 cwd면 git status(미커밋 변경)가 시스템 프롬프트 env 블록을 매 호출 바꿔
#   프롬프트 캐시를 깬다. 깨끗한 빈 cwd에서 claude를 spawn → prefix 안정 → cache_read 생존(입력비용↓).
#   이미지 접근은 --add-dir(절대경로)로 유지. 참고: docs/CLAUDE_P_CACHING.md.
CLEAN_DIR = os.environ.get('CLAUDE_P_CWD', '/tmp/claude_p_clean')
os.makedirs(CLEAN_DIR, exist_ok=True)
# ★git 블록 제거 → prompt 캐시 prefix 안정(cache_read 고정). clean cwd 와 벨트+멜빵.
#   --add-dir 가 레포(이미지)를 가리켜도 git status 가 system prompt 를 안 흔든다(실측 검증).
CLAUDE_ENV = {**os.environ, 'CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS': '1'}

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
# verifier 안전: 파일/네트워크/시스템 접근 금지 — 순수 수학만 허용.
# 위험 토큰은 *호출/import/속성 문맥*에 한정해 차단한다(bare word boundary 금지 X):
#   · 위험 모듈(os/subprocess/...): `import X` / `from X` / `X.` 속성접근만 차단
#   · 위험 빌트인(open/eval/exec): 메서드호출 `.eval(`(sympy Poly/expr) 은 허용,
#     `.`·식별자문자 앞이 없는 *bare* 호출만 차단
#   · `__import__(...)` 차단. `Path` 는 sympy 심볼/클래스명으로 합법 → 목록에서 제거하고
#     대신 pathlib/os.path import·속성접근으로 막는다.
_FORBID_MODS = r'os|subprocess|socket|shutil|requests|httpx|urllib|pathlib'
FORBIDDEN = re.compile(
    r'(?:\b(?:import|from)\s+(?:' + _FORBID_MODS + r')\b'      # import os / from subprocess ...
    r'|\b(?:' + _FORBID_MODS + r')\.'                          # os.path / subprocess.run 등 속성접근
    r'|(?<![.\w])(?:open|eval|exec)\s*\('                      # bare open(/eval(/exec( (메서드호출 .eval( 제외)
    r'|\b__import__\s*\()'                                     # 동적 import
)
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
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S, cwd=CLEAN_DIR, env=CLAUDE_ENV)
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




def call_model_text(problem_text: str, fmt: str, meta: str, model: str, effort: str) -> dict | None:
    """식-텍스트 우회 — 이미지 없이 searchable_text만으로 풀이(도구 없음). vision 누명 제거용."""
    prompt = build_text_prompt(problem_text, fmt, meta)
    args = ['claude', '-p', '--model', model, '--effort', effort,
            '--disallowedTools', 'Read,Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '6', '--system-prompt', SYSTEM_TEXT, '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S, cwd=CLEAN_DIR, env=CLAUDE_ENV)
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


def call_openbook(problem_text: str, gold: str, fmt: str, steps_text: str,
                  model: str, effort: str, hint: str = '', lite: bool = False) -> dict | None:
    """Open-book: 정답+풀이단계를 주고 역대입 검산기를 작성하게 함 (이미지 없음).
    lite=True: 핵심 관계식 하나만 검증하는 경량 모드(킬러 회복용)."""
    prompt = build_openbook_prompt(problem_text, gold, fmt, steps_text, lite=lite)
    if hint:
        prompt += f"\n\n{hint}"
    args = ['claude', '-p', '--model', model, '--effort', effort,
            '--disallowedTools', 'Read,Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '6', '--system-prompt', SYSTEM_TEXT, '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S, cwd=CLEAN_DIR, env=CLAUDE_ENV)
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
                       r'integrate|diff|limit|Poly|simplify|expand|factor|Matrix|det|Rational|'
                       r'binomial|factorial|permutations|combinations|product|ff|rf)\b')


def _set_candidate(code: str, val: str) -> str:
    return re.sub(r'(?m)^CANDIDATE\s*=.*$', f'CANDIDATE = {val}', code, count=1)


def hardcode_gate(code: str, gold: str, fmt: str) -> tuple[bool, str]:
    """역대입 검산기 진위 판정 — 변이테스트로 하드코딩 차단.
    반환 (통과, 사유). 통과 = 원래 문제식에 실제로 의존하는 검산기."""
    from fractions import Fraction
    # 객관식(gold=보기번호 1-5): 보기번호↔값 매핑(=선택지)을 솔버에 강제하지 않으면 보기번호 변이가
    # 성립 안 함. 변이테스트 도입(b639cd88) 전 2021 성공 방식 복원 — 실제 식 풀이 + 원본 통과만 요구.
    if fmt == 'choice':
        if not _REALMATH.search(code):
            return False, 'no-realmath'
        ok, _ = run_verifier(code)
        return (True, 'ok') if ok else (False, 'orig-fail')
    if not re.search(r'(?m)^CANDIDATE\s*=', code):
        return False, 'no-CANDIDATE'
    # CANDIDATE 리터럴이 gold 와 일치해야 함 (객관식: 값-6을 CANDIDATE로 잡고 gold보기번호와 안 엮는 lite 차단)
    mcand = re.search(r'(?m)^CANDIDATE\s*=\s*([^\n#]+?)\s*$', code)
    if mcand:
        try:
            if Fraction(mcand.group(1).strip()) != Fraction(str(gold)):
                return False, 'candidate-not-gold'
        except Exception:
            pass                                          # 파싱 불가 → 관대(변이테스트가 추가 방어)
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


# ───────────────── lite → full 승격 (파라미터 솔버 = 유사문제 재생성 가능) ─────────────────
def _run_code(code: str, timeout: int = 40) -> str:
    """코드 실행 후 전체 stdout+stderr 반환 (param 변이 하네스용)."""
    if FORBIDDEN.search(code):
        return 'FORBIDDEN'
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write(code); tmp = f.name
    try:
        r = subprocess.run([str(VENV_PY), tmp], capture_output=True, text=True, timeout=timeout)
        return r.stdout + '\n' + r.stderr
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
    finally:
        try: os.unlink(tmp)
        except Exception: pass


_PARAM_HARNESS = """
# === param-mutation harness (auto-appended) ===
def __param_test():
    import inspect
    try:
        base = solve()
    except Exception as e:
        print("PARAM_BASE_ERR:", e); return
    try:
        params = inspect.signature(solve).parameters
    except Exception:
        print("PARAM_NO_SIG"); return
    dep = False
    for nm, pr in params.items():
        d = pr.default
        cands = [not d] if isinstance(d, bool) else (
                [d + 1, d + 2, d - 1] if isinstance(d, (int, float)) else [])
        for c in cands:
            try:
                if solve(**{nm: c}) != base:
                    dep = True; break
            except Exception:
                continue
        if dep:
            break
    print("PARAM_DEPENDENT" if dep else "PARAM_INDEPENDENT")
__param_test()
"""


def param_mutation_gate(code: str, gold: str) -> tuple[bool, str]:
    """full(파라미터 솔버) 판정 — solve(**계수) 가 (1) 기본호출 시 정답 산출(VERIFY_PASS),
    (2) 문제 계수를 바꾸면 답이 바뀜(=유사문제 재생성 가능). lite·답박힘은 param-independent 로 탈락."""
    if not re.search(r'(?m)^\s*def\s+solve\s*\(', code):
        return False, 'no-solve-fn'
    ok, _ = run_verifier(code)                       # 기본호출 solve()==CANDIDATE==gold (솔버 자체검증)
    if not ok:
        return False, 'base-fail'
    out = _run_code(code + '\n' + _PARAM_HARNESS)
    if 'PARAM_DEPENDENT' in out:
        return True, 'ok'
    if 'PARAM_INDEPENDENT' in out:
        return False, 'param-independent'            # 계수 바꿔도 답 불변 = 재생성 불가(답만 박힘)
    if 'PARAM_BASE_ERR' in out:
        return False, 'base-err'
    return False, 'harness-err'




def call_promote(problem_text: str, gold: str, fmt: str, steps_text: str, lite_code: str,
                 model: str, effort: str, hint: str = '') -> dict | None:
    """lite 검산기를 앵커로 full 파라미터 솔버를 작성하게 함."""
    prompt = build_promote_prompt(problem_text, gold, fmt, steps_text, lite_code)
    if hint:
        prompt += f"\n\n{hint}"
    args = ['claude', '-p', '--model', model, '--effort', effort,
            '--disallowedTools', 'Read,Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '6', '--system-prompt', SYSTEM_TEXT, '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S, cwd=CLEAN_DIR, env=CLAUDE_ENV)
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
        r = subprocess.run(args, capture_output=True, text=True, timeout=AGENT_TIMEOUT, cwd=CLEAN_DIR, env=CLAUDE_ENV)
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


HANDSOLVE_MODE = os.environ.get('HANDSOLVE', '1') == '1'   # 도형·킬러·검증불가 → opus/agent 분단위 낭비 대신 손풀이 큐
HANDSOLVE_DIR = VERIFIER_DIR / '_handsolve'


def _round_parts(stem: str):
    """slug → (round, subject, number). 2019_고3_3월모의고사_나형_19 → (…모의고사, 나형, 19)."""
    parts = stem.rsplit('_', 2)
    return (parts[0], parts[1], parts[2]) if len(parts) == 3 else (stem, '', '')


def _tiles_for(p: Path) -> list[str]:
    """문제 원본 이미지의 vision 타일 절대경로(있으면). 오케스트레이터가 Read 로 직접 보도록 큐에 넣는다.
    [[feedback_tiles_for_llm]]: LLM 은 통이미지(다운스케일로 깨짐)가 아니라 원해상도 타일만 봐야 한다."""
    real_img = IMGDIR / f'{p.stem}.png'
    if not real_img.exists():
        return []
    try:
        return [str(t) for t in tile_for_vision(str(real_img))]
    except Exception:
        return []


def _queue_entry(p: Path, gold, fmt, has_fig, tier, reason, best_sol, trace):
    """손풀이 큐 json 만 기록(md 는 안 건드림). gold-match-무솔버 처럼 답은 맞았지만
    솔버가 필요한 경우에도 재사용."""
    rnd, subj, num = _round_parts(p.stem)
    HANDSOLVE_DIR.mkdir(parents=True, exist_ok=True)
    tiles = _tiles_for(p)
    entry = {
        'slug': p.stem, 'round': rnd, 'subject': subj, 'number': num,
        'gold': gold, 'format': fmt, 'has_figure': has_fig, 'tier': tier,
        'reason': reason,
        'best_answer': str((best_sol or {}).get('answer') or (best_sol or {}).get('answer_value') or ''),
        'best_steps': (best_sol or {}).get('solution_steps') or [],
        'trace': [f'{m}:{r}' for m, r in (trace or [])],
        'image': f'/problem-images/{p.stem}.png',
        # ★오케스트레이터 지시: 이 타일들을 Read 로 직접 보고 풀어라(통이미지·텍스트 추론만으로 도형 추측 금지).
        #   도형 문제는 특히 타일 판독이 필수. [[feedback_tiles_for_llm]] · scripts/CLAUDE.md 핸드솔브 프로토콜.
        'vision_tiles': tiles,
        'instruction': 'Read 로 vision_tiles 의 원해상도 타일을 직접 보고 풀이/솔버를 작성하라. 통이미지 다운스케일이나 텍스트 추론만으로 도형·그래프를 추측하지 말 것.',
    }
    (HANDSOLVE_DIR / f'{p.stem}.json').write_text(
        json.dumps(entry, ensure_ascii=False, indent=2), encoding='utf-8')


def _defer(p: Path, best_sol, gold, fmt, has_fig, tier, reason, solved_by, trace):
    """auto 가 검증된 솔버를 못 짠 문제(도형·킬러·검증불가)를 손풀이 큐로 넘긴다.
    opus/agent/salvage 의 분 단위 낭비를 끊고 gold·잠정답·부분풀이를 _handsolve/<slug>.json 으로
    핸드오프 → 세션의 Claude(오케스트레이터)가 **직접** 풀어 db/solutions/<slug>.py (파라미터 솔버)
    + verified:true 로 대체. ★서브에이전트/워크플로우 재위임 금지(=실패한 auto 반복). 큐 감지 즉시
    캐시 빌드와 **병렬·실시간**으로 드레인. 상세 프로토콜 scripts/CLAUDE.md '핸드솔브 — 정의와 진입시기'."""
    _queue_entry(p, gold, fmt, has_fig, tier, reason, best_sol, trace)
    steps = (best_sol or {}).get('solution_steps') or [f'auto 솔버 생성 실패({reason}) — 손풀이 대기(handsolve queue).']
    av = (best_sol or {}).get('answer_value') or (best_sol or {}).get('answer') or gold
    write_solution(p, {'answer_value': str(av), 'solution_steps': steps},
                   'handsolve-pending', 'handsolve', solved_by, trace, verified=False)
    return f'HANDSOLVE({reason})'


OPENBOOK_REROLL = int(os.environ.get('OPENBOOK_REROLL', '2'))


def _ob_gate_hint(why: str) -> str:
    """변이게이트 실패사유 → 다음 재롤 교정 힌트 (backfill 과 동일)."""
    if why == 'orig-fail':
        return ('⚠ 직전 검산기가 VERIFY_FAIL/크래시였다. 원래 문제의 식·조건에 CANDIDATE 를 '
                '역대입하는 로직을 처음부터 재검토해 다시 작성하라.')
    if why.startswith('mutation-pass'):
        return ('⚠ 직전 검산기가 *틀린 답*에도 VERIFY_PASS 를 냈다(하드코딩 의심). 원래 문제의 '
                '식·조건에 CANDIDATE 를 실제로 대입/풀이해서, 틀린 값이면 반드시 VERIFY_FAIL 이 나오게 하라.')
    if why == 'no-realmath':
        return ('⚠ 직전 검산기에 실제 수식 풀이(sympy solve/Eq/subs/isclose 등)가 없다. '
                '문제의 원래 식을 코드로 표현하고 CANDIDATE 를 대입해 판정하라.')
    if why == 'self-compare':
        return ('⚠ 직전 검산기가 답을 자기 자신과 직접 비교(if CANDIDATE == 정답)했다. 금지다. '
                '원래 문제의 식에 대입한 결과로만 판정하라.')
    if why == 'no-CANDIDATE':
        return '⚠ 맨 윗줄에 CANDIDATE = <정답> 정의가 없다. 반드시 그렇게 시작하라.'
    return ''


def openbook_phase(problem: str, gold: str, fmt: str, steps: str,
                   rerolls: int = OPENBOOK_REROLL, lite: bool = False) -> str | None:
    """정답+steps 주입 open-book 단계적 솔버 + 하드코딩 게이트(변이테스트). 통과 verifier_python / None.

    build_one(인제스트)·backfill 공용: blind 가 '답은 맞췄으나 검증기를 못 짤' 때, 이미 아는 정답과
    풀이단계를 주입해 Haiku 가 솔버를 단계적으로 작성하게 한다. 변이테스트로 하드코딩 가짜를 차단."""
    hint = ''
    for _ in range(rerolls + 1):                   # Haiku-only · open-book
        try:
            sol = call_openbook(problem, gold, fmt, steps, 'haiku', 'high', hint, lite=lite)
        except Exception:
            sol = None
        if not sol:
            continue
        vp = sol.get('verifier_python', '') or ''
        if not vp:
            continue
        good, why = hardcode_gate(vp, gold, fmt)    # ★ 하드코딩 게이트(변이테스트)
        if good:
            return vp
        hint = _ob_gate_hint(why)
    return None


def build_one(p: Path) -> str:
    t = p.read_text(encoding='utf-8')
    if already_cached(t):
        return 'skip-cached'
    gold = gold_answer(t)
    img = IMGDIR / (p.stem + '.png')
    if not gold or not img.exists():
        return 'skip-no-gold-or-img'
    # ── 전항정답(출제오류로 모두 정답) 등 비정수 gold: blind-solve 불가(정수 답과 영원히 불일치)
    #    → 가짜 FLAG 대신, 손-작성 솔버(db/solutions/<stem>.py)가 있으면 verified 로 연결한다. ──
    if not gold.lstrip('-').isdigit():
        if (VERIFIER_DIR / f'{p.stem}.py').exists():
            write_solution(p, {'answer_value': gold, 'solution_steps': [
                f'출제오류로 전항정답(모두 정답) 처리된 문항이라 단일 정답이 없다 (answer="{gold}").',
                f'그 사유(전제 모순 등)는 검증 솔버 db/solutions/{p.stem}.py 가 수학적으로 증명한다.',
            ]}, f'db/solutions/{p.stem}.py', 'hand', solved_by='errata', verified=True)
            return 'ERRATA(전항정답·hand-solver)'
        return 'skip-errata(no-hand-solver)'
    fm = re.search(r'^format:\s*(\w+)', t, re.M)
    fmt = fm.group(1) if fm else 'choice'
    tier = (re.search(r'^killer_tier:\s*(\w+)', t, re.M) or [None, None])[1]
    has_fig = bool(re.search(r'^has_figure:\s*true\b', t, re.M))
    ladder = LADDER_KILLER if tier == 'killer' else LADDER_DEFAULT   # 킬러는 Haiku 스킵
    meta = f"문항 형식: {'객관식 5지선다' if fmt == 'choice' else '단답형(정수 정답)'}"
    real_img = img.resolve()                        # 심링크 → 실제 db/raw 원본
    tiles = [str(t) for t in tile_for_vision(real_img)]  # 세로 길면 원해상도 N타일(tiles/ 하위)
    img_dir = str(real_img.parent)                  # 단일 이미지·tiles/ 둘 다 이 dir 아래
    last = ''
    trace = []           # 모델별 결과 (escalation 사유 기록)
    solved_by = None     # 최초로 답(ans==gold)을 맞힌 모델 = 난이도 신호 (검증기 통과와 무관)
    last_ok_sol = None   # 답은 맞췄으나 blind 검증기를 못 짠 sol (사다리 후 open-book·구제용)

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
                if vref_t == 'gold-match' and HANDSOLVE_MODE:   # 단답 gold-match(솔버 없음) → 솔버용 큐
                    _queue_entry(p, gold, fmt, has_fig, tier, 'no-solver:gold-match', solt,
                                 [('haiku-text', 'pass')])
                    return 'CACHED@T|need-solver'
                return 'CACHED@T'
        trace.append(('haiku-text', 'text-fail'))  # 텍스트 실패 → 이미지 사다리 폴백

    # ── 사전 defer: 킬러는 blind 검증기 사다리가 거의 항상 헛돔(분 단위 → 미검증 salvage) → a priori 손풀이.
    #    figure(도형)는 교정기가 텍스트+그래픽 대조를 끝냈으므로 이미지 사다리를 한 번은 태운다:
    #    도형 계산(좌표·각도·넓이)은 검증기가 짜이면 자동, 그래프 판독류는 gold-match로 떨어져 아래 840에서
    #    손풀이 큐로 간다(풀이 steps 는 vision 으로 자동 확보). (HANDSOLVE=0 으로 전체 끔)
    if HANDSOLVE_MODE and tier == 'killer':
        return _defer(p, None, gold, fmt, has_fig, tier, 'apriori:killer', solved_by, trace)

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
                last_ok_sol = sol                 # ① 답 맞췄으나 검증기 실패 → 보존(사다리 후 open-book·구제용)
                continue                          # ① opus 까지 모든 모델의 검증기를 escalate (sonnet 에서 멈추지 않음)
            VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
            (VERIFIER_DIR / f'{p.stem}.py').write_text(sol['verifier_python'], encoding='utf-8')
            vref = f'db/solutions/{p.stem}.py'
        else:
            vref = try_write_verifier(p, sol.get('verifier_python', ''), gold, fmt)  # 단답형 additive 검산기(게이트 통과 시만, 아니면 gold-match)
        trace.append((model, f'pass(retry×{vtry})' if vtry else 'pass'))
        write_solution(p, sol, vref, model, solved_by, trace)
        fix_score(p, str(sol.get('score', '')))   # 같은 이미지 읽기로 배점도 교정
        if vref == 'gold-match' and HANDSOLVE_MODE:   # 답은 gold 일치(verified)나 솔버 없음 → 솔버용 손풀이 큐
            _queue_entry(p, gold, fmt, has_fig, tier, 'no-solver:gold-match', sol, trace)
            return f'CACHED@{model[0]}|need-solver'
        return f'CACHED@{model[0]}'
    # 사다리 전멸(opus 까지 blind 검증기 실패) →
    # ★ ② open-book 단계적 솔버 (텍스트, 한 번): 답 맞췄으나 검증기 못 짠 경우 정답+풀이단계 주입
    if solved_by and last_ok_sol is not None:
        ob_problem = stext if (stext and len(stext) > 40) else (extract_searchable(t) or '')
        ob_steps = '\n'.join(f'- {s}' for s in (last_ok_sol.get('solution_steps') or []))
        if ob_problem:
            ob_vp = (openbook_phase(ob_problem, gold, fmt, ob_steps)
                     or openbook_phase(ob_problem, gold, fmt, ob_steps, lite=True))
            if ob_vp:
                VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
                (VERIFIER_DIR / f'{p.stem}.py').write_text(ob_vp, encoding='utf-8')
                trace.append(('open-book', 'pass'))
                write_solution(p, last_ok_sol, f'db/solutions/{p.stem}.py', solved_by, solved_by, trace)
                fix_score(p, str(last_ok_sol.get('score', '')))
                return f'CACHED@{solved_by[0]}+ob'
    # ② open-book(텍스트)도 실패 → 손풀이 큐 (opus/agent 분단위 낭비 대신 세션 Claude 가 직접 푼다)
    if HANDSOLVE_MODE:
        return _defer(p, last_ok_sol, gold, fmt, has_fig, tier, f'runtime:{last}', solved_by, trace)
    # ── (legacy, HANDSOLVE=0) 이미지 에이전트 → 미검증 구제 ──
    if AGENT_TIER:
        r = _agent_solve(p, tiles, fmt, meta, img_dir, gold, solved_by, trace)
        if r:
            return r
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
