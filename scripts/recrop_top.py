#!/usr/bin/env python3
"""상단 잘림(위첨자 클립) 보정 — gap-aware 재크롭. 크레딧 0 (순수 PIL + PDF 파싱).

완전성 우선: 첫 줄에서 위로 스캔해 작은 갭(위첨자)은 포함, 큰 갭(문제 사이)에서 정지.
페이지 헤더가 딸려와도 OK(문제 온전성 우선). 안 잘린 문제엔 사실상 no-op.
원본 페이지 렌더(pages/)에서 재크롭 → 사용자 이미지(db/raw/.../images, web symlink) 교체.

사용: python recrop_top.py --numbers 1[,2,3]   |   --list slug1,slug2   [--dry]
"""
from __future__ import annotations
import sys, re, glob, argparse, os, shutil
from pathlib import Path
from PIL import Image
import numpy as np

SKIP_TOP_INK = 20            # 현재 상단여백이 이보다 크면 이미 깨끗 → 재크롭 스킵


def _top_ink_row(path, t=0.015):
    a = np.asarray(Image.open(path).convert('L'))
    d = (a < 128).mean(axis=1)
    r = np.where(d > t)[0]
    return int(r[0]) if len(r) else 9999

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts' / 'ingest_kice'))
import crop_with_llm as CW       # noqa: E402
import ingest_v2 as IV           # noqa: E402

BLANK = CW.BLANK_ROW_INK_RATIO
_bbox_cache: dict = {}


def gap_aware(page_img: Image.Image, bbox_px, out_path: Path, exam_type, headroom=18):
    """인제스트 공용 crop_with_llm.crop_problem 위임 (단일 소스). 원래 경계 + 위로 headroom."""
    CW.crop_problem(page_img, bbox_px, out_path, exam_type=exam_type, headroom=headroom)


def _round_entries(round_slug, exam_type, session, subject):
    """회차 bbox 캐시. PDF 형식 3종:
      - 단일 `문제.pdf` (v2 평가원/수능·gyo12 고1/2)
      - 가/나형: `<가형|나형>_문제.pdf` + `pages_<subject>`
      - 교육청 고3(gyo3) 과목별: 선택은 `<미적분|기하|확률과통계>_문제.pdf`, 공통은
        미적분 PDF 안에. pages 는 `pages_<pdf과목>`.
    """
    raw = ROOT / 'db' / 'raw' / round_slug
    pdf_subject = None
    if (raw / '문제.pdf').exists():
        pdf = raw / '문제.pdf'; pages_dir = raw / 'pages'
    else:
        # 과목별 PDF 라운드. 공통은 선택 PDF(미적분 우선) 안에서 크롭.
        if subject in ('가형', '나형', '미적분', '기하', '확률과통계'):
            pdf_subject = subject
        elif subject == '공통':
            for cand in ('미적분', '기하', '확률과통계'):
                if (raw / f'{cand}_문제.pdf').exists():
                    pdf_subject = cand; break
        if not pdf_subject or not (raw / f'{pdf_subject}_문제.pdf').exists():
            _bbox_cache[round_slug + '|' + str(subject)] = None
            return None
        pdf = raw / f'{pdf_subject}_문제.pdf'
        pages_dir = raw / f'pages_{pdf_subject}'
        if not pages_dir.exists():
            pages_dir = raw / 'pages'
    key = round_slug + ('|' + pdf_subject if pdf_subject else '')   # PDF별 캐시
    if key in _bbox_cache:
        return _bbox_cache[key]
    pages_dir.mkdir(parents=True, exist_ok=True)
    if not list(pages_dir.glob('*.png')):
        IV.render_pdf_pages(pdf, pages_dir)
    page_by_num = {int(p.stem[1:]): p for p in pages_dir.glob('*.png')}
    et = '모의평가' if exam_type in ('모평', '모의평가') else exam_type
    ents = IV.extract_problem_bboxes(pdf, et, session)
    _bbox_cache[key] = (ents, page_by_num)
    return _bbox_cache[key]


