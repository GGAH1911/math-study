#!/usr/bin/env node
/**
 * 개념 .md 의 빈 템플릿 잔재를 청소한다.
 *
 * ingest 가 남긴 stub 템플릿("## 정의\n\n## 예시" 빈 헤더 + "(개념 정의는
 * 학습 시 채워집니다.)" placeholder)이 실제 내용(보통 `## 본문` 아래)과
 * 공존해서, 화면에 빈 섹션 헤더와 placeholder 문구가 미완성처럼 떠 있다.
 *
 * 규칙 (내용 있는 섹션은 절대 건드리지 않음):
 *   1. "(... 채워 ...)" 형태의 독립 placeholder 라인 제거.
 *   2. 헤더 텍스트 안의 placeholder 제거: "## 본문 (학습 시 채워짐)" → "## 본문".
 *   3. 본문이 빈 ## 섹션(하위 ### 헤더 제외 실제 텍스트 0) 통째 제거.
 *   4. 청소 후 유일하게 남은 ## 섹션이 "## 본문" 뿐이면, 그 헤더를 없애고
 *      아래 ### 들을 ## 로 승격(군더더기 "본문" 래퍼 제거).
 *
 * 기본 dry-run. --write 로 적용. (frontmatter 는 원문 그대로 보존)
 */
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DOCS = join(dirname(__dirname), '..', 'docs', 'concepts');
const PH = /\([^)]*채워[^)]*\)/;

function walkMd(dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...walkMd(p));
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

function cleanBody(body) {
  // 1. placeholder 독립 라인 제거
  let lines = body.split('\n').filter((l) => !new RegExp(`^\\s*${PH.source}\\s*$`).test(l));
  // 2. 헤더 텍스트 안의 placeholder 제거
  lines = lines.map((l) =>
    /^#{2,}\s/.test(l) && PH.test(l) ? l.replace(PH, '').replace(/\s+$/, '') : l,
  );
  // 3. 섹션 파싱 (## 기준)
  const pre = [];
  const secs = [];
  let cur = null;
  for (const l of lines) {
    if (/^##\s+/.test(l)) { cur = { header: l, content: [] }; secs.push(cur); }
    else if (cur) cur.content.push(l);
    else pre.push(l);
  }
  // 빈 섹션(하위 ### 헤더를 뺀 실제 텍스트가 없음) 제거
  const kept = secs.filter((s) => {
    const txt = s.content.filter((l) => !/^#{3,}\s/.test(l)).join('').replace(/\s/g, '');
    return txt.length > 0;
  });
  // 4. 유일 ## 가 "본문"이면 래퍼 제거 + ### 승격
  let out;
  if (kept.length === 1 && /^##\s+본문\s*$/.test(kept[0].header)) {
    const promoted = kept[0].content.map((l) => l.replace(/^###\s/, '## ')).join('\n');
    out = pre.join('\n').replace(/\n+$/, '') + '\n' + promoted;
  } else {
    out = pre.join('\n').replace(/\n+$/, '');
    for (const s of kept) out += '\n' + s.header + '\n' + s.content.join('\n');
  }
  return out.replace(/\n{3,}/g, '\n\n').trim() + '\n';
}

function main() {
  const write = process.argv.includes('--write');
  const files = walkMd(DOCS);
  const changed = [];
  for (const p of files) {
    const raw = readFileSync(p, 'utf-8');
    const m = raw.match(/^(---\n[\s\S]*?\n---\n)([\s\S]*)$/);
    if (!m) continue;
    const fm = m[1];
    const body = m[2];
    const cleaned = cleanBody(body);
    const newRaw = fm + '\n' + cleaned;
    // 공백만 다른 정상 파일(타입3)은 건너뛴다 — placeholder/빈섹션/승격 같은
    // 실질 변경이 있을 때만 기록해 diff 노이즈를 막는다.
    const norm = (s) => s.replace(/[ \t]+/g, ' ').replace(/\n{2,}/g, '\n').trim();
    if (norm(newRaw) !== norm(raw)) changed.push({ p, raw, newRaw, body, cleaned });
  }
  console.log(`══ clean-concept-templates ══`);
  console.log(`  스캔 ${files.length} · 변경 ${changed.length}`);

  // 샘플 before/after (앞 3개)
  for (const c of changed.slice(0, 3)) {
    console.log(`\n──── ${c.p.replace(DOCS + '/', '')} ────`);
    console.log('  [BEFORE]');
    console.log(c.body.trim().split('\n').slice(0, 9).map((l) => '   ' + l).join('\n'));
    console.log('  [AFTER]');
    console.log(c.cleaned.trim().split('\n').slice(0, 9).map((l) => '   ' + l).join('\n'));
  }

  if (!write) { console.log(`\n(dry-run; --write 로 ${changed.length}개 적용)`); return; }
  for (const c of changed) writeFileSync(c.p, c.newRaw, 'utf-8');
  console.log(`\n${changed.length}개 적용 완료.`);
}

main();
