#!/usr/bin/env python3
"""Last-resort override: spoke names like `곱의_미분_법칙` or
`삼각함수의_적분` reveal their grade unambiguously even when LLM
mis-set the prereq chain. Apply only for clearly-recognizable patterns
so we don't accidentally re-misclassify well-resolved spokes.
"""
from __future__ import annotations
import re
from pathlib import Path

CONCEPTS = Path('/home/insung/Projects/math-study/docs/concepts')

# Each rule: (regex, target grade, "only override if current grade is one of these")
RULES: list[tuple[str, str, set[str]]] = [
    # 미적분 indicators — only override if currently lower-level
    (r'곱의_미분|몫의_미분|합성함수의_미분|역함수의_미분|음함수의_미분|매개변수.*미분|로그.*미분|지수.*미분|삼각함수.*미분|미분과_증감|증감과_변곡|이계도|매끄러움',
     '미적분', {'수학1', '고1', '중3', '중2', '중1'}),
    (r'치환적분|부분적분|로그함수의_적분|지수함수의_적분|삼각함수의_적분|역함수의_적분|넓이의?_변화|회전체|구분구적|정적분의_활용|입체의_부피|적분의?_응용',
     '미적분', {'수학1', '고1', '중3', '중2', '중1'}),
    (r'리만|샌드위치|샌드위치_정리|수열의?_극한|급수|등비수열의?_합의?_극한|무한등비|무한급수|수열의_수렴',
     '미적분', {'수학1', '고1', '중3', '중2', '중1'}),
    (r'함수의?_극한|좌극한|우극한|연속성|불연속|중간값정리|최대최소정리|함수의_연속',
     '수학2', {'고1', '중3', '중2', '중1'}),
    # 기하 indicators
    (r'평면벡터|공간벡터|벡터의_내적|이차곡선|타원|쌍곡선|포물선의_초점|준선|좌표공간|법선_벡터',
     '기하', {'수학1', '고1', '중3'}),
    # 확률과 통계 indicators
    (r'이항분포|정규분포|확률밀도|연속확률|기댓값|표본평균|모평균|신뢰구간|이항정리|중복순열|중복조합',
     '확률과통계', {'수학1', '고1', '중3', '중2'}),
]


def parse_fm(text: str) -> dict:
    fm: dict = {}
    if not text.startswith('---'): return fm
    end = text.find('---', 3)
    if end < 0: return fm
    for line in text[3:end].splitlines():
        m = re.match(r'^([a-zA-Z_]+):\s*(.*)$', line)
        if m: fm[m.group(1)] = m.group(2).strip()
    return fm


def set_field(text: str, key: str, value: str) -> str:
    return re.sub(rf'^{key}:\s*.*$', f'{key}: {value}', text, count=1, flags=re.MULTILINE)


def main():
    all_files = sorted(CONCEPTS.glob('*.md'))
    changed = 0
    skipped = 0
    samples_changed: list[str] = []

    for p in all_files:
        text = p.read_text(encoding='utf-8')
        fm = parse_fm(text)
        if fm.get('concept_type') == 'unit':
            continue
        cur = fm.get('grade', '')
        slug = p.stem
        for pattern, target, override_from in RULES:
            if not re.search(pattern, slug):
                continue
            if cur not in override_from:
                continue
            new_text = set_field(text, 'grade', target)
            if new_text != text:
                p.write_text(new_text, encoding='utf-8')
                changed += 1
                if len(samples_changed) < 10:
                    samples_changed.append(f'{slug}: {cur} → {target}')
            break
        else:
            continue
        # broken out of inner loop (rule matched)
    print(f'═══ Summary ═══')
    print(f'  overrides applied: {changed}')
    if samples_changed:
        print(f'  samples:')
        for s in samples_changed: print(f'    {s}')


if __name__ == '__main__':
    main()
