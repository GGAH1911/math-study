"""claude -p 구독 인증 토큰 한 곳 — 세 스크립트가 각자 틀리던 것을 모은다.

★왜 필요한가: `claude -p` 는 인증이 없으면 "Not logged in" 한 줄만 뱉고 **exit 0** 으로
  끝난다. 반환코드만 보면 성공이라, 호출부가 그걸 "결과 없음"·"판정" 으로 오인한다.
  2026-08-14 하루에만 세 곳에서 같은 사고가 났다 —
    · ingest_round / run_stage1 → 인제스트 전 문항 unit=? 로 실패
    · build_solution_cache      → 46문제 전부 gen-fail → HANDSOLVE
    · build_figures_3d          → "3D 불필요" 판정으로 위장

★호스트마다 유효한 인증이 다르다. tme 는 디스크 자격증명(~/.claude/.credentials.json)이
  죽어 있고 deploy/.env 의 토큰이 정상이다. 옛 주석들은 정반대로 적혀 있었다(tme-laptop 기준).
  그래서 **명시적 토큰이 있으면 그걸 쓰고**, 없을 때만 디스크에 맡긴다.

★인증만이 아니라 **바이너리 유무**도 같은 사고를 낸다(2026-08-15). 크론의 PATH 는
  `/usr/bin:/bin` 뿐이라 `~/.local/bin/claude` 가 안 보이고, `subprocess.run(['claude', ...])`
  이 문항마다 `FileNotFoundError` 를 던져 **13건이 "실패" 로 기록됐다** — 환경 문제가
  문항 결함으로 위장된 것이라 위 세 사고와 같은 계열이다. `require_claude()` 로 배치
  시작 전에 한 번 묻고, 없으면 **한 건도 건드리기 전에** 죽는다.
"""
from __future__ import annotations
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def oauth_token() -> str:
    t = os.environ.get('CLAUDE_CODE_OAUTH_TOKEN', '').strip()
    if t:
        return t
    f = ROOT / 'deploy' / '.env'
    if f.exists():
        for line in f.read_text(encoding='utf-8').splitlines():
            if line.startswith('MS_CLAUDE_OAUTH_TOKEN='):
                return line.split('=', 1)[1].strip()
    return ''


def claude_env(base: dict | None = None) -> dict:
    """claude -p 서브프로세스에 넘길 env. git 블록 제거(프롬프트 캐시 안정) + 토큰 주입."""
    env = {**(base or os.environ), 'CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS': '1'}
    t = oauth_token()
    if t:
        env['CLAUDE_CODE_OAUTH_TOKEN'] = t
    return env


#: 로그인 셸에만 있고 크론 PATH 에는 없는 자리들. `which` 가 빈손일 때만 본다.
_EXTRA_BINDIRS = ('~/.local/bin', '~/.npm-global/bin', '/usr/local/bin')


def claude_bin() -> str:
    """`claude` 실행파일의 **절대경로**. 못 찾으면 빈 문자열.

    절대경로를 쓰는 이유: 호출부가 `env=` 를 넘기면(우리는 넘긴다) 그 env 의 PATH 로
    해석되므로, 이름으로 부르면 부모 PATH 를 고쳐도 안 먹는 경우가 생긴다.
    """
    p = shutil.which('claude')
    if p:
        return p
    for d in _EXTRA_BINDIRS:
        c = Path(d).expanduser() / 'claude'
        if c.is_file() and os.access(c, os.X_OK):
            return str(c)
    return ''


def require_claude() -> str:
    """배치 **시작 전** preflight. 없으면 아무것도 건드리지 않고 죽는다.

    ★워커 루프 안에서 터지면 항목마다 `FileNotFoundError` 가 잡혀 **실패 목록이
      오염된다**(2026-08-15: 13건). 회로차단이 6건에서 멈춰 주긴 하지만, 애초에
      한 건도 실패로 기록되면 안 되는 종류의 고장이다 — 문항이 아니라 환경이 틀렸다.
    """
    p = claude_bin()
    if not p:
        raise SystemExit(
            'claude 실행파일을 찾을 수 없다 — 배치를 시작하지 않는다.\n'
            f'  PATH={os.environ.get("PATH", "")}\n'
            f'  찾아본 곳: which claude · {" · ".join(_EXTRA_BINDIRS)}\n'
            '  크론이라면 PATH 가 /usr/bin:/bin 뿐이다. 호출 스크립트에서 PATH 를 넓혀라.')
    return p


def looks_unauthed(*outs: str) -> bool:
    """출력에 인증 실패 흔적이 있는가. exit code 는 0 이라 **본문을 봐야 한다.**"""
    s = ' '.join(o or '' for o in outs)
    return 'Not logged in' in s or 'Invalid API key' in s


#: 구독 쿼터 소진 문구. 인증 실패와 **구분해야 한다** — 자격증명은 멀쩡하고 시간만 지나면 풀린다.
_QUOTA_MARKS = (
    'usage limit reached',
    'Usage limit reached',
    'rate_limit_error',
    'limit will reset',
)


def looks_quota_exhausted(*outs: str) -> bool:
    """구독 쿼터가 말랐는가.

    ★왜 따로 필요한가: `looks_unauthed` 는 'Not logged in'/'Invalid API key' 만 본다.
      쿼터 소진은 **자격증명이 멀쩡한 채로** 오므로 그 검사를 통과하고, 무인 배치는
      남은 수천 건을 전부 "실패" 로 기록해 버린다(실패 목록이 쓰레기가 되고, 다음
      재시도 때 멀쩡한 문제까지 다시 돈다). 감지되면 배치를 **멈추는** 것이 맞다 —
      시간이 지나면 저절로 풀리는 조건이라 계속 두드릴 이유가 없다.
    """
    s = ' '.join(o or '' for o in outs)
    return any(m in s for m in _QUOTA_MARKS)
