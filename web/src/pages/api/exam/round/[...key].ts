// 회차 시험 구성 — `GET /api/exam/round/<year>/<round>` → `{title, problems, durationSec}`
//
// ★왜 전용 엔드포인트인가: 회차 하나(보통 30문항)를 보려고 문항 목록 4,210건을 클라이언트로
//   보낼 수는 없다. 시험 모드는 **딥링크로 바로 들어오는** 화면이라 `/problems` 를 거쳐 캐시가
//   덥혀 있다고 가정할 수도 없다. 자르는 일은 서버가 한다.
//
// ★계산(정렬·응시시간)도 여기서 한다. 클라이언트가 하면 SSR 판과 갈라지고, 앱·웹 두 곳에
//   같은 규칙을 두 벌로 두게 된다.
import type { APIRoute } from 'astro';
import { readFileSync } from 'node:fs';
import { mediaPath } from '../../../../lib/media-root.ts';
import { SUBJECT_ORDER, roundTitle } from '../../../../lib/problem-meta';

export const prerender = false;

const json = (body: unknown, status: number) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'private, max-age=300' },
  });

type Src = { agency?: string; exam_type?: string; grade?: string; session?: string;
             subject?: string; number?: number; score?: number };
type Row = { id: string; source?: Src; format?: string; problem_image?: string };

const ELECTIVES = ['미적분', '확률과통계', '기하'];
const TRACKS = ['가형', '나형'];

export const GET: APIRoute = async ({ params }) => {
  const key = String(params.key ?? '');
  if (!key) return json({ error: 'bad key' }, 400);

  const abs = mediaPath('/content/problems.index.json');
  if (!abs) return json({ error: 'bad path' }, 400);
  let rows: Row[];
  try {
    rows = (JSON.parse(readFileSync(abs, 'utf8')) as { entries?: Row[] }).entries ?? [];
  } catch {
    return json({ error: 'index not built', hint: 'node web/scripts/emit_content.mjs' }, 503);
  }

  const probs = rows.filter((p) => p.id.startsWith(key + '/'));
  if (probs.length === 0) return json({ error: 'round not found' }, 404);

  // 정렬 규칙은 SSR 판과 같다 — 과목 순서 → 문항 번호.
  const subjIdx = (s: string) => {
    const i = (SUBJECT_ORDER as readonly string[]).indexOf(s);
    return i < 0 ? 99 : i;
  };
  probs.sort((a, b) => {
    const sa = subjIdx(String(a.source?.subject ?? ''));
    const sb = subjIdx(String(b.source?.subject ?? ''));
    if (sa !== sb) return sa - sb;
    return Number(a.source?.number ?? 0) - Number(b.source?.number ?? 0);
  });

  const s0 = probs[0].source;
  const title = roundTitle({
    year: key.split('/')[0],
    agency: String(s0?.agency ?? ''),
    exam_type: String(s0?.exam_type ?? ''),
    grade: String(s0?.grade ?? ''),
    session: String(s0?.session ?? ''),
  });

  const problems = probs.map((p) => ({
    slug: p.id,
    number: Number(p.source?.number ?? 0),
    subject: String(p.source?.subject ?? ''),
    format: p.format ?? 'choice',
    image: p.problem_image ?? `/problem-images/${p.id.split('/').pop()}.png`,
    score: Number(p.source?.score ?? 0),
  }));

  // 응시 문항 수 추정 × 200초/문항, 최소 30분. 가/나형=한 계열 · 공통+선택=공통+선택8.
  const tracksPresent = TRACKS.filter((t) => problems.some((p) => p.subject === t));
  const commonCount = problems.filter((p) => !ELECTIVES.includes(p.subject)).length;
  const hasElective = problems.some((p) => ELECTIVES.includes(p.subject));
  const examCount = tracksPresent.length > 1
    ? problems.filter((p) => p.subject === tracksPresent[0]).length
    : commonCount + (hasElective ? 8 : 0);

  return json({ title, problems, durationSec: Math.max(1800, examCount * 200) }, 200);
};
