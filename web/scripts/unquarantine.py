#!/usr/bin/env python3
# unquarantine.py — 오케스트레이터(opus)가 격리 문제를 손교정 후 호출. 격리 해제 + 상태 갱신.
# 사용: unquarantine.py <slug> "<fix note>" [--st <새 searchable_text 파일>]
#   --st 없으면 기존 searchable_text 유지(텍스트는 정확, 격리 사유가 placeholder뿐인 경우).
#   --st 주면 그 파일 내용으로 searchable_text 교체(opus 가 이미지 보고 재전사한 경우).
import re, sys, glob, os
REPO = '/home/insung/Projects/math-study'

def main():
    slug = sys.argv[1]
    note = sys.argv[2] if len(sys.argv) > 2 else 'opus 손교정(격리 해제)'
    st_file = None
    if '--st' in sys.argv:
        st_file = sys.argv[sys.argv.index('--st') + 1]
    g = glob.glob(f'{REPO}/docs/problems/**/{slug}.md', recursive=True)
    if not g:
        print(f'못찾음: {slug}'); sys.exit(1)
    md = g[0]; t = open(md, encoding='utf-8').read()
    # searchable_text 교체(옵션)
    if st_file:
        new_st = open(st_file, encoding='utf-8').read().rstrip('\n')
        block = 'searchable_text: |\n' + '\n'.join('  ' + l for l in new_st.split('\n')) + '\n'
        m = re.search(r'\nsearchable_text: [|>]\n((?:  .*\n?)*)', t)  # | (literal) 와 > (folded) 둘 다
        t = t[:m.start() + 1] + block + t[m.end():]
    # 격리 해제 + 상태 갱신
    t = re.sub(r'\ncorrector_quarantine:\s*true', '', t)
    t = re.sub(r'\ncorrector_verify_issues:(?:\n  - .*)*', '', t)
    t = re.sub(r'\ncorrector_verify:\s*\S+', '', t)
    t = re.sub(r'\ncorrector_by:\s*\S+', '', t)
    t = re.sub(r'\ncorrector_done:\s*\S+', '', t)
    # corrector_fixes 에 노트 추가(기존 보존)
    fm = re.search(r'\ncorrector_fixes:\n((?:  - .*\n)*)', t)
    note_line = f'  - {note!r}'.replace("'", '"', 1)
    note_line = '  - "' + note.replace('"', "'") + '"'
    if fm:
        t = t[:fm.end()] + note_line + '\n' + t[fm.end():]
    else:
        t = re.sub(r'\nsearchable_text:', lambda m: f'\ncorrector_fixes:\n{note_line}\nsearchable_text:', t, count=1)  # lambda=백슬래시(\log 등) escape 회피
    # 상태 줄 재삽입(searchable_text 앞)
    t = re.sub(r'\nsearchable_text:', '\ncorrector_by: opus\ncorrector_done: true\ncorrector_verify: ok\nsearchable_text:', t, count=1)
    open(md, 'w', encoding='utf-8').write(t)
    print(f'✓ 격리해제 {slug}' + (' (텍스트 교체)' if st_file else ' (텍스트 유지)'))

if __name__ == '__main__':
    main()
