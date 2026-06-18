// Shared, PURE (string→string, no React/DOM) KaTeX normalization + strict
// policy. Imported by BOTH the client renderer (`mathish.tsx`) and the build
// chain (`astro.config.mjs`'s remarkKatexCompat + katexOptions) so syntheses /
// concepts / problems all render math with the *same* strength as the live
// client widgets.
//
// Lives as `.mjs` (not `.ts`) on purpose: `astro.config.mjs` is loaded by Node
// as native ESM, where importing a sibling `.ts` is fragile. A plain `.mjs`
// module imports cleanly from both the Node-loaded config and the TS client
// (tsconfig has `allowJs`).

/**
 * Normalize a LaTeX/math *segment* string before handing it to KaTeX.
 *
 * Two fixes, both born from real LLM-generated breakage:
 *
 *  1. Unescaped `%` → `\%`. In KaTeX/LaTeX `%` starts a comment, so
 *     `\text{171.8% 유효이자율}` lets the `%` swallow everything after it
 *     (the closing `}` / `$$`) → parse failure → raw text leaks to the page.
 *     Math-segment `%` is always a literal percent here, so escape it.
 *
 *  2. `\begin{align}` / `align*` / `eqnarray` → `aligned`. These are standard
 *     LaTeX but unsupported by KaTeX; LLM notes emit them routinely. Normalize
 *     to the closest supported environment instead of rendering a sea of red.
 *
 * IMPORTANT: apply this only to the *math segment* (the text between `$…$` /
 * inside a `math` node), never to whole prose — otherwise prose `%` and `50%`
 * outside math would get backslashed. Both callers already scope it that way.
 *
 * @param {string} tex
 * @returns {string}
 */
// \text{} 안에서 text mode hard-throw 를 일으키는 수학 관계/연산 유니코드 → 같은 글리프의 $math$ 섬.
const TEXT_MATH_SYM = [
  [/≠/g, '$\\ne$'], [/≤/g, '$\\le$'], [/≥/g, '$\\ge$'], [/≪/g, '$\\ll$'], [/≫/g, '$\\gg$'],
  [/⇔/g, '$\\Leftrightarrow$'], [/⇒/g, '$\\Rightarrow$'], [/⇐/g, '$\\Leftarrow$'],
  [/↔/g, '$\\leftrightarrow$'], [/→/g, '$\\to$'], [/←/g, '$\\leftarrow$'], [/↦/g, '$\\mapsto$'],
  [/×/g, '$\\times$'], [/÷/g, '$\\div$'], [/±/g, '$\\pm$'], [/∓/g, '$\\mp$'], [/⋅/g, '$\\cdot$'],
  [/≈/g, '$\\approx$'], [/≅/g, '$\\cong$'], [/≡/g, '$\\equiv$'], [/∝/g, '$\\propto$'], [/∼/g, '$\\sim$'],
  [/∈/g, '$\\in$'], [/∉/g, '$\\notin$'], [/∋/g, '$\\ni$'],
  [/⊂/g, '$\\subset$'], [/⊆/g, '$\\subseteq$'], [/⊃/g, '$\\supset$'], [/⊇/g, '$\\supseteq$'],
  [/∩/g, '$\\cap$'], [/∪/g, '$\\cup$'], [/∅/g, '$\\emptyset$'], [/∞/g, '$\\infty$'],
];

