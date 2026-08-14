#!/usr/bin/env python3
"""기존 솔버를 **파라미터화 규격**으로 개조하는 대량 배치.

★왜: `scripts/CLAUDE.md` 는 솔버의 핵심 용도를 "유사문제 무한 재생성" 이라 못 박는데,
  레포의 솔버 4,193개 중 `PARAMS` 를 가진 것은 50개뿐이다(2026-08-14 실측). 나머지는
  숫자가 박힌 **검증기**다 — 답은 맞히지만 새 문제를 못 찍어낸다. 그 간극을 메운다.

★왜 워크플로우가 아니라 배치 스크립트인가: 4,000건은 수십 시간짜리다. 세션이 끝나도
  살아남고, 죽은 자리에서 재개되고, `/progress` 로 관측돼야 한다. [[feedback_background_longtasks]]

★모델: **Sonnet**. 4건 표본에서 Opus 와 대등한 품질을 냈고(파라미터 생존율 12/12,
  두 게이트 통과) 토큰은 약 1/10 이었다. 개발·배치는 구독으로 돈다.
  [[feedback_claude_subscription_vs_product_api]]

안전장치:
  · 작업은 **스크래치 사본**에서 한다 — 에이전트는 레포를 못 본다(cwd=빈 폴더, 캐시 안정).
  · 결과는 **두 게이트**를 모두 통과해야 채택한다(파라미터화 규격 + 기존 하드코딩 게이트).
  · 하나라도 실패하면 **원본을 되돌린다.** 개악은 남기지 않는다.
  · 게이트는 서브프로세스로 돌린다 — 남의 코드를 인프로세스로 exec 하면 무한루프 하나에
    배치 전체가 멈춘다.

사용:
  python3 scripts/parameterize_solvers.py --limit 8            # 맛보기
  python3 scripts/parameterize_solvers.py --workers 6          # 전수(재개 가능)
  python3 scripts/parameterize_solvers.py --round 2026_수능    # 회차 한정
"""
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOL = ROOT / 'db' / 'solutions'
PROB = ROOT / 'docs' / 'problems'
STATE = ROOT / 'db' / 'solutions' / '_paramstate.json'
VENV = os.environ.get('MS_PY', str(Path.home() / '.venvs/ms-ingest/bin/python'))

sys.path.insert(0, str(ROOT / 'scripts'))
from claude_auth import claude_env, looks_unauthed  # noqa: E402

CLAUDE_ENV = claude_env()
TIMEOUT_S = int(os.environ.get('PARAM_TIMEOUT', '900'))
GATE_TIMEOUT_S = 180

# ★프롬프트 캐시 레인(2026-08-14). `claude -p` 의 시스템 프롬프트에는 **cwd 경로와 그
#   내용**이 들어간다. 항목마다 새 임시폴더를 cwd 로 주면 prefix 가 매번 달라져
#   **캐시가 전부 깨진다**(4,000건 배치에서는 입력비용이 통째로 재청구된다).
#   그래서 워커마다 **고정된 빈 cwd** 를 쓴다 — 워커별로 prefix 가 안 변하니 첫 항목
#   이후로는 계속 cache_read 가 걸린다. 작업 파일은 cwd 를 더럽히지 않도록 별도
#   폴더에 두고 `--add-dir` 로만 노출한다(빈 cwd 를 빈 채로 유지해야 prefix 가 산다).
#   [[project_claude_p_caching]]
LANES = Path(os.environ.get('PARAM_LANES', '/tmp/claude_p_param'))
_lane = threading.local()


def lane_dirs() -> tuple[Path, Path]:
    """이 스레드 전용 (빈 cwd, 작업폴더). 스레드마다 한 번만 만든다."""
    if not hasattr(_lane, 'idx'):
        with _lane_lock:
            global _lane_next
            _lane.idx = _lane_next
            _lane_next += 1
    cwd = LANES / f'cwd{_lane.idx}'
    work = LANES / f'work{_lane.idx}'
    cwd.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    for p in cwd.iterdir():            # cwd 는 **항상 비어 있어야** prefix 가 안 변한다
        shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True)
    for p in work.iterdir():
        shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True)
    return cwd, work


_lane_lock = threading.Lock()
_lane_next = 0

SYSTEM = (
    '당신은 한국 수능 수학 문제의 파이썬 솔버를 작성하는 전문가입니다. '
    '주어진 솔버는 답을 맞히지만 숫자가 박혀 있어 새 문제를 못 만듭니다. '
    '문제의 수학 구조를 파라미터로 드러내되, 원문제의 답은 반드시 그대로 재현해야 합니다.'
)

