"""평가원 수능/모평 정답표 텍스트레이어 파싱 (좌표 기반).

비전 LLM 파싱(extract_answers)이 '공통+선택 3과목' 다중컬럼 정답표에서 자주
틀린다 (선택 3과목 칸에 같은 컬럼을 복사, 공통 누락 등 — 2027_6월모평 실측 10/46).
정답표 PDF에 텍스트 레이어가 있으면 좌표 기반으로 정확히(=46/46) 뽑는다.

표 구조: 각 데이터 행 = (문항번호, 정답, 배점) 묶음이 좌→우로 나열.
  · 공통 1~22  (보통 2개 서브컬럼: 1-11, 12-22)
  · 선택 23~30 × 3과목  (헤더 x순서로 과목 매핑)
정답: ①~⑤ → '1'~'5', 단답형은 숫자 문자열 그대로.

반환: {(subject, number): answer_str}.  subject ∈ {'공통','미적분','확률과통계','기하'}.
"""
import re
from collections import defaultdict

import fitz  # PyMuPDF

CIRCLED = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}
# 선택과목 헤더 needle → 정규 subject 명 (기존 데이터 표기와 일치)
_SUBJECT_HEADERS = [('미적분', '미적분'), ('기하', '기하'),
                    ('확률', '확률과통계'), ('통계', '확률과통계')]
_isint = lambda s: bool(re.fullmatch(r'\d+', s))


def has_text_layer(pdf_path, min_chars=80):
    """정답표에 의미있는 텍스트 레이어가 있는지(스캔본 아님)."""
    doc = fitz.open(pdf_path)
    return sum(len(p.get_text().strip()) for p in doc) >= min_chars


def parse_answer_table(pdf_path):
    """평가원 공통+선택 정답표를 {(subject, number): answer} 로 파싱."""
    page = fitz.open(pdf_path)[0]
    words = [(round(w[0], 1), round(w[1], 1), w[4].strip())
             for w in page.get_text("words") if w[4].strip()]

    # y(행) 기준 클러스터링
    rows = defaultdict(list)
    for x, y, t in words:
        key = next((k for k in rows if abs(k - y) <= 6), y)
        rows[key].append((x, t))

    # 데이터행(첫 셀이 1~30 정수) vs 헤더
    data, hdr = [], []
    for y in sorted(rows):
        cells = sorted(rows[y])
        if cells and _isint(cells[0][1]) and 1 <= int(cells[0][1]) <= 30 and len(cells) >= 3:
            data.append(cells)
        else:
            hdr += cells

    # 선택과목을 헤더 x순서대로 (좌→우)
    seen = {}
    for x, t in hdr:
        for needle, subj in _SUBJECT_HEADERS:
            if needle in t and subj not in seen:
                seen[subj] = x
    sel_order = [s for s, _ in sorted(seen.items(), key=lambda kv: kv[1])]

    ans = {}
    for cells in data:
        groups = [cells[i:i + 3] for i in range(0, len(cells) - (len(cells) % 3), 3)]
        si = 0  # 이 행에서 만난 선택 묶음 순번
        for g in groups:
            if len(g) < 3:
                break
            (_xn, n), (_xa, a), (_xs, _sc) = g
            if not _isint(n):
                continue
            n = int(n)
            answer = CIRCLED.get(a, a)
            if n <= 22:
                ans[('공통', n)] = answer
            else:
                subj = sel_order[si] if si < len(sel_order) else f'선택{si}'
                ans[(subj, n)] = answer
                si += 1
    return ans


def is_choice(answer_str):
    """정답이 객관식(①~⑤ 환산 '1'~'5')인지 단답형(그 외 숫자)인지."""
    return answer_str in ('1', '2', '3', '4', '5')


if __name__ == '__main__':
    import sys
    for k, v in sorted(parse_answer_table(sys.argv[1])):
        print(k, v)
