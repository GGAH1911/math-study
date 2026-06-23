#!/usr/bin/env python3
# fix_inline_math.py — 개념/학습노트 본문의 인라인 수식 가독성 개선(③ + ② 보조).
#   ③ 인라인 $...$ 안의 \frac/\dfrac → \tfrac (textstyle 작은 분수 → 줄높이 안정, 줄간격 들쭉날쭉 해소).
#      블록 $$...$$ 안은 건드리지 않음(거기선 큰 분수가 정상).
#   ② 아주 긴 인라인 수식(= 2개↑ AND 70자↑ = 등식체인)은 $$ 블록으로 승격 옵션(--promote, 기본 off).
#      문장 중간 수식을 블록으로 빼면 흐름이 끊겨, 기본은 ③만(안전). nowrap+CSS 오버플로우와 병행.
#   결정적·멱등. dry-run 기본, --apply 로 수정.
import sys, glob, re

APPLY = '--apply' in sys.argv
PROMOTE = '--promote' in sys.argv
ROOT_GLOBS = ['docs/concepts/**/*.md', 'docs/syntheses/**/*.md']

# 인라인 $...$ 매칭(블록 $$ 아님, 한 줄 안).
INLINE = re.compile(r'(?<!\$)\$(?!\$)([^\$\n]+?)\$(?!\$)')


def tfrac_inline(body: str) -> str:
    # \dfrac → \frac 통일 후 \frac → \tfrac (인라인 한정). \tfrac 은 이미 작으니 패스.
    body = body.replace(r'\dfrac', r'\frac')
    body = re.sub(r'\\frac\b', r'\\tfrac', body)
    return body


def process(text: str) -> tuple[str, int, int]:
    n_tfrac = 0
    def repl(m):
        nonlocal n_tfrac
        body = m.group(1)
        new = tfrac_inline(body)
        if new != body:
            n_tfrac += 1
        return f'${new}$'
    out = INLINE.sub(repl, text)
    return out, n_tfrac, 0


def main():
    files = []
    for g in ROOT_GLOBS:
        files += glob.glob(g, recursive=True)
    stat = {'files': 0, 'tfrac': 0}
    for f in sorted(set(files)):
        t = open(f, encoding='utf-8').read()
        nt, n_tfrac, _ = process(t)
        if nt != t:
            stat['files'] += 1
            stat['tfrac'] += n_tfrac
            if APPLY:
                open(f, 'w', encoding='utf-8').write(nt)
    print(f"{'[적용]' if APPLY else '[dry-run]'} 수정파일 {stat['files']} · 인라인 frac→tfrac {stat['tfrac']}")


if __name__ == '__main__':
    main()
