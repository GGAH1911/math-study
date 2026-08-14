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
"""
from __future__ import annotations
import os
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


def looks_unauthed(*outs: str) -> bool:
    """출력에 인증 실패 흔적이 있는가. exit code 는 0 이라 **본문을 봐야 한다.**"""
    s = ' '.join(o or '' for o in outs)
    return 'Not logged in' in s or 'Invalid API key' in s
