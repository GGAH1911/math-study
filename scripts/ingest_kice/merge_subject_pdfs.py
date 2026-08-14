#!/usr/bin/env python3
"""과목별 문제 PDF 를 **통합본 문제.pdf** 로 합친다 (교육청 고3, 통합본 미배포 회차).

기존 고3 회차는 통합본 한 장으로 왔지만, 2026 7월처럼 **과목별 PDF 3개 + 해설 3개**만
배포되는 회차가 있다. 인제스트의 검증된 경로는 통합본을 전제하므로, 새 백엔드를 만드는
대신 입력을 통합본 모양으로 맞춘다.

★★핵심 규칙 — **공통 부분은 반드시 첫 선택과목(확률과통계) PDF 에서 가져온다.**
  섹션 마커가 "다음 과목 이름" 을 **앞 섹션 마지막 쪽에** 붙이는 구조라서다:

      진짜 통합본   8쪽 [ ]        12쪽 [미적분]   16쪽 [기하]
      확통 PDF      8쪽 [ ]        12쪽 [미적분]     ← 통합본과 동일
      미적 PDF      8쪽 [미적분]                     ← 여기서 공통을 가져오면 깨진다

  미적/기하 PDF 의 공통 마지막 쪽에는 자기 과목 이름이 박혀 있어, 그 뒤에 확통 선택
  문항을 붙이면 **확통 문항이 미적분으로 라벨된다.** 2026-08-14 실제로 그렇게 오염돼
  DB·파일을 통째로 롤백했다. 이 순서는 취향이 아니라 정확성 문제다.

사용:
    python3 scripts/ingest_kice/merge_subject_pdfs.py <round_raw_dir>
      (그 안의 <과목>_문제.pdf 3개를 읽어 문제.pdf 생성)
"""
from __future__ import annotations
import re, sys
from pathlib import Path

import fitz

# 통합본에서의 선택과목 순서 = 정답표·문제지 공통 관례.
ELECTIVE_ORDER = ['확률과통계', '미적분', '기하']


def elective_start(doc: fitz.Document) -> int:
    """23번이 시작하는 쪽(1-base). 못 찾으면 0."""
    for i, pg in enumerate(doc, 1):
        if re.search(r'(?m)^\s*23\.\s', pg.get_text()):
            return i
    return 0


def merge(raw: Path, out: Path | None = None) -> Path:
    out = out or raw / '문제.pdf'
    srcs = {s: raw / f'{s}_문제.pdf' for s in ELECTIVE_ORDER}
    missing = [s for s, p in srcs.items() if not p.exists()]
    if missing:
        raise SystemExit(f'과목별 문제 PDF 없음: {missing}  ({raw})')

    docs = {s: fitz.open(p) for s, p in srcs.items()}
    starts = {s: elective_start(d) for s, d in docs.items()}
    if 0 in starts.values() or len(set(starts.values())) != 1:
        raise SystemExit(f'선택 시작 쪽을 못 맞췄다: {starts} — 과목별 PDF 구성이 다르다')
    st = starts[ELECTIVE_ORDER[0]]

    merged = fitz.open()
    first = docs[ELECTIVE_ORDER[0]]                       # ★공통은 확률과통계 PDF 에서
    merged.insert_pdf(first, from_page=0, to_page=st - 2)  # 1..(st-1) 쪽 = 공통
    for s in ELECTIVE_ORDER:
        d = docs[s]
        merged.insert_pdf(d, from_page=st - 1, to_page=d.page_count - 1)
    merged.save(str(out))
    n = merged.page_count
    marks = {p: [x for x in ELECTIVE_ORDER if x in merged[p - 1].get_text()]
             for p in (st - 1, st + 3, st + 7)}
    merged.close()
    for d in docs.values():
        d.close()
    print(f'✓ {out.name} {n}쪽 (공통 {st - 1} + 선택 {(n - st + 1) // 3}×3)')
    print(f'  섹션 마커 {marks}  ← 앞 쪽은 비어 있어야 정상(다음 과목명이 앞 섹션 끝에 붙는 구조)')
    if marks.get(st - 1):
        print('  ⚠ 공통 마지막 쪽에 과목명이 있다 — 공통을 잘못된 PDF 에서 가져왔을 수 있다', flush=True)
    return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    merge(Path(sys.argv[1]))
