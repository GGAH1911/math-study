#!/usr/bin/env python3
"""회귀 baseline 덤프 — 모든(또는 지정) 회차의 문제 PDF를 bbox→decode_problem 전수 디코드해
jsonl({id,text})로 출력. 디코더 수정 전/후 이 덤프를 diff 하면 회귀를 결정론적으로 검출한다.

사용:
  python dump_decode.py > /tmp/decode_before.jsonl          # 전 회차
  python dump_decode.py 2020_고2_9월모의고사 ... > out.jsonl  # 지정 회차만
"""
from __future__ import annotations
import sys, json, glob, os
from pathlib import Path

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
import ingest_v2 as IV          # noqa: E402
import hancom_decode as hd      # noqa: E402

ROOT = IV.ROOT
RAW = ROOT / 'db' / 'raw'


def _round_dirs(only):
    for d in sorted(RAW.iterdir()):
        if not d.is_dir():
            continue
        if only and d.name not in only:
            continue
        yield d


def _problem_pdf(d: Path):
    for name in ('문제.pdf', '가형_문제.pdf', '나형_문제.pdf'):
        p = d / name
        if p.exists():
            yield p


def main():
    only = set(sys.argv[1:])
    for d in _round_dirs(only):
        for pdf in _problem_pdf(d):
            exam = '모의고사' if '모의고사' in d.name else ('수능' if '수능' in d.name else '모평')
            session = next((s for s in ('3월', '4월', '6월', '7월', '9월', '10월', '11월') if s in d.name), None)
            try:
                bboxes = IV.extract_problem_bboxes(str(pdf), exam, session)
            except Exception as e:
                print(f'# bbox-fail {d.name}/{pdf.name}: {e}', file=sys.stderr)
                continue
            track = '가형' if '가형' in pdf.name else ('나형' if '나형' in pdf.name else '단일')
            for e in bboxes:
                num = e.get('number')
                try:
                    txt = hd.decode_problem(str(pdf), e['page_num'], e['bbox_pdf'])
                except Exception as ex:
                    txt = f'<<decode-error:{ex}>>'
                rid = f"{d.name}/{track}/{num:02d}" if isinstance(num, int) else f"{d.name}/{track}/{num}"
                print(json.dumps({'id': rid, 'text': txt or ''}, ensure_ascii=False))


if __name__ == '__main__':
    main()
