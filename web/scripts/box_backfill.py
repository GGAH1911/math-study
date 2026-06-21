#!/usr/bin/env python3
# box_backfill.py — 교정완료(corrector_done) 문제의 searchable_text 에 detect_boxes 로 찾은
#   테두리 박스의 {{BOXn_START}}/{{BOXn_END}} 마커를 '결정적'으로 삽입한다(A 백필).
#   · 줄구조 보존(apply_md 처럼 한 줄로 합치지 않음 → 재교정 불필요·LLM 0)
#   · 멱등({{BOX 이미 있으면 skip)
#   · 읽기전용(PDF 만 읽음, extract() 미사용 → 도형 이미지 절대 안 건드림)
#   로그는 stdout (.venv/bin/python -u 로 실시간 — /progress 관측). docs/problems 만 쓰므로 4324(STABLE)는 안 깜박.
import sys, re, os, glob, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # web/scripts
import fitz
from extract_figures import find_region, detect_boxes, REPO


def norm(s):
    return re.sub(r'[^가-힣A-Za-z0-9]', '', s or '')


def _scan(lines, key_src, head, normfn):
    base = normfn(key_src)
    if len(base) < 4:
        return -1
    norm_lines = [normfn(ln) for ln in lines]
    for trim in range(len(base), 3, -1):
        key = base[:trim] if head else base[-trim:]
        for idx, nl in enumerate(norm_lines):
            if key in nl:
                return idx
    return -1

def match_line(lines, anchor, head):
    """anchor(머리=head True / 꼬리=head False)와 일치하는 corrected 줄 인덱스.
    ① 정규화(한글+영숫자) 엄격 패스 → ② 한글-only 완화 패스(PDF 가 '[4점]'을 '점 ? [4]'로 garble 해도 숫자/라틴 무시 매칭)."""
    i = _scan(lines, anchor, head, norm)
    if i >= 0:
        return i
    return _scan(lines, anchor, head, lambda s: re.sub(r'[^가-힣]', '', s or ''))


# 조건 (가)(나)(다)·보기 ㄱㄴㄷ·유도 (i)(ii)(iii) 마커로 '시작'하는 줄 — 박스 내용의 깨끗한 텍스트 신호.
#   질문줄("위의 (가), (나)에 …")은 '위의'로 시작하므로 매칭 안 됨(START 매칭).
_MARK = re.compile(r'^\s*(?:[(（]\s*[가-하]\s*[)）]|[ㄱ-ㅎ]\s*[.)）]|[(（]\s*(?:i{1,3}|iv|v|ⅰ|ⅱ|ⅲ|ⅳ)\s*[)）])')

def _runs(idxs, gap=2):
    """정렬된 줄 인덱스를 연속 run 으로 묶음(gap 이하 떨어지면 같은 run). [1,2,5,6,7]→[(1,2),(5,7)]."""
    if not idxs:
        return []
    idxs = sorted(idxs); out = [[idxs[0], idxs[0]]]
    for j in idxs[1:]:
        if j - out[-1][1] <= gap:
            out[-1][1] = j
        else:
            out.append([j, j])
    return [tuple(r) for r in out]

def box_range(page, REG, b, lines, single=False, idx=0, n=1):
    """박스 b=(xl,yt,xr,yb)가 감싸는 searchable_text 줄 범위 (lo, hi).
    ① 박스 '안' 본문 블록을 줄에 매칭(텍스트 위주). ② 수식 위주는 위/아래 경계. ③ 단일 박스면 마커 줄((가)(나)·ㄱㄴㄷ·(i)(ii)) run 으로 보강 — PDF 블록이 PUA·\begin{cases} 라 inside 가 비거나 부분일 때 핵심."""
    blocks = [bl for bl in page.get_text('blocks')
              if REG.x0 - 5 <= bl[0] and bl[2] <= REG.x1 + 5 and bl[1] >= REG.y0 - 5 and bl[3] <= REG.y1 + 5]
    def is_body(bl):
        return re.search(r'[가-힣]', bl[4]) and not re.match(r'^\s*\[그림\s*\d+\]\s*$', bl[4].strip())
    inside = sorted([bl for bl in blocks if b[1] - 3 <= (bl[1] + bl[3]) / 2 <= b[3] + 3 and is_body(bl)], key=lambda bl: bl[1])
    above = sorted([bl for bl in blocks if bl[3] <= b[1] + 5 and is_body(bl)], key=lambda bl: bl[3])
    below = sorted([bl for bl in blocks if bl[1] >= b[3] - 5 and is_body(bl)], key=lambda bl: bl[1])
    stem = lambda j: 0 <= j < len(lines) and bool(re.match(r'^\s*\d{1,2}\.\s', lines[j]))   # 문제번호 줄("19. …")
    a_idx = match_line(lines, above[-1][4], head=False) if above else -1   # 박스 위 줄
    b_idx = match_line(lines, below[0][4], head=True) if below else -1     # 박스 아래 줄
    in_idxs = [j for j in (match_line(lines, bl[4], head=True) for bl in inside) if j >= 0 and not stem(j)]
    allmark = [j for j, l in enumerate(lines) if _MARK.match(l) and not stem(j)]   # (가)(나)·ㄱㄴㄷ·(i)(ii) 시작 줄
    bound = (a_idx + 1, b_idx - 1) if (a_idx >= 0 and b_idx > a_idx + 1) else None
    runs = _runs(allmark)
    if n > 1 and len(runs) == n:
        # 멀티박스(조건+보기 등): 마커 run 을 박스 순서(위→아래)에 1:1 배정. ("보기"(2자) 짧아 경계 매칭 실패해도 동작)
        lo, hi = runs[idx]
    elif bound:
        # 박스 = stem 아래 ~ 질문 위. 그 경계 '안'의 마커 줄이 있으면 거기에 타이트하게(멀티박스도 박스별 경계로 마커 귀속).
        mk = [j for j in allmark if bound[0] <= j <= bound[1]]
        lo, hi = (min(mk), max(mk)) if mk else bound
    elif single and allmark:                                               # 경계 없음(단답형 등) + 단일 박스 → 마커 run
        lo, hi = min(allmark), max(allmark)
    elif in_idxs:                                                          # 최후: 박스 안 본문 블록 매칭
        lo, hi = min(in_idxs), max(in_idxs)
    else:
        return None
    if stem(lo):                                                           # stem 을 감싸면(본문 조건 누락 등) 무효 → skip(재교정 대상)
        return None
    return lo, hi


