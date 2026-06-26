#!/usr/bin/env node
// 위젯 있는 개념 id 매니페스트(SSOT) 생성. concept-widgets/*.json(spec 위젯) → concept-widgets-index.json.
//   모든 표면(개념목록·개념지도·path·문제·홈·사이드바)이 이 하나를 읽어 🔭 뱃지·필터를 그린다.
//   ★widget_spec_loop --commit이 매일 재생성 → 위젯 늘면 인덱스·뱃지 자동 동기화(SSOT 핵심).
import { readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const DIR = fileURLToPath(new URL('../src/data/concept-widgets', import.meta.url));
const OUT = fileURLToPath(new URL('../src/data/concept-widgets-index.json', import.meta.url));
const ids = readdirSync(DIR)
  .filter((f) => f.endsWith('.json'))
  .map((f) => f.replace(/\.json$/, '').replace(/__/g, '/'))
  .sort();
writeFileSync(OUT, JSON.stringify(ids));
console.log(`concept-widgets-index.json: ${ids.length}개 위젯 개념 id`);
