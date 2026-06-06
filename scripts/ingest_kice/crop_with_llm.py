#!/usr/bin/env python3
"""Per-problem crop — pure-PIL row-ink scan (v3.1, no LLM).

Algorithm decides column rect + vertical hard upper bound (next anchor).
This module finds the true bottom of the problem inside that window by
scanning row-ink density and detecting the first "large enough" stretch
of blank rows — that's the gap between problem end and next problem (or
page footer). All thresholds are ratio-based so they're DPI/page-width
agnostic.

The previous LLM-based variant (`crop_with_llm`) is preserved at the
bottom of this file for reference/fallback but is no longer used by
the ingest pipeline.
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
import time
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
from ingest_round import claude_p  # noqa: E402


# ---------- v3.1: gap-based pure-PIL crop ---------------------------------

INK_PIXEL_THRESHOLD = 200      # grayscale value < this = ink-ish
BLANK_ROW_INK_RATIO = 0.005    # row counts as blank if <0.5% of width has ink
PADDING_RATIO = 0.015          # top/bottom visual padding = 1.5% of candidate height
MIN_PADDING_PX = 28            # but at least ~10pt @200dpi so short single-line
                               # 단답형 problems don't end up cramped
DETACHED_GAP_RATIO = 0.10      # ink cluster separated by >10% of candidate
                               # height from the previous cluster = "detached"
FOOTER_MAX_RATIO = 0.08        # a *trailing* detached block shorter than 8% of
                               # candidate height = footer/page-number/instruction
                               # → drop. BIGGER detached blocks (a graph/table
                               # followed by its 질문+보기) are real content and
                               # MUST be kept — dropping them cut the question.
LEFT_TRIM_THRESHOLD = 12       # diff>12 (gray) = ink for left-margin trim


def _row_ink_ratios(gray_img: Image.Image) -> list[float]:
    """For each row y in the grayscale image, return the fraction of
    pixels darker than INK_PIXEL_THRESHOLD. O(w*h) using Image.point()
    so it's fast enough for 1000×2000 candidates."""
    # Binarize: pixels < threshold → 1, else 0.
    binary = gray_img.point(lambda v: 1 if v < INK_PIXEL_THRESHOLD else 0, mode='L')
    w, h = binary.size
    # PIL doesn't expose row sums directly — use getdata + chunk
    data = list(binary.getdata())
    out: list[float] = []
    for y in range(h):
        row_sum = sum(data[y * w:(y + 1) * w])
        out.append(row_sum / w if w else 0.0)
    return out


