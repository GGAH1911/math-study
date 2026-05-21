#!/usr/bin/env python3
"""Same as propagate_grade but for the `domain` field (수와식 / 방정식 /
함수 / 도형 / 확률통계 / 논리). First we try prereq + reverse chains;
remaining orphans get keyword-classified.
"""
from __future__ import annotations
import re
from pathlib import Path

CONCEPTS = Path('/home/insung/Projects/math-study/docs/concepts')

DOMAIN_RULES: list[tuple[str, str]] = [
    # 확률통계
    (r'확률|통계|분산|표준편차|기댓값|이항분포|정규분포|이항|순열|조합|중복순열|중복조합|평균|중앙값|빈도|독립시행|조건부확률', '확률통계'),
    # 도형 (기하)
    (r'벡터|공간|구면|구체|이차곡선|타원|쌍곡선|포물선|준선|좌표공간|법선|기하학|닮음|피타고라스|삼각비|원|호도|원주|중심각|원주각|접선의?_길이|접점|삼각형|사각형|다각형|입체|회전체|구|원기둥|원뿔|기둥', '도형'),
    # 함수 (미적분, 수열, 삼각함수, 지수로그)
    (r'미분|도함수|접선의?_방정식|극값|극대|극소|극솟?값|극댓?값|변곡점|적분|역도함수|넓이의?_변화율|곡선의_미분|곡선의_접촉|미분가능성|리만|샌드위치|속도|가속도|평균변화율|함수|그래프|수열|극한|연속|지수|로그|삼각함수|호도법|삼각방정식|삼각부등식|사인|코사인|탄젠트|sin|cos|tan|log|exp', '함수'),
    # 방정식 (방정식·부등식)
    (r'방정식|부등식|판별식|근의?_공식|연립|일대일대응|역함수의?_방정식|항등식', '방정식'),
    # 수와식
    (r'다항식|인수분해|복소수|나머지정리|인수정리|식의?_계산|제곱근|루트|소인수|약수|배수|소수|수의?_체계|정수|유리수|무리수|실수|허수|절댓값|문자와_식', '수와식'),
    # 논리
    (r'명제|논리|역|이|대우|충분조건|필요조건|집합|원소|부분집합|벤다이어그램|진리값|배중률', '논리'),
]


def parse_fm(path: Path):
    text = path.read_text(encoding='utf-8')
    fm = {}
    if not text.startswith('---'):
        return fm, text
    end = text.find('---', 3)
    if end < 0:
        return fm, text
    for line in text[3:end].splitlines():
        m = re.match(r'^([a-zA-Z_]+):\s*(.*)$', line)
        if not m: continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith('[') and v.endswith(']'):
            fm[k] = [s.strip().strip('"') for s in v[1:-1].split(',') if s.strip()]
        else:
            fm[k] = v
    return fm, text


def slug_of(s: str) -> str:
    return s.split('/')[-1].replace('.md', '')


def set_field(text: str, key: str, value: str) -> str:
    if re.search(rf'^{key}:\s*.*$', text, re.MULTILINE):
        return re.sub(rf'^{key}:\s*.*$', f'{key}: {value}', text, count=1, flags=re.MULTILINE)
    if re.search(r'^concept_type:.*$', text, re.MULTILINE):
        return re.sub(r'^(concept_type:.*)$', r'\1\n' + f'{key}: {value}',
                      text, count=1, flags=re.MULTILINE)
    return re.sub(r'^---\n', f'---\n{key}: {value}\n', text, count=1)


def classify_slug(slug: str) -> str | None:
    for pattern, domain in DOMAIN_RULES:
        if re.search(pattern, slug):
            return domain
    return None


def main():
    all_files = sorted(CONCEPTS.glob('*.md'))
    fms = {}
    texts = {}
    for p in all_files:
        fm, text = parse_fm(p)
        fms[p.stem] = fm
        texts[p.stem] = text

    reverse = {}
    for slug, fm in fms.items():
        for ref in (fm.get('prerequisites', []) if isinstance(fm.get('prerequisites'), list) else []):
            reverse.setdefault(slug_of(ref), []).append(slug)

    cache = {}

    def resolve(slug, seen=None):
        if slug in cache: return cache[slug]
        if seen is None: seen = set()
        if slug in seen: return None
        seen.add(slug)
        fm = fms.get(slug, {})
        my = fm.get('domain') if isinstance(fm.get('domain'), str) else None
        if my:
            cache[slug] = my; return my
        for ref in fm.get('prerequisites', []) if isinstance(fm.get('prerequisites'), list) else []:
            g = resolve(slug_of(ref), seen)
            if g: cache[slug] = g; return g
        for child in reverse.get(slug, []):
            g = resolve(child, seen)
            if g: cache[slug] = g; return g
        cache[slug] = None
        return None

    propagated = orphan_keyword = orphan_left = already = 0
    still: list[str] = []

    for p in all_files:
        slug = p.stem
        fm = fms[slug]
        existing = fm.get('domain') if isinstance(fm.get('domain'), str) else None
        if existing:
            already += 1
            continue
        target = resolve(slug)
        if not target:
            target = classify_slug(slug)
            if target:
                orphan_keyword += 1
            else:
                orphan_left += 1
                still.append(slug)
                continue
        else:
            propagated += 1
        text = texts[slug]
        p.write_text(set_field(text, 'domain', target), encoding='utf-8')

    print(f'\n═══ Summary ═══')
    print(f'  already had domain: {already}')
    print(f'  propagated via chains: {propagated}')
    print(f'  keyword fallback: {orphan_keyword}')
    print(f'  no match: {orphan_left}')
    if still[:20]:
        print(f'  examples: {", ".join(still[:20])}')


if __name__ == '__main__':
    main()
