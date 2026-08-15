// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';
import { fileURLToPath } from 'node:url';
// Pure KaTeX normalization shared with the client renderer (mathish.tsx) so
// the build chain renders syntheses/concepts/problems at the same strength.

// ★remark/rehype 체인은 `src/lib/markdown-pipeline.mjs` 로 옮겼다 — **빌드 밖(선렌더 방출기)도
//   같은 체인을 써야** 하기 때문이다. 두 벌로 두면 반드시 갈라진다(sympy 헤더 전례).
import { remarkPlugins, rehypePlugins } from './src/lib/markdown-pipeline.mjs';

// https://astro.build/config
export default defineConfig({
  site: 'http://localhost:4321',
  output: 'server',
  devToolbar: { enabled: false },  // 하단 Astro dev 툴바 숨김
  adapter: node({ mode: 'standalone' }),
  integrations: [
    react(),
    mdx({
      remarkPlugins,
      rehypePlugins,
    }),
  ],
  // 동시 구동 서버는 캐시를 분리해야 .astro content store 동시 write 충돌이 안 난다.
  // STABLE(4324 학습용)·DEV_NOAUTH(검증 전용 포트)는 각자 별도 캐시, 기본(4323)은 default.
  cacheDir: process.env.STABLE ? './.astro-stable' : process.env.DEV_NOAUTH ? './.astro-noauth' : undefined,
  vite: {
    plugins: [tailwindcss()],
    cacheDir: process.env.STABLE ? './node_modules/.vite-stable' : process.env.DEV_NOAUTH ? './node_modules/.vite-noauth' : undefined,
    server: {
      allowedHosts: [
        'localhost',
        '127.0.0.1',
        '.ts.net',           // any Tailscale MagicDNS hostname
        '.tailf47aa4.ts.net', // this tailnet specifically
      ],
      // worktree 의 node_modules 는 메인 레포로 심링크돼 있어, vite 가 심링크를
      // resolve 하면 서빙 루트(WT/web) 밖이 된다 → react client.js 등이 allow
      // list 밖으로 막힌다. 메인 레포 루트를 허용해 통과시킨다.
      fs: {
        allow: ['..', '/home/insung/Projects/math-study'],
      },
      // STABLE=1(학습용 안정 서버): docs/ 콘텐츠 전체 watch 제외 → 교정/개념 배치가 md를 고쳐도
      // glob-loader reload·HMR full-reload가 안 일어나 학습 중 안 깜박. 새 콘텐츠는 restart 때 반영.
      // ★ docs 는 vite root(web/) 밖(../docs)이라 상대 glob 만으론 chokidar 가 절대경로 watch 를
      //   못 잡는다 → 절대경로 glob 도 함께 준다. (problems 만 막던 것 → 개념 배치 깜박 갭까지 docs 전체로 확장, 2026-06-21.)
      ...(process.env.STABLE ? { watch: { ignored: ['**/docs/**', fileURLToPath(new URL('../docs/**', import.meta.url))] } } : {}),
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
    remarkPlugins,
    rehypePlugins,
  },
});