PROMPT = '''`{work}/solver.py` 를 **파라미터화 규격**으로 고쳐 쓰세요. `{work}/problem.txt` 가 원문제입니다.

## 규격
```python
CANDIDATE = <원문제의 정답>        # ★절대 바꾸지 마세요
PARAMS = dict(...)                # 문제를 정하는 값들 (계수·조건값·구간 등)
def solve(prm): ...               # 조건 → 답. 문제의 수학 구조를 코드로.
def statement(prm): ...           # 그 파라미터로 만들어지는 문제 문장(한국어)
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
```

## 반드시 지킬 것
1. `solve(PARAMS)` 가 `CANDIDATE` 를 재현해야 합니다. **정답을 바꾸지 마세요.**
2. **답을 실제로 바꾸는 파라미터가 2개 이상**이어야 합니다. 선언만 하고 안 쓰는 장식
   파라미터는 게이트에서 걸립니다. 각 파라미터를 바꿔 답이 정말 달라지는지 직접 돌려서 확인하세요.
3. 숫자를 그대로 반환하는 코드는 안 됩니다. **sympy 로 실제로 풀어야** 합니다.
4. 객관식이면 **값과 보기를 분리**하세요:
   `value(prm)`=수학적 답, `choices(prm)`=보기 목록(**값에서 유도**), `solve(prm)`=보기 번호.
   보기를 고정 튜플로 PARAMS 에 박으면 계수를 바꾸는 순간 값이 목록 밖으로 나가 죽습니다.
   유도한 보기가 원문제 보기와 같은지 `assert` 로 고정하세요.
5. 파라미터가 서로 **묶여 있어**(예: "자연수 m,n 을 구하시오" 처럼 정수해 조건) 하나만
   못 흔드는 문제라면, 성립하는 조합을 `VARIANTS = [dict(...), dict(...)]` 로 2개 이상
   제시하세요. 그중 2개 이상이 원문제와 **다른 답**을 내야 합니다.
6. 해가 없거나 파라미터 조합이 문제로 성립하지 않으면 `return None` 말고 **예외를 던지세요.**
7. 실행이 **40초를 넘으면 안 됩니다.** 탐색 범위를 좁히거나 닫힌 식을 쓰세요.
8. 주석은 한국어로, 어떤 수학 구조를 파라미터로 뽑았는지 적으세요.

## 작업 방법 — ★채점 게이트를 직접 돌리세요
`{work}/gate.py` 가 **실제 채점 게이트**입니다. 짐작하지 말고 이걸로 확인하세요:

```
{py} {work}/gate.py --file {work}/solver.py
```

`✅ 파라미터화 규격 충족` 이 나올 때까지 고치고 다시 돌리세요. 실패하면 무엇이 부족한지
(어떤 파라미터가 장식인지) 그대로 알려줍니다. **통과를 확인하지 않고 끝내지 마세요.**

- `{py} {work}/solver.py` 로도 돌려 `VERIFY_PASS` 를 확인하세요.
- 최종 결과를 **`{work}/solver.py` 에 그대로 저장**하세요. 다른 파일은 채점하지 않습니다.
- 임시 파일이 필요하면 `{work}` 안에만 만드세요. `gate.py` 는 수정하지 마세요.

게이트를 통과하지 못한 결과는 버려지고 원본이 복구됩니다.
'''


def _stdout_is(path: Path) -> bool:
    """stdout 이 이미 이 파일을 가리키는가.

    ★백그라운드로 띄울 때 `>> log` 로 stdout 을 로그파일에 붙이는데, 그 상태에서
      파일에도 또 쓰면 **모든 줄이 두 번 찍힌다**(2026-08-14 실측). 어떻게 띄우든
      스스로 알아채도록 inode 를 비교한다.
    """
    try:
        st = os.fstat(sys.stdout.fileno())
        ps = path.stat()
        return st.st_dev == ps.st_dev and st.st_ino == ps.st_ino
    except Exception:
        return False


def log(msg: str, path: Path | None = None) -> None:
    line = f'[{time.strftime("%H:%M:%S")}] {msg}'
    print(line, flush=True)
    if path and not _stdout_is(path):
        with path.open('a', encoding='utf-8') as f:
            f.write(line + '\n')


#: 캐시 실측 누계 — 주장하지 말고 재서 말한다.
CACHE = {'read': 0, 'write': 0, 'in': 0, 'out': 0, 'n': 0}


