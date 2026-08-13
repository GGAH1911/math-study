// 개념별 오개념 목록 로더 (서버 전용) — 튜터 프롬프트 주입용.
//   생성=DeepSeek V4 Flash(배치·저가), 검증=claude -p 구독(적대적, 기본 거부).
//   **verified:true 인 것만** 내보낸다. 미검증본이 학생에게 말해지면 안 된다.
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { WEB_ROOT } from './concept-fs';

export type Misconception = { belief: string; why_wrong: string; fix: string };

const DIR = join(WEB_ROOT, 'src/data/concept-misconceptions');
const cache = new Map<string, Misconception[]>();

export function misconceptionsFor(slug: string): Misconception[] {
  if (cache.has(slug)) return cache.get(slug)!;
  let items: Misconception[] = [];
  try {
    const p = join(DIR, `${slug.replace(/\//g, '__')}.json`);
    if (existsSync(p)) {
      const d = JSON.parse(readFileSync(p, 'utf8'));
      // ★검증 게이트: verified 가 아니면 쓰지 않는다(생성만 되고 검수 안 된 것 차단).
      if (d?.verified === true && Array.isArray(d.items)) items = d.items;
    }
  } catch { /* 없으면 빈 목록 — 튜터는 그대로 동작 */ }
  cache.set(slug, items);
  return items;
}

/** 튜터 시스템 프롬프트에 넣을 블록. 없으면 빈 문자열. */
export function misconceptionsBlock(slug: string): string {
  const items = misconceptionsFor(slug);
  if (!items.length) return '';
  const lines = items.map((m, i) =>
    `${i + 1}. 학생이 이렇게 말하면: "${m.belief}"\n   → 왜 틀렸나: ${m.why_wrong}\n   → 교정: ${m.fix}`).join('\n');
  return `

--- 이 개념의 흔한 오개념 (검수 완료 · 학생 발화 매칭용) ---
학생이 아래와 **비슷한 취지**의 말을 하면(표현이 달라도) 그 지점을 즉시 정확히 짚어라.
해당 없으면 언급하지 말 것 — 학생이 하지도 않은 오해를 지적하면 안 된다.
${lines}`;
}
