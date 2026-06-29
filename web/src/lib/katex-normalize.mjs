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
    .replace(/\\end\{eqnarray\*?\}/g, '\\end{aligned}')
    // 5. 가동첨자(movable-limits) 연산자의 첨자를 인라인($...$, textstyle)에서도 위아래로 쌓이게(\limits).
    //    인라인 기본은 첨자가 옆으로 가는데(∑_{k} → ∑ 옆), display 처럼 위아래로 = 교과서식.
    //    포함: lim류·max·min·sup·inf·gcd·det·arg·Pr·∑·∏·∐·⋃·⋂·⨁ 등 큰 연산자.
    //    ★제외: \int·\iint·\oint(적분)은 관례상 옆이 표준 → 목록 미포함.
    //    lookahead(다음이 글자/역슬래시면 제외)로 \limits 자체·이중적용·\infty(\inf+ty) 등 오염 방지.
    //    긴 이름 우선 정렬(liminf 가 lim 보다 먼저)로 부분매치 방지.
    .replace(
      /\\(?:varlimsup|varliminf|limsup|liminf|projlim|injlim|lim|max|min|sup|inf|gcd|det|arg|Pr|sum|prod|coprod|bigcup|bigcap|bigsqcup|bigoplus|bigotimes|bigodot|biguplus|bigvee|bigwedge)(?![a-zA-Z\\])/g,
      (m) => m + '\\limits',
    );
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

// HTML entity → KaTeX 가 이해하는 원문자/LaTeX. `&le;`/`&lt;=` 등 관계기호도 복원.
// (이전 ChatPanel.decodeEntities 와 동일 — 여기로 이전해 SSOT 화.)
export function decodeEntities(s) {
  return s
    .replace(/&amp;(le|ge)=?;/g, (_, k) => (k === 'le' ? '\\le' : '\\ge'))
    .replace(/&le;=?/g, '\\le').replace(/&ge;=?/g, '\\ge')
    .replace(/&lt;=/g, '\\le').replace(/&gt;=/g, '\\ge')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
}

// raw(마커 빠진) 부등호 chain·LaTeX 명령어 복원용 패턴 (ChatPanel 에서 이전).
const MATH_TOKEN = String.raw`(?:[A-Za-z0-9\-+*/^=,.]+|\\[A-Za-z]+(?:\{[^}]*\})*|\||\(|\)|\{|\})`;
const ENTITY_OP = String.raw`(?:&lt;|&gt;|&le;|&ge;|&amp;le;|&amp;ge;)=?`;
const INEQUALITY_RUN = new RegExp(`(${MATH_TOKEN}(?:\\s+${MATH_TOKEN})*)(\\s*${ENTITY_OP}\\s*${MATH_TOKEN}(?:\\s+${MATH_TOKEN})*)+`, 'g');
const LATEX_CMD_RUN = /(\\[A-Za-z]+(?:\{[^}]{0,80}\})*(?:\s+(?![A-Za-z]{3,}(?![A-Za-z]))[A-Za-z0-9\-+*/^=.,()|\\{}]+)*)/g;

// LLM 이 `$` 마커를 빠뜨린 raw 부등호/명령어를 수학 문맥에서만 KaTeX 로 복원.
// 실패하면 원본 유지(throwOnError:true 고정 — 복구는 항상 안전 폴백). HTML 태그 영역은 skip.
export function recoverBareMath(html, katex) {
  // ★이미 렌더된 KaTeX 스팬을 마스킹한 뒤 복구한다. 안 하면 아래 bare-command 복구(LATEX_CMD_RUN)가
  //   렌더 결과의 <annotation>(LaTeX 원본=인용 SSOT) 안에 든 raw `\frac{…}` 등을 *또* 렌더해
  //   annotation 을 중첩 KaTeX 로 오염시킨다 → 시각은 .katex-html 이라 멀쩡하지만 드래그 인용이
  //   annotation 을 읽어 "f(x) =" 처럼 잘린다. (display 수식 + 분수/근호 등에서 재현.)
  // 플레이스홀더 경계는 MATH_TOKEN/명령/엔티티 패턴 어디에도 안 걸리는 제어문자 → 인접 수식런에 안 휩쓸림.
  const SENT = String.fromCharCode(1);
  const masks = [];
  {
    let masked = '', i = 0;
    while (i < html.length) {
      const s = html.indexOf('<span class="katex', i);
      if (s === -1) { masked += html.slice(i); break; }
      masked += html.slice(i, s);
      const re = /<span\b|<\/span>/g; re.lastIndex = s;
      let depth = 0, end = html.length, m;
      while ((m = re.exec(html))) {
        if (m[0] === '</span>') { if (--depth === 0) { end = m.index + m[0].length; break; } }
        else depth++;
      }
      masks.push(html.slice(s, end));
      masked += `${SENT}${masks.length - 1}${SENT}`;
      i = end;
    }
    html = masked;
  }
  html = html.replace(INEQUALITY_RUN, (full) => {
    if (/[<>]/.test(full)) return full;
    try { return katex.renderToString(decodeEntities(full), { displayMode: false, throwOnError: true, strict: KATEX_STRICT }); } catch { return full; }
  });
  html = html.replace(LATEX_CMD_RUN, (full) => {
    if (/[<>]/.test(full)) return full;
    const tex = decodeEntities(full).trim();
    if (tex.length < 2) return full;
    try { return katex.renderToString(tex, { displayMode: false, throwOnError: true, strict: KATEX_STRICT }); } catch { return full; }
  });
  // 마스크 복원 — 렌더된 KaTeX 스팬 원본 그대로.
  html = html.replace(new RegExp(`${SENT}(\\d+)${SENT}`, 'g'), (_, n) => masks[+n]);
  return html;
}

