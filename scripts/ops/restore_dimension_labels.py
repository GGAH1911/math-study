#!/usr/bin/env python3
"""라벨 제거를 **되돌리되, 문제가 묻는 값만 계속 뺀다**.

★경위: 2026-08-14 에 "계산해서 나온 값" 라벨 28개를 지웠는데, 사장님 판단은
  "치수 라벨은 원본 도판에도 흔히 적혀 있으니 나쁘지 않다" 였다. 맞다 — 원본 기출도
  AB=4, MN=3 같은 치수는 그림에 적는다. 정말 빼야 하는 건 **문제가 묻는 그 값**뿐이다.

아래 KEEP_REMOVED 는 각 문제의 발문을 실제로 읽고 고른 것이다(근거를 함께 적었다).
그 외 21개는 복원한다.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/figures-3d'
# 라벨 제거 커밋 — 여기서 '지워지기 전' 파일을 꺼내 복원 원본으로 쓴다.
COMMIT = '62f20d46'   # 라벨 제거 커밋
BASE = f'{COMMIT}^'

# 계속 빼 둘 라벨: 발문이 바로 그 값을 묻는다.
KEEP_REMOVED: dict[str, list[tuple[str, str]]] = {
    '2020_수능_가형_12': [('title', '발문이 "k의 값은?" — 제목에 k=ln13 이 박혀 있었다')],
    '2022_고3_10월모의고사_기하_30': [('구하는 정사영 $S=4\\sqrt{3}$', '"구하는" 이라고 라벨에 적혀 있다')],
    '2023_9월모평_미적분_26': [('$y=\\sqrt{\\dfrac{8x}{2x^2+1}}$', '발문이 "k의 값은?" — 곡선식의 k 자리에 답 8 이 들어가 있다'),
                          ('$\\sqrt{\\dfrac{8x}{2x^2+1}}$', '같은 이유')],
    '2024_9월모평_기하_28': [('정사영 넓이 $=6$', '발문이 "정사영의 넓이의 최댓값은?"')],
    '2025_수능_기하_27': [('정사영 $\\dfrac{\\sqrt{10}}{4}\\pi$', '발문이 정사영 넓이를 묻는다')],
    '2025_수능_기하_28': [('$\\overline{PQ}=\\sqrt{55}$', '발문이 "선분 PQ의 길이는?" — 답 그 자체')],
}


def removed_in_commit(stem: str) -> set[str]:
    """그 커밋에서 **실제로 지워진** 라벨 문자열만. 이후 다른 작업이 뗀 것까지 되살리면 안 된다.

    ★2026-08-14: 처음엔 "옛 파일에 있고 지금 없는 것"을 전부 복원했더니, 그 사이 원본 대조
      워크플로가 어지럽다고 뗀 라벨까지 44개가 되살아났다. 커밋 하나의 diff 로 좁힌다.
    """
    rel = f'web/src/data/figures-3d/{stem}.json'
    before = subprocess.run(['git', 'show', f'{BASE}:{rel}'], capture_output=True, text=True, cwd=ROOT)
    after = subprocess.run(['git', 'show', f'{COMMIT}:{rel}'], capture_output=True, text=True, cwd=ROOT)
    if before.returncode or after.returncode:
        return set()
    def labels(txt: str) -> set[str]:
        e = json.loads(txt)
        out = {e['spec']['title']} if isinstance(e.get('spec', {}).get('title'), str) else set()
        for sh in e['spec']['shapes']:
            out |= {v for _, v in label_of(sh)}
        return out
    return labels(before.stdout) - labels(after.stdout)


def old_spec(stem: str) -> dict | None:
    rel = f'web/src/data/figures-3d/{stem}.json'
    r = subprocess.run(['git', 'show', f'{BASE}:{rel}'], capture_output=True, text=True, cwd=ROOT)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None


def label_of(shape: dict) -> list[tuple[str, str]]:
    return [(k, shape[k]) for k in ('label', 'text') if isinstance(shape.get(k), str)]


def main() -> int:
    apply = '--apply' in sys.argv
    restored = kept = 0
    for f in sorted(DIR.glob('*.json')):
        old = old_spec(f.stem)
        if not old:
            continue
        cur = json.loads(f.read_text(encoding='utf-8'))
        keep = {t for t, _ in KEEP_REMOVED.get(f.stem, [])}
        target = removed_in_commit(f.stem)      # 이 커밋에서 지운 것만
        if not target:
            continue
        # 제목
        if (old.get('spec', {}).get('title') in target and 'title' not in cur.get('spec', {})
                and 'title' not in keep):
            cur['spec']['title'] = old['spec']['title']; restored += 1
            print(f'  + {f.stem}: title 복원')
        # shape 별 라벨 — 인덱스가 아니라 **좌표**로 짝을 찾는다(그 사이 도형이 바뀌었을 수 있다).
        def key(s): return (s.get('type'), json.dumps(s.get('at') or s.get('from') or s.get('center')
                                                     or s.get('origin') or s.get('vertices'), sort_keys=True))
        by = {}
        for s in cur['spec']['shapes']:
            by.setdefault(key(s), []).append(s)
        for so in old['spec']['shapes']:
            for k, v in label_of(so):
                if v not in target:
                    continue
                if v in keep:
                    kept += 1; continue
                cands = by.get(key(so)) or []
                tgt = next((c for c in cands if k not in c), None)
                if tgt is not None:
                    tgt[k] = v; restored += 1
                    print(f'  + {f.stem}: {k}="{v[:40]}" 복원')
        if apply:
            assert cur.get('conditions') and cur.get('verify'), f'{f.stem}: 필수 필드 유실 — 쓰지 않음'
            f.write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'\n복원 {restored}개 · 계속 제외 {kept}개  {"(적용됨)" if apply else "(--apply 로 실행)"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
