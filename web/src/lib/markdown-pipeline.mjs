// 마크다운 렌더 파이프라인 — **빌드(astro.config.mjs)와 빌드 밖(선렌더 방출기)이 공유**한다.
//
// ★왜 빼냈나: 이 체인이 `astro.config.mjs` 안에 갇혀 있으면 Astro 빌드 안에서만 돌 수 있다.
//   Phase 3 은 콘텐츠를 **빌드 시 미리 HTML 로 구워** 앱이 오프라인에서도 읽게 하는 게 목표라,
//   같은 체인을 빌드 밖에서도 돌려야 한다. 두 벌로 유지하면 반드시 갈라진다 —
//   이 레포는 이미 sympy 헤더가 브라우저/서버로 갈려 사고를 낸 적이 있다(게이트까지 만들었다).
//
// ★★경로 주의: `CONCEPT_LEAF_MAP` 은 `docs/concepts` 를 **디스크에서 훑어** 만든다.
//   경로가 어긋나면 맵이 조용히 비고, 그러면 링크 재작성이 전부 no-op 이 된다 —
//   문항 4,164개 중 2,583개가 이 재작성에 의존한다. 그래서 아래에 **비면 던지는 가드**를 둔다.
//   (조용히 비는 것이 이 파일의 유일한 치명적 실패 모드다.)
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { visit } from 'unist-util-visit';
import { readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { normalizeKatex, KATEX_STRICT, KATEX_ERROR_COLOR } from './katex-normalize.mjs';

/** docs/ 루트. 이 파일은 `web/src/lib/` 에 있으므로 세 단계 위가 레포 루트다. */
const DOCS_ROOT = fileURLToPath(new URL('../../../docs', import.meta.url));

// 개념 leaf 이름 → 실제 중첩 slug 맵.
// 개념 .md 본문이 flat 링크(`/concepts/이차함수`)를 쓰는데 실제 라우트는 중첩
// (`/concepts/functions/middle-3/이차함수`)이라 통째로 404 나는 시스템 와이드 버그가
// 있다. 렌더 시 leaf 를 실제 slug 로 해석해 고친다(아래 remarkRewritePaths).
// readdir 은 macOS-origin 파일명이 NFD 라 세그먼트마다 NFC 정규화(Astro content id 와 일치).
/** 실제 존재하는 개념 full slug 집합 — 본문 링크 경로가 맞는지 검증하는 데 쓴다. */
export const CONCEPT_FULL_SET = new Set();
export const CONCEPT_LEAF_MAP = (() => {
  /** @type {Map<string, string>} */
  const map = new Map();
  /** @type {Map<string, number>} */
  const dups = new Map();
  let root;
  try { root = fileURLToPath(new URL('../../../docs/concepts', import.meta.url)); }
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
        CONCEPT_FULL_SET.add(full);
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

// KaTeX strict 모드: 한국어 콘텐츠라 `$...의 ...$` 같은 raw 한글이 자주 등장.
// 클라이언트 위젯(mathish)과 동일한 정책을 공유 — `unicodeTextInMathMode`
// 와 `unknownSymbol`(\text{} 안 raw 유니코드) 둘 다 ignore 하고 나머지
// (브래킷 불일치 등 실제 LaTeX 오류) 는 그대로 경고로 둔다. 파싱 실패시 표시되는
// errorColor 도 기본 빨강(#cc0000) 대신 amber 로 — 본문 한가운데 시뻘건
// 텍스트가 튀어나오는 사고를 막음. (LLM 이 만든 식이 종종 깨짐.)
export const katexOptions = {
  strict: KATEX_STRICT,
  errorColor: KATEX_ERROR_COLOR,
};

/**
 * Remark plugin: normalize math nodes with the *same* pure routine the client
 * widgets use (`normalizeKatex`):
 *  - rewrite KaTeX-unsupported environments (`align`, `align*`, `eqnarray`)
 *    to `aligned` — LLM notes routinely emit standard-LaTeX `\begin{align}`.
 *  - escape unescaped `%` → `\%` — otherwise a `%` (LaTeX comment) swallows
 *    the rest of the math segment and the whole equation silently vanishes.
 * Scoped to `math`/`inlineMath` nodes, so `%` escaping touches math only
 * (prose `50%` is untouched) — identical to how mathish confines it.
 */
function remarkKatexCompat() {
  return (/** @type {any} */ tree) => {
    visit(tree, ['math', 'inlineMath'], (node) => {
      if (typeof node.value === 'string') node.value = normalizeKatex(node.value);
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
    // 해석 실패한 개념 링크를 담아 뒀다가 마지막에 **평문으로 떨군다**.
    //   (visit 도중 트리를 바꾸면 순회가 꼬인다)
    /** @type {Array<{parent:any,index:number,node:any}>} */
    const unresolved = [];
    visit(tree, 'link', (node, index, parent) => {
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
      // ../<col>/<slug…>.md — 크로스 컬렉션. ★slug 는 **여러 세그먼트**일 수 있다.
      //   예전엔 `([^/]+)` 로 한 세그먼트만 잡아서 `../concepts/algebra/middle-3/제곱근.md`
      //   같은 중첩 경로가 통째로 매칭 실패 → 깨진 상대경로 그대로 렌더됐다.
      //   (문제 4,164개 중 2,583개가 이 형태였다. 링크를 눌러도 아무 데도 못 갔다.)
      // ★`docs/concepts/...md` 처럼 **레포 루트 기준 경로**로 적힌 것도 잡는다.
      //   어제는 `../concepts/...` 형태만 고쳤는데, 개념 파일 35개·링크 300개가 이 형태라
      //   변환되지 않고 `docs/concepts/....md` 가 그대로 href 로 나갔다(눌러도 안 열린다).
      const inter = node.url.match(/^(?:(?:\.\.\/)+|\.?\/?docs\/)(concepts|problems|mistakes|tools|syntheses)\/(.+)\.md$/);
      if (inter) {
        const col = inter[1];
        let rest = inter[2];
        try { rest = decodeURIComponent(rest); } catch { /* already raw */ }
        rest = rest.normalize('NFC');
        // ★본문에 적힌 경로가 실제와 다른 경우가 있다(중간 디렉터리 한 칸이 빠진 링크 등).
        //   존재하지 않으면 leaf 로 재해석한다 — 없는 경로로 보내느니 이름으로 찾는 게 낫다.
        if (col === 'concepts' && !CONCEPT_FULL_SET.has(rest)) {
          const full = CONCEPT_LEAF_MAP.get(rest.split('/').pop() ?? '');
          // ★그래도 없으면 **링크를 만들지 않는다.** 2026-06 노드 정리로 사라진 개념을
          //   본문이 아직 가리킨다 — 죽은 링크로 두면 눌렀을 때 404 를 보게 된다.
          if (!full) { if (parent && typeof index === 'number') unresolved.push({ parent, index, node }); return; }
          rest = full;
        }
        // 세그먼트별로 인코딩 — 통째로 하면 `/` 까지 %2F 가 돼 경로가 무너진다.
        node.url = `/${col}/${rest.split('/').map(encodeURIComponent).join('/')}`;
        return;
      }
      // ./<slug>.md or bare <slug>.md — sibling within current collection
      const sibling = node.url.match(/^(?:\.\/)?([^/]+)\.md$/);
      if (sibling && currentCol) {
        node.url = `/${currentCol}/${encodeURIComponent(sibling[1])}`;
        return;
      }
    });
    // 뒤에서부터 바꿔야 앞 인덱스가 밀리지 않는다.
    for (const { parent, index, node } of unresolved.reverse()) {
      parent.children.splice(index, 1, ...(node.children ?? [{ type: 'text', value: '' }]));
    }
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

// ★가드 — 맵이 비면 링크 재작성이 통째로 죽는다. 조용히 넘어가지 않는다.
if (CONCEPT_LEAF_MAP.size === 0) {
  throw new Error(
    `[markdown-pipeline] 개념 맵이 비었다 — docs 경로가 어긋났다: ${DOCS_ROOT}\n` +
    `  이대로 두면 링크 재작성이 전부 no-op 이 되고 문항 2,583개의 링크가 죽는다.`,
  );
}

/** 빌드와 방출기가 **같은 것**을 쓰도록 여기 한 벌만 둔다. */
export const remarkPlugins = [remarkMath, remarkKatexCompat, remarkRewritePaths, remarkStripSolutionPlaceholder];
export const rehypePlugins = [[rehypeKatex, katexOptions]];
