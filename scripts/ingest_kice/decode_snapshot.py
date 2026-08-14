#!/usr/bin/env python3
"""디코더 회귀 안전망 — `hancom_decode` 를 고치기 전/후 출력을 통째로 비교한다.

★왜 필요한가: `_parse`/`_render_line` 은 **글리프 좌표 기하**로 분수·지수·근호·cases 를
  복원한다. 한 줄만 건드려도 4,200문제 전 회차에 영향이 간다. 눈으로 몇 개 보고 "좋아졌다"고
  판단하면 다른 데가 조용히 깨진다 — 이 레포엔 정규식 하나로 파일을 날린 사고가 두 번 있다
  (`docs/ops/SHUTDOWN.md`).

사용:
    python3 scripts/ingest_kice/decode_snapshot.py --out /tmp/snap_before.json      # 고치기 전
    ...파서 수정...
    python3 scripts/ingest_kice/decode_snapshot.py --out /tmp/snap_after.json
    python3 scripts/ingest_kice/decode_snapshot.py --diff /tmp/snap_before.json /tmp/snap_after.json

★md 의 searchable_text 와 비교하지 않는다 — 그건 교정기(vision)가 이미 고친 뒤라 디코더
  출력이 아니다. **PDF 에서 직접 다시 디코드**해야 파서 변경의 순수 효과가 보인다.
"""
from __future__ import annotations
import argparse, json, sys, traceback
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
ROOT = _HERE.parent.parent


def snapshot(rounds: list[str], per_round: int) -> dict:
    from bbox import extract_problem_bboxes
    import hancom_decode as H
    out: dict[str, dict] = {}
    for rd in rounds:
        pdf = ROOT / 'db' / 'raw' / rd / '문제.pdf'
        if not pdf.exists():
            print(f'  · {rd}: 문제.pdf 없음 — 건너뜀', flush=True)
            continue
        try:
            ents = extract_problem_bboxes(str(pdf), exam_type='모의고사', grade='고3')
        except Exception as e:
            print(f'  ! {rd}: bbox 실패 {e}', flush=True)
            continue
        n = 0
        for e in ents:
            if per_round and n >= per_round:
                break
            key = f"{rd}|{e.get('subject','?')}|{e.get('number','?')}"
            try:
                out[key] = {'text': H.decode_problem(str(pdf), e['page_num'], e['bbox_pdf'])}
            except Exception as ex:
                out[key] = {'text': None, 'error': f'{type(ex).__name__}: {ex}'}
            n += 1
        print(f'  ✓ {rd}: {n}건', flush=True)
    return out


def diff(a_path: str, b_path: str) -> int:
    a = json.loads(Path(a_path).read_text(encoding='utf-8'))
    b = json.loads(Path(b_path).read_text(encoding='utf-8'))
    keys = sorted(set(a) | set(b))
    changed = [k for k in keys if a.get(k, {}).get('text') != b.get(k, {}).get('text')]
    newerr = [k for k in keys if not a.get(k, {}).get('error') and b.get(k, {}).get('error')]
    print(f'대상 {len(keys)} · 변경 {len(changed)} · 새 예외 {len(newerr)}')
    for k in newerr[:10]:
        print(f'  ★새 예외 {k}: {b[k]["error"]}')
    for k in changed[:25]:
        print(f'\n── {k}')
        print(f'  전: {(a.get(k,{}).get("text") or "")[:220]!r}')
        print(f'  후: {(b.get(k,{}).get("text") or "")[:220]!r}')
    if len(changed) > 25:
        print(f'\n… 외 {len(changed)-25}건 (전수는 json 을 직접 비교하라)')
    # 새 예외가 하나라도 생기면 실패로 알린다 — 조용한 퇴행 방지.
    return 1 if newerr else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='')
    ap.add_argument('--diff', nargs=2, default=None)
    ap.add_argument('--per-round', type=int, default=0, help='회차당 최대 문항수(0=전부)')
    ap.add_argument('--rounds', default='', help='쉼표구분. 비우면 db/raw 의 모든 회차')
    a = ap.parse_args()

    if a.diff:
        return diff(*a.diff)
    rounds = [r for r in a.rounds.split(',') if r] or \
        sorted(p.name for p in (ROOT / 'db' / 'raw').iterdir() if p.is_dir())
    print(f'회차 {len(rounds)}개 스냅샷…', flush=True)
    snap = snapshot(rounds, a.per_round)
    Path(a.out or '/tmp/decode_snapshot.json').write_text(
        json.dumps(snap, ensure_ascii=False), encoding='utf-8')
    print(f'✓ {len(snap)}건 → {a.out or "/tmp/decode_snapshot.json"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
