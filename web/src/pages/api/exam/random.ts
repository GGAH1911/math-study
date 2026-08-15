// 랜덤 모의시험 구성 — `GET /api/exam/random?format=&option=&diff=` → `{problems, durationSec, …}`
//
// ★**서버에 남기는 게 맞다.** 30문항을 뽑으려고 코퍼스 4,210건을 클라이언트로 보낼 수는 없다.
//   구성 규칙(난이도 가중·영역 배분·기초 혼합)도 서버 한 곳에 있어야 앱·웹이 같은 시험을 본다.
//
// ★매 요청 새로 뽑는다 — 그래서 `no-store` 다. 캐시되면 "랜덤"이 아니게 된다.
import type { APIRoute } from 'astro';
import { readFileSync } from 'node:fs';
import { mediaPath } from '../../../lib/media-root.ts';
import { buildRandomExam, ELECTIVES, FORMATS, type ExamFormat } from '../../../lib/exam-build';

export const prerender = false;

const json = (body: unknown, status: number) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });

const TRACKS = ['가형', '나형'];

export const GET: APIRoute = async ({ url }) => {
  const q = url.searchParams;
  const fmtRaw = String(q.get('format') ?? '2028');
  const format = (FORMATS.some((f) => f.key === fmtRaw) ? fmtRaw : '2028') as ExamFormat;
  const diff = Math.max(0, Math.min(100, Math.round(Number(q.get('diff') ?? 50)) || 0));

  // 양식별 옵션(선택과목/계열) — 잘못된 값은 기본값으로 떨어뜨린다(400 을 내지 않는다:
  // 사용자가 URL 을 손으로 고쳐도 시험은 떠야 한다).
  let option: string | undefined;
  if (format === 'gongseon') {
    const o = String(q.get('option') ?? '');
    option = ELECTIVES.includes(o) ? o : '미적분';
  } else if (format === 'ganah') {
    const o = String(q.get('option') ?? '');
    option = TRACKS.includes(o) ? o : '가형';
  }

  const abs = mediaPath('/content/problems.index.json');
  if (!abs) return json({ error: 'bad path' }, 400);
  let rows: Array<{ id: string; [k: string]: unknown }>;
  try {
    rows = (JSON.parse(readFileSync(abs, 'utf8')) as { entries?: typeof rows }).entries ?? [];
  } catch {
    return json({ error: 'index not built', hint: 'node web/scripts/emit_content.mjs' }, 503);
  }

  // `buildRandomExam` 은 컬렉션 엔트리 모양(`{id, data}`)을 기대한다.
  const shaped = rows.map((e) => ({ id: e.id, data: e }));
  const picks = buildRandomExam(shaped as never, { format, option, difficulty: diff / 100 });
  if (picks.length === 0) return json({ error: 'no problems' }, 503);

  const problems = picks.map((p, i) => {
    const s = (p.data.source ?? {}) as { subject?: string; score?: number };
    return {
      slug: p.id,
      number: i + 1,
      subject: String(s.subject ?? ''),
      format: p.data.format ?? 'choice',
      image: p.data.problem_image ?? `/problem-images/${p.id.split('/').pop()}.png`,
      score: Number(s.score ?? 0),
    };
  });

  return json({ format, option, diff, problems, durationSec: 100 * 60 }, 200);
};