/**
 * `$$...$$`/`$...$` 를 KaTeX HTML 로 렌더하는 **단일 진입점(SSOT)**. normalizeKatex·
 * KATEX_STRICT·KATEX_ERROR_COLOR·decodeEntities·recoverBareMath 정책을 공유 →
 * 챗(ChatPanel)·클라(mathish)·카드(서버)가 동일 렌더.
 * katex 인스턴스를 인자로 받음(이 모듈은 katex 를 import 안 함 → 클라 번들 안 불림).
 *
 * opts:
 *  - htmlInput: 입력이 이미 마크다운 렌더된 HTML(태그 포함). true 면 escape 안 함.
 *      (false=평문 → escapeHtml 선행. 카드/짧은 라벨용.)
 *  - display:  `$$…$$` 를 display 모드로. 미지정 시 htmlInput 값을 따름
 *      (챗=display, 평문=inline). 마크다운 멀티라인 `<br/>`→`\n` 복원 포함.
 *  - auto:     `$` 없는 순수 LaTeX 라벨을 통째 렌더(한글 토큰 \text{} 래핑). 평문 전용.
 *  - recoverBare: 마커 빠진 raw 수식 복원(recoverBareMath). 챗 전용.
 *  - throwOnError: 기본 true — 실패 시 원본 `$…$` 텍스트 유지(앰버 에러 HTML 아님).
 *
 * 불변식: {htmlInput:true, recoverBare:true} 호출은 (구) ChatPanel.applyKatex 와
 * 바이트 동일(scripts/katex-harness.mjs 가 매 실행 검증).
 */
export function renderMathSegments(text, katex, opts = {}) {
  if (!text) return '';
  const { htmlInput = false, display, auto = false, recoverBare = false, throwOnError = true } = opts;
  const ddDisplay = display === undefined ? htmlInput : display;

  // auto: `$` 없는 평문을 통째 LaTeX 로(한글/CJK 토큰은 \text{} 로 감싸 경고 회피).
  if (auto && !htmlInput && !text.includes('$')) {
    try {
      const wrapped = text.replace(/([ㄱ-힝]+|[一-鿿]+|[가-힣]+)/g, '\\text{$1}');
      return katex.renderToString(normalizeKatex(wrapped), { displayMode: false, throwOnError, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR });
    } catch { return escapeHtml(text); }
  }

  let html = htmlInput ? text : escapeHtml(text);
  // 1) $$…$$ — <br/>(마크다운 멀티라인)→\n 복원. <> 가드로 stray $ 폭주 방지.
  html = html.replace(/\$\$((?:<br\s*\/?>|[^<>])+?)\$\$/g, (m, tex) => {
    try {
      const clean = decodeEntities(tex.replace(/<br\s*\/?>/g, '\n'));
      return katex.renderToString(normalizeKatex(clean), { displayMode: ddDisplay, throwOnError, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR });
    } catch { return m; }
  });
  // 2) $…$ — \text{} 안 중첩 $ 허용 + <> 태그 가드.
  html = html.replace(/\$((?:\\text\{[^{}]*\}|[^\n$<>])+?)\$/g, (m, tex) => {
    try {
      return katex.renderToString(normalizeKatex(decodeEntities(tex)), { displayMode: false, throwOnError, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR });
    } catch { return m; }
  });
  // 3) 마커 빠진 raw 수식 복원(챗 전용).
  if (recoverBare) html = recoverBareMath(html, katex);
  return html;
}
