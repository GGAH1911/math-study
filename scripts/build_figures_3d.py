#!/usr/bin/env python3
"""인제스트 체인 — **미리 검증된 3D 도형 스펙**을 만든다.

풀이 캐시 **뒤**에 돈다. 캐시가 끝나면 검증된 정답이 있어서, 작성 에이전트에게
"이 값은 답이니 그림에 쓰지 마라" 를 정확히 알려 줄 수 있기 때문이다.

한 문제의 처리는 **루프**다 — 작성만 하고 자기 그림을 안 보면 보기 나쁜 그림이 남는다
(2026-08-14 교훈):

    조건 추출 → 좌표 → sympy 전수 검증 → 스펙 작성
      → (dev 서버가 살아 있으면) 렌더 → 원본 도판과 대조 → 카메라·배율 고쳐 재렌더
      → 결정적 게이트 통과해야 등록. 못 통과하면 **등록하지 않는다.**

반쯤 맞는 그림보다 없는 게 낫다 — 없으면 튜터가 "이 문제는 입체가 필요 없다" 로 안전하게 넘어간다.

사용:
    python3 scripts/build_figures_3d.py --list <slug,slug,...> [--parallel 3] [--force]
"""
from __future__ import annotations
import argparse, concurrent.futures as cf, hashlib, json, os, re, subprocess, sys, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / 'docs' / 'problems'
FIG_DIR = ROOT / 'web' / 'src' / 'data' / 'figures-3d'
MODEL = os.environ.get('FIG3D_MODEL', 'opus')
TIMEOUT_S = int(os.environ.get('FIG3D_TIMEOUT', '1800'))
BASE = os.environ.get('MS_BASE', 'http://100.67.69.121:4324')
COMPOSE = ['docker', 'compose', '-f', str(ROOT / 'deploy/docker-compose.yml')]
# git 블록 제거 — 미커밋 변경이 system prompt 를 흔들어 프롬프트 캐시를 깨는 것 방지.
CLAUDE_ENV = {**os.environ, 'CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS': '1'}

UNIT_3D = '공간도형과_공간벡터'
# 단원 밖에서도 입체가 쓸모 있는 것들(정적분의 활용 = 단면적분 입체, 정사영 등).
KW = re.compile(r'회전체|회전시킨|입체도형|정육면체|직육면체|사면체|각뿔|원뿔|원기둥|구면|이면각|정사영')
SKIP_ROUND = re.compile(r'검정고시')   # 20문제 4지선다 — 3D 문항이 사실상 없다


def md_of(slug: str) -> Path | None:
    hits = list(PROBLEMS.rglob(f'{slug}.md'))
    return hits[0] if hits else None


def is_candidate(p: Path) -> bool:
    if SKIP_ROUND.search(str(p)):
        return False
    t = p.read_text(encoding='utf-8', errors='ignore')
    u = re.search(r'^unit:\s*(.+)$', t[:1500], re.M)
    return bool((u and UNIT_3D in u.group(1)) or KW.search(t))


def answer_of(p: Path) -> str:
    m = re.search(r'^answer:\s*"?([^"\n]+)"?', p.read_text(encoding='utf-8', errors='ignore'), re.M)
    return (m.group(1).strip() if m else '')


def source_sha(p: Path) -> str:
    """문제 본문의 해시 — 나중에 본문이 바뀌면 스펙이 낡았음을 게이트가 잡는다."""
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def dev_token() -> str | None:
    """렌더 대조용 짧은 수명 세션. dev 서버가 안 뜨면 None(대조 없이 진행)."""
    try:
        urllib.request.urlopen(f'{BASE}/api/health', timeout=5).read()
    except Exception:
        return None
    import secrets
    tok = secrets.token_hex(32)
    h = hashlib.sha256(tok.encode()).hexdigest()
    # admin 이메일은 DB 컬럼이 아니라 컨테이너 env 의 allowlist 다 — 거기서 꺼내 쓴다.
    r = subprocess.run(COMPOSE + ['exec', '-T', 'web', 'sh', '-c', 'echo "$MATH_STUDY_ADMIN_EMAILS"'],
                       capture_output=True, text=True)
    email = (r.stdout or '').split(',')[0].strip()
    if not email:
        return None
    sql = (f"insert into sessions (user_id, token_hash, expires_at, user_agent) "
           f"select id, '{h}', now()+interval '2 hours', 'ingest-figures3d' from users "
           f"where email = '{email}' limit 1;")
    r = subprocess.run(COMPOSE + ['exec', '-T', 'db', 'psql', '-U', 'mathstudy', '-d', 'mathstudy', '-Atc', sql],
                       capture_output=True, text=True)
    if 'INSERT 0 1' not in (r.stdout + r.stderr):
        return None
    return tok


