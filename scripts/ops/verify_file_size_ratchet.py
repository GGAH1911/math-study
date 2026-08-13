#!/usr/bin/env python3
"""[파일 크기 래칫] 500줄을 넘는 파일은 **더 커지지 못한다.**

    python3 scripts/ops/verify_file_size_ratchet.py            # 검사 (셧다운/부팅)
    python3 scripts/ops/verify_file_size_ratchet.py --tighten  # 줄어든 만큼 기준선 조이기
    python3 scripts/ops/verify_file_size_ratchet.py --save     # 기준선 최초 생성

## 왜 「초과 금지」가 아니라 「증가 금지」인가

착수 시점에 500줄을 넘는 파일이 **16개**였다. 그걸 전부 실패로 치면 게이트는 첫날부터
빨갛고, **빨간 게이트는 곧 아무도 안 보는 게이트**가 된다(`도구/게이트.md` §36 —
거짓 경보는 게이트를 죽이는 가장 빠른 길이다).

그래서 **래칫**이다. 톱니바퀴처럼 한 방향으로만 돈다:

  · 기준선에 없던 파일이 500줄을 넘으면      → 🔴 실패
  · 기준선에 있는 파일이 **기록보다 커지면**  → 🔴 실패
  · 줄어들면                                → ✅ 통과 (그리고 `--tighten` 으로 기준선을 내린다)

즉 **오늘보다 나빠지는 것만 막는다.** 기존 16개는 각자의 사정이 있어 지금 당장 자를 수
없지만, 적어도 **더 자라지는 않는다.**

## 왜 500인가

이 프로젝트가 스스로 정한 선이다 — "코드는 모듈화 우선, 500줄쯤부터 분리 검토".
숫자 자체보다 **더 커지지 않게 하는 것**이 목적이다. 실측 사례: ChatPanel 1,972줄을
582줄로 갈랐을 때(−70%), 같은 상태를 여러 곳에서 만지던 버그가 함께 사라졌다.

착수 시점 초과가 18개다. 전부 실패로 치면 첫날부터 빨갛고, **빨간 게이트는 곧 아무도
안 보는 게이트**가 된다. 그래서 기준선으로 인정하고 «더 자라지 않는 것»만 본다.

## 늘려야 할 때

정당하게 커지는 경우가 있다(기능 추가, 데이터 표 확장). 그때는 **기준선을 고치는 커밋에
이유를 적는다.** 조용히 숫자만 올리지 않는다 — 그 순간 래칫이 아니게 된다.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# scripts/ops/<이 파일> → 레포 루트
BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "file_size_ratchet_baseline.json")

LIMIT = 500
EXTS = (".py", ".ts", ".tsx", ".mjs", ".js", ".jsx", ".astro")
# 우리가 쓰지 않은 코드는 세지 않는다.
SKIP = ("node_modules/", "/build/", "/venv/", "venv/", ".min.js", "/dist/", "web/public/")


def tracked_sizes() -> dict[str, int]:
    """git 추적 코드 파일의 줄 수."""
    out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                         capture_output=True, text=True, timeout=120).stdout
    sizes = {}
    for rel in out.split("\n"):
        if not rel.endswith(EXTS) or any(s in rel for s in SKIP):
            continue
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                sizes[rel] = sum(1 for _ in f)
        except OSError:
            continue
    return sizes


def load() -> dict[str, int]:
    if not os.path.exists(BASELINE):
        return {}
    with open(BASELINE, encoding="utf-8") as f:
        return json.load(f)


def store(d: dict[str, int]) -> None:
    with open(BASELINE, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(d.items())), f, ensure_ascii=False, indent=1)
        f.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="기준선 최초 생성")
    ap.add_argument("--tighten", action="store_true", help="줄어든 만큼 기준선을 내린다")
    ap.add_argument("--quiet", action="store_true", help="통과 시 한 줄만")
    a = ap.parse_args()

    cur = tracked_sizes()
    over = {f: n for f, n in cur.items() if n > LIMIT}

    if a.save:
        if os.path.exists(BASELINE):
            print(f"[WARN] 기준선이 이미 있다: {BASELINE}")
            print("       새로 만들려면 그 파일을 지워라. 조이려면 `--tighten` 을 쓴다.")
            return 1
        store(over)
        print(f"[OK] 기준선 저장 — {LIMIT}줄 초과 {len(over)}개 → {BASELINE}")
        for f, n in sorted(over.items(), key=lambda x: -x[1]):
            print(f"   {n:>5}  {f}")
        return 0

    # ⚠️ **빈 기준선(`{}`)과 기준선 없음을 구분한다.** 예전엔 `if not base:` 하나로 묶여
    #    있었는데, 500줄 초과를 **전부 없애는 데 성공한 순간** 기준선이 `{}` 가 되면서
    #    게이트가 「기준선 없음」으로 빨개졌다(2026-08-05, 16→0 달성 직후 실측).
    #    목표를 달성했다고 실패하는 게이트는 그 자리에서 신뢰를 잃는다.
    if not os.path.exists(BASELINE):
        print(f"[FAIL] 기준선 없음. 먼저 `--save`: {BASELINE}")
        return 1
    base = load()

    grown, added, shrunk, gone = [], [], [], []
    for f, n in sorted(over.items(), key=lambda x: -x[1]):
        if f not in base:
            added.append((f, n))
        elif n > base[f]:
            grown.append((f, n, base[f]))
    for f, b in base.items():
        n = cur.get(f)
        if n is None:
            gone.append((f, b))
        elif n < b:
            shrunk.append((f, n, b))

    if a.tighten:
        # 지금 500 을 넘는 것들의 **현재 크기**가 곧 새 기준선이다.
        #   500 아래로 내려왔거나 사라진 파일은 `over` 에 없으므로 자동으로 빠진다.
        # ⚠️ 자란 것이 있으면 조이지 않는다 — 그러면 위반을 기준선으로 덮는 셈이다.
        if grown or added:
            print(f"🔴 자란 파일이 {len(grown) + len(added)}건 있다 — 조이지 않는다.")
            print("   먼저 그것부터 처리하라. 지금 조이면 위반을 기준선으로 덮게 된다.")
            return 1
        new = dict(over)
        store(new)
        print(f"[OK] 기준선 조임 — {LIMIT}줄 초과 {len(new)}개")
        for f, n, b in shrunk:
            print(f"   ↓ {b:>5} → {n:<5}  {f}")
        for f, b in gone:
            print(f"   ✓ 사라짐({b}줄)  {f}")
        return 0

    bad = len(grown) + len(added)
    if not bad:
        head = f"✅ 파일 크기 래칫 — {LIMIT}줄 초과 {len(over)}개, 아무것도 자라지 않았다."
        if a.quiet:
            print(head)
            return 0
        print(head)
        if shrunk or gone:
            print("\n   줄어든 것:")
            for f, n, b in sorted(shrunk, key=lambda x: x[1] - x[2]):
                print(f"     ↓ {b:>5} → {n:<5}  {f}")
            for f, b in gone:
                print(f"     ✓ 500 아래로 내려감 또는 삭제({b}줄)  {f}")
            print("\n   → `--tighten` 으로 기준선을 내려 두면 되돌아가는 것도 막힌다.")
        return 0

    print(f"🔴 파일 크기 래칫 위반 {bad}건\n")
    for f, n in added:
        print(f"   🆕 {n:>5}줄  {f}")
        print(f"        {LIMIT}줄을 **새로** 넘었다. 지금 가르는 것이 가장 싸다.")
    for f, n, b in grown:
        print(f"   📈 {n:>5}줄  {f}")
        print(f"        기준선 {b} → {n} (**+{n - b}**). 이미 큰 파일이 더 커졌다.")
    print("\n   무엇을 하나:")
    print("   · 가른다 — 줄 수가 아니라 **무엇이 무엇에 붙어 있는지**로 경계를 찾는다.")
    print("     헬퍼가 어느 함수에 쓰이는지 전수 대조하면 경계가 저절로 드러난다")
    print("     (회귀 방지: 베이스라인 → 순수 이동 → 타입체커 → 스모크 → 체크포인트 커밋).")
    print("   · 가르기 전에 **동작 게이트**부터. 모양만 같고 안이 죽는 사고를 여러 번 겪었다.")
    print("   · 정당하게 커져야 한다면 **기준선을 고치는 커밋에 이유를 적는다.**")
    print("     조용히 숫자만 올리면 그 순간 래칫이 아니다.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
