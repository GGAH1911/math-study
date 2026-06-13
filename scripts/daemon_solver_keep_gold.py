#!/usr/bin/env python3
"""
KEEP-GOLD 실시간 추적 + 솔버 생성 daemon

백필 로그를 5초마다 체크:
  - 신규 KEEP-GOLD 감지
  - Agent(Sonnet) 호출로 솔버 생성
  - db/solutions/{problem_id}.py 저장
  - md 파일 업데이트 (solution.generated_by=sonnet)

로그: /tmp/daemon_solver_keep_gold.log
"""

import os
import sys
import time
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import deque

PROJECT_ROOT = Path(__file__).parent.parent
BACKFILL_LOG = Path('/tmp/ingest_logs/backfill_solvers.log')
STATE_FILE = Path('/tmp/daemon_solver_state.json')
LOG_FILE = Path('/tmp/daemon_solver_keep_gold.log')
SOLUTIONS_DIR = PROJECT_ROOT / 'db' / 'solutions'
PROBLEMS_DIR = PROJECT_ROOT / 'docs' / 'problems'

def log(msg: str):
    """로그 기록"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def load_state() -> set:
    """처리 완료한 KEEP-GOLD 로드"""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return set(data.get('processed', []))
        except:
            return set()
    return set()

def save_state(processed: set):
    """처리 완료 상태 저장"""
    STATE_FILE.write_text(json.dumps({
        'processed': sorted(list(processed)),
        'updated_at': datetime.now().isoformat()
    }, indent=2, ensure_ascii=False))

def extract_keep_gold_from_log() -> set:
    """백필 로그에서 현재 KEEP-GOLD 목록 추출"""
    if not BACKFILL_LOG.exists():
        return set()

    content = BACKFILL_LOG.read_text(encoding='utf-8')
    # [123/980] · 2021_6월모평_가형_28 → KEEP-GOLD
    pattern = r'\] · ([^ ]+) → KEEP-GOLD'
    matches = re.findall(pattern, content)
    return set(matches)

def find_problem_md(problem_id: str) -> Path | None:
    """problem_id에 해당하는 .md 파일 찾기"""
    pattern = f"{problem_id}.md"
    for md_path in PROBLEMS_DIR.glob(f"**/{pattern}"):
        return md_path
    return None

def generate_solver(problem_id: str) -> bool:
    """
    Sonnet Agent를 통해 솔버 생성
    반환: 성공 여부
    """
    md_path = find_problem_md(problem_id)
    if not md_path:
        log(f"  ❌ {problem_id}: md 파일 없음")
        return False

    try:
        md_content = md_path.read_text(encoding='utf-8')
    except Exception as e:
        log(f"  ❌ {problem_id}: md 읽기 실패 - {e}")
        return False

    # Agent 호출 프롬프트
    prompt = f"""
문제: {problem_id}

md 파일 내용:
---
{md_content[:2000]}
---

이 문제의 Python 솔버를 작성해주세요.

요구사항:
1. db/solutions/{problem_id}.py 경로에 저장 가능한 형태
2. if __name__ == '__main__': 로 직접 실행 가능
3. 마지막 줄에 print(f"답: {{answer}}")로 답 출력
4. 코드만 응답 (마크다운 제외)

Python 코드 전체를 출력하세요:
"""

    try:
        # Claude API 호출 (실제 구현에서는 SDK 사용)
        # 여기선 간단히: 성공 가정 + 로그만 기록
        # 실제로는 anthropic SDK로 호출
        result = call_claude_api(problem_id, prompt)
        if result:
            log(f"  ✅ {problem_id}: 솔버 생성 완료")
            return True
        else:
            log(f"  ⚠️  {problem_id}: 솔버 생성 실패 (API)")
            return False
    except Exception as e:
        log(f"  ❌ {problem_id}: 예외 - {e}")
        return False

def call_claude_api(problem_id: str, prompt: str) -> bool:
    """
    실제 Sonnet API 호출 (placeholder)

    실제 구현:
    - anthropic.Anthropic() 초기화
    - message.create() 호출
    - solver 코드 추출
    - 파일 저장 + md 업데이트
    """
    # TODO: 실제 API 호출 로직
    log(f"  [API] {problem_id}: Sonnet 호출 필요")
    return False

def daemon_loop():
    """메인 daemon loop"""
    log("=== KEEP-GOLD 솔버 daemon 시작 ===")
    log(f"체크 간격: 5초")

    processed = load_state()
    log(f"이미 처리된: {len(processed)}개")

    iteration = 0
    while True:
        iteration += 1
        try:
            # 현재 KEEP-GOLD 추출
            current = extract_keep_gold_from_log()
            log(f"[#{iteration}] 백필 로그 체크: 총 {len(current)}개 KEEP-GOLD")

            # 신규 항목
            new_items = current - processed

            if new_items:
                log(f"  🆕 신규 {len(new_items)}개 감지")
                for problem_id in sorted(new_items):
                    log(f"  → {problem_id} 처리 중...")
                    if generate_solver(problem_id):
                        processed.add(problem_id)
                        save_state(processed)
                    time.sleep(0.5)  # API rate limit
            else:
                log(f"  신규 없음 (처리: {len(processed)}/{len(current)})")

            time.sleep(5)

        except KeyboardInterrupt:
            log("=== daemon 종료 (Ctrl+C) ===")
            break
        except Exception as e:
            log(f"❌ daemon 오류: {e}")
            time.sleep(5)

if __name__ == '__main__':
    daemon_loop()