def _find_problem_end(row_ink: list[float], h: int, gap_ratio: float = DETACHED_GAP_RATIO) -> int:
    """Walk rows top→bottom and return one past the last ACCEPTED ink row.

    The candidate's y_end is already capped at `next_anchor.y - 6pt` by
    bbox.py, but for the last problem in a column the cap is the page
    footer line and the candidate can still contain detached footer
    elements (page-number boxes that the per-page footer detector
    missed, KICE 수능 page-end "* 확인 사항" instruction boxes, etc).

    Strategy: group ink rows into clusters separated by blank rows, then
    peel off TRAILING clusters that are BOTH (a) detached by a gap larger
    than `gap_ratio * h` AND (b) small (< FOOTER_MAX_RATIO * h). Those are
    footer/page-number/thin-instruction blocks at the bottom.

    The old version broke at the *first* big gap and dropped everything
    below it — which destroyed problems where a graph/table is followed by
    its question + answer choices (the graph→question gap is big, but the
    question+choices below it is the real content). Peeling only *small*
    trailing blocks keeps that content while still dropping the footer.

    gap_ratio override: 검정고시는 candidate가 컴팩트해서 한 문제 안의
    빈 줄도 0.10 임계값을 넘을 수 있음 → 호출자가 더 큰 비율 전달.
    """
    big_gap = max(1, int(gap_ratio * h))
    footer_max = max(1, int(FOOTER_MAX_RATIO * h))
    # Build ink clusters [(start, end_exclusive), ...] in one pass.
    clusters: list[tuple[int, int]] = []
    cs = ce = -1
    for y in range(h):
        if row_ink[y] >= BLANK_ROW_INK_RATIO:
            if cs < 0:
                cs = y
            ce = y
        elif cs >= 0:
            clusters.append((cs, ce + 1))
            cs = -1
    if cs >= 0:
        clusters.append((cs, ce + 1))
    if not clusters:
        return h
    # Peel trailing *small detached* clusters (footer / page-number / instruction).
    # Stop at the first trailing block that is attached (small gap) or substantial
    # (a real graph→question+보기 block) — never drop real content.
    # 맨 아래에서부터 "큰 여백으로 떨어진 그룹" 단위로 푸터를 peel.
    # 푸터가 여러 줄(여러 클러스터)로 쪼개져 있어도 — 그 줄들 사이 여백은 작으니 —
    # 위로 큰 여백을 만날 때까지 한 그룹으로 묶은 뒤 그룹째 판정한다.
    # (기존엔 클러스터 1개씩 보다가 푸터 줄 사이 작은 여백에서 멈춰, 답안여백+'확인 사항'
    #  푸터를 통째 남겼다 — 단답 킬러가 세로로 길어진 원인.)
    end_idx = len(clusters) - 1
    while end_idx > 0:
        grp_start = end_idx
        while grp_start > 0 and (clusters[grp_start][0] - clusters[grp_start - 1][1]) <= big_gap:
            grp_start -= 1
        if grp_start == 0:
            break  # 위에 큰 여백 없음 = 본문 → 보존
        gap = clusters[grp_start][0] - clusters[grp_start - 1][1]
        content_h = clusters[grp_start - 1][1] - clusters[0][0]   # 이 여백 위쪽 본문 전체 높이
        ink = sum(clusters[j][1] - clusters[j][0] for j in range(grp_start, end_idx + 1))
        # 푸터 그룹째 제거 조건 (둘 다):
        #  (a) 앞 여백 > 그 위 본문 전체 높이 → 답안여백이 본문을 압도(단답 킬러 크롭실패).
        #  (b) 그룹 잉크 < footer_max → 페이지번호·'확인 사항' 류.
        # 디스플레이 수식 뒤 짧은 질문줄("…구하시오 [4점]")은 여백이 본문보다 작아 보존된다.
        if gap > content_h and ink < footer_max:
            end_idx = grp_start - 1
        else:
            break
    return clusters[end_idx][1]


def _find_problem_start(row_ink: list[float], h: int) -> int:
    """First non-blank row (where the "N." anchor sits)."""
    for y in range(h):
        if row_ink[y] >= BLANK_ROW_INK_RATIO:
            return y
    return 0


def _left_trim_x(cropped: Image.Image) -> int:
    """Return the leftmost x containing ink so we can crop off the wide
    white left margin of the column rect. -12px breathing room baked in."""
    gray = cropped.convert('L')
    bg = Image.new('L', gray.size, 255)
    diff = ImageChops.difference(gray, bg)
    diff = diff.point(lambda v: 255 if v > LEFT_TRIM_THRESHOLD else 0)
    bbox = diff.getbbox()
    if not bbox:
        return 0
    return max(0, bbox[0] - 12)


def crop_by_gap(candidate_png: Path, output_path: Path, exam_type: str | None = None) -> bool:
    """Crop a column-rect candidate to its true vertical extent using
    row-ink gap detection. Returns True on success (always — no LLM,
    no failure mode beyond IO).

    exam_type 힌트: 검정고시는 한 문제가 1줄 본문 + 1줄 선택지 처럼
    매우 컴팩트하다. candidate 자체가 짧고 (~300px) 본문/선택지 사이
    빈 줄이 기본 DETACHED_GAP_RATIO=0.10 을 넘으면 선택지 cluster가
    'detached footer'로 오인돼 잘려나간다 → 검정고시는 gap_ratio를
    크게 잡아 candidate 전체 ink 영역을 한 문제로 본다.
    """
    img = Image.open(candidate_png)
    w, h = img.size
    if w < 4 or h < 4:
        return False
    gray = img.convert('L')
    row_ink = _row_ink_ratios(gray)
    start_y = _find_problem_start(row_ink, h)
    gap_ratio = 0.25 if exam_type == '검정고시' else DETACHED_GAP_RATIO
    end_y = _find_problem_end(row_ink, h, gap_ratio=gap_ratio)
    pad = max(MIN_PADDING_PX, int(PADDING_RATIO * h))
    start_y = max(0, start_y - pad)
    end_y = min(h, end_y + pad)
    if end_y - start_y < 4:
        # Degenerate (mostly blank candidate) — save as-is so the caller
        # can still see something instead of crashing.
        end_y = h
        start_y = 0
    cropped = img.crop((0, start_y, w, end_y))
    # Left-margin trim — column rect starts at page left edge.
    x0 = _left_trim_x(cropped)
    if x0 > 0:
        cropped = cropped.crop((x0, 0, cropped.width, cropped.height))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(output_path, 'PNG', optimize=True)
    return True