export function normalizeKatex(tex) {
  return tex
    .replace(/(?<!\\)%/g, '\\%')
    // 3. 다자리 아래/위첨자 brace 보정. `_10` 은 `_1` 만 첨자돼 `₁0` 으로 깨진다(₁₀P₃ 등
    //    조합·순열 기호). `_{10}` 으로 묶어 전체를 첨자화. 숫자 2자리+ 만(단일 `_n` 불변).
    //    (주의: \text{} 안 `$n$`·`$r$` 같은 다중 math 섬을 건드리는 규칙은 금물 — 짝을 깨
    //     수식 전체가 raw 로 노출됨. KaTeX 는 valid \text{$math$ 한글} 를 스스로 렌더한다.)
    .replace(/([_^])(\d{2,})/g, '$1{$2}')
    // 4. \text{} 안 곧은 ASCII 따옴표("…") → 곱슬 따옴표(“…”). KaTeX 는 스마트따옴표가 없어
    //    여닫이가 같은 곧은 글리프로 보인다. \text{} 안의 *짝지은* "…" 만 변환(내부 $n$·$r$
    //    math 섬은 [^"]* 가 $ 를 통과시켜 그대로 보존). \text 밖 math 의 " 는 안 건드림.
    // 4-b. \text{} 안의 수학 관계/연산 유니코드(≠ → × ÷ ± ≤ ≥ ⇒ ≈ ∈ …)를 $…$ 수식 섬으로.
    //    KaTeX 는 이들을 \mathrel/\mathbin 으로 매핑하는데 text mode 에선 "Can't use \mathrel
    //    in text mode" 로 **hard throw** → 수식 전체 raw 노출(예: \text{분자 ≠ 1인 …}). 같은
    //    글리프를 $\ne$ 처럼 math 섬으로 감싸면 정상 렌더. (\text 밖 math 의 유니코드는 안 건드림.)
    .replace(/\\text\{([^{}]*)\}/g, (_m, inner) => {
      let t = inner;
      for (const [re, rep] of TEXT_MATH_SYM) t = t.replace(re, rep);
      t = t.replace(/"([^"]*)"/g, '“$1”'); // 곧은 따옴표 → 곱슬(KaTeX 스마트따옴표 없음)
      return '\\text{' + t + '}';
    })
    .replace(/\\begin\{align\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{align\*?\}/g, '\\end{aligned}')
    .replace(/\\begin\{eqnarray\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{eqnarray\*?\}/g, '\\end{aligned}');
}

/**
 * KaTeX `strict` callback shared by client + build.
 *
 * Korean prose routinely puts Hangul inside `$…$` (set elements like
 * `{가, 나, 다}`), which trips `unicodeTextInMathMode` — one warning per
 * character, flooding the console. `\text{증가 → 감소}` with raw unicode
 * (→·×·≈ …) trips `unknownSymbol` similarly while still rendering the glyph
 * correctly. Muting *both* keeps the console quiet without changing output;
 * every other code (brace mismatch, undefined command, …) stays a real `warn`
 * so genuine LaTeX errors remain visible.
 *
 * @param {string} code
 * @returns {'ignore' | 'warn' | 'error'}
 */
export function KATEX_STRICT(code) {
  return code === 'unicodeTextInMathMode' || code === 'unknownSymbol' ? 'ignore' : 'warn';
}

// Muted error color for cases that DO fall through (unknown commands, brace
// mismatches the LLM still produces). Bright red `#cc0000` is too alarming for
// an otherwise-readable body; amber keeps it visible without making the whole
// note feel broken.
export const KATEX_ERROR_COLOR = '#a16207';

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
// KaTeX 가 `$...$` 안에서 원문자를 보게 escape 역변환.
function decodeHtml(s) {
  return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}

/**
 * `$$...$$`/`$...$` 가 섞인 평문을 KaTeX HTML 로 렌더한다. 정규화·strict·errorColor
 * 정책을 normalizeKatex/KATEX_STRICT/KATEX_ERROR_COLOR 로 통일 → 마크다운(rehype),
 * 클라이언트(mathish), 카드(서버)가 동일 렌더를 공유하는 SSOT 진입점.
 * katex 인스턴스를 인자로 받아(이 모듈은 katex 를 import 안 함 → 클라 번들 안 불림)
 * 서버는 `import katex`, 클라는 `ensureKatex()` 결과를 넘긴다.
 * @param {string} text
 * @param {{renderToString:(t:string,o?:object)=>string}} katex
 * @param {{display?:boolean, auto?:boolean}} [opts]
 * @returns {string} HTML
 */
export function renderMathSegments(text, katex, opts = {}) {
  if (!text) return '';
  const { display = false, auto = false } = opts;
  const ren = (tex, displayMode) =>
    katex.renderToString(normalizeKatex(decodeHtml(tex)), {
      displayMode, throwOnError: false, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR,
    });
  try {
    if (display && text.includes('$$')) {
      let out = escapeHtml(text).replace(/\$\$([^$]+?)\$\$/g, (_, t) => ren(t, true));
      return out.replace(/\$([^\n$]+?)\$/g, (_, t) => ren(t, false));
    }
    if (text.includes('$')) {
      let out = escapeHtml(text);
      // `$$...$$` 를 먼저 소비(안 하면 인라인 정규식이 안쪽만 잡아 바깥 `$` 가 남음).
      if (out.includes('$$')) out = out.replace(/\$\$([^$]+?)\$\$/g, (_, t) => ren(t, false));
      return out.replace(/\$([^\n$]+?)\$/g, (_, t) => ren(t, false));
    }
    if (auto) {
      // 한글/CJK 토큰은 \text{} 로 감싸 unicodeTextInMathMode 경고 회피.
      const wrapped = text.replace(/([ㄱ-힝]+|[一-鿿]+|[가-힣]+)/g, '\\text{$1}');
      return ren(wrapped, false);
    }
    return escapeHtml(text);
  } catch {
    return escapeHtml(text);
  }
}
