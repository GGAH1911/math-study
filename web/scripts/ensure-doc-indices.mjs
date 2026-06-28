#!/usr/bin/env node
// =============================================================================
// 📝 Index Generator — per-directory 00_<DIR>.md 자동생성/갱신 (docs + 소스코드)
// =============================================================================
// TME 토폴로지를 docs 뿐 아니라 소스(web/src·scripts)까지 확장 → 설계(docs)부터 구현(code)까지
// 같은 인덱스 망으로 연결(spec→module traverse). 규칙:
//   - docs/: .md 나열, 콘텐츠 메시(concepts 등)는 제외(audit-lwip 관할).
//   - web/src·scripts: 소스 파일(.ts/.tsx/.astro/.mjs/.css/.py) 나열. 인덱스 자체는 .md(LWIP 규약).
//     ★content collection 은 docs/ 만 glob 하므로 src 의 00_*.md 는 Astro 가 안 건드림(검증됨).
//   - <!-- AUTO_INDEX_SECTION --> ~ 다음 '---' 사이만 재생성. 그 위 제목·아래 수동 설명/링크는 보존.
//   - 사람이 쓴 설명(`- \`file\` — 설명`)은 파일이 남아있으면 유지.
// prebuild/predev 체인에서 audit-lwip 와 함께 실행.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '../..');

const EXCLUDE_DIR = new Set(['node_modules', '.git', '.obsidian', '__pycache__', '.astro', 'dist', 'build', '.vercel']);
const MARK = '<!-- AUTO_INDEX_SECTION -->';

// 인덱싱 루트들. exts=나열할 파일 확장자, excludeTop=루트 직속 제외 폴더, rootParent=루트 인덱스의 상위 링크.
const ROOTS = [
  {
    dir: path.join(REPO, 'docs'), exts: ['.md'], rootParent: '[[index]]',
    // 콘텐츠 메시 = audit-lwip 관할 → 제외.
    excludeTop: new Set(['concepts', 'problems', 'hubs', 'mistakes', 'notes', 'syntheses', 'paths', '_archive', 'assets']),
  },
  {
    dir: path.join(REPO, 'web', 'src'), exts: ['.ts', '.tsx', '.astro', '.mjs', '.css'],
    rootParent: '[[00_ARCHITECTURE|docs/architecture/]]', excludeTop: new Set(),
  },
  {
    dir: path.join(REPO, 'scripts'), exts: ['.py', '.mjs'],
    rootParent: '[[00_ARCHITECTURE|docs/architecture/]]', excludeTop: new Set(),
  },
];

let created = 0, updated = 0, skipped = 0;

// 폴더의 00_ 인덱스 파일명 — TME 규약: 00_<DIRNAME_UPPER>.md
const indexName = (dir) => `00_${path.basename(dir).toUpperCase().replace(/[^A-Z0-9]+/g, '_')}.md`;
const indexStem = (dir) => indexName(dir).replace(/\.md$/, '');

// 기존 인덱스에서 '- `file` — 설명' 의 설명을 회수(파일 살아있으면 보존).
function existingDescriptions(text) {
  const map = new Map();
  for (const m of text.matchAll(/^- `([^`]+)`\s*(?:—\s*(.*))?$/gm)) {
    map.set(m[1], (m[2] ?? '').trim());
  }
  return map;
}

function buildSection(files, subDirs, dir, prevDesc) {
  const lines = [];
  // 하위 폴더 → 그 폴더의 00_ 인덱스로 링크(트리 traverse).
  for (const d of subDirs) lines.push(`- 📁 [[${indexStem(path.join(dir, d))}|${d}/]]`);
  for (const f of files) {
    const desc = prevDesc.get(f);
    lines.push(`- \`${f}\`${desc ? ` — ${desc}` : ' — 등록 자산'}`);
  }
  return lines.join('\n');
}

// dir 을 처리. parentLink = 이 폴더 인덱스의 '상위 분류' 링크.
function processDir(dir, cfg, isTop, parentLink) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const subDirsAll = entries
    .filter((e) => e.isDirectory() && !EXCLUDE_DIR.has(e.name))
    .filter((e) => !(isTop && cfg.excludeTop.has(e.name)))
    .map((e) => e.name);
  const files = entries
    .filter((e) => e.isFile() && !e.name.startsWith('00_') && cfg.exts.some((x) => e.name.endsWith(x)))
    .map((e) => e.name)
    .sort();

  const myLink = `[[${indexStem(dir)}]]`;
  // 하위 폴더 먼저 재귀(부모 링크 = 내 인덱스). 인덱싱 결과 자식이 비면 링크에서 빼야 하므로 수집.
  const liveSubDirs = [];
  for (const sd of subDirsAll) {
    if (processDir(path.join(dir, sd), cfg, false, myLink)) liveSubDirs.push(sd);
  }
  if (isTop && cfg.excludeTop.size) skipped += subDirsAll.length === 0 ? 0 : 0; // (집계용 noop)

  if (files.length === 0 && liveSubDirs.length === 0) return false;  // 인덱싱할 게 없으면 인덱스 안 만듦

  const idxPath = path.join(dir, indexName(dir));
  const section = buildSection(files, liveSubDirs, dir,
    fs.existsSync(idxPath) ? existingDescriptions(fs.readFileSync(idxPath, 'utf8')) : new Map());

  if (!fs.existsSync(idxPath)) {
    const body = `---\nsources: []\ncreated: ${today()}\nupdated: ${today()}\n---\n\n# 📝 ${indexStem(dir)} (자동 생성 인덱스)\n> 분류: Wiki / Auto-Generated\n\n## 전수 명세\n\n${MARK}\n${section}\n\n---\n## 🔗 지식망 연결\n- **상위 분류**: ${parentLink}\n`;
    fs.writeFileSync(idxPath, body, 'utf8');
    created++;
    return true;
  }

  // 기존 파일 — AUTO_INDEX_SECTION ~ 다음 '---' 사이만 교체(나머지 보존).
  const cur = fs.readFileSync(idxPath, 'utf8');
  const mi = cur.indexOf(MARK);
  if (mi === -1) { skipped++; return true; }                  // 마커 없으면 손대지 않음(수동 인덱스)
  const after = cur.indexOf('\n---', mi);
  const end = after === -1 ? cur.length : after;
  const next = cur.slice(0, mi + MARK.length) + '\n' + section + '\n' + cur.slice(end);
  if (next !== cur) { fs.writeFileSync(idxPath, next, 'utf8'); updated++; }
  return true;
}

function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

for (const cfg of ROOTS) {
  if (fs.existsSync(cfg.dir)) processDir(cfg.dir, cfg, true, cfg.rootParent);
}
console.log(`[indices] created ${created} · updated ${updated} · skipped ${skipped}`);
