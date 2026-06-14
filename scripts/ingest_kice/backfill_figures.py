#!/usr/bin/env python3
"""도형 백필 — figures.map_to_problems 로 임베드 도형 추출+stitch →
web/public/problem-images/<stem>_fig.png 저장 + .md frontmatter 에 figure_image 추가.
searchable_text 백필(backfill_rosetta)과 별도 필드라 순차 실행. 진행 로그.
"""
import sys, os, re, glob, time, argparse
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figures as FIG
from backfill_rosetta import parse_md, pdf_for, REPO

PUBIMG = os.path.join(REPO, 'web', 'public', 'problem-images')


def set_figure_image(txt, webpath):
    if re.search(r'^figure_image:', txt, re.M):
        return re.sub(r'^figure_image:.*$', lambda m: f'figure_image: {webpath}', txt, count=1, flags=re.M)
    if re.search(r'^has_figure:', txt, re.M):
        return re.sub(r'^(has_figure:.*)$', lambda m: m.group(1) + f'\nfigure_image: {webpath}', txt, count=1, flags=re.M)
    return txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--round', default='')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--log', default='/tmp/ingest_logs/figure_backfill.log')
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.log), exist_ok=True)
    os.makedirs(PUBIMG, exist_ok=True)
    logf = open(a.log, 'a', buffering=1)
    def log(*m):
        s = ' '.join(str(x) for x in m); print(s); logf.write(s + '\n')

    mds = sorted(glob.glob(os.path.join(REPO, 'docs', 'problems', '**', '*.md'), recursive=True))
    if a.round:
        mds = [m for m in mds if a.round in m]
    groups = defaultdict(list)
    for p in mds:
        md = parse_md(p)
        if md['num'] is None:
            continue
        pdf = pdf_for(md)
        if pdf:
            groups[(pdf, md['exam_type'] or '모의고사', md['grade'] or '고3')].append(md)
    log(f'[{time.strftime("%H:%M:%S")}] 도형 백필: {len(mds)} md, {len(groups)} PDF, apply={a.apply}')
    saved = tagged = 0
    for gi, ((pdf, et, gr), items) in enumerate(sorted(groups.items())):
        try:
            figmap = {(m['subject'], m['problem']): m['image']
                      for m in FIG.map_to_problems(pdf, exam_type=et, grade=gr) if m['problem']}
        except Exception as e:
            log(f'  ✗ {os.path.basename(pdf)}: {str(e)[:60]}'); continue
        bykey = {(m['subject'], m['num']): m for m in items}  # 선택과목 번호충돌 방지: (과목,번호) 키
        for key, img in figmap.items():
            md = bykey.get(key)
            if not md:
                continue
            stem = os.path.basename(md['path'])[:-3]
            webpath = f'/problem-images/{stem}_fig.png'
            if a.apply:
                try:
                    img.save(os.path.join(PUBIMG, f'{stem}_fig.png'))
                    saved += 1
                except Exception:
                    continue
                new = set_figure_image(md['txt'], webpath)
                if new != md['txt']:
                    open(md['path'], 'w', encoding='utf-8').write(new); tagged += 1
            else:
                saved += 1
        if gi % 10 == 0 or gi == len(groups) - 1:
            log(f'[{time.strftime("%H:%M:%S")}] PDF {gi+1}/{len(groups)} | 도형저장 {saved} | 태그 {tagged}')
    log(f'[{time.strftime("%H:%M:%S")}] 완료: 도형 {saved} | 태그 {tagged} | {"APPLIED" if a.apply else "DRY"}')


if __name__ == '__main__':
    main()
