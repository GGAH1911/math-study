#!/usr/bin/env python3
"""콘텐츠 본문의 개발용/영문 표현 정제 — 사용자 노출 페이지(concepts·syntheses)에서만.

콘텐츠 생성기가 LWIP 파이프라인 단계·enum·룰번호를 본문에 박은 것을 사용자 친화 문구로.
frontmatter 는 안 건드림(메타데이터). 학습 콘텐츠(개념 링크·수식)는 보존.

usage: clean_dev_expressions.py [--apply]   (기본 dry-run)
"""
from __future__ import annotations
import sys, re, glob, os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# (정규식, 치환) — 본문에만 적용. 변형(spoke로 분해/분해됨, Phase 3/Phase 3 진단 대상 등) 포괄.
RULES = [
    # 헤딩의 파이프라인 단계 주석 제거 (괄호 안 Phase 표기 변형 모두)
    (re.compile(r'^(## 다룰 정의 / 정리 / 예제) ?\(Phase 2[^)]*\)', re.M), r'\1'),
    (re.compile(r'^(## 평가 기준) ?\(Phase 3[^)]*\)', re.M), r'\1'),
    # 네비게이션의 개발 표기: "다음: 없음 (말단 노드 / Phase 1에서 미정의)" → "다음: 없음"
    (re.compile(r'(다음: ?없음) ?\(말단 노드[^)]*\)'), r'\1'),
    # 영문 병기 제거 (헤딩 마커 + 본문 산문 둘 다)
    (re.compile(r'정의\(definition\)'), '정의'),
    (re.compile(r'정리\(theorem\)'), '정리'),
    (re.compile(r'예제\(example\)'), '예제'),
    # 평가 기준 줄의 enum·룰번호 → 자연어 (백틱 유무 모두)
    (re.compile(r'`?mastery: ?proficient`? 승급'), '숙달(마스터)로 인정'),
    (re.compile(r'같은 단원의 `?concept_gap`? 오답이 3회 누적되면 root concept 보강 알림 ?\(D6\)'),
     '같은 단원에서 비슷한 유형의 오답이 반복되면 기초 개념 보강을 안내'),
    (re.compile(r'같은 ?단원의? ?`?concept_gap`? ?3회 누적 시 root concept 보강 알림 ?\(D6\)'),
     '같은 단원에서 비슷한 유형의 오답이 반복되면 기초 개념 보강을 안내'),
    # syntheses 푸터의 개발 출처 주석 정리 (LWIP/lifecycle 내부 표기 제거, 출처 링크는 보존)
    (re.compile(r'페이지에서 진행한 LLM 튜터 대화를 영구 wiki 노드로 promote '
                r'\(LWIP Query & Promote, lifecycle\.md §Query-Promote\)\.'),
     '페이지에서 진행한 학습 대화를 정리한 노트입니다.'),
]

# spoke 본문이 "LLM 메타 대화"로 깨진 것(콘텐츠 부재) — 정제 아닌 별도 보고
BROKEN_SPOKE = re.compile(r'필수 정보가 누락|spoke 페이지를 작성|확인이 필요합니다|작성하기 전에')


def split_body(t: str):
    parts = t.split('---\n', 2)
    if len(parts) >= 3:
        return '---\n' + parts[1] + '---\n', parts[2]
    return '', t


def main():
    apply = '--apply' in sys.argv
    areas = ['concepts', 'syntheses']
    npatch = 0
    broken = []
    for area in areas:
        for md in sorted(glob.glob(os.path.join(REPO, f'docs/{area}/**/*.md'), recursive=True)):
            t = open(md, encoding='utf-8').read()
            head, body = split_body(t)
            new = body
            applied = []
            for rx, repl in RULES:
                new2, n = rx.subn(repl, new)
                if n:
                    applied.append((rx.pattern[:40], n))
                    new = new2
            if BROKEN_SPOKE.search(body):
                broken.append(os.path.relpath(md, REPO))
            if applied:
                npatch += 1
                rel = os.path.relpath(md, REPO)
                print(f'{rel}: {sum(n for _, n in applied)} 치환')
                if apply:
                    open(md, 'w', encoding='utf-8').write(head + new)
    print(f'\n{"적용" if apply else "DRY-RUN"}: {npatch} md 정제')
    if broken:
        print(f'\n⚠️ 본문이 LLM 메타대화로 깨진 spoke {len(broken)}건 (정제 아닌 재생성 필요):')
        for b in broken:
            print(f'   {b}')


if __name__ == '__main__':
    main()
