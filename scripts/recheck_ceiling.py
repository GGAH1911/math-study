#!/usr/bin/env python3
"""모델 천장(ceiling) 문제 재점검 — 모델이 업데이트되면 실행해 '이제 풀리는지' 확인.

배경: 일부 킬러는 현재 모델이 blind 추론(코드 없이)으로 답을 못 낸다(예: 확통_28 도로망).
정답·풀이는 수동 주입돼 있지만, 모델이 새 버전으로 갱신되면 스스로 풀 수도 있다. 이 스크립트는
db/model_ceiling.json 의 각 문제를 *파이프라인과 동일한 조건*(opus·blind·Read-only·코드불가)으로
다시 풀려보고, ans==gold 가 나오면 'solvable-now'로 표시한다(→ 정식 캐시 승격 후보).

사용:
  python scripts/recheck_ceiling.py [--timeout 900]
장시간 작업이므로 백그라운드 권장:
  setsid bash -c 'python scripts/recheck_ceiling.py > /tmp/ingest_logs/recheck.log 2>&1' & disown
"""
import sys, os, re, json
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_solution_cache as B   # call_model/find/gold_answer/tile_for_vision 재사용

WATCH = B.ROOT / 'db' / 'model_ceiling.json'


def recheck(timeout: int = 900, runs: int = 2) -> dict:
    data = json.loads(WATCH.read_text(encoding='utf-8'))
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    B.TIMEOUT_S = timeout          # 재점검은 드물게 도니 충분한 시간 부여
    B.HEARTBEAT = True             # 단일콜 진행 관측(60s 하트비트)
    promoted = []
    for item in data.get('problems', []):
        if item.get('status') == 'solvable-now':
            continue
        slug = item['slug']
        p = B.find(slug)
        if not p:
            print(f"  ⚠ {slug}: md 없음 — 스킵", flush=True); continue
        t = p.read_text(encoding='utf-8')
        gold = B.gold_answer(t)
        fmt = (re.search(r'^format:\s*(\w+)', t, re.M) or [None, 'choice'])[1]
        img = (B.IMGDIR / (p.stem + '.png')).resolve()
        tiles = [str(x) for x in B.tile_for_vision(img)]
        meta = f"문항 형식: {'객관식 5지선다' if fmt == 'choice' else '단답형(정수 정답)'}"
        # blind·Read-only(코드불가)로 N회 시도 — 객관식 1/5 우연 방지로 '전부 일치'만 PASS
        oks = []
        for k in range(runs):
            print(f"  ▶ {slug} 재점검 {k+1}/{runs} (opus·blind·Read-only·≤{timeout}s)…", flush=True)
            sol = B.call_model(tiles, fmt, meta, 'opus', 'max', str(img.parent), with_verifier=False)
            ans = str(sol.get('answer')).strip().strip('\'"') if sol else None
            oks.append(ans == gold)
            print(f"     → 답={ans} (gold={gold}) {'✅' if ans == gold else '❌'}", flush=True)
            if not oks[-1]:
                break                      # 한 번이라도 틀리면 아직 천장 — 나머지 생략
        ok = all(oks) and len(oks) == runs
        item['last_checked'] = stamp
        item['last_result'] = f"PASS×{runs}" if ok else 'FAIL'
        if ok:
            item['status'] = 'solvable-now'
            promoted.append(slug)
        print(f"  {'🎉 이제 풀림 — 승격 후보!' if ok else '여전히 천장'}: {slug}", flush=True)
    WATCH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"\n=== 재점검 완료 ({stamp}) · 새로 풀린 문제 {len(promoted)}개 ===", flush=True)
    for s in promoted:
        print(f"  🎉 {s} — `python scripts/build_solution_cache.py --slug {s}` 로 정식 캐시 후 목록에서 제거하세요.", flush=True)
    if not promoted:
        print("  (변화 없음 — 다음 모델 업데이트 때 다시 점검)", flush=True)
    return data


if __name__ == '__main__':
    to = 900
    if '--timeout' in sys.argv:
        to = int(sys.argv[sys.argv.index('--timeout') + 1])
    recheck(timeout=to)
