// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { visit } from 'unist-util-visit';
import { readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// 개념 leaf 이름 → 실제 중첩 slug 맵.
// 개념 .md 본문이 flat 링크(`/concepts/이차함수`)를 쓰는데 실제 라우트는 중첩
// (`/concepts/functions/middle-3/이차함수`)이라 통째로 404 나는 시스템 와이드 버그가
// 있다. 렌더 시 leaf 를 실제 slug 로 해석해 고친다(아래 remarkRewritePaths).
// readdir 은 macOS-origin 파일명이 NFD 라 세그먼트마다 NFC 정규화(Astro content id 와 일치).
const CONCEPT_LEAF_MAP = (() => {
  /** @type {Map<string, string>} */
  const map = new Map();
  /** @type {Map<string, number>} */
  const dups = new Map();
  let root;
  try { root = fileURLToPath(new URL('../docs/concepts', import.meta.url)); }
  catch { return map; }
  /** @param {string} dir @param {string} prefix */
  const walk = (dir, prefix) => {
    /** @type {import('node:fs').Dirent[]} */
    let ents = [];
    try { ents = readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const ent of ents) {
      const nfc = ent.name.normalize('NFC');
      if (ent.isDirectory()) {
        walk(`${dir}/${ent.name}`, prefix ? `${prefix}/${nfc}` : nfc);
      } else if (ent.name.endsWith('.md')) {
        const leaf = nfc.replace(/\.md$/, '');
        const full = prefix ? `${prefix}/${leaf}` : leaf;
        // 첫 매칭 우선. 같은 leaf 가 여러 경로에 있으면(드묾) 카운트해 경고.
        if (map.has(leaf)) dups.set(leaf, (dups.get(leaf) ?? 1) + 1);
        else map.set(leaf, full);
      }
    }
  };
  walk(root, '');
  if (dups.size) console.warn(`[concept-links] 중복 leaf ${dups.size}개 — 첫 경로로 해석:`, [...dups.keys()].slice(0, 8).join(', '));
  return map;
})();

// KaTeX strict 모드: 한국어 콘텐츠라 `$...의 ...$` 같은 raw 한글이
// 자주 등장. `unicodeTextInMathMode` 만 ignore하고 나머지 (브래킷 불일치
// 등 실제 LaTeX 오류) 는 그대로 경고로 둔다. 파싱 실패시 표시되는
// errorColor 도 기본 빨강(#cc0000) 대신 amber 로 — 본문 한가운데 시뻘건
// 텍스트가 튀어나오는 사고를 막음. (LLM 이 만든 식이 종종 깨짐.)
const katexOptions = {
  strict: (/** @type {string} */ code) => (code === 'unicodeTextInMathMode' ? 'ignore' : 'warn'),
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
  const rewrite = (/** @type {string} */ src) => src
    .replace(/\\begin\{align\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{align\*?\}/g, '\\end{aligned}')
    .replace(/\\begin\{eqnarray\*?\}/g, '\\begin{aligned}')
    .replace(/\\end\{eqnarray\*?\}/g, '\\end{aligned}');
  return (/** @type {any} */ tree) => {
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
  return (/** @type {any} */ tree, /** @type {any} */ file) => {
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
      // `/concepts/<leaf>` (flat 단일 세그먼트) → 실제 중첩 slug 로 해석. 개념 본문
      // 링크가 flat 인데 라우트는 중첩이라 404 나는 시스템 와이드 버그 보정.
      // leaf 가 top-level(맵값==leaf)이거나 맵에 없으면 원본 유지.
      const flat = node.url.match(/^\/concepts\/([^/?#]+)\/?$/);
      if (flat) {
        let leaf = flat[1];
        try { leaf = decodeURIComponent(leaf); } catch { /* already raw */ }
        leaf = leaf.normalize('NFC');
        const full = CONCEPT_LEAF_MAP.get(leaf);
        if (full && full !== leaf) node.url = '/concepts/' + full;
        return;
      }
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

/**
 * Remark plugin: strip the legacy `## 풀이 (학습 시 채워짐)` placeholder section
 * from problem bodies. 이 섹션은 SolutionPanel(검증된 풀이 캐시)로 대체돼 중복.
 * 해당 heading + 다음 heading 전까지(placeholder 문단) 제거. 파일을 건드리지
 * 않고 렌더 시점에만 제거 → 백그라운드 빌드(frontmatter write)와 충돌 없음.
 * "학습 시 채워짐" 텍스트로 스코프되므로 실제 풀이가 적힌 경우엔 매칭 안 됨.
 */
function remarkStripSolutionPlaceholder() {
  return (/** @type {any} */ tree) => {
    const kids = tree.children;
    if (!Array.isArray(kids)) return;
    for (let i = 0; i < kids.length; i++) {
      const node = kids[i];
      if (node.type !== 'heading' || node.depth !== 2) continue;
      const text = (node.children || []).map((/** @type {any} */ c) => c.value || '').join('');
      if (!(text.includes('풀이') && text.includes('학습 시 채워짐'))) continue;
      let j = i + 1;
      while (j < kids.length && kids[j].type !== 'heading') j++;
      kids.splice(i, j - i);
      i--;
    }
  };
}

// https://astro.build/config
export default defineConfig({
  site: 'http://localhost:4321',
  output: 'server',
  devToolbar: { enabled: false },  // 하단 Astro dev 툴바 숨김
  adapter: node({ mode: 'standalone' }),
  integrations: [
    react(),
    mdx({
      remarkPlugins: [remarkMath, remarkKatexCompat, remarkRewritePaths, remarkStripSolutionPlaceholder],
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
    //
    // @xyflow/react 도 동일: /graph 의 ConceptDAG 는 client:only 아일랜드라
    // startup 스캔에 안 잡혀, /graph 첫 방문 시 vite가 @xyflow 를 뒤늦게
    // 발견→재최적화→그 페이지의 stale hash 가 504(Outdated Optimize Dep)로
    // 깨지고 노드가 안 보였다. pre-bundle 로 회피.
    optimizeDeps: {
      include: ['mathlive', '@xyflow/react'],
    },
  },
  markdown: {
    remarkPlugins: [remarkMath, remarkKatexCompat, remarkRewritePaths, remarkStripSolutionPlaceholder],
    rehypePlugins: [[rehypeKatex, katexOptions]],
  },
});
