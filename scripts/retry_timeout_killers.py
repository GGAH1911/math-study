#!/usr/bin/env python3
"""timeout-capped 킬러(refine_status=killer-timeout-capped)를 600s로 한 번 더 → 확정.
풀리면 solved_by 내림(corrected-*-600), 600s로도 미완이면 confirmed-hard(opus 유지)."""
import re, glob, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import refine_opus as R  # noqa: E402  (solve_ex, update_md 재사용; main은 __main__ 가드라 미실행)


def f(t, k):
    m = re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)
    return m.group(1).strip().strip('\'"') if m else None


def main():
    tg = []
    for fp in sorted(glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)):
        if 'README' in fp:
            continue
        t = Path(fp).read_text(encoding='utf-8')
        if f(t, 'refine_status') == 'killer-timeout-capped':
            tg.append((Path(fp), Path(fp).stem, f(t, 'answer')))
    print(f"═══ timeout-capped 재시도 (Haiku/Sonnet 각 600s) — {len(tg)}개 ═══\n", flush=True)
    tot = 0.0
    for path, stem, gold in tg:
        a, c, sa = R.solve_ex(stem, 'haiku', 600); tot += c
        if a == gold:
            R.update_md(path, 'haiku', [('haiku', 'verify-fail')], 'corrected-haiku-600')
            print(f"  {stem}: opus→haiku ✅ (600s에 풀림) ${c:.3f}", flush=True); continue
        a2, c2, sb = R.solve_ex(stem, 'sonnet', 600); tot += c2
        if a2 == gold:
            R.update_md(path, 'sonnet', [('haiku', sa), ('sonnet', 'verify-fail')], 'corrected-sonnet-600')
            print(f"  {stem}: opus→sonnet ✅ (600s) ${c + c2:.3f}", flush=True); continue
        R.update_md(path, 'opus', [('haiku', sa), ('sonnet', sb)], 'confirmed-hard')
        print(f"  {stem}: opus 유지 🔒 confirmed-hard (600s로도 미완) ${c + c2:.3f}", flush=True)
    print(f"\n═══ 완료 ═══ ${tot:.2f}", flush=True)


if __name__ == '__main__':
    main()
