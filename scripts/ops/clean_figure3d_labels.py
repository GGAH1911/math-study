#!/usr/bin/env python3
"""도형 위 라벨에서 **설명 문장**을 걷어낸다.

★왜: 라벨은 이름표(`A`, `구 S`, `평면 BCD`)나 수식(`$\\overline{AB}=4$`)이어야 한다.
  생성 에이전트가 "H 에서 평면 ABD 에 내린 수선" 같은 문장을 써 넣으면 글씨가 도형을
  덮어 정작 봐야 할 입체가 안 보인다(2026-08-14 검수에서 10/28 건이 그랬다).

규칙 두 개뿐이다:
  ① 꼬리 괄호 설명을 뗀다 — "AC = √41 (원의 지름)" → "AC = √41"
  ② 그래도 문장이면 라벨을 **지운다.** 도형은 그대로 그려지고, 그 정보는 이미
     entry.conditions 에 검증된 조건으로 들어 있다.

사용: python3 scripts/ops/clean_figure3d_labels.py [--apply]
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/figures-3d'
sys.path.insert(0, str(ROOT / 'scripts/ops'))
from verify_figures_3d import _is_prose  # noqa: E402  같은 판정을 써야 게이트와 어긋나지 않는다


def shorten(v: str) -> str | None:
    """정리된 라벨. None 이면 라벨 자체를 지운다."""
    if not _is_prose(v):
        return v
    head = re.sub(r'\s*\([^)]*\)\s*$', '', v).strip()
    if head and not _is_prose(head):
        return head or None
    return None


def main() -> int:
    apply = '--apply' in sys.argv
    changed = 0
    for f in sorted(DIR.glob('*.json')):
        e = json.loads(f.read_text(encoding='utf-8'))
        shapes = e['spec']['shapes']
        before = len(shapes)
        hits = []
        for s in shapes:
            for key in ('label', 'text'):
                v = s.get(key)
                if not isinstance(v, str) or not _is_prose(v):
                    continue
                new = shorten(v)
                hits.append((key, v, new))
                if apply:
                    if new is None:
                        s.pop(key)
                    else:
                        s[key] = new
        if not hits:
            continue
        changed += 1
        print(f'■ {f.stem}')
        for key, v, new in hits:
            print(f'    {key}: "{v[:45]}" → {"삭제" if new is None else chr(34)+new+chr(34)}')
        if apply:
            assert len(e['spec']['shapes']) == before, f'{f.stem}: shape 개수가 변했다 — 쓰지 않음'
            assert e.get('conditions') and e.get('verify'), f'{f.stem}: 필수 필드 유실 — 쓰지 않음'
            f.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'\n{changed}건 {"정리함" if apply else "정리 대상 (--apply 로 실행)"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
