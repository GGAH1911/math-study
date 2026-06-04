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
    end_idx = len(clusters) - 1
    while end_idx > 0:
        gap = clusters[end_idx][0] - clusters[end_idx - 1][1]
        height = clusters[end_idx][1] - clusters[end_idx][0]
        if gap > big_gap and height < footer_max:
            end_idx -= 1
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
