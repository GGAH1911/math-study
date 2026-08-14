// 문제별 **미리 검증된 3D 도형 스펙** 레지스트리 (서버 전용).
//
// ★왜 만드나: 입체 작도는 튜터가 실시간으로 하기에 가장 비싼 일이다. 조건을 뽑고 →
//   좌표를 세우고 → sympy 로 검증하고 → 받아 적는 4턴짜리 절차이고, 한 번이라도
//   미끄러지면 학생에게 **납작한 그림이나 지어낸 좌표**가 나간다(2026-08-14 실사고).
//   그래서 3D 가 필요한 문제는 **미리 좌표를 세워 검증해 두고**, 런타임에는 받아 적기만 한다.
//
// ★왜 frontmatter 가 아니라 별도 파일인가: 재인제스트가 frontmatter 를 통째로 다시 쓴다
//   (docs/TODO.md · 풀이가 그렇게 날아간 적이 있다). 스펙은 문제 md 바깥에 둬야 산다.
//   파일명은 문제 파일의 stem — 4,164건 전부 유일함을 확인했다(2026-08-14).
//
// ★기본값은 **금지**다. 레지스트리에 없는 문제에서는 geometry3d 를 쓰지 못하게 한다.
//   입체가 필요 없는 문제에 억지로 3D 를 그리면 이해를 돕기는커녕 방해가 된다.

import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { WEB_ROOT } from './concept-fs';

export const FIGURES_3D_DIR = join(WEB_ROOT, 'src/data/figures-3d');

export interface Figure3DEntry {
  /** 문제 파일 stem (예: 2026_수능_기하_28) */
  stem: string;
  /** 렌더러가 그대로 받는 geometry3d spec */
  spec: Record<string, unknown>;
  /** 이 좌표가 만족함을 sympy 로 확인한 조건들 — 사람이 읽는 근거이자 재검증 입력 */
  conditions: string[];
  /** 좌표를 재현하는 sympy 코드. 회귀 게이트가 이걸 다시 돌린다. */
  verify: string;
  /** 학생에게 보일 한 줄 설명 */
  note?: string;
}

/** 문제 slug(`2026/수능/2026_수능_기하_28`) → stem */
export function stemOf(slug: string): string {
  return slug.split('/').pop() ?? slug;
}

export function readFigure3D(slug: string): Figure3DEntry | null {
  const stem = stemOf(slug);
  // 경로 조작 차단 — stem 은 파일명 한 조각이어야 한다.
  if (!stem || stem.includes('/') || stem.includes('..')) return null;
  const path = join(FIGURES_3D_DIR, `${stem}.json`);
  if (!existsSync(path)) return null;
  try {
    const e = JSON.parse(readFileSync(path, 'utf-8')) as Figure3DEntry;
    return e && e.spec ? { ...e, stem } : null;
  } catch {
    return null;   // 깨진 파일 때문에 튜터가 죽지는 않게
  }
}

export function listFigure3D(): string[] {
  if (!existsSync(FIGURES_3D_DIR)) return [];
  return readdirSync(FIGURES_3D_DIR).filter((n) => n.endsWith('.json')).map((n) => n.replace(/\.json$/, ''));
}

/**
 * 시스템 프롬프트에 넣을 블록.
 *
 * 스펙이 있으면 "이미 검증됐으니 그대로 써라", 없으면 "이 문제엔 입체를 그리지 마라".
 * 후자가 이 레지스트리의 절반이다 — 3D 를 **안 그리게** 하는 것도 기능이다.
 */
export function figure3DBlock(slug: string): string {
  const e = readFigure3D(slug);
  if (!e) {
    return `--- 입체 도형 (이 문제) ---
이 문제는 **입체 도형이 필요 없다.** \`\`\`geometry3d\`\`\` 를 쓰지 마라.
평면으로 충분하거나(\`\`\`geometry\`\`\`), 좌표가 본문에 이미 주어져 그림이 이해를 돕지 않는
문제다. 학생이 "입체로 그려 달라"고 하면, 그리는 대신 **왜 평면으로 충분한지** 한 줄로
설명하고 필요한 그림을 2D 로 그려라(예: 단면·전개도·정사영 평면).`;
  }
  return `--- 입체 도형 (이 문제 · **이미 검증된 좌표**) ---
아래 스펙의 좌표는 문제 조건을 sympy 로 전부 확인한 것이다:
${e.conditions.map((c) => `  · ${c}`).join('\n')}

학생이 도형을 원하면 **STEP A-D 를 밟지 말고**(좌표를 다시 계산하지 마라)
아래 JSON 을 \`\`\`geometry3d\`\`\` 블록에 **글자 그대로** 넣어 emit 하라.
${e.note ? `설명은 이렇게: ${e.note}\n` : ''}
\`\`\`geometry3d
${JSON.stringify(e.spec)}
\`\`\`

학생이 다른 요소(단면·정사영·보조점)를 추가로 요청하면, 그때만 위 좌표를 **출발점으로**
삼아 sympy 로 추가 좌표를 구해라. 이미 있는 점의 좌표는 다시 계산하지 마라.`;
}
