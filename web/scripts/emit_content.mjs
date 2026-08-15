#!/usr/bin/env node
// 콘텐츠 선렌더 방출기 — 마크다운을 **빌드 시** HTML 로 구워 파일로 낸다.
//
// ★왜: Phase 3 은 화면을 서버가 아니라 앱/브라우저가 그리게 하는 공사다. 그런데 링크 재작성이
//   빌드 산물(`CONCEPT_LEAF_MAP`, `docs/` 전체 스캔)에 의존해 **원리적으로 브라우저에서 못 돈다.**
//   그래서 "클라이언트 포팅"이 아니라 "빌드 시 선렌더"가 유일한 길이다.
//   부수 효과가 크다 — 콘텐츠가 정적 파일이 되므로 기기에 캐시할 수 있고, 그게 곧 오프라인 동작이다.
//
// ★파이프라인은 `src/lib/markdown-pipeline.mjs` 한 벌을 **빌드와 공유**한다. 두 벌이면 갈라진다.
//   다만 Astro 는 그 위에 자기 기본값(gfm·smartypants·raw HTML 허용)을 얹으므로 여기서도 얹는다.
//   **같은 입력에 같은 HTML 이 나오는지는 추측하지 않고 잰다** → `--verify` 참조.
//
// ★출력 위치가 보안 결정이다: `web/private/` 아래에 쓴다. `public/` 이나 `dist/client/` 에 쓰면
//   정적 핸들러가 미들웨어보다 먼저 응답해 **인증이 조용히 꺼진다** — 2026-08-14 에 기출 이미지
//   5,774장이 정확히 그 이유로 무인증 노출됐다. 같은 실수를 반복하지 않는다.
//
// 사용:
//   node web/scripts/emit_content.mjs                 # 전체 방출
//   node web/scripts/emit_content.mjs --col concepts  # 한 컬렉션만
//   node web/scripts/emit_content.mjs --limit 20      # 표본만(빠른 확인)
import { readdirSync, readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { gzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';
import matter from 'gray-matter';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkSmartypants from 'remark-smartypants';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeStringify from 'rehype-stringify';
import { VFile } from 'vfile';
import { remarkPlugins, rehypePlugins } from '../src/lib/markdown-pipeline.mjs';

const ROOT = fileURLToPath(new URL('../..', import.meta.url));
const DOCS = join(ROOT, 'docs');
const OUT = join(ROOT, 'web', 'private', 'content');
const COLLECTIONS = ['concepts', 'problems', 'mistakes', 'syntheses', 'tools'];

const args = process.argv.slice(2);
const arg = (k, d = null) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const only = arg('--col');
const limit = Number(arg('--limit', '0')) || 0;

/** Astro 기본값(gfm·smartypants·raw HTML)을 우리 체인 앞뒤로 얹는다. 순서가 결과를 바꾼다. */
function processor() {
  let p = unified().use(remarkParse).use(remarkGfm).use(remarkSmartypants);
  for (const pl of remarkPlugins) p = p.use(pl);
  p = p.use(remarkRehype, { allowDangerousHtml: true }).use(rehypeRaw);
  for (const pl of rehypePlugins) Array.isArray(pl) ? p = p.use(pl[0], pl[1]) : p = p.use(pl);
  return p.use(rehypeStringify, { allowDangerousHtml: true });
}

function walk(dir, out = []) {
  let ents = [];
  try { ents = readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of ents) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

const count = (s, re) => (s.match(re) || []).length;

// ★미리 압축해서 굽는다. 실측: 문항 목록 2,380KB → 245KB (**9.7배**).
//   서버는 지금 응답을 **전혀 압축하지 않는다**(gzip 을 요청해도 원본 크기 그대로 온다).
//   방출물은 정적이라 요청마다 압축할 이유가 없다 — 빌드 때 한 번, 최대 압축률로 굽는다.
//   요청당 CPU 0, 압축률은 gzip -9. CDN 이 하는 일을 그대로 한다.
function writeBoth(path, body) {
  writeFileSync(path, body);
  writeFileSync(path + '.gz', gzipSync(body, { level: 9 }));
  return body.length;
}

// ── 목록용 필드 화이트리스트 ────────────────────────────────────────────────
// ★왜 화이트리스트인가: 문항 frontmatter 에는 `searchable_text`·`solution`·`corrector_fixes`
//   처럼 **본문급으로 큰** 필드가 있다. 목록에 그대로 실으면 4,210건 × 수 KB 라 목록이
//   본문보다 커진다 — SPA 로 옮기는 이유가 사라진다. 그래서 화면이 실제로 쓰는 것만 담는다.
// ★출처: 각 index 페이지와 `lib/problem-card.ts` 가 읽는 필드를 세어서 정했다(추측 아님).
//   페이지가 새 필드를 쓰기 시작하면 **여기에 추가해야 한다** — 안 하면 화면에서 조용히 빈다.
const LIST_FIELDS = {
  concepts:  ['title', 'concept_type', 'domain', 'grade', 'unit'],
  problems:  ['source', 'unit', 'killer_tier', 'cognitive_type', 'format', 'status', 'problem_image', 'exam_intent'],
  syntheses: ['title', 'created', 'origin_concept', 'review_state'],
  mistakes:  ['error_type', 'lesson', 'problem', 'revisit_date'],
  tools:     ['kind', 'title', 'url'],
};

// syntheses 목록은 `title`·`excerpt`·`origin_title` 을 쓰는데, 이건 frontmatter 가 아니라
// **별도 빌드 산출물**(`src/data/syntheses-by-concept.json`)에 있다. 본문에서 다시 뽑으면
// 기존 화면과 미묘하게 달라지므로(제목 정제 규칙이 그 안에 있다) **있는 것을 그대로 합친다.**
// 없으면 조용히 넘어간다 — 그 경우 화면은 id 로 떨어지고, 그건 SSR 때도 같았다.
const SYN_INDEX = (() => {
  try {
    const j = JSON.parse(readFileSync(join(ROOT, 'web', 'src', 'data', 'syntheses-by-concept.json'), 'utf8'));
    return new Map((j.recent ?? []).map((r) => [r.slug, r]));
  } catch { return new Map(); }
})();

const pickFields = (col, data) => {
  const keys = LIST_FIELDS[col];
  if (!keys) return {};
  const out = {};
  for (const k of keys) if (data[k] !== undefined) out[k] = data[k];
  return out;
};

/** 컬렉션별 보강 — frontmatter 밖에서 오는 목록 필드. */
const enrich = (col, id, out) => {
  if (col !== 'syntheses') return out;
  const r = SYN_INDEX.get(id);
  if (!r) return out;
  for (const k of ['title', 'excerpt', 'origin_concept', 'origin_title', 'created', 'review_state']) {
    if (r[k] !== undefined && out[k] === undefined) out[k] = r[k];
  }
  return out;
};

const proc = processor();
const summary = [];
let failures = 0;

for (const col of COLLECTIONS) {
  if (only && col !== only) continue;
  let files = walk(join(DOCS, col));
  if (limit) files = files.slice(0, limit);
  if (!files.length) { console.log(`  ${col.padEnd(10)} (문서 없음)`); continue; }

  const outDir = join(OUT, col);
  if (!limit) rmSync(outDir, { recursive: true, force: true }); // 표본 실행은 기존 것을 지우지 않는다
  mkdirSync(outDir, { recursive: true });

  let katex = 0, links = 0, bytes = 0, errs = 0;
  const index = [];   // 컬렉션 목록 — 요청마다 수천 파일을 읽을 수는 없다
  for (const f of files) {
    // id 는 Astro content id 와 같아야 한다 — 확장자 제거 + NFC(맥 파일명은 NFD 로 온다).
    const id = relative(join(DOCS, col), f).replace(/\.md$/, '').normalize('NFC');
    let html;
    try {
      const { content, data } = matter(readFileSync(f, 'utf8'));
      // ★vfile 의 path 를 반드시 넘긴다 — remarkRewritePaths 가 이걸로 컬렉션을 판별한다.
      //   빠뜨리면 sibling 링크 재작성이 통째로 죽는데, 예외는 안 나고 링크만 조용히 원본으로 남는다.
      html = String(proc.processSync(new VFile({ value: content, path: f })));
      const dst = join(outDir, id + '.json');
      mkdirSync(dirname(dst), { recursive: true });
      writeBoth(dst, JSON.stringify({ id, collection: col, data, html }));
      index.push({ id, ...enrich(col, id, pickFields(col, data)) });
      katex += count(html, /class="[^"]*\bkatex\b/g);
      links += count(html, /<a\s[^>]*href="\//g);
      bytes += html.length;
    } catch (e) {
      errs++; failures++;
      if (errs <= 3) console.error(`  🔴 ${col}/${id}: ${String(e).slice(0, 110)}`);
    }
  }
  // 표본 실행(--limit)은 목록을 덮어쓰지 않는다 — 20건짜리 목록이 전체를 가리면 화면이 텅 빈다.
  let idxKb = 0, gzKb = 0;
  if (!limit) {
    const body = JSON.stringify({ collection: col, n: index.length, entries: index });
    writeBoth(join(OUT, `${col}.index.json`), body);
    idxKb = Math.round(body.length / 1024);
    gzKb = Math.round(gzipSync(body, { level: 9 }).length / 1024);
  }
  summary.push({ col, n: files.length, katex, links, kb: Math.round(bytes / 1024), errs, idxKb });
  console.log(`  ${col.padEnd(10)} ${String(files.length).padStart(5)}건  수식 ${String(katex).padStart(6)}  내부링크 ${String(links).padStart(6)}  본문 ${String(Math.round(bytes / 1024)).padStart(6)}KB  목록 ${String(idxKb).padStart(5)}KB→${String(gzKb).padStart(4)}KB  실패 ${errs}`);
}

const tot = summary.reduce((a, s) => ({ n: a.n + s.n, katex: a.katex + s.katex, links: a.links + s.links, kb: a.kb + s.kb }), { n: 0, katex: 0, links: 0, kb: 0 });
console.log(`\n합계 ${tot.n}건 · 수식 ${tot.katex} · 내부링크 ${tot.links} · ${tot.kb}KB → ${relative(ROOT, OUT)}`);
if (failures) { console.error(`🔴 ${failures}건 실패`); process.exitCode = 1; }
// ★한 건도 못 냈으면 성공이 아니다. 조용한 0 이 제일 나쁘다.
else if (tot.n === 0) { console.error('🔴 방출된 문서가 0건이다 — docs 경로를 확인한다.'); process.exitCode = 1; }
