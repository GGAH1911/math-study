#!/usr/bin/env python3
"""로제타 백필 — 기존 문제 .md 의 searchable_text를 기하 디코드(LLM-free)로 재생성 +
도형 추출 + has_figure 재계산. PDF 단위 처리(extract_pages 1회/PDF). 진행률 로그.

깨진 ⋄/오독(m→a) searchable_text를 hancom_decode(로제타 121종 + 분수·지수·첨자·cases·근호
기하 복원)로 교체. 백그라운드 실행 + /tmp/ingest_logs/<name>.log 관측.

usage: backfill_rosetta.py [--round SUBSTR] [--apply] [--limit N]
  기본 dry-run(파일 미수정). --apply 시 .md 패치.
"""
import sys, os, re, glob, time, argparse, traceback
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hancom_decode as H
from bbox import extract_problem_bboxes
import figures as FIG
from pdfminer.high_level import extract_pages

REPO = os.path.abspath(os.path.join(HERE, '..', '..'))

# 선택과목(확통/미적/기하) collapse 가드. 수능/모평 문제.pdf 는 보통 한 선택과목 부클릿(공통22+한선택23-30)
# 이라, pdf_for 가 모든 선택과목을 같은 문제.pdf 로 폴백하면 번호(23-30) 충돌로 다른 과목 내용이
# 덮어써진다(예: 기하_26 ← 확통_26). 디코드 내용이 md 과목과 '다른 선택과목'으로 판정되면 skip(원본 보존).
_SUBJ_SIG = {
    '확률과통계': ['정규분포', '표본평균', '신뢰구간', '이항분포', '확률밀도', '모평균', '조건부확률', '이항정리'],
    '미적분': ['등비급수', '매개변수', '음함수', '이계도함수', '정적분', '부정적분', '삼각함수의 극한'],
    '기하': ['타원', '쌍곡선', '포물선', '점근선', '정사영', '방향벡터', '법선벡터', '평면벡터'],
}


def _subject_mismatch(text, subject):
    if subject not in _SUBJ_SIG:
        return False  # 공통/단일은 번호충돌 없음
    sc = {k: sum(t in text for t in v) for k, v in _SUBJ_SIG.items()}
    best = max(sc, key=sc.get)
    return sc[best] >= 2 and best != subject