def drop_token(tok: str) -> None:
    h = hashlib.sha256(tok.encode()).hexdigest()
    subprocess.run(COMPOSE + ['exec', '-T', 'db', 'psql', '-U', 'mathstudy', '-d', 'mathstudy',
                              '-Atc', f"delete from sessions where token_hash='{h}';"],
                   capture_output=True, text=True)


SYSTEM = (ROOT / 'scripts' / 'prompts' / 'figures_3d_system.md').read_text(encoding='utf-8') \
    if (ROOT / 'scripts' / 'prompts' / 'figures_3d_system.md').exists() else ''


def build_prompt(slug: str, md: Path, img: str, answer: str, tokfile: str | None) -> str:
    render = (f"""
**렌더해서 네 그림을 직접 봐라** (이게 이 작업의 핵심이다):
    MS_DEV_TOKEN_FILE={tokfile} node scripts/ops/render_figure3d.mjs {slug}
  → /tmp/fig3d/{slug}.png 를 Read 로 열어 **원본 도판과 나란히 비교**해라.
  다르면 cameraPosition·cameraTarget·displayScale·색·불투명도를 고쳐 **다시 렌더**해라. 최대 3회.
""" if tokfile else """
(dev 서버가 없어 렌더 대조는 건너뛴다. 좌표와 게이트만으로 판단해라.)
""")
    return f"""작업 디렉터리: {ROOT}

수능 기출 **한 문제**에 학생이 볼 입체 도형 스펙을 만들어 등록한다.
런타임에 튜터(작은 모델)가 좌표를 계산하지 않아도 되게 하는 것이 목적이다.

대상: {slug}
문제 md: {md}
원본 도판: {img or '(없음)'}
검증된 정답: {answer or '(없음)'}

절차:
1. 문제 md 를 Read. 원본 도판이 있으면 그것도 Read — **점 이름과 배치를 원본과 맞춘다.**
2. **입체가 정말 필요한지 판단.** 좌표가 본문에 다 주어진 계산 문항이거나 평면으로 충분하면
   **파일을 만들지 말고** 한 줄로 이유만 답하고 끝내라. 억지로 만들지 마라.
3. 필요하면 문제의 모든 기하 조건을 만족하는 좌표를 세우고, 조건마다 assert_* 를 호출해
   `echo '<코드>' | python3 scripts/ops/sympy_run.py` 로 전수 검증해라. 전부 [VERIFY OK] 가 될 때까지.
   ★**좌표계를 고를 때부터 원본 도판과 같은 배치가 되게 잡아라.** 나중에 화면을 비틀어
     맞추려 하지 마라 — cameraUp 은 회전이 잠기는 극점을 만들어 금지돼 있다(게이트가 막는다).
4. 스펙을 web/src/data/figures-3d/{slug}.json 에 써라:
   {{"spec": {{"shapes": [...], "cameraPosition": [..], "title": ".."}},
     "conditions": ["실제로 assert 한 조건들, 한국어"],
     "verify": "<위에서 통과시킨 sympy 코드 전문>",
     "note": "학생에게 보일 한 줄 설명"}}
{render}
5. 마지막으로 `python3 scripts/ops/verify_figures_3d.py --deep` 를 돌려 **네 파일에**
   빨간 줄이 없는지 확인해라. 있으면 고쳐라.

라벨 규칙(중요):
- 도형 위 글씨는 **이름표(A, 구 S, 평면 BCD)나 문제가 준 치수**만.
- **문제가 묻는 값은 절대 쓰지 마라.** 이 문제의 답은 `{answer}` 다 — 그 값이나 그것으로
  바로 이어지는 중간 결과를 라벨에 쓰면 학생이 풀 게 없어진다.
- 설명 문장을 라벨에 쓰지 마라(도형을 덮는다). 설명은 note 에.
"""


