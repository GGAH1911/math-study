#!/usr/bin/env python3
"""DeepSeek-OCR HTTP client + format conversion to our markdown convention.

The server (docs/tools/deepseek_ocr_api.md) returns:
  - text:    LaTeX `\\(...\\)` inline + `\\[...\\]` display, problem headers like "27."
  - regions: [{ref, bbox_pixels, crop_b64}] for figures/text/equation
We convert to our internal convention:
  - `## N번 [X점]` problem headers (X점 inferred from "[X점]" pattern if present, else default 3점)
  - KaTeX `$...$` inline, `$$...$$` display
  - `# 영역: <name>` if subject detected
  - `<img src="../figures/p<N>_<i>.png" alt="figure">` for each figure region
"""
from __future__ import annotations
import base64
import os
import re
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

OCR_URL = os.environ.get('OCR_API_URL', 'https://macbook-pro.tailf47aa4.ts.net')
OCR_KEY = os.environ.get('OCR_API_KEY', '')
SSH_HOST = os.environ.get('OCR_SSH_HOST', 'macbook-pro.tailf47aa4.ts.net')
TIMEOUT = 60       # per-call cap; fail fast → faster runner kill on hang
UNLOAD_EVERY = 20  # proactive: runner drifts well before 30 calls in practice
SLOW_THRESHOLD = 30.0  # seconds — anything past this is a sign of runner drift

_call_counter = 0
_consecutive_slow = 0
_consecutive_fail = 0  # 연속 failure (timeout/non-200) — 2회 시 runner kill


def is_healthy() -> bool:
    try:
        r = httpx.get(f'{OCR_URL}/health', timeout=10)
        d = r.json()
        return d.get('status') == 'ok' and d.get('ollama_reachable') is True
    except Exception:
        return False


def _hard_restart_runner() -> None:
    """SSH into the OCR host and FULLY restart ollama (serve + runner).

    Killing only the runner isn't enough when ollama 0.24's serve process
    itself enters a stuck state — the freshly-spawned runner inherits the
    broken sched/queue and the next /api/generate also hangs. Killing
    both processes and restarting `ollama serve` gives a clean slate
    (~8-10s downtime before /health responds again)."""
    import subprocess, time as _t
    try:
        cmd = ('pkill -9 -f "ollama" 2>/dev/null; sleep 3; '
               'nohup /opt/homebrew/bin/ollama serve > /tmp/ollama_$(date +%H%M%S).log 2>&1 & disown; '
               'sleep 5; echo restarted')
        subprocess.run(
            ['ssh', '-o', 'ConnectTimeout=5', '-o', 'BatchMode=yes', SSH_HOST, cmd],
            timeout=30, check=False, capture_output=True,
        )
        # Poll health until ready (max ~15s)
        for _ in range(15):
            try:
                r = httpx.get(f'{OCR_URL}/health', timeout=3)
                if r.status_code == 200 and r.json().get('ollama_reachable'):
                    print(f'  [ocr] hard-restarted ollama (serve+runner) via SSH', flush=True)
                    return
            except Exception:
                pass
            _t.sleep(1)
        print(f'  [ocr] ollama restart sent but health not confirmed within 15s', flush=True)
    except Exception as e:
        print(f'  [ocr] ollama full-restart failed: {e}', flush=True)


def _maybe_unload() -> None:
    """Periodically force ollama to drop the model from GPU so the next call
    cold-loads fresh. Empirically, ollama 0.24's runner slows from 5s/page to
    80-200s/page after ~100 sustained requests; the cost of one cold reload
    (~10s) beats waiting through a hang. Called from ocr_page_raw."""
    global _call_counter
    _call_counter += 1
    if _call_counter % UNLOAD_EVERY != 0:
        return
    if not OCR_KEY:
        return
    try:
        httpx.post(
            f'{OCR_URL}/admin/unload',
            headers={'Authorization': f'Bearer {OCR_KEY}'},
            timeout=15,
        )
        print(f'  [ocr] unloaded model after {_call_counter} calls', flush=True)
    except Exception as e:
        print(f'  [ocr] unload failed: {e}', flush=True)