def _record_cache(stdout: str) -> None:
    """`--output-format json` 의 usage 에서 캐시 적중을 실제로 읽어 누적한다."""
    try:
        u = (json.loads(stdout) or {}).get('usage') or {}
    except Exception:
        return
    with _cache_lock:
        CACHE['read'] += int(u.get('cache_read_input_tokens') or 0)
        CACHE['write'] += int(u.get('cache_creation_input_tokens') or 0)
        CACHE['in'] += int(u.get('input_tokens') or 0)
        CACHE['out'] += int(u.get('output_tokens') or 0)
        CACHE['n'] += 1


_cache_lock = threading.Lock()


def cache_line() -> str:
    c = CACHE
    tot = c['read'] + c['write'] + c['in']
    hit = 100.0 * c['read'] / tot if tot else 0.0
    return (f'캐시 {hit:.0f}% 적중 (read {c["read"]:,} · write {c["write"]:,} · '
            f'in {c["in"]:,} · out {c["out"]:,} · {c["n"]}콜)')


def problem_md(stem: str) -> Path | None:
    hits = list(PROB.rglob(f'{stem}.md'))
    return hits[0] if hits else None


def problem_text(md: Path) -> tuple[str, str, str]:
    """(문제 본문, 정답, 형식)"""
    t = md.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'^searchable_text:\s*[|>][-+]?\s*\n(.*?)(?=^\S|\Z)', t, re.M | re.S)
    body = m.group(1).strip() if m else ''
    ans = re.search(r'^answer:\s*"?([^"\n]+)', t, re.M)
    fmt = re.search(r'^format:\s*"?([^"\n]+)', t, re.M)
    steps = re.findall(r'^\s+- (?:"|\')?(.+?)(?:"|\')?$', t, re.M)
    if steps:
        body += '\n\n[기존 풀이 단계]\n' + '\n'.join(f'  - {s}' for s in steps[:12])
    return body, (ans.group(1).strip() if ans else ''), (fmt.group(1).strip() if fmt else '')


def gate_params(stem: str) -> tuple[bool, str]:
    """파라미터화 규격 게이트 — 서브프로세스(무한루프 격리)."""
    try:
        r = subprocess.run([VENV, str(ROOT / 'scripts/ops/verify_solver_params.py'), stem],
                           capture_output=True, text=True, timeout=GATE_TIMEOUT_S, cwd=str(ROOT))
    except subprocess.TimeoutExpired:
        return False, '게이트 타임아웃'
    if r.returncode == 0:
        return True, 'ok'
    why = [ln.strip() for ln in r.stdout.splitlines() if ln.startswith('     ')]
    return False, (why[0] if why else '규격 미충족')[:200]


GATE_HARD = '''
import sys, pathlib, importlib.util as u
sys.path.insert(0, {scripts!r})
s = u.spec_from_file_location('b', {bsc!r}); m = u.module_from_spec(s)
try: s.loader.exec_module(m)
except SystemExit: pass
ok, why = m.accept_verifier(pathlib.Path({sol!r}).read_text(encoding='utf-8'), {gold!r}, {fmt!r})
print('OK' if ok else 'NO', why)
'''


def gate_hardcode(stem: str, gold: str, fmt: str) -> tuple[bool, str]:
    """기존 하드코딩 게이트(실제 수식 풀이 + 변이테스트)."""
    code = GATE_HARD.format(scripts=str(ROOT / 'scripts'), bsc=str(ROOT / 'scripts/build_solution_cache.py'),
                            sol=str(SOL / f'{stem}.py'), gold=gold, fmt=fmt)
    try:
        r = subprocess.run([VENV, '-c', code], capture_output=True, text=True,
                           timeout=GATE_TIMEOUT_S, cwd=str(ROOT))
    except subprocess.TimeoutExpired:
        return False, '하드코딩 게이트 타임아웃'
    out = (r.stdout or '').strip()
    return out.startswith('OK'), out[3:][:200] or (r.stderr or '')[-200:]


