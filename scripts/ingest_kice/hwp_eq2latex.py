r"""HWP 수식 스크립트 → LaTeX 트랜스파일러.

한컴 HWP 수식 편집기 스크립트(공식 명세 '한글문서파일형식_수식_revision1.3')를 LaTeX 로 변환.
HWP 수식은 .hwp 파일 안에 이 스크립트(구조 원본)로 저장되므로, PDF 기하 추측 없이 완벽 변환 가능.

문법 요약(명세 1.2):
  A over B → \frac{A}{B}      A atop B → {A \atop B}
  sqrt X → \sqrt{X}           root N of X → \sqrt[N]{X}
  X ^{Y} / X SUP Y → X^{Y}    X _{Y} / X SUB Y → X_{Y}
  LEFT ( … RIGHT ) → \left( … \right)
  TIMES → \times   sum/int/lim → \sum \int \lim (한계는 _ ^ 로 붙음)
  cases { A # B } → \begin{cases} A \\ B \end{cases}
  { } 묶음, # 줄바꿈, & 정렬, ~ 빈칸, ` 1/4빈칸
"""
from __future__ import annotations
import re

GREEK = {
    'alpha': r'\alpha', 'beta': r'\beta', 'gamma': r'\gamma', 'delta': r'\delta',
    'epsilon': r'\epsilon', 'varepsilon': r'\varepsilon', 'zeta': r'\zeta', 'eta': r'\eta',
    'theta': r'\theta', 'vartheta': r'\vartheta', 'iota': r'\iota', 'kappa': r'\kappa',
    'lambda': r'\lambda', 'mu': r'\mu', 'nu': r'\nu', 'xi': r'\xi', 'pi': r'\pi',
    'rho': r'\rho', 'sigma': r'\sigma', 'tau': r'\tau', 'upsilon': r'\upsilon',
    'phi': r'\phi', 'varphi': r'\varphi', 'chi': r'\chi', 'psi': r'\psi', 'omega': r'\omega',
    'Gamma': r'\Gamma', 'Delta': r'\Delta', 'Theta': r'\Theta', 'Lambda': r'\Lambda',
    'Xi': r'\Xi', 'Pi': r'\Pi', 'Sigma': r'\Sigma', 'Phi': r'\Phi', 'Psi': r'\Psi', 'Omega': r'\Omega',
}
FUNC = {'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'ln', 'lg', 'max', 'min',
        'exp', 'sinh', 'cosh', 'tanh', 'arcsin', 'arccos', 'arctan', 'det', 'gcd',
        'lcm', 'mod', 'deg', 'lim', 'Lim', 'arg', 'dim', 'ker', 'hom', 'Pr'}
_DIG_GREEK = re.compile(r'^(\d+)(' + '|'.join(GREEK) + r')$')
_FONTCMD = {'rm', 'it', 'bold', 'sf', 'tt', 'sout'}
SYM = {
    'times': r'\times', 'cdot': r'\cdot', 'div': r'\div', 'pm': r'\pm', 'mp': r'\mp',
    'leq': r'\leq', 'geq': r'\geq', 'neq': r'\neq', 'sim': r'\sim', 'simeq': r'\simeq',
    'approx': r'\approx', 'equiv': r'\equiv', 'propto': r'\propto',
    'infty': r'\infty', 'inf': r'\infty', 'partial': r'\partial', 'nabla': r'\nabla',
    'cdots': r'\cdots', 'ldots': r'\ldots', 'dots': r'\dots', 'vdots': r'\vdots',
    'rightarrow': r'\rightarrow', 'leftarrow': r'\leftarrow', 'to': r'\to',
    'rarrow': r'\rightarrow', 'larrow': r'\leftarrow', 'lrarrow': r'\leftrightarrow',
    'uparrow': r'\uparrow', 'downarrow': r'\downarrow', 'Rarrow': r'\Rightarrow',
    'Rightarrow': r'\Rightarrow', 'Leftarrow': r'\Leftarrow', 'leftrightarrow': r'\leftrightarrow',
    'in': r'\in', 'notin': r'\notin', 'subset': r'\subset', 'subseteq': r'\subseteq',
    'supset': r'\supset', 'cup': r'\cup', 'cap': r'\cap', 'emptyset': r'\emptyset',
    'forall': r'\forall', 'exists': r'\exists', 'angle': r'\angle', 'perp': r'\perp',
    'parallel': r'\parallel', 'prime': r"'", 'circ': r'\circ', 'degree': r'^{\circ}',
    'sum': r'\sum', 'prod': r'\prod', 'int': r'\int', 'oint': r'\oint',
}
DELIM = {'(': '(', ')': ')', '[': '[', ']': ']', '|': '|', '{': r'\{', '}': r'\}', '.': '.', 'LBRACE': r'\{', 'RBRACE': r'\}'}


def _clean(s: str) -> str:
    """추출 잡음 제거. HWP 수식 스크립트는 순수 ASCII 명령어 → ASCII+한글만 남기고
    Ұ(0x04B0) 같은 종결자·바이너리 잔재 제거."""
    s = ''.join(ch for ch in s if 0x20 <= ord(ch) < 0x7F or 0xAC00 <= ord(ch) <= 0xD7A3 or ch == '\t')
    s = s.strip()
    s = re.sub(r"^['\";:`]+", '', s)  # 선행 따옴표/백틱/세미콜론 잔재 제거
    s = re.sub(r'^[A-Za-z](?=LEFT|RIGHT|sqrt|root|sum|int|lim)', '', s)  # 'ALEFT' 류
    return s.strip()


def _tokenize(s: str):
    s = s.replace('`', ' ').replace('~', ' ')  # 빈칸 명령 → 공백
    s = s.replace('{', ' { ').replace('}', ' } ')
    s = re.sub(r'(\^|_)', r' \1 ', s)
    return [t for t in s.split(' ') if t != '']