def ocr_page_raw(image_path: Path, include_crops: bool = True) -> dict[str, Any] | None:
    """Call DeepSeek-OCR /ocr endpoint. Returns parsed JSON or None on failure."""
    global _consecutive_slow, _consecutive_fail
    if not OCR_KEY:
        return None
    import time as _t
    t0 = _t.time()
    try:
        with open(image_path, 'rb') as f:
            r = httpx.post(
                f'{OCR_URL}/ocr',
                headers={'Authorization': f'Bearer {OCR_KEY}'},
                files={'file': (image_path.name, f, 'image/png')},
                data={'mode': 'markdown', 'include_crops': str(include_crops).lower()},
                timeout=TIMEOUT,
            )
        elapsed = _t.time() - t0
        if r.status_code != 200:
            _consecutive_fail += 1
            print(f'  [ocr] non-200 ({r.status_code}) — consecutive fail: {_consecutive_fail}', flush=True)
            if _consecutive_fail >= 2:
                _hard_restart_runner()
                _consecutive_fail = 0
            return None
        _consecutive_fail = 0
        if elapsed > SLOW_THRESHOLD:
            _consecutive_slow += 1
            print(f'  [ocr] slow call: {elapsed:.1f}s (consecutive: {_consecutive_slow})', flush=True)
            if _consecutive_slow >= 2:
                print(f'  [ocr] forcing unload after {_consecutive_slow} slow calls', flush=True)
                try:
                    httpx.post(f'{OCR_URL}/admin/unload',
                               headers={'Authorization': f'Bearer {OCR_KEY}'}, timeout=15)
                except Exception:
                    pass
                _consecutive_slow = 0
        else:
            _consecutive_slow = 0
        _maybe_unload()
        return r.json()
    except Exception as e:
        _consecutive_fail += 1
        print(f'  [ocr] exception: {type(e).__name__} (consecutive fail: {_consecutive_fail})', flush=True)
        if _consecutive_fail >= 2:
            _hard_restart_runner()
            _consecutive_fail = 0
        return None


def detect_area(text: str) -> str | None:
    """Detect 영역 (공통/확률과통계/미적분/기하) from page text.

    Page footers include the next-page advisory
    "선택과목(미적분) 문제가 제시되오니..." which would otherwise be
    matched as the current page's area. Strip lines containing those
    advisory phrases before classifying."""
    filtered_lines = []
    for line in text.split('\n'):
        if re.search(r'선\s*택\s*과\s*목|다음\s*[은이]?\s*[「\[\(].*?[\]\)\]]?\s*문제|이어서', line):
            continue
        filtered_lines.append(line)
    t = '\n'.join(filtered_lines)
    if '확률과 통계' in t or '확률과통계' in t:
        return '확률과통계'
    if '미적분' in t:
        return '미적분'
    if '기하' in t and '도형' not in t[:200]:
        return '기하'
    if '수학 영역' in t or '수학영역' in t or '공통' in t[:300]:
        return '공통'
    return None


# Pattern: line starting with "N." where N is 1-50 (problem header).
# We also capture optional "[X점]" suffix.
PROBLEM_HEADER_RE = re.compile(r'(?:^|\n)\s*(\d{1,2})\.\s+(.*?)(?=(?:\n\s*\d{1,2}\.\s)|\Z)', re.DOTALL)
SCORE_RE = re.compile(r'\[(\d)\s*점\]')


def _canonical_numbers_for_page(pdf_path: Path | None, page_num: int | None) -> list[int]:
    """Sorted list of canonical problem numbers on this PDF page, from text layer."""
    if not pdf_path or page_num is None:
        return []
    try:
        import fitz
        d = fitz.open(pdf_path)
        if page_num - 1 >= len(d):
            d.close()
            return []
        t = d[page_num - 1].get_text()
        d.close()
    except Exception:
        return []
    nums: set[int] = set()
    for m in re.finditer(r'(?:^|\n)\s*(\d{1,2})\.\s', t):
        n = int(m.group(1))
        if 1 <= n <= 50:
            nums.add(n)
    return sorted(nums)


