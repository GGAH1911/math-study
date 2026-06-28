#!/usr/bin/env node
// =============================================================================
// 📝 Doc Index Generator — 개발문서 폴더의 per-directory 00_<DIR>.md 자동생성/갱신
// =============================================================================
// TME(ensure_wiki_indices.py) 포팅. 단 우리 사정에 맞춰:
//   - 콘텐츠 메시(concepts·problems·hubs·mistakes·notes·syntheses·paths)는 제외 — audit-lwip 관할.
//   - <!-- AUTO_INDEX_SECTION --> ~ 다음 '---' 사이만 재생성(그 위 제목·아래 수동 설명/링크는 보존).
//   - 기존 항목의 사람이 쓴 설명(`- \`file\` — 설명`)은 파일이 남아있으면 그대로 유지.
// prebuild/predev 체인에서 audit-lwip와 함께 실행.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DOCS = path.resolve(__dirname, '../../docs');           // <repo>/docs

// 콘텐츠 메시 = audit-lwip 관할 → 자동인덱스 대상 아님.
const EXCLUDE_TOP = new Set([
  'concepts', 'problems', 'hubs', 'mistakes', 'notes', 'syntheses', 'paths',
  '_archive', 'assets',
]);
const EXCLUDE_DIR = new Set(['node_modules', '.git', '.obsidian', '__pycache__']);
const MARK = '<!-- AUTO_INDEX_SECTION -->';

let created = 0, updated = 0, skipped = 0;

// 폴더의 00_ 인덱스 파일명 — TME 규약: 00_<DIRNAME_UPPER>.md
const indexName = (dir) => `00_${path.basename(dir).toUpperCase().replace(/[^A-Z0-9]+/g, '_')}.md`;

// 기존 인덱스에서 '- `file` — 설명' 의 설명을 회수(파일 살아있으면 보존).
function existingDescriptions(text) {
  const map = new Map();
  for (const m of text.matchAll(/^- `([^`]+)`\s*(?:—\s*(.*))?$/gm)) {
    map.set(m[1], (m[2] ?? '').trim());
  }
  return map;
}

function buildSection(mdFiles, subDirs, prevDesc) {
  const lines = [];
  for (const d of subDirs) lines.push(`- 📁 [[${path.basename(d, '.md')}|${d}/]]`);
  for (const f of mdFiles) {
    const desc = prevDesc.get(f);
    lines.push(`- \`${f}\`${desc ? ` — ${desc}` : ' — 등록 자산'}`);
  }
  return lines.join('\n');
}

function processDir(dir, isTop) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const subDirs = entries.filter((e) => e.isDirectory() && !EXCLUDE_DIR.has(e.name)).map((e) => e.name);
  const mdFiles = entries
    .filter((e) => e.isFile() && e.name.endsWith('.md') && !e.name.startsWith('00_'))
    .map((e) => e.name)
    .sort();

  // 하위 폴더 먼저 재귀(콘텐츠 제외 폴더는 통째 스킵).
  for (const sd of subDirs) {
    if (isTop && EXCLUDE_TOP.has(sd)) { skipped++; continue; }
    processDir(path.join(dir, sd), false);
  }

  if (mdFiles.length === 0 && subDirs.length === 0) return;   // 빈 폴더엔 인덱스 안 만듦

  const idxPath = path.join(dir, indexName(dir));
  const section = buildSection(mdFiles, subDirs.filter((s) => !(isTop && EXCLUDE_TOP.has(s))),
    fs.existsSync(idxPath) ? existingDescriptions(fs.readFileSync(idxPath, 'utf8')) : new Map());

  if (!fs.existsSync(idxPath)) {
    const name = indexName(dir).replace('.md', '');
    const body = `---\nsources: []\ncreated: ${today()}\nupdated: ${today()}\n---\n\n# 📝 ${name} (자동 생성 인덱스)\n> 분류: Wiki / Auto-Generated\n\n## 전수 명세\n\n${MARK}\n${section}\n\n---\n## 🔗 지식망 연결\n- **상위 분류**: [[index]]\n`;
    fs.writeFileSync(idxPath, body, 'utf8');
    created++;
    return;
  }

  // 기존 파일 — AUTO_INDEX_SECTION ~ 다음 '---' 사이만 교체(나머지 보존).
  const cur = fs.readFileSync(idxPath, 'utf8');
  const mi = cur.indexOf(MARK);
  if (mi === -1) { skipped++; return; }                       // 마커 없으면 손대지 않음(수동 인덱스)
  const after = cur.indexOf('\n---', mi);
  const end = after === -1 ? cur.length : after;
  const next = cur.slice(0, mi + MARK.length) + '\n' + section + '\n' + cur.slice(end);
  if (next !== cur) { fs.writeFileSync(idxPath, next, 'utf8'); updated++; }
}

function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

processDir(DOCS, true);
console.log(`[doc-indices] created ${created} · updated ${updated} · skipped(content/excluded) ${skipped}`);
