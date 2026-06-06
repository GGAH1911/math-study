#!/usr/bin/env python3
"""빈칸추론형 searchable_text를 이미지와 재대조해 OCR 결함률 측정 (값-스캔이 못 보는 결함까지).
이미지=ground truth, 저장 전사본=검수대상. Sonnet에게 둘을 대조시켜 불일치만 JSON으로 받음.
#18에서 본 '그럴듯하지만 틀린 값 / 환각 유도 / 누락'을 정량화 — '유니크냐 광범위냐'를 측정으로.
환경: AUDIT_LIMIT(10), AUDIT_MODEL(sonnet), AUDIT_TO(200), AUDIT_WORKERS(4)."""
from __future__ import annotations
import re, sys, json, glob, os, subprocess, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

LIMIT = int(os.environ.get('AUDIT_LIMIT', '10'))
MODEL = os.environ.get('AUDIT_MODEL', 'sonnet')
TO = int(os.environ.get('AUDIT_TO', '200'))
WORKERS = int(os.environ.get('AUDIT_WORKERS', '4'))
SYSTEM = ("당신은 한국 수능 수학 문제의 OCR 전사를 검수하는 꼼꼼한 교정자다. "
          "첨부 이미지가 정답(ground truth)이고 저장 전사본이 검수 대상이다. 추측 금지, 이미지에서 확인되는 것만.")


def extract_searchable(text):
    m = re.search(r'^searchable_text:\s*[|>][-+]?\s*\n(.*?)(?=^\S|\Z)', text, re.M | re.S)
    return (m.group(1) if m else '').strip()


def prompt_for(tiles, stored):
    listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(tiles))
    return (f"문제 이미지(여러 장일 수 있음):\n{listing}\n\n"
            f"저장된 전사본:\n\"\"\"\n{stored}\n\"\"\"\n\n"
            f"위 이미지를 Read로 모두 연 뒤, 저장 전사본을 이미지와 한 글자씩 대조하라. "
            f"이미지와 **다른** 부분만 골라라 — 틀린 수식/값, 이미지에 없는 내용 환각, 빠진 내용. "
            f"표현 차이(띄어쓰기·기호 표기)는 무시하고 **수학적 의미가 다른 것만**. "
            f"마지막에 오직 하나의 ```json 블록:\n"
            f'```json\n{{"defects": [{{"stored": "전사본의 틀린 부분", "correct": "이미지의 올바른 값", '
            f'"kind": "wrong-value|hallucination|omission"}}]}}\n```\n일치하면 {{"defects": []}}.')


def audit_one(item):
    path, stem, stored = item
    img = IMGDIR / (stem + '.png')
    if not img.exists():
        return dict(stem=stem, err='no-img', defects=[], cost=0.0)
    real = img.resolve()
    tiles = [str(t) for t in tile_for_vision(real)]
    args = ['claude', '-p', '--model', MODEL, '--effort', 'medium', '--allowedTools', 'Read',
            '--add-dir', str(real.parent), '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '12', '--system-prompt', SYSTEM, '--output-format', 'json', '--', prompt_for(tiles, stored)]
    t0 = time.time()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TO)
    except subprocess.TimeoutExpired:
        return dict(stem=stem, err='timeout', defects=[], cost=0.0, sec=TO)
    try:
        env = json.loads(r.stdout)
    except Exception:
        env = {}
    cost = (env or {}).get('total_cost_usd', 0) or 0.0
    txt = (env or {}).get('result', '') or ''
    defects = []
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            defects = json.loads(b).get('defects', [])
            break
        except Exception:
            pass
    return dict(stem=stem, err=None, defects=defects, cost=cost, sec=round(time.time() - t0))


def find_targets():
    out = []
    for f in sorted(glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)):
        if 'README' in f:
            continue
        st = extract_searchable(Path(f).read_text(encoding='utf-8'))
        if '(가)' in st and '(다)' in st:                 # 빈칸추론형
            out.append((Path(f), Path(f).stem, st))
    return out


def main():
    tg = find_targets()
    print(f"═══ 빈칸추론형 OCR 재대조 (이미지 vs 전사본, {MODEL}) ═══")
    print(f"  전체 빈칸추론형 {len(tg)}개 중 샘플 {min(LIMIT, len(tg))}개\n", flush=True)
    tg = tg[:LIMIT]
    res, tot = [], 0.0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed({ex.submit(audit_one, it): it for it in tg}):
            r = fut.result(); res.append(r); tot += r['cost']
            n = len(r['defects'])
            mark = '✅ 일치' if (n == 0 and not r['err']) else (f'🔴 결함 {n}건' if not r['err'] else f'⚠ {r["err"]}')
            print(f"  [{len(res)}/{len(tg)}] {r['stem']:34s} {mark}  ${r['cost']:.3f}", flush=True)
            for d in r['defects']:
                print(f"        · [{d.get('kind','?')}] 저장 \"{d.get('stored','')}\" → 실제 \"{d.get('correct','')}\"", flush=True)
    buggy = [r for r in res if r['defects']]
    ndef = sum(len(r['defects']) for r in res)
    clean = sum(1 for r in res if not r['defects'] and not r['err'])
    print(f"\n═══ 완료 ═══  {len(res)}개 · ${tot:.2f}", flush=True)
    print(f"  결함 있는 문제: {len(buggy)}/{len(res)}  ({100*len(buggy)/max(1,len(res)):.0f}%)  · 총 결함 {ndef}건 · 무결 {clean}", flush=True)
    print(f"  → 빈칸추론형 추정 결함률 ≈ {100*len(buggy)/max(1,len(res)):.0f}%  (#18만의 문제인지 광범위인지의 답)", flush=True)


if __name__ == '__main__':
    main()
