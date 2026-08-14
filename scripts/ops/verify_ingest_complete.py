#!/usr/bin/env python3
"""인제스트 완결성 게이트 — 회차가 **모든 단계를 다 탔는지** 기계가 판정한다.

★왜 생겼나 (2026-08-14): `2026_고3_7월모의고사` 가 인제스트는 됐는데 **교정 단계를 통째로
  못 탄 채** 며칠을 지냈다. 사장님이 눈으로 보고서야 발견했다. 증상은 셋이었지만 원인은
  하나였고, 그 하나를 아무도 못 본 이유는 **"다 됐는지"를 확인하는 것이 없었기 때문**이다.

  당시 실제 상태: corrector_done 0/46 · figures 0 · {{BOX}} 0 · 도형 라벨 6건 본문 누출 ·
  killer_tier 7건 공백. 정상 회차는 corrector_done 100% 다 — **한 줄만 비교했어도 잡혔다.**

사용:
    python3 scripts/ops/verify_ingest_complete.py 2026_고3_7월모의고사
    python3 scripts/ops/verify_ingest_complete.py --all           # 전 회차
    python3 scripts/ops/verify_ingest_complete.py --all --quiet   # 실패한 회차만

exit 0 = 통과 / 1 = 실패(차단) / 2 = 경고만
"""
from __future__ import annotations
import argparse, os, re, sys
from pathlib import Path

ROOT = Path(os.environ.get('MATHSTUDY_ROOT') or Path(__file__).resolve().parent.parent.parent)
PROB = ROOT / 'docs' / 'problems'
MEDIA = ROOT / 'web' / 'private' / 'problem-images'   # ★public 아님(인증 게이팅 — lib/media-root.ts)

RE_ST = re.compile(r'^searchable_text: \|\n(.*?)(?=^\S)', re.M | re.S)
RE_TIER = re.compile(r'^killer_tier:([^\n]*)$', re.M)
RE_FIGS = re.compile(r'^figures:(.*?)(?=^\S)', re.M | re.S)
RE_IMG = re.compile(r'/problem-images/(\S+?\.(?:png|jpe?g))')
RE_SCORE = re.compile(r'^  score: (\d+)$', re.M)
RE_PTS = re.compile(r'\[(\d)점\]')
# 도형 라벨이 본문에 낱개로 남은 것(예: "C_{2}" / "M N" / "D B C" 만 있는 줄)
RE_LABEL = re.compile(r'^\s{0,4}[A-Za-z0-9_{}^\\\'′´]{1,4}(\s+[A-Za-z0-9_{}^\\\'′´]{1,4}){0,5}\s*$')


def round_dir(rd: str) -> Path | None:
    hits = [p for p in PROB.glob(f'*/{rd}') if p.is_dir()]
    return hits[0] if hits else None


def check(rd: str) -> tuple[list[str], list[str], int]:
    """(차단사유, 경고, 문제수)"""
    d = round_dir(rd)
    if d is None:
        return [f'회차 폴더 없음: {rd}'], [], 0
    mds = sorted(d.glob('*.md'))
    n = len(mds)
    if not n:
        return [f'{rd}: md 0건'], [], 0

    done = ok = 0
    empty_tier: list[str] = []
    empty_text: list[str] = []
    quarantined: list[str] = []
    missing_img: list[str] = []
    orphan_marker: list[str] = []
    leak: list[str] = []
    score_mismatch: list[str] = []

    for p in mds:
        t = p.read_text(encoding='utf-8', errors='replace')
        stem = p.stem
        if re.search(r'^corrector_done:', t, re.M):
            done += 1
        m = re.search(r'^corrector_verify:\s*(\S+)', t, re.M)
        if m and m.group(1).strip('"') == 'ok':
            ok += 1
        if 'corrector_quarantine' in t:
            quarantined.append(stem)

        mt = RE_TIER.search(t)
        if not (mt and mt.group(1).strip().strip('"')):
            empty_tier.append(stem)

        ms = RE_ST.search(t)
        body = ms.group(1) if ms else ''
        if len(body.strip()) < 20:
            empty_text.append(stem)

        # 선언된 도형 이미지가 실제로 있는가
        mf = RE_FIGS.search(t)
        declared = set(RE_IMG.findall(mf.group(1))) if mf else set()
        for img in declared:
            if not (MEDIA / img).exists():
                missing_img.append(f'{stem}:{img}')
        # {{FIGn}} 마커는 있는데 선언이 없는가(반대 방향 고아)
        if '{{FIG' in body and not declared:
            orphan_marker.append(stem)

        if sum(1 for ln in body.split('\n') if RE_LABEL.match(ln)) >= 2:
            leak.append(stem)

        sc, pts = RE_SCORE.search(t), RE_PTS.search(t)
        if sc and pts and sc.group(1) != pts.group(1):
            score_mismatch.append(stem)

    block: list[str] = []
    warn: list[str] = []

    # ── 차단: 단계 누락 ──────────────────────────────────────────────────────
    if done < n:
        block.append(f'교정 미실행 {n-done}/{n}건 — corrector 파이프라인을 안 탔다')
    if ok < n:
        warn.append(f'verify!=ok {n-ok}건')
    if quarantined:
        block.append(f'격리 {len(quarantined)}건 — {", ".join(quarantined[:3])}'
                     f'{" 외" if len(quarantined) > 3 else ""}'
                     ' (★인증 실패가 격리로 위장되는 전례가 있다 — 토큰부터 확인하라)')
    if empty_tier:
        block.append(f'난이도 공백 {len(empty_tier)}건 — {", ".join(empty_tier[:3])}')
    if empty_text:
        block.append(f'전사 비었음 {len(empty_text)}건 — {", ".join(empty_text[:3])}')
    if missing_img:
        block.append(f'선언된 도형 파일 없음 {len(missing_img)}건 — {missing_img[0]}')

    # ── 경고: 품질 신호 ──────────────────────────────────────────────────────
    if leak:
        warn.append(f'도형 라벨 본문 누출 의심 {len(leak)}건 — {", ".join(leak[:3])}'
                    ' (교정이 돌았는데도 남으면 extract_figures 미검출)')
    if orphan_marker:
        warn.append(f'{{{{FIG}}}} 마커는 있는데 figures 선언 없음 {len(orphan_marker)}건')
    if score_mismatch:
        warn.append(f'배점 불일치 {len(score_mismatch)}건 (docs/TODO.md 등록 이슈 — 회차 고유 아님)')
    return block, warn, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('rounds', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--quiet', action='store_true', help='통과한 회차는 출력 생략')
    a = ap.parse_args()

    targets = a.rounds
    if a.all or not targets:
        targets = sorted({p.name for p in PROB.glob('*/*') if p.is_dir()})
    bad = 0
    warned = 0
    for rd in targets:
        block, warn, n = check(rd)
        if block:
            bad += 1
            print(f'🔴 {rd} ({n}문제)')
            for b in block:
                print(f'   ✗ {b}')
            for w in warn:
                print(f'   ! {w}')
        elif warn:
            warned += 1
            if not a.quiet:
                print(f'🟡 {rd} ({n}문제)')
                for w in warn:
                    print(f'   ! {w}')
        elif not a.quiet:
            print(f'✅ {rd} ({n}문제)')
    print(f'\n회차 {len(targets)} · 차단 {bad} · 경고 {warned}')
    return 1 if bad else (2 if warned else 0)


if __name__ == '__main__':
    sys.exit(main())
