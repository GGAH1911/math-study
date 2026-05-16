// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { visit } from 'unist-util-visit';

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
      remarkPlugins: [remarkMath, remarkRewritePaths],
      rehypePlugins: [rehypeKatex],
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
  },
  markdown: {
    remarkPlugins: [remarkMath, remarkRewritePaths],
    rehypePlugins: [rehypeKatex],
  },
});