def _nest(tokens):
    """{ } 로 중첩 리스트 구성."""
    stack = [[]]
    for t in tokens:
        if t == '{':
            new = []
            stack[-1].append(new)
            stack.append(new)
        elif t == '}':
            if len(stack) > 1:
                stack.pop()
        else:
            stack[-1].append(t)
    return stack[0]


def _tok2tex(t: str) -> str:
    if t in _FONTCMD:
        return ''  # rm/it/bold 등 글꼴명령 → 드롭(텍스트는 그대로 렌더됨)
    if t in GREEK:
        return GREEK[t]
    m = _DIG_GREEK.match(t)  # 2pi → 2\pi
    if m:
        return m.group(1) + GREEK[m.group(2)]
    low = t.lower()
    if low in GREEK:
        return GREEK[low]
    if low in FUNC:
        return '\\' + ('lim' if low == 'lim' else low)
    if low in SYM:
        return SYM[low]
    if t == '#':
        return r' \\ '
    if t == '&':
        return ' & '
    if t in ('~', '`'):
        return r'\,'
    return t


def _braces(x: str) -> str:
    x = x.strip()
    if x.startswith('{') and x.endswith('}'):
        return x
    return '{' + x + '}'


def _render(seq) -> str:
    atoms = []  # 렌더된 latex 조각들
    i, n = 0, len(seq)

    def render_next(j):
        """seq[j] 한 원자를 렌더하고 다음 인덱스 반환."""
        if j >= n:
            return '{}', j
        it = seq[j]
        if isinstance(it, list):
            return '{' + _render(it) + '}', j + 1
        return _braces(_tok2tex(it)), j + 1

    while i < n:
        it = seq[i]
        if isinstance(it, list):
            atoms.append('{' + _render(it) + '}')
            i += 1
            continue
        low = it.lower()
        if low in ('over', 'atop'):
            num = atoms.pop() if atoms else '{}'
            den, i = render_next(i + 1)
            if low == 'over':
                atoms.append('\\frac' + _braces(num) + _braces(den))
            else:
                atoms.append('{' + num.strip('{}') + ' \\atop ' + den.strip('{}') + '}')
        elif low == 'sqrt':
            rad, i = render_next(i + 1)
            atoms.append('\\sqrt' + _braces(rad))
        elif low == 'root':
            idx, i = render_next(i + 1)
            if i < n and isinstance(seq[i], str) and seq[i].lower() == 'of':
                i += 1
            rad, i = render_next(i)
            atoms.append('\\sqrt[' + idx.strip('{}') + ']' + _braces(rad))
        elif it == '^' or low == 'sup':
            sup, i = render_next(i + 1)
            frag = '^' + _braces(sup)
            if atoms:
                atoms[-1] += frag
            else:
                atoms.append(frag)
        elif it == '_' or low == 'sub':
            sub, i = render_next(i + 1)
            frag = '_' + _braces(sub)
            if atoms:
                atoms[-1] += frag
            else:
                atoms.append(frag)
        elif low == 'left':
            delim = seq[i + 1] if i + 1 < n and isinstance(seq[i + 1], str) else '.'
            atoms.append('\\left' + DELIM.get(delim, delim))
            i += 2
        elif low == 'right':
            delim = seq[i + 1] if i + 1 < n and isinstance(seq[i + 1], str) else '.'
            atoms.append('\\right' + DELIM.get(delim, delim))
            i += 2
        elif low == 'cases':
            body, i = render_next(i + 1)
            inner = body.strip('{}')
            atoms.append('\\begin{cases}' + inner + '\\end{cases}')
        elif low in ('matrix', 'pile', 'lpile', 'rpile'):
            body, i = render_next(i + 1)
            inner = body.strip('{}')
            atoms.append('\\begin{matrix}' + inner + '\\end{matrix}')
        else:
            atoms.append(_tok2tex(it))
            i += 1
    return ' '.join(a for a in atoms if a != '')


def eq2latex(script: str) -> str:
    """HWP 수식 스크립트 → LaTeX 본문(델리미터 없이)."""
    s = _clean(script)
    if not s:
        return ''
    # LEFT/RIGHT 뒤 중괄호 델리미터를 그룹기호 { } 와 분리(LBRACE/RBRACE 토큰)
    s = re.sub(r'\bLEFT\s+\{', 'LEFT LBRACE ', s)
    s = re.sub(r'\bLEFT\s+\}', 'LEFT RBRACE ', s)
    s = re.sub(r'\bRIGHT\s+\}', 'RIGHT RBRACE ', s)
    s = re.sub(r'\bRIGHT\s+\{', 'RIGHT LBRACE ', s)
    seq = _nest(_tokenize(s))
    out = _render(seq)
    out = re.sub(r'\s+', ' ', out).strip()
    return out


if __name__ == '__main__':
    tests = [
        'root {3} of {9} TIMES 3 ^{{1} over {3}}',
        '{5} over {3} pi',
        'LEFT ( x ^{2} - {1} over {x} RIGHT ) ^{2} LEFT ( x-2 RIGHT ) ^{5}',
        'sum _{n=1} ^{20} LEFT ( -1 RIGHT ) ^{n} n ^{2}',
        'sum _{k=1} ^{4} a _{k} =45',
        '- {2 sqrt {5}} over {5}',
        'cases {2x+y=4 # 3x-4y=-1}',
        'y= lim _{x -> 0} {{1} over {x}}',
        'int _1 ^2 {3x ^{2}} dx',
    ]
    for t in tests:
        print(f'{t}\n  → {eq2latex(t)}\n')
