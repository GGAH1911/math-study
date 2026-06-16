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
export function normalizeKatex(tex) {
  return tex
    .replace(/(?<!\\)%/g, '\\%')
    // 3. 한글을 감싼 나머지 `$…$` 제거. LLM 이 `\text{$n개의 …$}` 처럼 \text{} 안에서
    //    `$…$` 로 math 모드를 켜고 한글을 넣는 오용 → math 모드의 한글은 자간이 뭉개진다.
    //    delimiter 만 제거하면 평문(\text 안)으로 정상 렌더. `$n$`(비한글 math)은 보존.
    .replace(/\$([^$]*[가-힣][^$]*)\$/g, '$1')
    // 4. 다자리 아래/위첨자 brace 보정. `_10` 은 `_1` 만 첨자돼 `₁0` 으로 깨진다(₁₀P₃ 등
    //    조합·순열 기호). `_{10}` 으로 묶어 전체를 첨자화. 숫자 2자리+ 만(단일 `_n` 불변).
    .replace(/([_^])(\d{2,})/g, '$1{$2}')
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
