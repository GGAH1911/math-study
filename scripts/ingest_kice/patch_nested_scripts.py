#!/usr/bin/env python3
"""중첩 첨자 평탄화 수정 — md searchable_text 의 깨진 첨자 토큰만 정밀 패치.

hancom_decode 재귀화 수정 이전에 인제스트된 문제는 첨자 안의 중첩 위/아래첨자가
평탄화돼 있다(예: log_{2n} ← log_{2^{n}}, e^{x2} ← e^{x^{2}}). 이 스크립트는
첨자 그룹 `_{...}` / `^{...}` 안에서만 평탄화 패턴을 찾아 중첩 구조로 복원한다.

본문 일반 텍스트(한글·평문 변수)는 건드리지 않는다 — 오직 `_{}`/`^{}` *그룹 내부*만.

usage: patch_nested_scripts.py [--apply] [SLUG_SUBSTR ...]
  기본 dry-run. --apply 시 .md 패치.
"""
from __future__ import annotations
import sys, re, glob, os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _fix_group(inner: str) -> str:
    """첨자 그룹 내부 문자열에서 중첩 평탄화를 복원.
    규칙: 그룹 안에서 '베이스영숫자' 뒤에 곧바로 오는 '지수영숫자'를 ^{}/_{} 로 분리.
    보수적으로, 잘 알려진 평탄 패턴만 처리:
      - 변수+숫자: x2→x^{2}, kx2→kx^{2}, an→a_{n}, 2n→2^{n}(밑이 숫자2일 때만 모호 → 아래 한정)
    실제 평탄화는 디코더가 이미 고쳤으므로, 여기선 *기존 md* 의 알려진 깨짐만 좁게 친다."""
    s = inner
    # ① log/ln 의 밑: 'log2x'·'log23' → 'log_{2}x' (log 뒤 숫자 1개 = 밑, 위첨자 아님)
    #    'ln3' 은 자연로그(밑 e)라 첨자 아님 → 'ln' 은 건드리지 않음.
    s = re.sub(r'log(\d)', r'log_{\1}', s)
    # ② 변수 뒤 한 자리 숫자 = 지수: x2→x^{2}, kx2→kx^{2}.
    #    단 'log'/'ln' 의 g·n 뒤 숫자는 ①에서 이미 처리됐거나(밑) e-base(첨자아님)이므로,
    #    바로 앞이 'lo'(g) 또는 'l'(n) 인 경우는 제외.
    s = re.sub(r'(?<!lo)(?<!l)([a-zA-Z])(\d)(?=[^0-9]|$)', r'\1^{\2}', s)
    return s


# 첨자 그룹 `_{...}` 또는 `^{...}` (한 단계, 중첩 없는 단순 그룹) 내부만 치환.
GROUP = re.compile(r'([_^])\{([^{}]*)\}')


# log 밑이 거듭제곱: 'log_{2n}'·'log_{2k}' → 'log_{2^{n}}'.
# 로그 밑이 '숫자+단일영문자' 로 쓰인 건 사실상 항상 거듭제곱(밑 2^n). 일반 '_{2k}'(2k번째 항
# 같은 정당 케이스)는 안 건드리고 **log_ 문맥**에서만 친다.
LOGBASE = re.compile(r'(log)_\{(\d)([a-zA-Z])\}')


def fix_text(t: str) -> tuple[str, list]:
    changes = []

    def repl(m):
        sym, inner = m.group(1), m.group(2)
        fixed = _fix_group(inner)
        if fixed != inner:
            changes.append((f'{sym}{{{inner}}}', f'{sym}{{{fixed}}}'))
            return f'{sym}{{{fixed}}}'
        return m.group(0)

    out = GROUP.sub(repl, t)

    def logrepl(m):
        a, b, c = m.group(1), m.group(2), m.group(3)
        changes.append((f'{a}_{{{b}{c}}}', f'{a}_{{{b}^{{{c}}}}}'))
        return f'{a}_{{{b}^{{{c}}}}}'

    out = LOGBASE.sub(logrepl, out)
    return out, changes


def _searchable_block(md: str):
    m = re.search(r'(searchable_text:\s*\|\n)(.*?)(\n(?:[a-z_]+:|solution:))', md, re.S)
    return m


def main():
    args = [a for a in sys.argv[1:] if a != '--apply']
    apply = '--apply' in sys.argv
    mds = sorted(glob.glob(os.path.join(REPO, 'docs/problems/**/*.md'), recursive=True))
    if args:
        mds = [p for p in mds if any(a in p for a in args)]
    npatch = 0
    for mp in mds:
        txt = open(mp, encoding='utf-8').read()
        m = _searchable_block(txt)
        if not m:
            continue
        body = m.group(2)
        fixed, changes = fix_text(body)
        if not changes:
            continue
        npatch += 1
        rel = os.path.relpath(mp, REPO)
        print(f'{rel}:')
        for a, b in changes:
            print(f'    {a!r} → {b!r}')
        if apply:
            new = txt[:m.start(2)] + fixed + txt[m.end(2):]
            open(mp, 'w', encoding='utf-8').write(new)
    print(f'\n{"적용" if apply else "DRY-RUN"}: {npatch} md 패치')


if __name__ == '__main__':
    main()
