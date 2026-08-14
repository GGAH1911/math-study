"""난이도(killer_tier)·인지유형 분류 어휘의 **단일 정본**.

★왜 이 파일이 생겼나 (2026-08-14):
  `ingest_round.py` 는 프롬프트에서 모델에게 `"early|mid|high|killer"` 를 쓰라고 지시하면서
  (:125 · 가이드 :133 "high: 20-22번대, 4점, 까다로운 추론"), 검증기는
  `ALLOWED_TIER = {'early','mid','killer'}` 로 **high 를 몰랐다**. 시킨 대로 `high` 를 답하면
  값이 조용히 버려져 **난이도가 빈 채로** 기록됐다. `text_meta.py`·`vision_meta.py` 는 프롬프트도
  검증기도 high 를 빼서 내부적으론 일관됐지만, **스키마(`web/src/content.config.ts`)와
  UI(`TIER_BADGE`)는 high 를 정식 지원**하고 실데이터에도 687건이 high 다.
  → 같은 어휘가 네 곳에 각자 적혀 있어 어긋났다. 그래서 **한 곳에 모은다.**

  실측 피해: 2026 고3 7월모의고사 46문제 중 **7건**이 난이도 빈 값. 메타 호출 자체는
  성공해 unit·concepts·exam_intent·cognitive_type 은 다 채워졌고 tier 만 탈락했다.
  비결정적이라 인제스트할 때마다 몇 건씩 계속 샜을 것이다.

★어휘를 바꿀 일이 생기면 **여기만** 고치고, 아래 세 곳이 이 파일을 import 하는지 확인한다:
  `ingest_round.py` · `text_meta.py` · `vision_meta.py`
  스키마/UI 도 함께 봐야 한다 — `web/src/content.config.ts` · `web/src/lib/problem-meta.ts`
"""
from __future__ import annotations
import re
import sys

#: 난이도 4단계. **스키마(content.config.ts)·UI(TIER_BADGE)와 반드시 같아야 한다.**
ALLOWED_TIER = {'early', 'mid', 'high', 'killer'}

ALLOWED_COG = {'계산', '개념', '응용', '추론', '통합'}

#: 프롬프트에 그대로 끼워 넣는 가이드. 파이프라인마다 다르게 적어서 어긋났던 부분이다.
TIER_GUIDE = """killer_tier 기준:
- early: 1-15번 수준 (2-3점, 단순 계산·개념 확인)
- mid: 16-20번 또는 23-26번 (3-4점, 표준 응용)
- high: 14-15·21-22·27-28번대 (4점, 까다로운 추론 — mid 와 killer 사이)
- killer: 21·22·28·29·30번 같은 최고난도 (4점, 통합 추론)"""


def pick_enum(val, allowed: set[str], field: str = '', ctx: str = ''):
    """열거값 정규화. **규격 밖이면 버리되, 조용히 버리지 않는다.**

    ★조용한 드롭이 이 버그의 본체였다 — 5개월간 아무도 몰랐고 사장님이 목록을 눈으로
      보고서야 발견됐다. 버리는 것 자체는 맞지만 **흔적은 남겨야** 다음에 빨리 잡는다.
    """
    if not val:
        return None
    if isinstance(val, list):
        val = val[0] if val else None
        if not val:
            return None
    s = str(val).strip()
    if s in allowed:
        return s
    for tok in re.split(r'[|,/、]', s):
        tok = tok.strip()
        if tok in allowed:
            return tok
    print(f'  ! {field or "enum"} 규격 밖 값 버림: {s!r} (허용 {sorted(allowed)})'
          f'{" — " + ctx if ctx else ""}', file=sys.stderr, flush=True)
    return None