def crop_problem(page_img, bbox_px, out_path, exam_type=None, headroom=18):
    """문제 크롭 (인제스트·재크롭 공용). crop_by_gap 의 top/bottom 경계 + **위로 headroom 픽셀**.

    crop_by_gap 은 후보(=bbox crop) 안만 봐서 bbox 가 위첨자를 자르면 못 살린다. 여기선 페이지+bbox 를
    받아 *원래 경계에서 위로 headroom* 만큼 페이지에서 다시 잘라 위첨자 클립을 복구한다(스캔 없음 →
    멀리 있는 헤더는 안 딸려옴). 안 잘린 문제엔 상단 여백만 더해진다."""
    from pathlib import Path as _P
    out_path = _P(out_path)
    x0, y0, x1, y1 = [int(v) for v in bbox_px]
    cand = page_img.crop((x0, y0, x1, y1))
    if cand.width < 4 or cand.height < 4:
        return False
    ri = _row_ink_ratios(cand.convert('L'))
    h = cand.height
    gr = 0.25 if exam_type == '검정고시' else DETACHED_GAP_RATIO
    pad = max(MIN_PADDING_PX, int(PADDING_RATIO * h))
    orig_top = max(0, _find_problem_start(ri, h) - pad)
    orig_bot = min(h, _find_problem_end(ri, h, gap_ratio=gr) + pad)
    page_top = max(0, y0 + orig_top - headroom)             # 원래 top 에서 위로 headroom
    # (키 큰 분수·지수가 bbox 위로 솟어 잘리는 문제는 bbox.py 의 extract_problem_bboxes 가
    #  span 클러스터로 y0 를 이미 올바르게 잡으므로 여기선 추가 스캔 불필요.)
    # 전체폭 룰(헤더/풋터 구분선) 가로지르기 방지: headroom 이 위로 가다 컬럼을 가득 채우는
    # 가로선(ink>0.7; 문제 안 박스·표는 좁아 해당 X)을 만나면 그 아래로 클램프해 헤더 차단.
    # band 를 y0 보다 약간 아래(LOOK)까지 봐서 룰이 bbox top 바로 밑에 걸쳐도 잡는다.
    LOOK = 10
    band_bot = min(y0 + LOOK, y0 + orig_bot)
    if 0 < page_top < band_bot:
        bi = _row_ink_ratios(page_img.crop((x0, page_top, x1, band_bot)).convert('L'))
        rule_rows = [r for r, v in enumerate(bi) if v > 0.70]
        if rule_rows:
            page_top = page_top + max(rule_rows) + 1         # 가장 아래 룰 바로 밑
    cropped = page_img.crop((x0, page_top, x1, y0 + orig_bot))
    xt = _left_trim_x(cropped)
    if xt > 0:
        cropped = cropped.crop((xt, 0, cropped.width, cropped.height))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(out_path, 'PNG', optimize=True)
    return True


# ---------- legacy: LLM-guided crop (unused as of v3.1) -------------------


