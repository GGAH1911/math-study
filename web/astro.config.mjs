// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { visit } from 'unist-util-visit';

/**
 * Remark plugin: rewrite asset paths and inter-doc links in markdown.
 *  - `(../)+assets/...` (image URL)        -> `/assets/...`  (docs/assets is mirrored to public/assets)
 *  - `(../)*<col>/<slug>.md` (link URL)    -> `/<col>/<slug>` (encoded)
 *  - `<slug>.md` (sibling link)            -> left alone; collection page handles
 */
function remarkRewritePaths() {
  return (tree) => {
    visit(tree, 'image', (node) => {
      if (typeof node.url !== 'string') return;
      const m = node.url.match(/(?:\.\.\/)+assets\/(.+)$/);
      if (m) node.url = '/assets/' + m[1];
    });
    visit(tree, 'link', (node) => {
      if (typeof node.url !== 'string') return;
      const inter = node.url.match(/(?:\.\.\/)+(concepts|problems|mistakes|tools)\/([^/]+)\.md$/);
      if (inter) {
        node.url = `/${inter[1]}/${encodeURIComponent(inter[2])}`;
        return;
      }
    });
  };
}

// https://astro.build/config
export default defineConfig({
  site: 'http://localhost:4321',
  integrations: [
    react(),
    mdx({
      remarkPlugins: [remarkMath, remarkRewritePaths],
      rehypePlugins: [rehypeKatex],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    remarkPlugins: [remarkMath, remarkRewritePaths],
    rehypePlugins: [rehypeKatex],
  },
});