def run_one(stem: str, model: str, logf: Path) -> tuple[str, bool, str]:
    src = SOL / f'{stem}.py'
    md = problem_md(stem)
    if not src.exists():
        return stem, False, '솔버 파일 없음'
    if md is None:
        return stem, False, '문제 md 없음'
    body, gold, fmt = problem_text(md)
    if not gold:
        return stem, False, '정답 없음'
    original = src.read_text(encoding='utf-8', errors='replace')

    cwd, work = lane_dirs()
    (work / 'solver.py').write_text(original, encoding='utf-8')
    (work / 'problem.txt').write_text(
        f'[정답] {gold}\n[형식] {fmt}\n\n{body}\n', encoding='utf-8')
    # ★게이트 **원본을 그대로** 복사한다. 규격을 프롬프트로 옮겨 적으면 갈라진다.
    shutil.copy(ROOT / 'scripts/ops/verify_solver_params.py', work / 'gate.py')
    args = ['claude', '-p', '--output-format', 'json', '--model', model,
            '--allowedTools', 'Read,Write,Edit,Bash', '--add-dir', str(work),
            '--disallowedTools', 'WebFetch,WebSearch',
            '--max-turns', '40', '--system-prompt', SYSTEM, '--',
            PROMPT.format(work=str(work), py=VENV)]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S,
                           cwd=str(cwd), env=CLAUDE_ENV, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return stem, False, f'모델 타임아웃({TIMEOUT_S}s)'
    if looks_unauthed(r.stdout, r.stderr):
        raise SystemExit('claude -p 인증 실패 — 배치 중단 (claude_auth.py 참조)')
    _record_cache(r.stdout)

    new = (work / 'solver.py').read_text(encoding='utf-8', errors='replace')
    if new.strip() == original.strip():
        return stem, False, '변경 없음'
    if 'PARAMS' not in new or 'def solve(' not in new:
        return stem, False, '규격 미작성'

    src.write_text(new, encoding='utf-8')
    ok1, why1 = gate_params(stem)
    if not ok1:
        src.write_text(original, encoding='utf-8')
        return stem, False, f'파라미터화 게이트: {why1}'
    ok2, why2 = gate_hardcode(stem, gold, fmt)
    if not ok2:
        src.write_text(original, encoding='utf-8')
        return stem, False, f'하드코딩 게이트: {why2}'
    return stem, True, 'ok'


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {'done': {}, 'failed': {}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--model', default='sonnet')
    ap.add_argument('--round', default='')
    ap.add_argument('--stems', nargs='*', default=[])
    ap.add_argument('--retry-failed', action='store_true', help='이전에 실패한 것도 다시 시도')
    ap.add_argument('--log', default='')
    a = ap.parse_args()

    logf = Path(a.log) if a.log else Path(f'/tmp/ingest_logs/parameterize_{time.strftime("%Y%m%d_%H%M%S")}.log')
    logf.parent.mkdir(parents=True, exist_ok=True)

    state = load_state()
    if a.stems:
        todo = list(a.stems)
    else:
        todo = sorted(p.stem for p in SOL.glob('*.py') if not p.stem.startswith('_'))
        if a.round:
            todo = [s for s in todo if a.round in s]
        todo = [s for s in todo if s not in state['done']]
        if not a.retry_failed:
            todo = [s for s in todo if s not in state['failed']]
    if a.limit:
        todo = todo[:a.limit]

    log(f'대상 {len(todo)}건 · 모델 {a.model} · 병렬 {a.workers} · 로그 {logf}', logf)
    lock = threading.Lock()
    n_ok = n_no = 0
    t0 = time.time()

    def worker(stem: str):
        nonlocal n_ok, n_no
        try:
            s, ok, why = run_one(stem, a.model, logf)
        except SystemExit:
            raise
        except Exception as e:
            s, ok, why = stem, False, f'예외 {type(e).__name__}: {e}'
        with lock:
            if ok:
                n_ok += 1
                state['done'][s] = time.strftime('%Y-%m-%d %H:%M')
                state['failed'].pop(s, None)
            else:
                n_no += 1
                state['failed'][s] = why
            done = n_ok + n_no
            rate = done / max(1e-9, (time.time() - t0) / 3600)
            log(f'{"✅" if ok else "🔴"} {s} — {why}   [{done}/{len(todo)} · 성공 {n_ok} · '
                f'시간당 {rate:.0f}건 · 남은 예상 {(len(todo)-done)/max(rate,1e-9):.1f}h]', logf)
            # ★매 건 기록한다. 10건마다 쓰면 중단 시 마지막 9건이 상태에서 증발해
            #   재개할 때 다시 돌린다(방금 그렇게 날렸다). 파일이 작아 비용은 무시할 만하다.
            STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding='utf-8')

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(worker, todo))
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding='utf-8')
    log(f'끝 — 성공 {n_ok} · 실패 {n_no} (누적 완료 {len(state["done"])})', logf)
    log(cache_line(), logf)
    return 0


if __name__ == '__main__':
    sys.exit(main())
