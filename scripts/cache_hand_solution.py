#!/usr/bin/env python3
"""손풀이 솔루션을 frontmatter 에 캐시. (Opus 직접 풀이 — 이미지 기준 정답)

cache(slug, answer, answer_value, steps): answer 필드 교정 + solution 블록 삽입.
answer = 객관식 보기번호(또는 단답 숫자), answer_value = 실제 값 표시용.
이미지 기준으로 풀었으므로 홀수/짝수 폼 문제와 무관하게 정답.
"""
import re
from pathlib import Path

ROOT = Path(__import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))))  # ★레포 위치 자동(이동 내성)
DOCS = ROOT / 'docs' / 'problems'


def _q(s: str) -> str:
    # YAML 더블쿼트 스칼라: 백슬래시·쿼트 이스케이프
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def cache(slug: str, answer: str, answer_value: str, steps: list[str]) -> str:
    hits = list(DOCS.rglob(f'{slug}.md'))
    if not hits:
        return f'✗ {slug} 파일없음'
    p = hits[0]
    t = p.read_text(encoding='utf-8')
    old_ans = (re.search(r'^answer:\s*["\']?([^"\'\n]+)', t, re.M) or [None, '?'])[1]
    # answer 필드 교정 (이미지 기준)
    t = re.sub(r'^(answer:\s*)["\']?[^"\'\n]+["\']?', rf'\g<1>"{answer}"', t, count=1, flags=re.M)
    # solution 블록 (이미 있으면 교체)
    block = 'solution:\n'
    block += f'  answer_value: {_q(answer_value)}\n'
    block += '  verified: true\n'
    block += '  generated_by: opus-hand\n'
    block += '  steps:\n'
    for s in steps:
        block += f'    - {_q(s)}\n'
    # frontmatter 끝(두 번째 ---) 직전에 삽입
    parts = t.split('---\n', 2)
    if len(parts) < 3:
        return f'✗ {slug} frontmatter 파싱실패'
    fm = parts[1]
    # 기존 solution 블록 제거 (있으면)
    fm = re.sub(r'(?m)^solution:\n(?:[ \t]+.*\n)*', '', fm)
    fm = fm.rstrip('\n') + '\n' + block
    p.write_text('---\n' + fm + '---\n' + parts[2], encoding='utf-8')
    chg = f'(answer {old_ans}→{answer})' if str(old_ans) != str(answer) else '(answer 동일)'
    return f'✅ {slug}: {answer_value} = 보기{answer} {chg}, steps {len(steps)}개 캐시'
