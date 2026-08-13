#!/usr/bin/env python3
"""개념 매핑 재작업 — 평면 참조를 가진 문제를 **원본 이미지 직독**으로 다시 매핑한다.

★배경(2026-08-13): 매핑이 틀린 진짜 이유는 모델이 아니라 입력이었다. 전사본이 지수를
  근호로 뭉개(4^(2/3) → 4√3/2) 수능 문제가 중3 무리수 문제처럼 보였고, 어떤 문항은
  본문이 통째로 사라져 "주어진 식의 값을 구하시오." 한 줄만 남아 있었다.
  그래서 이미지를 유일한 근거로 삼는다.

설계
  · 과목별로 묶어 돈다 — 메뉴가 시스템 프롬프트에 있어 **같은 과목끼리 붙여야 캐시가 산다**
    (실측: 두 번째 호출부터 cache_create 26k→10k, cache_read 72k→88k).
  · 중단·재개. 결과를 문제마다 즉시 JSONL 에 적고, 이미 처리한 슬러그는 건너뛴다.
    4시간짜리 작업에서 이게 없으면 한 번의 중단이 하루를 날린다.
  · 기본 dry-run. `--apply` 를 줘야 파일을 고친다. 되돌리기는 git(작업 전 clean 상태 확인).

사용:
  python3 scripts/remap_concepts.py --limit 100            # 파일럿(dry-run)
  python3 scripts/remap_concepts.py --limit 100 --apply    # 파일럿 반영
  python3 scripts/remap_concepts.py --apply                # 전수
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, time, types
import concurrent.futures as cf
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'ingest_kice'))
for _m in ('psycopg', 'fitz', 'psycopg.rows'):
    sys.modules.setdefault(_m, types.ModuleType(_m))
sys.modules['psycopg'].rows = sys.modules['psycopg.rows']
sys.modules['psycopg.rows'].dict_row = None

import ingest_round as IR          # noqa: E402
import run_stage1 as RS            # noqa: E402
import concept_remap as CR         # noqa: E402

PROGRESS = Path('/tmp/remap_concepts.jsonl')


def targets() -> list[dict]:
    """평면 참조(교육과정 트리 밖)를 하나라도 가진 문제. 그것이 이번 사고의 흔적이다."""
    out = []
    for f in ROOT.glob('docs/problems/**/*.md'):
        t = f.read_text(encoding='utf-8')[:6000]
        m = re.search(r'^concepts: \[(.*?)\]', t, re.M)
        if not m or not m.group(1).strip():
            continue
        refs = [r.strip() for r in m.group(1).split(',') if r.strip()]
        rels = [r.replace('docs/concepts/', '').replace('.md', '') for r in refs]
        if not any('/' not in r for r in rels):
            continue
        g = lambda p, d='': (re.search(p, t, re.M).group(1).strip() if re.search(p, t, re.M) else d)  # noqa: E731
        # 고등 회차인지 — 경로로 판정(수능·모평·고3·예시). grade 가 비어도 중학 후보는 막는다.
        is_high = any(k in str(f) for k in ('수능', '모평', '고3', '예시'))
        out.append({'md': f, 'slug': f.stem, 'is_high': is_high, 'subject': g(r'^  subject: (.+)$'),
                    'grade': g(r'^  grade: (.+)$'), 'number': g(r'^  number: (\d+)$', '0'),
                    'score': g(r'^  score: (\d+)$', '3'),
                    'image': g(r'^problem_image: (.+)$'), 'before': m.group(1)[:120]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--par', type=int, default=4)
    ap.add_argument('--model', default='sonnet')
    args = ap.parse_args()

    if args.apply:
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', 'docs/problems'],
                               capture_output=True, text=True, cwd=ROOT).stdout.strip()
        if dirty:
            print('[중단] docs/problems 에 커밋 안 된 변경이 있다 — 되돌릴 수 있게 먼저 정리하라')
            return 1

    done = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding='utf-8').splitlines():
            try: done.add(json.loads(line)['slug'])
            except Exception: pass

    items = [t for t in targets() if t['slug'] not in done]
    # 과목별로 묶는다 — 메뉴(시스템 프롬프트)가 같아야 캐시가 산다.
    by_subj = defaultdict(list)
    for t in items:
        by_subj[t['subject'] or '?'].append(t)
    ordered = [t for subj in sorted(by_subj, key=lambda s: -len(by_subj[s])) for t in by_subj[subj]]
    if args.limit:
        ordered = ordered[:args.limit]
    print(f'대상 {len(ordered)}건 (이미 처리 {len(done)}건 건너뜀) · 과목 {len(by_subj)}종 · '
          f'{"적용" if args.apply else "dry-run"} · {args.model} · 병렬 {args.par}', flush=True)

    idx_cache: dict[tuple, dict] = {}
    lock_out = []
    t_start = time.time()

    def work(t: dict) -> dict:
        key = (t['subject'], t['grade'], t['is_high'])
        if key not in idx_cache:
            idx_cache[key] = IR.load_concept_index(IR.scope_for(t['subject'], t['grade'], t['is_high']))
        index = idx_cache[key]
        if not index:
            return {'slug': t['slug'], 'status': 'no-scope'}
        img = ROOT / 'web' / 'public' / t['image'].lstrip('/')
        t0 = time.time()
        meta = RS.map_problem_once('', int(t['number'] or 0), int(t['score'] or 3), index,
                                   subject=t['subject'], grade=t['grade'], model=args.model,
                                   image=img if img.exists() else None)
        sec = round(time.time() - t0, 1)
        if not meta or not meta.get('unit'):
            return {'slug': t['slug'], 'status': 'map-fail', 'sec': sec}
        ok, why = IR.validate_mapping(meta['unit'], meta.get('concepts'), index)
        rec = {'slug': t['slug'], 'status': 'ok' if ok else 'partial', 'sec': sec,
               'unit': meta['unit'], 'concepts': meta.get('concepts') or [],
               'before': t['before'], 'why': why}
        if args.apply:
            st, info = CR.apply_map(str(t['md']), meta)
            rec['write'] = st
        return rec

    with cf.ThreadPoolExecutor(max_workers=args.par) as ex:
        for i, rec in enumerate(ex.map(work, ordered), 1):
            lock_out.append(rec)
            with PROGRESS.open('a', encoding='utf-8') as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + '\n')
            if i % 10 == 0 or i == len(ordered):
                el = time.time() - t_start
                print(f'  {i}/{len(ordered)} · {el/i:.1f}s/건 · 남은 예상 {(len(ordered)-i)*el/i/60:.0f}분', flush=True)

    st = defaultdict(int)
    for r in lock_out:
        st[r['status']] += 1
    print(f'\n결과: {dict(st)}')
    changed = [r for r in lock_out if r.get('unit')]
    if changed:
        print(f'평균 {sum(r["sec"] for r in changed)/len(changed):.1f}s/건')
        print('\n샘플 5건:')
        for r in changed[:5]:
            print(f"  {r['slug']}\n    이전: {r['before']}\n    이후: {r['unit']} + {len(r['concepts'])}개")
    print(f'\n진행기록: {PROGRESS}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
