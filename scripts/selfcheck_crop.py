#!/usr/bin/env python3
"""크롭 자기검증 — 전 문제에 대해 (1)헤더 포함, (2)상단 짤림 잔존 탐지.

recrop_top 의 _round_entries 로 bbox 를 얻고, crop_problem 과 동일하게 최종 crop-top 을
재현한 뒤:
  - 헤더 포함: crop-top 위 85px 안에 전체폭 룰(헤더 구분선)이 있으면 = 헤더 들어옴.
  - 상단 짤림: crop-top 바로 위에 같은 문제 잉크가 연속(gap<6px)으로 ≥8px 남았고
    그 위가 섹션라벨/룰 천장 아래면 = 내용이 잘림.
출력: clip_px / header 플래그를 큰 순으로.
"""
import sys, glob, os, re
sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ingest_kice')
import recrop_top as RT, crop_with_llm as CW, bbox as BB
import fitz
from PIL import Image

ROOT = RT.ROOT


def final_top(page, bbox):
    x0, y0, x1, y1 = [int(v) for v in bbox]
    if (y1 - y0) < 4 or (x1 - x0) < 4:
        return y0
    ri = CW._row_ink_ratios(page.crop((x0, y0, x1, y1)).convert('L')); h = y1 - y0
    pad = max(CW.MIN_PADDING_PX, int(CW.PADDING_RATIO * h))
    pt = max(0, y0 + max(0, CW._find_problem_start(ri, h) - pad) - 18)
    look_bot = min(y0 + 10, y1)
    if 0 < pt < look_bot:
        bi = CW._row_ink_ratios(page.crop((x0, pt, x1, look_bot)).convert('L'))
        rr = [r for r, v in enumerate(bi) if v > 0.70]
        if rr:
            pt = pt + max(rr) + 1
    return pt


def main():
    md_by = {os.path.basename(p)[:-3]: p for p in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)}
    header_hits, clip_hits, skipped = [], [], 0
    rule_cache = {}
    for slug in sorted(md_by):
        t = open(md_by[slug]).read()
        def f(k):
            m = re.search(rf'^\s*{k}:\s*(.+)$', t, re.M)
            return m.group(1).strip().strip('"\'') if m else None
        m = (re.search(r'image_paths:\s*\[([^\]\n]+)', t) or re.search(r'image_paths:\s*\n\s*-\s*(\S+)', t))
        if not m:
            skipped += 1; continue
        img_rel = m[1].split(',')[0].strip()
        try:
            round_slug = img_rel.split('/')[2]
        except IndexError:
            skipped += 1; continue
        subject, number = f('subject'), f('number')
        if not number or not number.isdigit():
            skipped += 1; continue
        number = int(number)
        got = RT._round_entries(round_slug, f('exam_type'), f('session'), subject)
        if not got:
            skipped += 1; continue
        ents, pages = got
        cands = [e for e in ents if e['number'] == number]
        if len(cands) > 1:
            sub = [e for e in cands if e.get('subject') == subject]
            if sub:
                cands = sub
        if not cands:
            skipped += 1; continue
        e = cands[0]
        page_path = pages.get(e['page_num'])
        if not page_path:
            skipped += 1; continue
        page = Image.open(page_path)
        x0, y0, x1, y1 = [int(v) for v in e['bbox_px']]
        ft = final_top(page, e['bbox_px'])
        # rules (px) for this round+page
        rk = (round_slug, e['page_num'], id(ents))
        if rk not in rule_cache:
            # ents 가 어느 PDF 에서 나왔는지 모르니, 페이지 이미지 자체로 full-width dark row 탐지
            import numpy as np
            arr = np.asarray(page.convert('L'))
            rule_cache[rk] = [yy for yy in range(min(arr.shape[0], y1)) if (arr[yy] < 128).mean() > 0.55]
        rules_px = rule_cache[rk]
        # (1) 헤더 포함: crop-top 위(작은 y) 85px 안에 전체폭 룰
        if any(ft < r < ft + 85 for r in rules_px):
            header_hits.append((round_slug, subject, number, ft))
        # (2) 상단 짤림: crop-top 바로 위 연속 잉크
        import numpy as np
        top = max(0, ft - 60)
        if ft - top > 4:
            col = np.asarray(page.crop((x0, top, x1, ft)).convert('L'))
            ink = (col < 128).mean(axis=1)
            gap = 0; reached = ft
            for j in range(len(ink) - 1, -1, -1):
                if ink[j] > 0.02:
                    gap = 0; reached = top + j
                else:
                    gap += 1
                    if gap >= 6:
                        break
            clip = ft - reached
            # 룰/라벨 위는 헤더라 짤림 아님 → reached 가 어떤 룰보다 아래여야 진짜 짤림
            above_rule = any(reached <= r < ft for r in rules_px)
            if clip >= 8 and not above_rule:
                clip_hits.append((clip, round_slug, subject, number))
    clip_hits.sort(reverse=True)
    print(f'검사 제외(이미지/bbox 없음): {skipped}')
    print(f'헤더 포함 의심: {len(header_hits)}')
    for r, s, n, ft in header_hits[:30]:
        print(f'   HEADER {r} {s}_{n} (ft={ft})')
    print(f'상단 짤림 의심(≥8px): {len(clip_hits)}')
    for c, r, s, n in clip_hits[:40]:
        print(f'   CLIP {c}px {r} {s}_{n}')


if __name__ == '__main__':
    main()
