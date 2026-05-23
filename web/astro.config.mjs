// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { visit } from 'unist-util-visit';

// KaTeX strict 모드: 한국어 콘텐츠라 `$...의 ...$` 같은 raw 한글이
// 자주 등장. `unicodeTextInMathMode` 만 ignore하고 나머지 (브래킷 불일치
// 등 실제 LaTeX 오류) 는 그대로 경고로 둔다. 파싱 실패시 표시되는
// errorColor 도 기본 빨강(#cc0000) 대신 amber 로 — 본문 한가운데 시뻘건
// 텍스트가 튀어나오는 사고를 막음. (LLM 이 만든 식이 종종 깨짐.)
const katexOptions = {
  strict: (code) => (code === 'unicodeTextInMathMode' ? 'ignore' : 'warn'),
  errorColor: '#a16207',
};

/**
 * Remark plugin: rewrite LaTeX environments that KaTeX doesn't support
 * (`align`, `align*`, `eqnarray`) to the closest supported equivalent
 * (`aligned`). LLM-generated notes routinely emit `\begin{align}` since
 * it's standard LaTeX, even though KaTeX rejects it. Rather than make
 * every author memorize the difference, normalize here.
 */
function remarkKatexCompat() {
  const rewrite = (src) => src
    .replace(/\\begin\{align\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{align\*?\}/g, '\\end{aligned}')
    .replace(/\\begin\{eqnarray\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{eqnarray\*?\}/g, '\\end{aligned}');
  return (tree) => {
    visit(tree, ['math', 'inlineMath'], (node) => {
      if (typeof node.value === 'string') node.value = rewrite(node.value);
    });
  };
}

/**
 * Remark plugin: rewrite asset paths and inter-doc links in markdown.
 *  - `(../)+assets/...` (image)               -> `/assets/...`
 *  - `(../)+<col>/<slug>.md`                  -> `/<col>/<slug>`  (cross-collection)
 *  - `./<slug>.md` or bare `<slug>.md`        -> `/<currentCollection>/<slug>` (sibling)
 *
 * Current collection is detected from the source file path
 * (`docs/<collection>/...`) via vfile.history/path.
 */
function remarkRewritePaths() {
  return (tree, file) => {
    const filePath = (file?.history?.[0] ?? file?.path ?? '').toString();
    const colMatch = filePath.match(/[\\/]docs[\\/](concepts|problems|mistakes|tools|syntheses)[\\/]/);
    const currentCol = colMatch ? colMatch[1] : null;

    visit(tree, 'image', (node) => {
      if (typeof node.url !== 'string') return;
      const m = node.url.match(/(?:\.\.\/)+assets\/(.+)$/);
      if (m) node.url = '/assets/' + m[1];
    });
    visit(tree, 'link', (node) => {
      if (typeof node.url !== 'string') return;
      // External / anchor / absolute — skip
      if (/^(https?:|mailto:|#|\/)/.test(node.url)) return;
      // ../<col>/<slug>.md or similar cross-collection
      const inter = node.url.match(/^(?:\.\.\/)+(concepts|problems|mistakes|tools|syntheses)\/([^/]+)\.md$/);
      if (inter) {
        node.url = `/${inter[1]}/${encodeURIComponent(inter[2])}`;
        return;
      }
      // ./<slug>.md or bare <slug>.md — sibling within current collection
      const sibling = node.url.match(/^(?:\.\/)?([^/]+)\.md$/);
      if (sibling && currentCol) {
        node.url = `/${currentCol}/${encodeURIComponent(sibling[1])}`;
        return;
      }
    });
  };
}

// https://astro.build/config
export default defineConfig({
  site: 'http://localhost:4321',
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  integrations: [
    react(),
    mdx({
      remarkPlugins: [remarkMath, remarkKatexCompat, remarkRewritePaths],
      rehypePlugins: [[rehypeKatex, katexOptions]],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
    server: {
      allowedHosts: [
        'localhost',
        '127.0.0.1',
        '.ts.net',           // any Tailscale MagicDNS hostname
        '.tailf47aa4.ts.net', // this tailnet specifically
      ],
    },
    // mathlive 는 ChatPanel 의 '∑ 수식' 버튼을 처음 누를 때 동적 import
    // 된다. dev 서버 startup 시 vite가 정적 import 만 스캔하므로 mathlive
    // 가 deps 캐시에 안 들어가고, 첫 동적 import 시 vite가 재최적화 →
    // 그동안 페이지가 들고있던 stale browser-hash URL이 504 로 깨짐.
    // 명시적으로 pre-bundle 시키면 startup 직후부터 deps 캐시에 존재해
    // 재최적화 사이클을 회피.
    optimizeDeps: {
      include: ['mathlive'],
    },
  },
  markdown: {
    remarkPlugins: [remarkMath, remarkKatexCompat, remarkRewritePaths],
    rehypePlugins: [[rehypeKatex, katexOptions]],
  },
});
