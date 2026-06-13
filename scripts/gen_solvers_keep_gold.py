#!/usr/bin/env python3
"""
KEEP-GOLD 문제들의 솔버를 batch로 생성 + md 업데이트

각 문제마다:
1. docs/problems에서 md 찾기
2. Agent(Sonnet)로 솔버 생성
3. db/solutions/{problem_id}.py 저장
4. md의 solution 필드 업데이트
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
KEEP_GOLD_LIST_FILE = Path('/tmp/keep_gold_list.txt')
SOLUTIONS_DIR = PROJECT_ROOT / 'db' / 'solutions'
PROBLEMS_DIR = PROJECT_ROOT / 'docs' / 'problems'

def find_problem_md(problem_id: str) -> Path | None:
    """problem_id에 해당하는 .md 파일 찾기"""
    # 예: 2021_6월모평_가형_28 → 2021/6월모평/2021_6월모평_가형_28.md
    pattern = f"{problem_id}.md"
    for md_path in PROBLEMS_DIR.glob(f"**/{pattern}"):
        return md_path
    return None

def read_problem_md(md_path: Path) -> dict:
    """md 파일에서 문제 정보 추출"""
    content = md_path.read_text(encoding='utf-8')

    # frontmatter 파싱
    match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = match.group(1)
    meta = {}
    for line in frontmatter.split('\n'):
        if ': ' in line:
            key, val = line.split(': ', 1)
            meta[key.strip()] = val.strip()

    return {
        'path': str(md_path),
        'answer': meta.get('answer', 'N/A'),
        'content': content,
    }

def generate_solver_via_agent(problem_id: str, problem_info: dict) -> dict | None:
    """Agent를 통해 솔버 생성"""
    md_path = problem_info['path']
    answer = problem_info['answer']

    # 간단한 curl 호출로 Agent 대신 요청 (실제로는 API 호출)
    # 여기선 간단히: 정보만 수집하고 나중에 일괄 처리하도록

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {problem_id}: 수집 완료 (답: {answer})")
    return {
        'problem_id': problem_id,
        'md_path': md_path,
        'answer': answer,
        'status': 'pending'
    }

def main():
    # KEEP-GOLD 목록 읽기
    if not KEEP_GOLD_LIST_FILE.exists():
        print(f"Error: {KEEP_GOLD_LIST_FILE} not found")
        return 1

    keep_gold_ids = [line.strip() for line in KEEP_GOLD_LIST_FILE.read_text().split('\n') if line.strip()]
    print(f"로드된 KEEP-GOLD: {len(keep_gold_ids)}개")

    # 각 문제의 md 찾기
    problems = []
    for problem_id in keep_gold_ids:
        md_path = find_problem_md(problem_id)
        if not md_path:
            print(f"⚠️  {problem_id}: md 파일 못 찾음")
            continue

        info = read_problem_md(md_path)
        if info:
            problems.append({
                'id': problem_id,
                'path': md_path,
                'answer': info.get('answer', '?'),
            })

    print(f"\n✅ {len(problems)}개 md 파일 찾음")

    # 로그 파일로 저장 (향후 Agent 호출 시 참고)
    log_file = Path('/tmp/keep_gold_solver_batch.log')
    with open(log_file, 'w') as f:
        f.write(f"KEEP-GOLD 솔버 생성 배치\n")
        f.write(f"생성 시간: {datetime.now()}\n")
        f.write(f"총 문제: {len(problems)}\n\n")
        for p in problems:
            f.write(f"{p['id']:40} | 답: {p['answer']:4} | {p['path']}\n")

    print(f"로그: {log_file}")
    print(f"\n다음 단계: Agent 호출하여 솔버 생성")
    print(f"명령어: gen_solvers_via_agent.py")

    return 0

if __name__ == '__main__':
    sys.exit(main())