_AREA_TOKENS = [
    ('확률과통계', re.compile(r'\(\s*확\s*률\s*과?\s*통\s*계\s*\)')),
    ('미적분', re.compile(r'\(\s*미\s*적\s*분\s*\)')),
    ('기하', re.compile(r'\(\s*기\s*하\s*\)')),
]


def _canonical_area_for_page(pdf_path: Path | None, page_num: int | None) -> str | None:
    """KICE 수능/모평 문제지 페이지 헤더는 '(확률과 통계)' / '(미적분)' / '(기하)'
    형태로 PDF text-layer에 보존된다. 페이지 상단(첫 300자) 안에 매칭되면
    그 영역을 반환. 매칭 없으면 None (공통 페이지 또는 비-수능 PDF)."""
    if not pdf_path or page_num is None:
        return None
    try:
        import fitz
        d = fitz.open(pdf_path)
        if page_num - 1 >= len(d):
            d.close()
            return None
        head = d[page_num - 1].get_text()[:300]
        d.close()
    except Exception:
        return None
    for area, pat in _AREA_TOKENS:
        if pat.search(head):
            return area
    return None


def convert_to_lwip_markdown(
    ocr_text: str,
    figure_links: dict[int, list[str]] | None = None,
    canonical_numbers: list[int] | None = None,
    canonical_area: str | None = None,
) -> str:
    """Transform DeepSeek-OCR text into LWIP convention:
      - ## N번 [X점] headers (realigned to canonical PDF numbers when available)
      - $...$ inline math, $$...$$ display
      - <img src> embeds for figures (keyed by canonical problem number)

    If canonical_area is provided (from PDF text-layer header like
    '(확률과 통계)'), it overrides OCR-based area detection. This prevents
    bleed from footer text like "선택과목(미적분)" that appears at the
    bottom of every 확률과통계 last-page.
    """
    area = canonical_area or detect_area(ocr_text)
    out: list[str] = []
    if area:
        out.append(f'# 영역: {area}')
        out.append('')

    # Strip license/footer text
    body = re.sub(r'\n*이\s*문제지에\s*관한\s*저작권은[^\n]*', '', ocr_text)
    # LaTeX delimiter conversion: \(...\) → $...$  /  \[...\] → $$...$$
    body = re.sub(r'\\\(\s*', '$', body)
    body = re.sub(r'\s*\\\)', '$', body)
    body = re.sub(r'\\\[\s*', '$$', body)
    body = re.sub(r'\s*\\\]', '$$', body)
    # Some OCR variants use \( ... \) on multi-line with whitespace before
    # → already handled by the above.

    # Split into problem chunks by header pattern
    matches = list(PROBLEM_HEADER_RE.finditer(body))
    if not matches:
        # No structured headers; return body as-is (under area header if any)
        out.append(body.strip())
        return '\n'.join(out)

    figure_links = figure_links or {}
    # If canonical numbers from PDF text are available AND count matches the
    # OCR-detected count, realign by position (1st OCR header → 1st canonical, ...).
    ocr_nums = [int(m.group(1)) for m in matches]
    use_canonical = (canonical_numbers
                     and len(canonical_numbers) == len(matches)
                     and ocr_nums != canonical_numbers)
    for i, m in enumerate(matches):
        ocr_num = int(m.group(1))
        if not (1 <= ocr_num <= 50):
            continue
        num = canonical_numbers[i] if use_canonical else ocr_num
        chunk = m.group(2).strip()
        score_match = SCORE_RE.search(chunk)
        score = score_match.group(1) if score_match else '3'
        out.append(f'## {num}번 [{score}점]')
        out.append('')
        out.append(chunk)
        for fp in figure_links.get(num, []):
            out.append('')
            out.append(f'<img src="{fp}" alt="figure {num}">')
        out.append('')
        out.append('---')
        out.append('')

    return '\n'.join(out)


