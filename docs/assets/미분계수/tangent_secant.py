"""
Tangent vs secant line comparison for f(x) = x² at x = 1.
Demonstrates the limit definition of the derivative (미분계수).

  f'(1) = lim_{h→0} [f(1+h) - f(1)] / h

Verification (D11): sympy confirms f'(1) = 2.
Output (D16 L3):  tangent_secant.svg in this directory.
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

# 한글 폰트 설정 (없으면 그대로 두기)
for candidate in ['NanumGothic', 'Noto Sans CJK KR', 'Source Han Sans KR']:
    if any(candidate in f.name for f in mpl.font_manager.fontManager.ttflist):
        mpl.rcParams['font.family'] = candidate
        break
mpl.rcParams['axes.unicode_minus'] = False

# ─── D11: sympy 검산 ──────────────────────────────────────────────
x = sp.symbols('x')
f = x**2
fprime = sp.diff(f, x)
slope_at_1 = fprime.subs(x, 1)
assert slope_at_1 == 2, f"Expected f'(1)=2, got {slope_at_1}"

# 한계 정의를 직접 평가해 같은 결과를 얻는지 확인
h = sp.symbols('h')
limit_form = sp.limit(((1 + h)**2 - 1**2) / h, h, 0)
assert limit_form == 2, f"Expected limit=2, got {limit_form}"
print(f"[sympy verify] f'(1) = {slope_at_1}  (한계정의: {limit_form})")

# ─── matplotlib 플롯 ──────────────────────────────────────────────
xs = np.linspace(-0.3, 2.3, 400)
fx = xs**2

fig, ax = plt.subplots(figsize=(7.5, 6))
ax.plot(xs, fx, color='#222', lw=2.2, label=r'$f(x)=x^{2}$')

# 접선 (tangent): y = 2(x - 1) + 1 = 2x - 1
tangent = 2 * xs - 1
ax.plot(xs, tangent, color='#c0392b', lw=2.2, label=r'tangent at $x{=}1$: $y=2x-1$')

# 점 (1, 1)
ax.plot([1], [1], 'o', color='#c0392b', ms=8, zorder=5)
ax.annotate(r'$(1, 1)$', xy=(1, 1), xytext=(1.05, 0.6), fontsize=11)

# 할선들 (secant): h = 1, 0.5, 0.25, 0.1
secant_colors = ['#3498db', '#2980b9', '#1abc9c', '#16a085']
for h_val, color in zip([1.0, 0.5, 0.25, 0.1], secant_colors):
    x1, y1 = 1.0, 1.0
    x2, y2 = 1.0 + h_val, (1.0 + h_val) ** 2
    slope = (y2 - y1) / h_val
    sx = np.linspace(-0.2, 2.2, 200)
    sy = slope * (sx - x1) + y1
    ax.plot(sx, sy, color=color, lw=1.2, alpha=0.85,
            label=fr'secant $h={h_val}$ (slope={slope:.3g})')
    ax.plot([x2], [y2], 'o', color=color, ms=5)

ax.set_xlim(-0.3, 2.3)
ax.set_ylim(-1.2, 5)
ax.axhline(0, color='#888', lw=0.6)
ax.axvline(0, color='#888', lw=0.6)
ax.grid(True, alpha=0.25)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(r"$h \to 0$ 으로 갈수록 할선의 기울기가 접선의 기울기 $f'(1)=2$ 로 수렴")
ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

out_path = Path(__file__).resolve().parent / 'tangent_secant.svg'
fig.savefig(out_path, format='svg', bbox_inches='tight')
print(f"[saved] {out_path}")