def recrop_slug(slug, md_text, dry=False):
    def f(k, d=None):
        m = re.search(rf'^\s*{k}:\s*(.+)$', md_text, re.M)
        return m.group(1).strip().strip('"\'') if m else d
    # image_paths 는 인라인(`[a, b]`) 또는 블록(`image_paths:\n  - a`) 두 형식 다 존재.
    # 둘 다 파싱(블록만 보던 게 84문제를 'no-img-path'로 잘못 스킵하던 버그).
    m = (re.search(r'image_paths:\s*\[([^\]\n]+)', md_text)
         or re.search(r'image_paths:\s*\n\s*-\s*(\S+)', md_text))
    img_rel = m[1] if m else None
    if not img_rel:
        return 'no-img-path'
    img_fs = ROOT / img_rel.split(',')[0].strip()
    round_slug = img_rel.split('/')[2]               # db/raw/<ROUND>/images/...
    exam_type, session = f('exam_type'), f('session')
    subject, number = f('subject'), int(f('number', '0'))
    got = _round_entries(round_slug, exam_type, session, subject)
    if not got:
        return 'no-pdf'
    ents, page_by_num = got
    cands = [e for e in ents if e['number'] == number]      # ganah PDF는 트랙별이라 번호로 충분
    if len(cands) > 1:                                       # v2 다과목: 번호 중복 시 subject로 좁힘
        sub = [e for e in cands if e.get('subject') == subject]
        if sub:
            cands = sub
    if not cands:
        return 'no-bbox'
    e = cands[0]
    page = page_by_num.get(e['page_num'])
    if not page:
        return 'no-page'
    # 전수 적용: gap_aware 는 bbox+페이지에서 매번 재계산(idempotent) → 원래크롭+headroom 으로 통일.
    # 깨끗한 문제엔 여백만 더해지고, 클립은 복구된다.
    before = Image.open(img_fs).size if img_fs.exists() else None
    if not dry:
        gap_aware(Image.open(page), e['bbox_px'], img_fs, '모의고사' if exam_type == '모의고사' else exam_type)
        # 웹 심링크 실타깃(메인 레포 db/raw)도 갱신 → dev 서버 즉시 반영 (worktree 심링크가 메인 가리킴)
        web = ROOT / 'web' / 'public' / 'problem-images' / f'{slug}.png'
        if web.exists():
            real = Path(os.path.realpath(web))
            if real != img_fs.resolve():
                shutil.copy(img_fs, real)
    after = Image.open(img_fs).size if img_fs.exists() else None
    return f'ok {before}→{after}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--numbers', help='쉼표구분 문제번호 (예: 1 또는 1,2,3)')
    ap.add_argument('--list', help='쉼표구분 slug')
    ap.add_argument('--all', action='store_true', help='전체 문제 (잘린 것만 자동 보정)')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    md_by = {p.split('/')[-1][:-3]: p for p in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)}
    if a.list:
        slugs = [s.strip() for s in a.list.split(',') if s.strip()]
    elif a.all:
        slugs = list(md_by)
    elif a.numbers:
        nums = set(a.numbers.split(','))
        slugs = [s for s in md_by if s.rsplit('_', 1)[-1] in {n.zfill(2) for n in nums}]
    else:
        print('--numbers / --list / --all 필요'); return
    print(f"대상 {len(slugs)}개 (dry={a.dry})", flush=True)
    from collections import Counter
    res = Counter()
    for i, s in enumerate(sorted(slugs), 1):
        try:
            r = recrop_slug(s, open(md_by[s]).read(), a.dry)
        except Exception as ex:
            r = f'err:{ex}'
        tag = r.split()[0]
        res[tag] += 1
        if tag != 'ok' or i <= 5:
            print(f"  [{i}/{len(slugs)}] {s}: {r}", flush=True)
    print(f"\n결과: {dict(res)}", flush=True)


if __name__ == '__main__':
    main()