_doc_cache = {}
def open_doc(round_, subj):
    pdf = f'{REPO}/db/raw/{round_}/{subj}_문제.pdf'
    if not os.path.exists(pdf):
        pdf = f'{REPO}/db/raw/{round_}/문제.pdf'
    if not os.path.exists(pdf):
        return None
    if pdf not in _doc_cache:
        _doc_cache[pdf] = fitz.open(pdf)
    return _doc_cache[pdf]


def process(md):
    txt = open(md, encoding='utf-8').read()
    if '{{BOX' in txt:
        return ('skip-already', 0, None)
    if 'corrector_done: true' not in txt:
        return ('skip-uncorrected', 0, None)
    m = re.search(r'\nsearchable_text: \|\n((?:  .*\n?)*)', txt)
    if not m:
        return ('no-searchable', 0, None)
    base = os.path.basename(md)[:-3]
    mm = re.match(r'^(.+)_([^_]+)_(\d+)$', base)
    if not mm:
        return ('name-parse-fail', 0, None)
    round_, subj, num = mm.group(1), mm.group(2), int(mm.group(3))
    doc = open_doc(round_, subj)
    if doc is None:
        return ('no-pdf', 0, None)
    try:
        pi, REG = find_region(doc, num)
    except Exception as e:
        return ('region-exc', 0, str(e))
    if REG is None:
        return ('no-region', 0, None)
    page = doc[pi]
    boxes = detect_boxes(page, REG)
    if not boxes:
        return ('no-box', 0, None)
    raw = m.group(1).rstrip('\n')
    lines = [l[2:] if l.startswith('  ') else l for l in raw.split('\n')]
    detail = [f'{len(boxes)}박스{boxes}']
    inserts = []
    single = len(boxes) == 1
    for i, b in enumerate(boxes):
        rng = box_range(page, REG, b, lines, single, idx=i, n=len(boxes))
        if rng is None:
            # all-or-nothing: 한 박스라도 매핑 실패 → 이 문제는 통째 스킵(부분마커=나머지 박스 유실 방지).
            #   마커 0 이므로 reconstruct 가 이 문제는 휴리스틱 폴백으로 렌더(전환기). 재추출(B) 때 결정적으로 채워짐.
            return ('partial-skip', 0, f'{detail[0]} | 박스{i} 매핑실패 → 전체 스킵')
        lo, hi = rng
        inserts.append((lo, f'{{{{BOX{i}_START}}}}'))        # 첫 내용 줄 '앞'
        inserts.append((hi + 1, f'{{{{BOX{i}_END}}}}'))       # 끝 내용 줄 '뒤'
        detail.append(f'박스{i}: 줄{lo}~{hi} START앞"{lines[lo][:18]}" END뒤"{lines[hi][:18]}"')
    for pos, marker in sorted(inserts, key=lambda x: -x[0]):   # 높은 인덱스부터(시프트 안 밀림)
        lines.insert(pos, marker)
    block_str = 'searchable_text: |\n' + '\n'.join('  ' + l for l in lines) + '\n'
    open(md, 'w', encoding='utf-8').write(txt[:m.start() + 1] + block_str + txt[m.end():])
    return ('OK', len(inserts) // 2, ' | '.join(detail))


def main():
    files = sorted(glob.glob(f'{REPO}/docs/problems/**/*.md', recursive=True))
    print(f'══ box_backfill 시작 {time.strftime("%F %T")} · {len(files)} md 스캔 · 대상=corrector_done · 읽기전용·LLM0', flush=True)
    stat = Counter(); markers = 0; t0 = time.time()
    for n, md in enumerate(files, 1):
        try:
            res, nb, detail = process(md)
        except Exception as e:
            res, nb, detail = ('exc', 0, repr(e))
        stat[res] += 1
        base = os.path.basename(md)[:-3]
        if res == 'OK':
            markers += nb
            print(f'[{n}/{len(files)}] ✅ {base} → {nb}박스 | {detail}', flush=True)
        elif res in ('partial-skip', 'no-pdf', 'no-region', 'name-parse-fail', 'exc', 'region-exc'):
            print(f'[{n}/{len(files)}] ⚠ {base} → {res}{": " + detail if detail else ""}', flush=True)
        # no-box / skip-already / skip-uncorrected / no-searchable 는 요약에만(노이즈 방지)
        if n % 100 == 0:
            print(f'  ··· {n}/{len(files)} {time.time()-t0:.0f}s · OK {stat["OK"]}({markers}박스) · {dict(stat)}', flush=True)
    print(f'══ 완료 {time.time()-t0:.0f}s · OK {stat["OK"]}({markers}박스 마커) · 전체 {dict(stat)}', flush=True)


if __name__ == '__main__':
    main()
