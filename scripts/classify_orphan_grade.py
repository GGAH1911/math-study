#!/usr/bin/env python3
"""For spokes whose grade couldn't be resolved via prereq/enables propagation,
guess the grade from keywords in the slug name. Most orphans are 미적분 /
수학Ⅱ flavored (구간별, 미분, 적분, 극값, 교점 등).
"""
from __future__ import annotations
import re
from pathlib import Path

CONCEPTS = Path(__import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__)))) / 'docs/concepts'  # ★레포 위치 자동(이동 내성)

# Keyword → grade priority. First match wins.
RULES: list[tuple[str, str]] = [
    # 기하 (도형, 공간)
    (r'벡터|공간|구면|구체|이차곡선|타원|쌍곡선|포물선의_초점|준선|좌표공간|법선|기하학', '기하'),
    # 확률과 통계
    (r'확률|통계|분산|표준편차|기댓값|이항분포|정규분포|이항|순열|조합|중복순열|중복조합|평균|중앙값', '확률과통계'),
    # 미적분 (계산 기반) — 극대/극소/극값/속도/가속도/리만/샌드위치 추가
    (r'미분|도함수|접선|극값|극대|극소|극솟?값|극댓?값|변곡점|적분|역도함수|넓이의?_변화율|곡선의_미분|곡선의_접촉|미분가능성|리만|샌드위치|속도|가속도|평균변화율', '미적분'),
    # 수학Ⅱ
    (r'수열|극한|연속|함수의_극한', '수학2'),
    # 수학Ⅰ
    (r'지수|로그|삼각함수|일반각|호도법|삼각방정식|삼각부등식', '수학1'),
    # 고1 (공통)
    (r'다항식|인수분해|근의?_공식|판별식|이차방정식|이차함수|이차부등식|연립방정식|연립부등식|복소수|항등식|나머지정리|인수정리|함수와_그래프|일차함수|근의', '고1'),
    # 중3
    (r'제곱근|루트|상수항|일차_방정식|소인수|약수|배수|소수|소수성', '중3'),
    # 두 직선 사이의 각 등 — 수학Ⅰ (지수·로그·삼각함수 단원 정의에 흔히 나옴)
    (r'두_직선|두_평면|두_벡터|각도', '수학1'),
    # 기울기 (직선) → 고1
    (r'기울기', '고1'),
    # General-fall through for "함수", "방정식" without other markers → 수학1
    (r'함수|방정식|부등식|그래프', '수학1'),
    # 교점/구간별: typically 미적분 territory in 수능 context
    (r'교점|구간별|영역|넓이|극한|상수결정|상수_결정|범위_결정|경계점', '미적분'),
]


def parse_grade(text: str) -> str:
    m = re.search(r'^grade:\s*(.*)$', text, re.MULTILINE)
    return m.group(1).strip() if m else ''


def has_concept_type_line(text: str) -> bool:
    return bool(re.search(r'^concept_type:', text, re.MULTILINE))


def set_grade(text: str, grade: str) -> str:
    if re.search(r'^grade:\s*.*$', text, re.MULTILINE):
        return re.sub(r'^grade:\s*.*$', f'grade: {grade}', text, count=1, flags=re.MULTILINE)
    if has_concept_type_line(text):
        return re.sub(r'^(concept_type:.*)$', r'\1\n' + f'grade: {grade}',
                      text, count=1, flags=re.MULTILINE)
    return re.sub(r'^---\n', f'---\ngrade: {grade}\n', text, count=1)


def classify_slug(slug: str) -> str | None:
    for pattern, grade in RULES:
        if re.search(pattern, slug):
            return grade
    return None


def main():
    orphans: list[Path] = []
    for p in sorted(CONCEPTS.glob('*.md')):
        text = p.read_text(encoding='utf-8')
        if not parse_grade(text):
            orphans.append(p)
    print(f'orphans without grade: {len(orphans)}', flush=True)
    if not orphans:
        return
    filled = 0
    still = []
    for p in orphans:
        guess = classify_slug(p.stem)
        if not guess:
            still.append(p.stem)
            continue
        text = p.read_text(encoding='utf-8')
        p.write_text(set_grade(text, guess), encoding='utf-8')
        filled += 1
    print(f'\n═══ Summary ═══')
    print(f'  filled (keyword match): {filled}')
    print(f'  still no match: {len(still)}')
    if still[:20]:
        print(f'  examples: {", ".join(still[:20])}')


if __name__ == '__main__':
    main()
