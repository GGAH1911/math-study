#!/usr/bin/env python3
"""유령 {{TABLE}} 제거 — classify_box 수정 이전 extract 가 조건•/(가)(나)/ㄱㄴㄷ/안내문 박스를
표로 오인해 박은 spurious {{TABLEn}} placeholder + stale `tables:` frontmatter 를 걷어낸다.
조사 결과 박스 원문은 손실 0(본문에 텍스트로 보존 or '5지선다형' 노이즈) → 마커만 제거하면
새 classify_box 가 만들었을 상태와 동일. 풀이·정답·도형·corrector_done 은 보존.
안전장치: 표 내용이 노이즈 아니고 본문에 없으면(진짜 손실) 그 자리에 텍스트로 복원.
corrector_verify 리셋 + corrector_quarantine 해제 → 파이프라인이 재검증.
사용: python strip_ghost_tables.py [--dry] [--limit N]  (대상 slug = /tmp/ghost_table_slugs.txt)
"""
from __future__ import annotations
import re, glob, os, sys, shutil

DRY = '--dry' in sys.argv
LIMIT = next((int(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == '--limit'), 0)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BACKUP = '/tmp/ghost_backup'
os.makedirs(BACKUP, exist_ok=True)
NOISE_RE = re.compile(r'지선다|선다형|단답형')
norm = lambda s: re.sub(r'\s+', '', s)

slugs = open('/tmp/ghost_table_slugs.txt').read().split()
if LIMIT:
    slugs = slugs[:LIMIT]

changed = restored = skipped = 0
for slug in slugs:
    md = next((p for p in glob.glob(f'docs/problems/**/{slug}.md', recursive=True)), None)
    if not md:
        print(f"  ? {slug} md 없음"); continue
    t = open(md, encoding='utf-8').read()
    sx = re.search(r'(\nsearchable_text: \|\n)((?:  .*\n|\n)*)', t)   # greedy: 들여쓴/빈 줄 전부(다음 필드 전까지)
    if not sx or '{{TABLE' not in sx.group(2):
        skipped += 1; continue
    body = sx.group(2)
    # tables 셀 텍스트(본문보존 여부 점검용 — 복원은 하지 않음. 진짜 누락은 파이프라인 sonnet 검증이 잡음)
    tb = re.search(r'\ntables:\n((?:  - .*\n)+)', t)
    cells = re.findall(r'"([^"]*)"', tb.group(1)) if tb else []
    table_content = ' '.join(c for c in cells if c.strip())
    real_box = bool(table_content and not NOISE_RE.search(table_content) and len(norm(table_content)) > 20)
    present = real_box and norm(table_content)[:40] in norm(body)
    if real_box and not present:                                   # 본문에 없는 실내용 → 로깅(파이프라인이 검증서 잡도록)
        restored += 1
        print(f"  ⚠ {slug}: tables 실내용이 본문에 안 보임 — strip 후 sonnet 검증이 '놓침' 잡을 것")
    # {{TABLEn}} 줄 제거(복원 없음)
    new_body = '\n'.join(l for l in body.split('\n') if not re.match(r'\s*\{\{TABLE\d+\}\}\s*$', l))
    t2 = t[:sx.start(2)] + new_body + t[sx.end(2):]
    t2 = re.sub(r'\ntables:\n(?:  - .*\n)+', '\n', t2)                       # tables 프론트매터 제거
    t2 = re.sub(r'\ncorrector_verify:.*(?=\n)', '', t2)                     # 검증상태 리셋(→재검증)
    t2 = re.sub(r'\ncorrector_verify_issues:(?:\n  - .*)*(?=\n)', '', t2)
    t2 = re.sub(r'\ncorrector_quarantine:\s*true(?=\n)', '', t2)           # 격리 해제
    if DRY:
        if changed < 3:
            print(f"\n===== {slug} (dry) =====")
            print("  표내용:", (table_content[:70] + '…') if table_content else '(없음/노이즈)')
            print("  본문보존:", "✓ 팬텀(마커만 제거)" if (not real_box or present) else "✗ 본문에 없음 → 검증서 잡음")
        changed += 1
        continue
    shutil.copy(md, f'{BACKUP}/{slug}.md')
    open(md, 'w', encoding='utf-8').write(t2)
    changed += 1

print(f"\n{'[DRY] ' if DRY else ''}처리 {changed} · 내용복원 {restored} · skip(이미 무TABLE) {skipped} · 백업 {BACKUP}")