def gate(slug: str) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, str(ROOT / 'scripts/ops/verify_figures_3d.py'), '--deep'],
                       capture_output=True, text=True, cwd=ROOT)
    out = r.stdout + r.stderr
    if f'🔴 {slug}' not in out:
        return True, ''
    block = out.split(f'🔴 {slug}')[1].split('🔴')[0]
    return False, block.strip()[:400]


def run_one(slug: str, tokfile: str | None, force: bool) -> dict:
    md = md_of(slug)
    if not md:
        return {'slug': slug, 'state': 'skip', 'why': '문제 md 없음'}
    out = FIG_DIR / f'{slug}.json'
    if out.exists() and not force:
        return {'slug': slug, 'state': 'skip', 'why': '이미 등록됨'}
    if not is_candidate(md):
        return {'slug': slug, 'state': 'skip', 'why': '3D 후보 아님'}
    imgs = list((ROOT / 'db' / 'raw').rglob(f'{slug}.png'))
    prompt = build_prompt(slug, md, str(imgs[0]) if imgs else '', answer_of(md), tokfile)
    args = ['claude', '-p', '--output-format', 'json', '--model', MODEL,
            '--allowedTools', 'Read,Write,Edit,Bash,Glob,Grep',
            '--add-dir', str(ROOT), '--max-turns', '60', '--', prompt]
    if SYSTEM:
        args[-3:-3] = ['--system-prompt', SYSTEM]
    try:
        subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S, cwd=ROOT, env=CLAUDE_ENV)
    except subprocess.TimeoutExpired:
        out.unlink(missing_ok=True)
        return {'slug': slug, 'state': 'fail', 'why': f'{TIMEOUT_S}s 타임아웃'}
    if not out.exists():
        return {'slug': slug, 'state': 'none', 'why': '3D 불필요로 판단'}
    ok, detail = gate(slug)
    if not ok:
        out.unlink()
        return {'slug': slug, 'state': 'fail', 'why': f'게이트 실패 → 등록 안 함: {detail}'}
    e = json.loads(out.read_text(encoding='utf-8'))
    e['source_sha'] = source_sha(md)      # 본문이 바뀌면 게이트가 낡음을 잡는다
    out.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding='utf-8')
    return {'slug': slug, 'state': 'ok', 'why': f"조건 {len(e.get('conditions', []))}개 검증"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', required=True, help='쉼표로 구분한 slug 목록')
    ap.add_argument('--parallel', type=int, default=3)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    slugs = [s.strip() for s in a.list.split(',') if s.strip()]
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    tok = dev_token()
    tokfile = None
    if tok:
        tf = Path('/tmp/fig3d_devtok'); tf.write_text(tok, encoding='utf-8'); tf.chmod(0o600)
        tokfile = str(tf)
        print('  · dev 서버 확인 — 렌더 대조까지 수행', flush=True)
    else:
        print('  · dev 서버 없음 — 렌더 대조 생략(좌표·게이트만)', flush=True)

    try:
        with cf.ThreadPoolExecutor(max_workers=max(1, a.parallel)) as ex:
            results = list(ex.map(lambda s: run_one(s, tokfile, a.force), slugs))
    finally:
        if tok:
            drop_token(tok); Path('/tmp/fig3d_devtok').unlink(missing_ok=True)

    reg = [r for r in results if r['state'] == 'ok']
    fail = [r for r in results if r['state'] == 'fail']
    none = [r for r in results if r['state'] == 'none']
    print(f"\n✓ 3D 스펙 {len(reg)}건 등록 · 불필요 {len(none)}건 · 실패 {len(fail)}건 "
          f"· 건너뜀 {len(results) - len(reg) - len(fail) - len(none)}건", flush=True)
    for r in reg:
        print(f'   + {r["slug"]}  ({r["why"]})', flush=True)
    for r in fail:
        print(f'   ✗ {r["slug"]}  {r["why"]}', flush=True)
    if reg:
        print(f'   검수: {BASE}/dev/figgallery3d?src=problems&per=2', flush=True)
    with open(os.environ.get('FIG3D_LOG', '/tmp/ingest_logs/figures3d.log'), 'a') as f:
        f.write(f'{datetime.now().isoformat(timespec="seconds")}\t등록 {len(reg)}\t실패 {len(fail)}\t'
                f'불필요 {len(none)}\t{",".join(r["slug"] for r in reg)}\n')
    return 0


if __name__ == '__main__':
    os.makedirs('/tmp/ingest_logs', exist_ok=True)
    sys.exit(main())