CROP_SYSTEM = """너는 한국 수능 시험지 이미지에서 한 문제의 끝 위치를 정확히 찾는 도구다.

이미지는 한 문제의 후보 영역이다 — 문제 번호로 시작해서 다음 문제 직전까지 (또는 페이지 하단까지). 영역 안에는:
- 문제 본문 (글)
- 그림/도형 (있을 수도)
- 보기 (①②③④⑤ 또는 단답형이면 없음)
- 그 다음엔 빈 공간

너의 임무: 이미지를 Read 툴로 열고, **본문 + 보기 + 그림이 진짜 끝나는 세로 위치**를 0.0~1.0 사이 y_ratio로 답하라.

- y_ratio = 1.0 → 이미지 맨 아래
- y_ratio = 0.5 → 중간
- 보기가 한 줄에 ①②③④⑤ 다 있으면 그 줄 아래 약간까지 포함
- 그림이 보기보다 아래로 내려가면 그림 끝까지 포함

오직 JSON 한 줄로 답하라: {"y_ratio": 0.42}
"""


def _sha1_of_file(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:12]


def llm_find_end_ratio(image_path: Path, cache_dir: Path | None = None,
                      cache_key: str | None = None,
                      timeout: int = 60) -> float | None:
    """Send a column-cropped image to Sonnet, get back a single y_ratio.
    Cached by image sha1 + cache_key. Returns None on failure."""
    sha = _sha1_of_file(image_path)
    cache_file = None
    if cache_dir and cache_key:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f'{cache_key}.json'
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text(encoding='utf-8'))
                if data.get('sha') == sha and isinstance(data.get('y_ratio'), (int, float)):
                    return float(data['y_ratio'])
            except Exception:
                pass

    abs_path = image_path.absolute()
    user = f"""이미지: {abs_path}

위 시스템 프롬프트대로 y_ratio JSON을 출력하라."""
    add_dir = str(abs_path.parent)

    last_err = None
    for attempt in range(3):
        out = claude_p(CROP_SYSTEM, user, model='sonnet', max_turns=2,
                       add_dir=add_dir, timeout=timeout, retries=1)
        if not out:
            last_err = 'empty'
            continue
        out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
        m = re.search(r'\{[^{}]*?"y_ratio"[^{}]*?\}', out, re.DOTALL)
        if not m:
            last_err = f'no JSON in: {out[:120]!r}'
            continue
        try:
            data = json.loads(m.group(0))
            y = float(data.get('y_ratio'))
        except Exception as e:
            last_err = f'parse {e}'
            continue
        # clamp
        y = max(0.05, min(1.0, y))
        if cache_file:
            try:
                cache_file.write_text(json.dumps({'sha': sha, 'y_ratio': y}), encoding='utf-8')
            except Exception:
                pass
        return y
    print(f'  ! crop_llm gave up for {image_path.name}: {last_err}', flush=True)
    return None


def crop_with_llm(candidate_png: Path, output_path: Path,
                  cache_dir: Path | None = None,
                  cache_key: str | None = None,
                  pad_px: int = 12) -> bool:
    """Given a candidate column-cropped PNG (anchor → hard_end), ask the
    LLM where to truncate vertically, then PIL crop. Output overwrites
    output_path. Returns True if cropped, False if LLM failed (in which
    case caller can fall back to the candidate as-is)."""
    from PIL import ImageChops, Image as PILImage
    y_ratio = llm_find_end_ratio(candidate_png, cache_dir=cache_dir,
                                  cache_key=cache_key)
    if y_ratio is None:
        return False
    img = Image.open(candidate_png)
    w, h = img.size
    y_end = min(h, int(h * y_ratio) + pad_px)
    cropped = img.crop((0, 0, w, y_end))

    # Left-side ink trim — the column rect starts at the page edge so the
    # left ~80px is always white margin. Detect the leftmost ink column
    # and crop to it (with a small padding). We trim left-only because
    # the right side may extend into the column separator area, which
    # PIL would otherwise misread as ink.
    gray = cropped.convert('L')
    bg = PILImage.new('L', gray.size, 255)
    diff = ImageChops.difference(gray, bg)
    diff = diff.point(lambda v: 255 if v > 12 else 0)
    ink_bbox = diff.getbbox()
    if ink_bbox:
        ix0 = max(0, ink_bbox[0] - 12)
        cropped = cropped.crop((ix0, 0, cropped.width, cropped.height))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(output_path, 'PNG', optimize=True)
    return True


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('input_png')
    ap.add_argument('output_png')
    args = ap.parse_args()
    ok = crop_with_llm(Path(args.input_png), Path(args.output_png))
    print('OK' if ok else 'FAIL')
