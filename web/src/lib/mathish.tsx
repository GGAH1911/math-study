// Shared KaTeX rendering + text helpers used by all graphic components
// (Graph, Geometry, Numberline, StatsChart, GraphicsTest, etc.).
//
// Before this lived as four near-identical copies — each module had its own
// `XxxLabel` component that loaded KaTeX, escaped HTML, and parsed `$...$`.
// The duplication drifted (e.g. some forgot to support bare LaTeX, others
// had slightly different escape sequences). This module is the single
// source of truth.

import { useEffect, useState } from 'react';
// Pure string→string normalization + strict policy live in a shared `.mjs`
// module so the build chain (astro.config.mjs) renders syntheses/concepts/
// problems with the *same* strength as these client widgets. Re-exported
// below so existing `from './mathish'` importers keep working unchanged.
import { normalizeKatex, KATEX_STRICT, KATEX_ERROR_COLOR } from './katex-normalize.mjs';

export { normalizeKatex, KATEX_STRICT, KATEX_ERROR_COLOR };

// Cached KaTeX singleton — once one component loads it, all share the same
// instance via `window.katex`. function-plot also pulls KaTeX in, so most
// of the time it's already loaded by the time we ask.
type KatexStrictReturn = 'ignore' | 'warn' | 'error';
type KatexOpts = {
  displayMode?: boolean;
  throwOnError?: boolean;
  errorColor?: string;
  strict?: KatexStrictReturn | ((code: string) => KatexStrictReturn);
};
type Katex = { renderToString: (tex: string, opts?: KatexOpts) => string };
let _katex: Katex | null = null;

export async function ensureKatex(): Promise<Katex | null> {
  if (_katex) return _katex;
  if (typeof window === 'undefined') return null;
  const w = window as Window & { katex?: Katex };
  if (w.katex) { _katex = w.katex; return _katex; }
  try {
    const mod = await import('katex');
    _katex = (mod.default ?? mod) as Katex;
    w.katex = _katex;
    return _katex;
  } catch {
    return null;
  }
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Render `text` with KaTeX. Three modes (in priority order):
//   1. text contains `$$...$$`  → display-mode KaTeX (when `display` true)
//   2. text contains `$...$`    → inline KaTeX on the wrapped segments
//   3. text has no `$` and `auto`=true → render the whole string as LaTeX
//   else → plain escaped text
//
// If KaTeX fails to load or render, we fall back to the escaped plain text
// so the user always sees *something* rather than an empty string.
export type MathishProps = {
  text: string;
  /** Treat a bare (no `$`) string as raw LaTeX. Useful for short labels. */
  auto?: boolean;
  /** Allow `$$...$$` display-mode equations. */
  display?: boolean;
  className?: string;
};

export function MathishText({ text, auto = false, display = false, className }: MathishProps) {
  const [html, setHtml] = useState<string>('');
  useEffect(() => {
    if (!text) { setHtml(''); return; }
    let cancelled = false;
    (async () => {
      const k = await ensureKatex();
      if (!k) { if (!cancelled) setHtml(escapeHtml(text)); return; }
      try {
        let out: string;
        if (display && text.includes('$$')) {
          out = escapeHtml(text).replace(/\$\$([^$]+?)\$\$/g, (_, tex) =>
            k.renderToString(normalizeKatex(decodeHtml(tex)), { displayMode: true, throwOnError: false, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR }));
          // Then inline pass on remaining `$...$`
          out = out.replace(/\$([^\n$]+?)\$/g, (_, tex) =>
            k.renderToString(normalizeKatex(decodeHtml(tex)), { displayMode: false, throwOnError: false, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR }));
        } else if (text.includes('$')) {
          out = escapeHtml(text);
          // display=false 인 기본 경로에서도 `$$...$$` 를 먼저 소비한다. 안 하면
          // 아래 인라인 정규식 `\$([^\n$]+?)\$` 가 `$$x$$` 의 안쪽 `$x$` 만 잡아
          // 바깥 `$` 두 개가 stray literal 로 화면에 남는다. (display 미요청이므로
          // 인라인 모드로 렌더.)
          if (out.includes('$$')) {
            out = out.replace(/\$\$([^$]+?)\$\$/g, (_, tex) =>
              k.renderToString(normalizeKatex(decodeHtml(tex)), { displayMode: false, throwOnError: false, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR }));
          }
          out = out.replace(/\$([^\n$]+?)\$/g, (_, tex) =>
            k.renderToString(normalizeKatex(decodeHtml(tex)), { displayMode: false, throwOnError: false, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR }));
        } else if (auto) {
          // 한글/CJK 문자가 섞이면 그 토큰을 \text{...} 로 감싸 KaTeX 의
          // unicodeTextInMathMode warning 회피. 영문/수식 토큰은 math 모드 유지.
          const wrapped = text.replace(/([ㄱ-힝]+|[一-鿿]+|[가-힣]+)/g, '\\text{$1}');
          out = k.renderToString(normalizeKatex(wrapped), { displayMode: false, throwOnError: false, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR });
        } else {
          out = escapeHtml(text);
        }
        if (!cancelled) setHtml(out);
      } catch {
        if (!cancelled) setHtml(escapeHtml(text));
      }
    })();
    return () => { cancelled = true; };
  }, [text, auto, display]);
  if (!text) return null;
  return <span className={className} dangerouslySetInnerHTML={{ __html: html || escapeHtml(text) }} />;
}

// Reverse the HTML-escape we applied so KaTeX sees the original characters
// inside the `$...$` capture. Otherwise `&lt;`, `&gt;` etc. break math.
function decodeHtml(s: string): string {
  return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}
