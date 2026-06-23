#!/usr/bin/env python3
"""Fill empty spoke bodies (concept_type != unit, no auto_explained: true)
via parallel claude -p (haiku). ThreadPool max_workers=4 — same pattern
as ingest_round.py.

Idempotent: skips spokes already marked auto_explained: true.
"""
from __future__ import annotations
import concurrent.futures as cf
import re
import subprocess
import sys
import time
from pathlib import Path

CONCEPTS = Path('/home/insung/Projects/math-study/docs/concepts')
TIMEOUT = 90
MODEL = 'haiku'
WORKERS = 24

TUTOR_SYSTEM = """당신은 한국 수능을 준비하는 학생용 수학 wiki의 콘텐츠 라이터입니다.
개념 페이지(정의/정리/예제) 하나의 '본문' 섹션을 작성합니다.

요구사항:
1. 한국어로. 한국 고등학교 교육과정 용어 우선 (근의 공식, 도함수, 정적분 등).
2. 수식은 KaTeX inline `$...$` 또는 display `$$...$$`로. ★가독성: 긴 등식/부등식 체인
   (lim...=lim...=L, 3중 부등식 a≤b≤c)은 인라인 말고 `$$...$$` 블록으로 빼라(인라인은
   줄바꿈으로 쪼개진다). 인라인 분수는 `\frac` 대신 `\tfrac`(작은 분수, 줄높이 안정).
3. 200-400 단어 분량.
4. 구조:
   - 정의: ### 정확한 진술 → ### 직관/기하적 의미 → ### 한 줄 예
   - 정리: ### 진술 + 가정 → ### 간단한 유도/증명 스케치 → ### 의의/응용
   - 예제: ### 문제 → ### 단계별 풀이 → ### 답 → ### 변형/주의
5. h1, h2 헤더 절대 사용 금지. h3(###) 이하만.
6. 검산 가능한 수치 예제는 sympy 코드 한 줄 포함 가능 (예: `sympy.solve(x**2 - 5*x + 6, x)`).
7. 출력은 본문 마크다운만. "본문:" 같은 라벨 금지. ### 헤더로 시작.
8. ★사용자에게 보이는 글이다. 자연스러운 한국어만 쓰고 개발 용어·영문 표기를 본문에 노출하지 말 것
   (definition/theorem/example, spoke, mastery, concept_gap, Phase, LWIP 같은 단어 금지).
9. ★절대 학생에게 되묻지 말 것. "어떤 개념인지 확인이 필요합니다", "정보가 누락되어 있습니다"
   같은 질문·요청을 본문으로 쓰지 마라. 제목이 모호하면 slug·단원·선수개념으로 가장 합리적인
   표준 교육과정 개념을 스스로 판단해 그 본문을 바로 작성하라. 도저히 판단이 불가능하면
   짧은 표준 정의 한 문단만 쓰고 끝내라(질문 금지)."""


def parse_fm_field(text: str, key: str) -> str:
    m = re.search(rf'^{key}:\s*(.+)$', text, re.MULTILINE)
    return (m.group(1).strip() if m else '')


def parse_list_field(text: str, key: str) -> list[str]:
    m = re.search(rf'^{key}:\s*\[(.*?)\]', text, re.MULTILINE)
    if not m or not m.group(1).strip(): return []
    return [x.strip() for x in m.group(1).split(',') if x.strip()]


def generate_body(slug, ctype, grade, unit, brief, prereqs):
    pre_labels = ', '.join(Path(p).stem.replace('_', ' ') for p in prereqs) or '없음'
    user = f"""다음 개념 페이지의 본문을 작성하세요.

페이지 제목: {slug.replace('_', ' ')}
타입: {ctype}
학년: {grade}
소속 단원: {unit}
선수 개념: {pre_labels}
페이지 요약(1줄): {brief}

이 개념을 처음 보는 학생에게 친절하면서도 정확하게 설명해 주세요. 되묻지 말고 바로 본문을 작성합니다. h3(###) 이하 헤더만. markdown 본문만."""
    for attempt in range(3):
        try:
            r = subprocess.run(
                ['claude', '-p',
                 '--model', MODEL,
                 '--max-turns', '1',
                 '--output-format', 'text',
                 '--no-session-persistence',
                 '--system-prompt', TUTOR_SYSTEM,
                 user],
                capture_output=True, text=True, timeout=TIMEOUT,
            )
            if r.returncode == 0 and r.stdout.strip():
                body = r.stdout.strip()
                # strip any accidental h1/h2 prefix
                body = re.sub(r'^\s*#{1,2}\s+[^\n]+\n+', '', body, count=1)
                return body
            if attempt < 2:
                time.sleep(3)
        except subprocess.TimeoutExpired:
            if attempt < 2:
                time.sleep(3)
    return None


def splice_body(text: str, new_body: str) -> str:
    pattern = re.compile(r'(## 본문[^\n]*\n)(.*?)(\n## )', re.DOTALL)
    m = pattern.search(text)
    if m:
        return text[:m.start(2)] + '\n' + new_body + '\n' + text[m.end(2)-1:]
    check = text.find('## 학습 체크')
    if check >= 0:
        return text[:check] + '## 본문\n\n' + new_body + '\n\n' + text[check:]
    return text.rstrip() + '\n\n## 본문\n\n' + new_body + '\n'


def mark_auto_explained(text: str) -> str:
    if 'auto_explained:' in text:
        return re.sub(r'^auto_explained:.*$', 'auto_explained: true', text, count=1, flags=re.MULTILINE)
    return re.sub(r'^(updated:.*)$', r'\1\nauto_explained: true', text, count=1, flags=re.MULTILINE)


def process_one(spoke_path: Path) -> tuple[Path, bool, str]:
    text = spoke_path.read_text(encoding='utf-8')
    ctype = parse_fm_field(text, 'concept_type')
    if ctype == 'unit' or 'auto_explained: true' in text:
        return spoke_path, True, 'skip'
    grade = parse_fm_field(text, 'grade')
    unit = parse_fm_field(text, 'unit')
    prereqs = parse_list_field(text, 'prerequisites')
    brief_match = re.search(r'## 요약\s*\n([^\n#]+)', text)
    brief = brief_match.group(1).strip() if brief_match else ''

    t0 = time.time()
    body = generate_body(spoke_path.stem, ctype, grade, unit, brief, prereqs)
    dt = time.time() - t0
    if not body:
        return spoke_path, False, f'failed ({dt:.0f}s)'
    new = splice_body(text, body)
    new = mark_auto_explained(new)
    spoke_path.write_text(new, encoding='utf-8')
    return spoke_path, True, f'{len(body)} chars ({dt:.0f}s)'


def main():
    targets = []
    for p in sorted(CONCEPTS.glob('*.md')):
        text = p.read_text(encoding='utf-8')
        ctype = parse_fm_field(text, 'concept_type')
        if ctype == 'unit':
            continue
        if 'auto_explained: true' in text:
            continue
        targets.append(p)
    print(f'Targets: {len(targets)} spokes (workers={WORKERS})', flush=True)
    done = 0
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for p, ok, msg in ex.map(process_one, targets):
            done += 1
            mark = '✓' if ok and msg != 'skip' else ('-' if msg == 'skip' else '✗')
            print(f'  [{done:>3}/{len(targets)}] {mark} {p.stem:<40} {msg}', flush=True)


if __name__ == '__main__':
    main()
