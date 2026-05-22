import type { APIRoute } from 'astro';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

export const prerender = false;

const WEB_ROOT = process.cwd();
const CONCEPTS_DIR = resolve(WEB_ROOT, '..', 'docs', 'concepts');
const GRAPH_JSON_PATH = resolve(WEB_ROOT, 'src', 'data', 'concept-graph.json');

const MASTERY_LEVELS = ['unknown', 'learning', 'proficient', 'mastered'] as const;
type MasteryLevel = typeof MASTERY_LEVELS[number];

type Body = {
  slug: string;
  to: MasteryLevel;
  reason?: string;
  evidence?: string[];
};

function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

/**
 * Frontmatter 안의 `mastery`, `mastery_updated`, `mastery_evidence` 3개 필드를
 * 안전하게 교체. evidence는 기존 entry에 dedupe append (같은 reason 중복 차단).
 *
 * 자체 line-based YAML 편집 — 단순 schema 가정:
 *   - `key: value` (스칼라) 또는
 *   - `key:`        (다음 줄에 `  - item` 들여쓰기)
 *   - `key: []`     (빈 배열, multi-line으로 승급)
 */
function patchFrontmatter(text: string, to: MasteryLevel, newEvidence: string[]): string {
  const lines = text.split('\n');
  if (lines[0] !== '---') throw new Error('no frontmatter');
  let fmEnd = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i] === '---') { fmEnd = i; break; }
  }
  if (fmEnd < 0) throw new Error('frontmatter unclosed');

  // 1) 기존 mastery_evidence 키 + 그 child들을 모두 제거하고 위치만 기억.
  //    (빈 배열 `[]` / multi-line 둘 다 처리)
  const evidenceItems: string[] = [];
  let evidenceLineIdx = -1;
  for (let i = 1; i < fmEnd; i++) {
    if (/^mastery_evidence:/.test(lines[i])) {
      evidenceLineIdx = i;
      const inline = lines[i].match(/^mastery_evidence:\s*\[(.*)\]\s*$/);
      if (inline) {
        // `[]` 또는 `["a", "b"]`. 내용 추출 (쉼표 split, 따옴표 제거)
        const body = inline[1].trim();
        if (body) {
          for (const part of body.split(',')) {
            const trimmed = part.trim().replace(/^["']|["']$/g, '');
            if (trimmed) evidenceItems.push(trimmed);
          }
        }
      } else {
        // multi-line: 다음 줄들이 `  - ...` indented
        let j = i + 1;
        while (j < fmEnd && /^\s+-\s+/.test(lines[j])) {
          const item = lines[j].replace(/^\s+-\s+/, '').replace(/^["']|["']$/g, '');
          if (item) evidenceItems.push(item);
          j++;
        }
        // 제거할 range = [i+1, j) — 일단 표시만, 실제 splice는 한 번에.
        lines.splice(i + 1, j - i - 1);
        fmEnd -= (j - i - 1);
      }
      break;
    }
  }

  // 2) dedup append.
  for (const e of newEvidence) {
    if (!evidenceItems.includes(e)) evidenceItems.push(e);
  }

  // 3) 기존 mastery_evidence 라인 자리에 새 형식으로 재구성.
  const today = todayISO();
  // YAML single-quote 안: ' 만 '' 로 escape, backslash는 literal.
  // double-quote에 LaTeX `\overline` 같은 게 들어가면 unknown-escape 에러로
  // Astro content collection 빌드 자체가 깨진다.
  const newEvidenceLines = evidenceItems.length === 0
    ? ['mastery_evidence: []']
    : ['mastery_evidence:', ...evidenceItems.map((e) => `  - '${e.replace(/'/g, "''")}'`)];

  if (evidenceLineIdx >= 0) {
    lines.splice(evidenceLineIdx, 1, ...newEvidenceLines);
    fmEnd += newEvidenceLines.length - 1;
  } else {
    // 키가 아예 없으면 frontmatter 끝에 추가
    lines.splice(fmEnd, 0, ...newEvidenceLines);
    fmEnd += newEvidenceLines.length;
  }

  // 4) mastery / mastery_updated in-place replace 또는 append.
  let masteryReplaced = false;
  let updatedReplaced = false;
  for (let i = 1; i < fmEnd; i++) {
    if (/^mastery:\s*/.test(lines[i]) && !/^mastery_/.test(lines[i].replace(/^mastery:/, ''))) {
      lines[i] = `mastery: ${to}`;
      masteryReplaced = true;
    } else if (/^mastery_updated:\s*/.test(lines[i])) {
      lines[i] = `mastery_updated: ${today}`;
      updatedReplaced = true;
    }
  }
  if (!masteryReplaced) { lines.splice(fmEnd, 0, `mastery: ${to}`); fmEnd++; }
  if (!updatedReplaced) { lines.splice(fmEnd, 0, `mastery_updated: ${today}`); fmEnd++; }

  return lines.join('\n');
}

export const POST: APIRoute = async ({ request }) => {
  let body: Body;
  try { body = (await request.json()) as Body; }
  catch { return new Response(JSON.stringify({ error: 'invalid JSON body' }), { status: 400 }); }

  if (!body.slug || !body.to) {
    return new Response(JSON.stringify({ error: 'slug + to required' }), { status: 400 });
  }
  if (!MASTERY_LEVELS.includes(body.to)) {
    return new Response(JSON.stringify({ error: `to must be one of ${MASTERY_LEVELS.join(', ')}` }), { status: 400 });
  }
  // sub-dir slug ('algebra/근의_공식') 허용. `..` 와 backslash 만 차단.
  if (/\\/.test(body.slug) || body.slug.includes('..') || !/^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$/.test(body.slug)) {
    return new Response(JSON.stringify({ error: 'invalid slug' }), { status: 400 });
  }

  const filepath = resolve(CONCEPTS_DIR, `${body.slug}.md`);
  if (!filepath.startsWith(resolve(CONCEPTS_DIR) + '/')) {
    return new Response(JSON.stringify({ error: 'path escape' }), { status: 400 });
  }
  if (!existsSync(filepath)) {
    return new Response(JSON.stringify({ error: 'concept not found', path: filepath }), { status: 404 });
  }

  const original = readFileSync(filepath, 'utf-8');
  const m = original.match(/^mastery:\s*(\w+)/m);
  const from = (m?.[1] ?? 'unknown') as MasteryLevel;

  const newEvidence: string[] = [];
  if (body.reason) newEvidence.push(`chat-judgment @ ${todayISO()}: ${body.reason}`);
  if (body.evidence) for (const e of body.evidence) newEvidence.push(e);

  try {
    const patched = patchFrontmatter(original, body.to, newEvidence);
    writeFileSync(filepath, patched, 'utf-8');

    // concept-graph.json도 한 노드의 mastery만 patch — /graph 페이지가 stale
    // 안 보이도록. 전체 재빌드(2786 nodes) 대신 단일 노드 update가 빠름.
    try {
      if (existsSync(GRAPH_JSON_PATH)) {
        const graph = JSON.parse(readFileSync(GRAPH_JSON_PATH, 'utf-8'));
        if (Array.isArray(graph.nodes)) {
          for (const n of graph.nodes) {
            if (n.id === body.slug || n.slug === body.slug) {
              n.mastery = body.to;
              break;
            }
          }
          writeFileSync(GRAPH_JSON_PATH, JSON.stringify(graph, null, 2), 'utf-8');
        }
      }
    } catch { /* graph sync 실패는 무시 — frontmatter는 갱신됐고 다음 빌드 시 자동 sync */ }

    return new Response(JSON.stringify({ ok: true, from, to: body.to, path: filepath }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: (e as Error).message }), { status: 500 });
  }
};