def save_figure_crops(
    result: dict, page_num: int, figures_dir: Path,
) -> list[tuple[list[int], str]]:
    """Persist each figure/image crop to disk. Returns [(bbox_pixels, relative_path)]."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    saved: list[tuple[list[int], str]] = []
    for i, reg in enumerate(result.get('regions', [])):
        if reg.get('ref') not in ('figure', 'image'):
            continue
        b64 = reg.get('crop_b64')
        if not b64:
            continue
        fname = f'p{page_num:02d}_fig{i:02d}.png'
        path = figures_dir / fname
        try:
            path.write_bytes(base64.b64decode(b64))
            # Relative path used in markdown
            saved.append((reg.get('bbox_pixels') or [0, 0, 0, 0], f'../figures/{fname}'))
        except Exception:
            continue
    return saved


def _problem_header_positions_from_pdf(
    pdf_path: Path, page_num: int, image_height_px: int
) -> list[tuple[int, float]]:
    """Use PyMuPDF text-layer to find (problem_number, y_pixel) for each
    `N.` problem header on the given page. y is scaled to the OCR image's
    pixel height (since PDF coords are in points, image is in pixels)."""
    try:
        import fitz  # local import to avoid hard dep on callers that don't need it
        d = fitz.open(pdf_path)
        if page_num - 1 >= len(d):
            d.close()
            return []
        p = d[page_num - 1]
        page_h = p.rect.height
        td = p.get_text("dict")
        d.close()
    except Exception:
        return []
    positions: list[tuple[int, float]] = []
    for block in td.get('blocks', []):
        if block.get('type') != 0:
            continue
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                txt = span.get('text', '').strip()
                # Match standalone "N." problem header
                m = re.match(r'^(\d{1,2})\.\s*$', txt)
                if not m:
                    m = re.match(r'^(\d{1,2})\.\s', txt)
                if not m:
                    continue
                try:
                    n = int(m.group(1))
                except ValueError:
                    continue
                if not (1 <= n <= 50):
                    continue
                y_pdf = span['bbox'][1]
                y_px = (y_pdf / page_h) * image_height_px if page_h else 0
                positions.append((n, y_px))
    # Dedup: keep the FIRST y per problem number (header is the topmost occurrence)
    seen = {}
    for n, y in sorted(positions, key=lambda kv: kv[1]):
        if n not in seen:
            seen[n] = y
    return sorted(seen.items(), key=lambda kv: kv[1])


def attach_figures_to_problems(
    ocr_result: dict,
    saved_figures: list[tuple[list[int], str]],
    pdf_path: Path | None = None,
    page_num: int | None = None,
) -> dict[int, list[str]]:
    """Match each figure crop to the nearest problem header above it,
    using PDF text-layer to anchor problem header y-coordinates."""
    out: dict[int, list[str]] = {}
    if not saved_figures:
        return out
    text = ocr_result.get('text', '')
    image_h = (ocr_result.get('image_size') or [0, 0])[1]

    anchors: list[tuple[int, float]] = []
    if pdf_path and page_num is not None and image_h:
        anchors = _problem_header_positions_from_pdf(pdf_path, page_num, image_h)
    # Fallback if PDF text-layer didn't give us anchors: use ordered numbers
    # from OCR text and distribute figures roughly by index.
    if not anchors:
        nums_in_text = [int(m.group(1)) for m in PROBLEM_HEADER_RE.finditer(text)
                        if 1 <= int(m.group(1)) <= 50]
        if not nums_in_text:
            return out
        # Distribute figures evenly across detected problems
        per = max(1, len(saved_figures) // len(nums_in_text) + (1 if len(saved_figures) % len(nums_in_text) else 0))
        for i, (_, path) in enumerate(saved_figures):
            idx = min(i // per, len(nums_in_text) - 1)
            out.setdefault(nums_in_text[idx], []).append(path)
        return out

    # Anchored: for each figure (use its top-y), find the problem whose
    # anchor y is the largest one ≤ figure_y (i.e., immediately above).
    for bbox_px, path in saved_figures:
        if not bbox_px or len(bbox_px) != 4:
            continue
        fig_top_y = bbox_px[1]
        # Find the anchor with largest y still ≤ fig_top_y
        candidate = anchors[0][0]  # default: first problem
        for n, y in anchors:
            if y <= fig_top_y:
                candidate = n
            else:
                break
        out.setdefault(candidate, []).append(path)
    return out


def _split_into_columns(image_path: Path) -> tuple[Path, Path] | None:
    """Split a 2-column exam page into left + right halves.
    Returns (left_path, right_path) of temp PNGs, or None on failure.
    Adds 5% overlap on the centerline to avoid clipping problems that straddle.
    """
    try:
        from PIL import Image
        img = Image.open(image_path)
        w, h = img.size
        overlap = w // 20  # 5% overlap on each side of the centerline
        left = img.crop((0, 0, w // 2 + overlap, h))
        right = img.crop((w // 2 - overlap, 0, w, h))
        lp = image_path.parent / f'_split_{image_path.stem}_L.png'
        rp = image_path.parent / f'_split_{image_path.stem}_R.png'
        left.save(lp)
        right.save(rp)
        return lp, rp
    except Exception:
        return None


def ocr_page_to_markdown(image_path: Path, figures_dir: Path | None = None,
                        page_num: int | None = None,
                        pdf_path: Path | None = None) -> str | None:
    """End-to-end: OCR a PNG page → LWIP-format markdown with figure embeds.

    Strategy:
      1. Full-page OCR first (cheap — single call per page).
      2. If detected `## ` count < PDF-text canonical count, retry with L/R column split.
      `split_problems` will dedup any overlap from split.
    """
    canonical = _canonical_numbers_for_page(pdf_path, page_num)
    canonical_area = _canonical_area_for_page(pdf_path, page_num)
    expected = len(canonical) if canonical else 0

    def _save_and_attach(sub_result: dict) -> dict[int, list[str]]:
        if not (sub_result and figures_dir and page_num is not None):
            return {}
        saved = save_figure_crops(sub_result, page_num, figures_dir)
        return attach_figures_to_problems(sub_result, saved, pdf_path=pdf_path, page_num=page_num)

    # 1) Full-page pass
    full = ocr_page_raw(image_path, include_crops=bool(figures_dir))
    text = full.get('text', '') if full else ''
    figure_links: dict[int, list[str]] = _save_and_attach(full or {})
    detected = len(re.findall(r'(?:^|\n)\s*(\d{1,2})\.\s', text))

    # 2) L/R split fallback if under-detected
    if expected > 0 and detected < expected:
        print(f'  [page {page_num}] full-pass {detected}/{expected} → L/R split', flush=True)
        split = _split_into_columns(image_path)
        if split:
            left_path, right_path = split
            combined = text
            for sub_path in (left_path, right_path):
                sub = ocr_page_raw(sub_path, include_crops=bool(figures_dir))
                if sub and sub.get('text'):
                    combined += '\n\n' + sub['text']
                for k, v in _save_and_attach(sub or {}).items():
                    for fp in v:
                        if fp not in figure_links.get(k, []):
                            figure_links.setdefault(k, []).append(fp)
            try:
                left_path.unlink()
                right_path.unlink()
            except Exception:
                pass
            text = combined

    if not text:
        return None
    return convert_to_lwip_markdown(text, figure_links, canonical_numbers=canonical,
                                    canonical_area=canonical_area)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: ocr_client.py <page.png>')
        sys.exit(1)
    p = Path(sys.argv[1])
    print(ocr_page_to_markdown(p))
