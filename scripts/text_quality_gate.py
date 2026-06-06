#!/usr/bin/env python3
"""텍스트 품질 게이트 — 인제스트 시 searchable_text 글리프 손상 자동 감지·재전사.

손상 신호(치환문자 □◇�·전사실패 마커·빈값) 감지 → 이미지서 충실 재전사(regen_one) → 재검.
재전사로도 안 고쳐지면 플래그(무손상, 로그만 — 검증/정답/솔버는 안 건드림).
인제스트가 build_solution_cache 빌드 *전*에 호출해 깨끗한 텍스트로 캐시·코퍼스를 보장한다.
솔버 파이프라인의 하드코딩 게이트(accept_verifier)에 대응하는 '텍스트 게이트'.

사용:
  python text_quality_gate.py --list slug1,slug2   # 인제스트 직후(특정 회차)
  python text_quality_gate.py --all                # 전체 코퍼스 일괄 청소(기존 손상분)
  REGEN_MODEL/REGEN_TO/REGEN_WORKERS 환경변수는 regenerate_searchable 와 공유.
"""
from __future__ import annotations
import re, sys, glob, argparse
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import regenerate_searchable as R   # noqa: E402  regen_one(이미지=정답 충실 전사) 재사용

SEARCH = re.compile(r'^searchable_text:\s*[|>][-+]?\s*\n(.*?)(?=^\S|\Z)', re.M | re.S)
# 인코딩/폰트 깨짐 치환문자
REPLACE_CHARS = re.compile(r'[⋄�□◇▢◻╳]')
# 전사 실패 시 LLM/폴백이 남기는 마커 (정상 수학 본문엔 거의 안 나옴 → 고정밀)
MARKERS = re.compile(r'손상|불명확|글리프|복원 ?불가|판독 ?불가|확인 ?불가|해석 ?불가|'
                     r'수식 없음|텍스트 없음|\[수식|\[내용|\[조건식|PDF.{0,6}오류')
# 마커 없이 '조용히 틀린' 전사: sin/cos 절댓값이 1 초과 = 수학적으로 불가능 = OCR 버그
TRIG_IMPOSSIBLE = re.compile(r'\b(sin|cos)\b[^=\n]{0,18}=\s*([+-]?\d+(?:\.\d+)?)')


def extract(t: str) -> str:
    m = SEARCH.search(t)
    return m.group(1).strip() if m else ''


def is_corrupted(text: str) -> tuple[bool, str]:
    """손상 여부 + 사유. 고정밀 신호만 사용(오탐 시 멀쩡한 텍스트를 재전사 = 비용·품질손해)."""
    if not text or len(text) < 10:
        return True, 'empty'
    if REPLACE_CHARS.search(text):
        return True, 'replace-char'
    if MARKERS.search(text):
        return True, 'marker'
    for fn, val in TRIG_IMPOSSIBLE.findall(text):    # 불가능값(조용한 손상)
        try:
            if abs(float(val)) > 1.0001:
                return True, f'impossible-{fn}={val}'
        except ValueError:
            pass
    return False, ''


def gate_one(md_path: Path) -> dict:
    text = extract(md_path.read_text(encoding='utf-8'))
    bad, reason = is_corrupted(text)
    if not bad:
        return dict(stem=md_path.stem, action='clean', ok=True, reason='', cost=0.0)
    # 손상 → 이미지서 충실 재전사 (정답·검증기·솔버는 이미지 파생이라 안 건드림)
    res = R.regen_one((md_path, md_path.stem))
    cost = res.get('cost', 0.0) or 0.0
    if not res.get('ok'):
        return dict(stem=md_path.stem, action='flagged', ok=False,
                    reason=f'{reason}; regen:{res.get("err")}', cost=cost)
    bad2, reason2 = is_corrupted(extract(md_path.read_text(encoding='utf-8')))
    if bad2:
        return dict(stem=md_path.stem, action='flagged', ok=False, reason=f'still:{reason2}', cost=cost)
    return dict(stem=md_path.stem, action='regenerated', ok=True, reason=reason, cost=cost)


def run_gate(slugs: list[str], workers: int = 4) -> list[dict]:
    paths = []
    for s in slugs:
        hits = glob.glob(str(ROOT / 'docs' / 'problems' / '**' / f'{s}.md'), recursive=True)
        if hits:
            paths.append(Path(hits[0]))
    res = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fut in as_completed({ex.submit(gate_one, p): p for p in paths}):
            r = fut.result()
            res.append(r)
            if r['action'] != 'clean':
                mark = {'regenerated': '✅재전사', 'flagged': '⚠플래그'}.get(r['action'], '?')
                print(f"  {mark} {r['stem']} ({r['reason']}) ${r['cost']:.3f}", flush=True)
    c = Counter(r['action'] for r in res)
    tot = sum(r['cost'] for r in res)
    print(f"  텍스트게이트: clean {c['clean']} · 재전사 {c['regenerated']} · 플래그 {c['flagged']} · ${tot:.2f}",
          flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', help='쉼표구분 slug (인제스트 직후 회차)')
    ap.add_argument('--all', action='store_true', help='전체 코퍼스 일괄')
    ap.add_argument('--workers', type=int, default=int(R.WORKERS))
    a = ap.parse_args()
    if a.all:
        slugs = [Path(f).stem for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)
                 if 'README' not in f]
    elif a.list:
        slugs = [s.strip() for s in a.list.split(',') if s.strip()]
    else:
        print('--list 또는 --all 필요', flush=True)
        return
    print(f"═══ 텍스트 품질 게이트 — {len(slugs)}개 검사 ═══", flush=True)
    run_gate(slugs, a.workers)


if __name__ == '__main__':
    main()