def _f(txt, key):
    m = re.search(rf'^\s*{key}:\s*(.+)$', txt, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def parse_md(path):
    txt = open(path, encoding='utf-8').read()
    fm = txt.split('---', 2)[1] if txt.startswith('---') else txt
    num = _f(fm, 'number')
    return {
        'path': path, 'txt': txt,
        'num': int(num) if num and num.isdigit() else None,
        'subject': _f(fm, 'subject'), 'exam_type': _f(fm, 'exam_type'), 'grade': _f(fm, 'grade'),
    }


def pdf_for(md):
    """md → 실제 문제 PDF 경로. docs/problems/<year>/<round>/ → db/raw/<year>_<round>/<subj>_문제.pdf"""
    p = md['path']; parts = p.split(os.sep)
    try:
        i = parts.index('problems'); year = parts[i + 1]; rnd = parts[i + 2]
    except Exception:
        return None
    slug = f'{year}_{rnd}'
    base = os.path.join(REPO, 'db', 'raw', slug)
    for cand in (f"{md['subject']}_문제.pdf", '문제.pdf'):
        fp = os.path.join(base, cand)
        if os.path.exists(fp):
            return fp
    hits = glob.glob(os.path.join(base, '*문제*.pdf'))
    return hits[0] if hits else None


def patch(txt, new_st, has_fig, fig_after=None):
    block = 'searchable_text: |\n' + '\n'.join(('  ' + l) if l.strip() else '' for l in new_st.split('\n')) + '\n'
    txt2 = re.sub(r'^searchable_text:\s*\|?\s*\n(?:[ \t]+.*\n|\n)*', lambda m: block, txt, count=1, flags=re.M)
    txt2 = re.sub(r'^has_figure:\s*\S+', lambda m: f'has_figure: {str(bool(has_fig)).lower()}', txt2, count=1, flags=re.M)
    # figure_after_line: 기존 줄 제거 후 도형 있을 때만 has_figure 뒤에 기록(없으면 .astro 가 1로 폴백)
    txt2 = re.sub(r'^figure_after_line:.*\n', '', txt2, count=1, flags=re.M)
    if has_fig and fig_after is not None:
        txt2 = re.sub(r'^(has_figure:.*\n)', lambda m: m.group(1) + f'figure_after_line: {int(fig_after)}\n', txt2, count=1, flags=re.M)
    return txt2


def _lines_above(rc, fig_bbox):
    """도형 위쪽 '본문' 텍스트 줄 수 = 재구성에서 도형 삽입 위치(그 줄 뒤).
    rc=문제영역 글자(pdfminer bottom-left), fig_bbox=도형 bbox(pdfminer 동일계). 줄=center-y 밴드.
    첨자/분수 보조밴드(작은 글자만 있는 밴드)는 _parse가 본문 줄에 합치므로 제외 → searchable_text 줄과 정렬."""
    if not rc:
        return 1
    sizes = sorted(c.size for c in rc); main = sizes[len(sizes) // 2] or 10
    fig_top = fig_bbox[3]  # pdfminer max-y (도형 위쪽 가장자리)
    above = sorted((c for c in rc if (c.y0 + c.y1) / 2 > fig_top), key=lambda c: -(c.y0 + c.y1) / 2)
    bands = []; cur = []; last = None
    for c in above:
        cy = (c.y0 + c.y1) / 2
        if last is not None and last - cy > main * 0.7:
            bands.append(cur); cur = []
        cur.append(c); last = cy
    if cur:
        bands.append(cur)
    return sum(1 for bd in bands if any(c.size >= main * 0.85 for c in bd))


def decode_pdf(pdf, exam_type, grade):
    """PDF 의 전 문제 searchable_text(기하 디코드) + 도형보유 집합. extract_pages 1회."""
    pages = {}; has_pua = False
    for pi, page in enumerate(extract_pages(pdf)):
        chars, bars = H._page_chars_bars(page)
        pages[pi] = (page.height, chars, bars)
        if not has_pua and any(0xE000 <= ord(ch) <= 0xF8FF for c in chars for ch in c.get_text()):
            has_pua = True
    if not has_pua:
        return {}, set(), {}  # 비-한컴(PUA 없음): 기존 searchable_text 정상 → 회귀 방지 위해 건너뜀
    ents = extract_problem_bboxes(pdf, exam_type=exam_type, grade=grade)
    out = {}; prob_chars = {}
    for e in ents:
        pi = e['page_num'] - 1
        if pi not in pages:
            continue
        Hh, chars, bars = pages[pi]
        bx0, by0, bx1, by1 = e['bbox_pdf']
        rc = [c for c in chars if bx0 - 2 <= (c.x0 + c.x1) / 2 <= bx1 + 2 and by0 - 2 <= (Hh - (c.y0 + c.y1) / 2) <= by1 + 2]
        rb = [b for b in bars if bx0 - 2 <= (b[0] + b[1]) / 2 <= bx1 + 2 and by0 - 2 <= (Hh - b[2]) <= by1 + 2]
        try:
            t = H._parse(rc, rb)
            t = re.sub(r'^\s*\d{1,2}\s*[.．]\s*', '', t).strip()
            t = re.sub(r'\s*[*★●∗]?\s*확인\s*사항[\s\S]*?답안지[\s\S]*$', '', t).rstrip()  # 답안지 안내 footer 제거
            t = re.sub(r'(?m)^[ \t]*[|‖∣｜](?:[ \t]*[|‖∣｜])*[ \t]*$\n?', '', t)  # 파이프만 있는 줄(cases 중괄호/HWP 잔재) 제거
            t = re.sub(r'━+', '', t)  # 구분선(U+2501) 런 제거
            _dm = re.search(r'(([가-힣])\2{1,2}\s*){3,}', t)  # doubled footer(선선택택…/확확인인 사사항항, 그룹 사이 공백 허용) → 끝까지
            if _dm:
                t = t[:_dm.start()].rstrip(' *\n\t')
            out[(e['subject'], e['number'])] = t
        except Exception:
            out[(e['subject'], e['number'])] = None
        prob_chars[(e['subject'], e['number'])] = rc
    figset = set(); figpos = {}
    try:
        for m in FIG.map_to_problems(pdf, exam_type=exam_type, grade=grade):
            num = m['problem']
            if not num:
                continue
            key = (m.get('subject'), num)  # 선택과목 번호충돌 방지: (과목,번호) 키
            figset.add(key)
            rc = prob_chars.get(key)
            if rc:
                figpos[key] = _lines_above(rc, m['bbox'])
    except Exception:
        pass
    return out, figset, figpos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--round', default='')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--log', default='/tmp/ingest_logs/rosetta_backfill.log')
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.log), exist_ok=True)
    logf = open(a.log, 'a', buffering=1)
    def log(*m):
        s = ' '.join(str(x) for x in m); print(s); logf.write(s + '\n')

    mds = sorted(glob.glob(os.path.join(REPO, 'docs', 'problems', '**', '*.md'), recursive=True))
    if a.round:
        mds = [m for m in mds if a.round in m]
    # PDF 단위 그룹
    groups = defaultdict(list)
    for p in mds:
        md = parse_md(p)
        if md['num'] is None:
            continue
        pdf = pdf_for(md)
        if pdf:
            groups[(pdf, md['exam_type'] or '모의고사', md['grade'] or '고3')].append(md)
    log(f'[{time.strftime("%H:%M:%S")}] 백필 시작: {len(mds)} md, {len(groups)} PDF, apply={a.apply}')
    done = changed = failed = 0; t0 = time.time()
    for gi, ((pdf, et, gr), items) in enumerate(sorted(groups.items())):
        try:
            decoded, figset, figpos = decode_pdf(pdf, et, gr)
        except Exception as e:
            log(f'  ✗ PDF 실패 {os.path.basename(pdf)}: {str(e)[:80]}'); failed += len(items); continue
        for md in items:
            done += 1
            st = decoded.get((md['subject'], md['num']))
            if not st:  # subject 라벨 불일치(가형/나형/단일 .md ↔ bbox추출기 '공통') → 번호 폴백
                cands = [v for (s, n), v in decoded.items() if n == md['num']]
                if len(cands) == 1:  # PDF당 단일과목이면 번호로 유일 매칭(안전); 다과목이면 보류
                    st = cands[0]
            if not st or len(st) < 8:
                continue
            if _subject_mismatch(st, md['subject']):
                continue  # (안전망) 디코드 내용이 다른 선택과목이면 원본 보존
            hf = (md['subject'], md['num']) in figset
            new = patch(md['txt'], st, hf, figpos.get((md['subject'], md['num'])))
            if new != md['txt']:
                changed += 1
                if a.apply:
                    open(md['path'], 'w', encoding='utf-8').write(new)
        if gi % 5 == 0 or gi == len(groups) - 1:
            log(f'[{time.strftime("%H:%M:%S")}] PDF {gi+1}/{len(groups)} | 문제 {done} | 변경 {changed} | 실패 {failed} | {time.time()-t0:.0f}s')
        if a.limit and done >= a.limit:
            log('  (limit 도달)'); break
    log(f'[{time.strftime("%H:%M:%S")}] 완료: 처리 {done} | 변경 {changed} | 실패 {failed} | {time.time()-t0:.0f}s | {"APPLIED" if a.apply else "DRY-RUN"}')


if __name__ == '__main__':
    main()
