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

SYSTEM = """당신은 한국 수능 수학 문제를 정확히 푸는 전문가입니다. 첨부된 문제 이미지를 Read 도구로 먼저 본 뒤 풀이하세요. 도형·조건·보기 값은 모두 이미지에서 확인합니다. 추측 금지."""


def build_prompt(img_abs: str, fmt: str, meta: str) -> str:
    lines = ['  "answer": <네가 푼 보기 번호 1-5 정수>,' if fmt == 'choice'
             else '  "answer": <네가 푼 단답형 정답 정수(0-999)>,']
    lines.append('  "answer_value": "<최종 답의 값만, 설명·중간식 없이. 예: -7/64 또는 163>",')
    lines.append('  "score": <2|3|4 정수, 이미지 상단의 "[N점]" 배점 그대로>,')
    if fmt == 'choice':
        lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."],')
        lines.append('  "verifier_python": "<자기완결 파이썬. **이미지에 주어진 원래 함수·방정식·조건**에 네 답을 역대입해 검사. 네가 유도한 *근사식·중간식을 쓰지 말고* 반드시 원래 문제의 식을 코드로 표현(필요하면 수치 root-find)해 답이 만족하는지 sympy/numpy 로 확인. 통과 시 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print. 파일·네트워크·os 금지, 수학 라이브러리만.>"')
    else:
        lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."]')
    body = '\n'.join(lines)
    return f"""문제 이미지: {img_abs}
{meta}

위 이미지를 Read 로 연 뒤 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** **마지막 메시지에 오직 하나의 ```json 블록**만 출력 (설명 산문 금지):

```json
{{
{body}
}}
```"""


def call_model(img_abs: str, fmt: str, meta: str, model: str, effort: str) -> dict | None:
    prompt = build_prompt(img_abs, fmt, meta)
    args = ['claude', '-p', '--model', model, '--effort', effort,
            '--allowedTools', 'Read', '--add-dir', str(IMGDIR),
            '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '14', '--system-prompt', SYSTEM, '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None
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


def gold_answer(md_text: str) -> str | None:
    """choice → 보기번호(1-5), numeric → 정수. 중첩 따옴표 제거."""
    m = re.search(r'^answer:\s*(.+?)\s*$', md_text, re.M)
    return m.group(1).strip().strip('\'"') if m else None


def already_cached(md_text: str) -> bool:
    return bool(re.search(r'^solution:\s*$', md_text, re.M))


def write_solution(p: Path, sol: dict, verifier_rel: str, model: str = MODEL):
    t = p.read_text(encoding='utf-8')
    if re.search(r'^solution:', t, re.M):
        return  # 동시 실행 레이스 방어 — 이미 solution 블록 있으면 중복 삽입 안 함

    steps = '\n'.join(f'    - {json.dumps(s, ensure_ascii=False)}' for s in sol['solution_steps'])
    block = (f"solution:\n"
             f"  answer_value: {json.dumps(str(sol.get('answer_value','')), ensure_ascii=False)}\n"
             f"  verified: true\n"
             f"  generated_by: {model}\n"
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
    last = ''
    for model, effort in ladder:                  # 모델별 1회 (blind)
        sol = call_model(str(img), fmt, meta, model, effort)
        if not sol:
            last = f'{model}:gen-fail'; continue
        ans = str(sol.get('answer')).strip().strip('\'"')
        if ans != gold:                           # blind 답이 공식 gold 와 불일치 → escalate
            last = f'{model}:ans{ans}≠{gold}'; continue
        # 단답형: gold 정수 일치로 충분. 5지선다: 원본식 역대입 검증기까지.
        if fmt == 'choice':
            ok, log = run_verifier(sol.get('verifier_python', ''))
            if not ok:
                last = f'{model}:verify-fail:{log[:30]}'; continue
            VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
            (VERIFIER_DIR / f'{p.stem}.py').write_text(sol['verifier_python'], encoding='utf-8')
            vref = f'db/solutions/{p.stem}.py'
        else:
            vref = 'gold-match'                    # 단답형 — 검증기 없음
        write_solution(p, sol, vref, model)
        fix_score(p, str(sol.get('score', '')))   # 같은 이미지 읽기로 배점도 교정
        return f'CACHED@{model[0]}'
    return f'FLAG({last})'


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

    if easy_first: targets = targets[::-1]
    print(f'대상 {len(targets)}문제 · 병렬 {parallel} · {"쉬운순" if easy_first else "난이도순"}\n', flush=True)
    res = Counter(); flags = []; t0 = time.time(); done = 0
    # circuit-breaker: 연속 N개 실패면 API 한도/장애로 보고 중단 (죽은 API에 헛 FLAG 방지).
    # CACHED 가 나오면 리셋, skip(이미 캐시)은 무시.
    consec_fail = 0; ABORT_AFTER = 8; aborted = False
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        futs = {ex.submit(build_one, p): p for p in targets}
        for fut in as_completed(futs):
            p = futs[fut]; done += 1
            try: r = fut.result()
            except Exception as e: r = f'ERROR:{type(e).__name__}'
            cat = _bucket(r)
            res[cat] += 1
            if cat in ('FLAG', 'ERROR'):
                flags.append(f'{p.stem}: {r}')
                # breaker 는 API 장애 신호(gen-fail/ERROR)만 카운트. ans≠gold·verify-fail 은
                # 개별 데이터/검증 문제라 연속돼도 API 죽음 아님 → 리셋(false-trip 방지).
                consec_fail = consec_fail + 1 if ('gen-fail' in r or cat == 'ERROR') else 0
            elif cat == 'CACHED':
                consec_fail = 0
            print(f'[{done}/{len(targets)}] {p.stem}  →  {r}', flush=True)
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
