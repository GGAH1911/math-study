import type { APIRoute } from 'astro';
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, unlinkSync, existsSync, readdirSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { buildTutorPrompt, searchConcepts } from '../../lib/chat-context.ts';
import { buildLearnerContext } from '../../lib/learner.ts';
import { getMastery } from '../../lib/mastery.ts';
import problemIndex from '../../data/problems-by-concept.json';

export const prerender = false;

type ChatMessage = { role: 'user' | 'assistant'; content: string; images?: string[] };

type ChatRequest = {
  slug: string;            // <collection>/<slug> the chat is anchored to ('__nav__' for dashboard)
  collection?: 'concepts' | 'problems' | 'dashboard';
  messages: ChatMessage[]; // full conversation history, last entry is the new user msg
  model?: 'haiku' | 'sonnet' | 'opus';
};

// --- Security hardening ----------------------------------------------------
// The chat endpoint spawns the `claude` CLI on every request. Without these
// guards a user (or anyone they share the URL with over Tailscale) could
// prompt-inject the model into reading /etc/passwd, dumping ~/.ssh, running
// arbitrary shell, etc. Hard limits on input + zero tool access on the CLI
// side keep the blast radius to "just text in, just text out".
const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$|^__nav__$/;
const ALLOWED_COLLECTIONS: ReadonlySet<'concepts' | 'problems' | 'dashboard'> =
  new Set(['concepts', 'problems', 'dashboard']);
const ALLOWED_MODELS: ReadonlySet<'haiku' | 'sonnet' | 'opus'> =
  new Set(['haiku', 'sonnet', 'opus']);
const MAX_USER_MESSAGE_CHARS = 4000;
const MAX_ASSISTANT_MESSAGE_CHARS = 12_000; // 다단 작도 응답 (의존 그래프 + sympy + geometry spec) 수용
const MAX_HISTORY_TURNS = 30;
const MAX_TOTAL_HISTORY_CHARS = 60_000;

// Only forward env vars the claude CLI actually needs. Strip ssh agents,
// AWS creds, git tokens, anything sensitive that happens to live in
// process.env.
function safeChildEnv(): NodeJS.ProcessEnv {
  const ALLOW = ['PATH', 'HOME', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TERM',
                 'ANTHROPIC_API_KEY', 'CLAUDE_CONFIG_DIR'];
  const out: NodeJS.ProcessEnv = {};
  for (const k of ALLOW) {
    const v = process.env[k];
    if (v !== undefined) out[k] = v;
  }
  return out;
}

const TMP_IMG_DIR = join(tmpdir(), 'mathstudy-chat');
// 모듈 로드 시 1시간 지난 임시 첨부 이미지 청소 (leak 방지).
try {
  if (existsSync(TMP_IMG_DIR)) {
    const now = Date.now();
    for (const f of readdirSync(TMP_IMG_DIR)) {
      const p = join(TMP_IMG_DIR, f);
      try { if (now - statSync(p).mtimeMs > 3_600_000) unlinkSync(p); } catch { /* */ }
    }
  }
} catch { /* */ }

function formatHistory(messages: ChatMessage[]): string {
  // Take all but the last (which is the new user message)
  const history = messages.slice(0, -1);
  if (history.length === 0) return '';
  return [
    '--- 이전 대화 ---',
    ...history.map((m) => `[${m.role === 'user' ? '학생' : '튜터'}]: ${m.content}`),
    '',
    '--- 학생의 새 질문 ---',
  ].join('\n');
}

// --- 연결된 기출 주입 -------------------------------------------------------
// 개념 노드의 튜터가 "이 개념에 연결된 기출이 뭔지" 몰라 "DB 접근 못 한다"고 답하던 문제 수정.
// 보안 설계: LLM CLI 는 여전히 DB·도구 접근이 전혀 없다(--tools ""). **서버**가 predev 로 빌드된
// 정적 인덱스(problems-by-concept.json)에서 비민감 메타(연도·번호·배점·난이도·링크)만 조회해
// 프롬프트에 텍스트로 주입한다. 정답·풀이는 넣지 않는다(답 유출 방지). 프롬프트·비용 한도 위해
// 상위 N개만 주입하고 총 개수는 명시. 조회는 미들웨어 인증 게이팅 하에서만 도달한다(신규 표면 0).
type ProblemBrief = {
  slug: string; year: number | null; exam_type: string | null; session: string | null;
  grade: string | null; subject: string | null; number: number | null; score: number | null;
  killer_tier: string | null; format: string | null; has_image: boolean;
};
const LINKED_PROBLEM_CAP = 12;
function linkedProblemLabel(p: ProblemBrief): string {
  const yearShort = p.year ? String(p.year).slice(2) : '';
  const subj = p.subject && p.subject !== '단일' && p.subject !== '공통' ? ` ${p.subject}` : '';
  const session = p.session ? ` ${p.session}` : '';
  const exam = p.exam_type ?? '';
  const grade = p.grade && p.exam_type !== '수능' ? ` ${p.grade}` : '';
  return `${yearShort}${grade}${session} ${exam}${subj} ${p.number ?? '?'}번`.replace(/\s+/g, ' ').trim();
}
function linkedProblemsBlock(slug: string): string {
  const by = (problemIndex as { byConcept?: Record<string, ProblemBrief[]> }).byConcept ?? {};
  let list = by[slug];
  if (!Array.isArray(list) || list.length === 0) {
    // byConcept 키는 정식(중첩)경로 + flat leaf 혼재 → leaf 폴백(개념 페이지와 동일 보정).
    const leaf = (slug.split('/').pop() ?? slug).normalize('NFC');
    list = by[leaf] ?? [];
  }
  if (!Array.isArray(list) || list.length === 0) return '';
  const TIER: Record<string, number> = { early: 0, mid: 1, high: 2, killer: 3 };
  const sorted = [...list].sort((a, b) => {
    const ta = TIER[a.killer_tier ?? ''] ?? 1, tb = TIER[b.killer_tier ?? ''] ?? 1;
    if (ta !== tb) return ta - tb;            // 쉬운 것부터(학생 부담 적게)
    return (b.year ?? 0) - (a.year ?? 0);     // 그 안에서 최신순
  });
  const total = list.length;
  const lines = sorted.slice(0, LINKED_PROBLEM_CAP).map((p) => {
    const tier = p.killer_tier && p.killer_tier !== 'early' ? ` [${p.killer_tier}]` : '';
    const sc = p.score != null ? ` ${p.score}점` : '';
    return `  - ${linkedProblemLabel(p)}${sc}${tier}:  /problems/${p.slug}`;
  }).join('\n');
  const more = total > LINKED_PROBLEM_CAP
    ? `\n  …외 ${total - LINKED_PROBLEM_CAP}개 (총 ${total}개 — 이 페이지 '이 개념의 기출' 섹션에 전체 목록)`
    : '';
  return `

--- 이 개념에 연결된 기출 문제 (서버가 DB 인덱스에서 주입 · 총 ${total}개) ---
이 개념 노드에 실제로 연결된 기출 목록이다. 학생이 "이 개념 기출 뭐 있어?"처럼 물으면
**반드시 이 목록에서** 안내한다 — "DB 접근을 못 한다"는 식으로 답하지 말 것. 링크는 아래
\`/problems/...\` 경로를 **글자 그대로** 제시한다(경로를 줄이거나 바꾸면 404). 다만 너는 지금
문제 **본문은 볼 수 없고** 메타데이터(연도·번호·배점·난이도)만 안다 — 특정 문제를 같이 풀고
싶으면 그 문제 페이지로 가도록 안내하라(거기선 튜터가 문제를 직접 본다). 목록에 없는 문제나
정답은 지어내지 말 것.
${lines}${more}`;
}

export const POST: APIRoute = async ({ request, locals }) => {
  // --- Input validation -------------------------------------------------
  // Note: no Origin/Host check here on purpose. The app is reachable both
  // via the Astro dev host (127.0.0.1:4321) and a Tailscale reverse proxy
  // (tme-laptop.tailf47aa4.ts.net:8443); request.url stays on the dev
  // host even when the client is on the proxy, so a same-host comparison
  // produces false positives. Host-side hardening relies instead on
  // (a) `--tools ""` (claude CLI has no Read/Write/Bash), (b) slug regex
  // + path.resolve guards in chat-context, (c) env whitelist on the
  // child process, (d) message length / turn count caps below.
  let body: ChatRequest;
  try { body = (await request.json()) as ChatRequest; }
  catch {
    return new Response(JSON.stringify({ error: 'invalid json' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  const { slug, collection = 'concepts', messages, model = 'haiku' } = body;

  if (!slug || typeof slug !== 'string' || !SLUG_RE.test(slug)) {
    return new Response(JSON.stringify({ error: 'invalid slug' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  if (!ALLOWED_COLLECTIONS.has(collection)) {
    return new Response(JSON.stringify({ error: 'invalid collection' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  if (!ALLOWED_MODELS.has(model)) {
    return new Response(JSON.stringify({ error: 'invalid model' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  if (!Array.isArray(messages) || messages.length === 0) {
    return new Response(JSON.stringify({ error: 'messages required' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  if (messages.length > MAX_HISTORY_TURNS) {
    return new Response(JSON.stringify({ error: `too many turns (>${MAX_HISTORY_TURNS})` }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  let totalChars = 0;
  for (const m of messages) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant') ||
        typeof m.content !== 'string') {
      return new Response(JSON.stringify({ error: 'invalid message shape' }), {
        status: 400, headers: { 'Content-Type': 'application/json' },
      });
    }
    const lim = m.role === 'assistant' ? MAX_ASSISTANT_MESSAGE_CHARS : MAX_USER_MESSAGE_CHARS;
    if (m.content.length > lim) {
      return new Response(JSON.stringify({ error: `${m.role} message too long (>${lim} chars)` }), {
        status: 400, headers: { 'Content-Type': 'application/json' },
      });
    }
    totalChars += m.content.length;
  }
  if (totalChars > MAX_TOTAL_HISTORY_CHARS) {
    return new Response(JSON.stringify({ error: 'history too long' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  const lastUser = messages[messages.length - 1];
  if (lastUser.role !== 'user') {
    return new Response(JSON.stringify({ error: 'last message must be user' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  // 첨부 이미지 검증 — data:image/* base64, 1장, ~5MB.
  if (lastUser.images !== undefined) {
    if (!Array.isArray(lastUser.images) || lastUser.images.length > 6) {   // 자동 타일 최대 6장
      return new Response(JSON.stringify({ error: 'invalid images' }), {
        status: 400, headers: { 'Content-Type': 'application/json' },
      });
    }
    for (const u of lastUser.images) {
      if (typeof u !== 'string' || !/^data:image\/(png|jpe?g|webp);base64,/.test(u) || u.length > 7_000_000) {
        return new Response(JSON.stringify({ error: 'invalid image dataURL' }), {
          status: 400, headers: { 'Content-Type': 'application/json' },
        });
      }
    }
  }

  // 현재 개념의 **사용자별** mastery — promote(승급/강등) 판정의 기준 상태.
  // frontmatter mastery(전역)는 멤버십 후 무의미하므로, 로그인 사용자의 concept_mastery
  // 를 buildTutorPrompt 에 주입해 튜터가 "현재 상태"를 정확히 알고 판단하게 한다.
  // (이게 없으면 튜터가 절대 레벨을 던져, 실제보다 낮으면 강등으로 뒤집혀 보였다.)
  let userMastery: string | undefined;
  if (collection === 'concepts' && locals.user?.id) {
    try {
      const m = await getMastery(locals.user.id, slug);
      if (m?.mastery) userMastery = m.mastery;
    } catch { /* 조회 실패 시 frontmatter 폴백 */ }
  }
  const { systemPrompt: basePrompt, allowedDirs: baseDirs } = buildTutorPrompt(slug, collection, userMastery);
  // Retrieval grounding: 학생 질문에 매칭되는 *실존* 개념 노드를 프롬프트에 주입해
  // 튜터가 경로를 지어내지 않게 한다(개념 튜터는 현재 페이지 이웃만 알아 멀리 있는
  // 개념은 추측하던 문제). concepts 컬렉션에서만.
  let systemPrompt = basePrompt;
  if (collection === 'concepts' && lastUser.content) {
    const hits = searchConcepts(lastUser.content, 6);
    if (hits.length > 0) {
      // 표시이름(개념명) + **그대로 복사할 완전한 URL**. Haiku 가 긴 nested 경로를 줄여
      // 쓰면 404 (라우트는 전체 경로만 인식) → URL 통째 제시 + verbatim 강조.
      const lines = hits.map((c) => {
        const name = (c.slug.split('/').pop() ?? c.slug).replace(/_/g, ' ');
        return `  - ${name}${c.grade ? ` (${c.grade})` : ''}:  /concepts/${c.slug}`;
      }).join('\n');
      systemPrompt += `\n\n--- 질문 관련 개념 후보 (개념지도에 *실존* · 링크 URL 그대로 복사) ---
학생 질문과 매칭된 실제 개념 노드들. 어디로 가야 할지 안내할 때 **반드시 이 목록에서 고르고**,
마크다운 링크 URL은 **아래 \`/concepts/...\` 를 글자 그대로 복사**한다 — 경로를 절대 줄이거나
바꾸지 말 것(줄이면 404). **이 목록에 없는 개념 경로는 지어내지 말 것**; 적절한 후보가 없으면
"개념지도에 아직 해당 노드가 없다"고 솔직히 말한다.
${lines}`;
    }
  }
  // 이 개념에 연결된 기출(메타데이터)을 서버가 인덱스에서 조회해 주입 — 튜터가 "DB 접근 못 함"
  // 으로 답하던 문제 해결. LLM 은 여전히 DB·도구 접근 0(--tools ""), 비민감 메타만 텍스트로 받음.
  if (collection === 'concepts') {
    systemPrompt += linkedProblemsBlock(slug);
  }
  // 학습자 모델: 이 학생의 정량 수준 + 정성 프로필을 프롬프트에 주입(per-user, 하드코딩 0).
  const learnerUserId = locals.user?.id;
  if (learnerUserId) {
    try {
      const learner = await buildLearnerContext(learnerUserId);
      if (learner) systemPrompt += `\n\n${learner}`;
    } catch { /* 학습자 컨텍스트 실패는 튜터 동작을 막지 않음 */ }
  }

  let userPrompt = (formatHistory(messages) + '\n' + lastUser.content).trim();

  // 사용자가 첨부한 이미지를 임시 PNG 로 저장 → claude CLI 가 Read 도구로 직접 본다
  // (문제 PNG 와 동일 메커니즘). 응답 종료 시 삭제(cleanup).
  const tmpImagePaths: string[] = [];
  const allowedDirs = [...(baseDirs ?? [])];
  if (lastUser.images && lastUser.images.length > 0) {
    try {
      mkdirSync(TMP_IMG_DIR, { recursive: true });
      for (const dataUrl of lastUser.images) {
        const m = dataUrl.match(/^data:image\/(png|jpe?g|webp);base64,(.+)$/);
        if (!m) continue;
        const ext = m[1] === 'jpeg' ? 'jpg' : m[1];
        const p = join(TMP_IMG_DIR, `${randomUUID()}.${ext}`);
        writeFileSync(p, Buffer.from(m[2], 'base64'));
        tmpImagePaths.push(p);
      }
      if (tmpImagePaths.length) {
        if (!allowedDirs.includes(TMP_IMG_DIR)) allowedDirs.push(TMP_IMG_DIR);
        // 큰 이미지는 클라가 원해상도 타일 N장으로 쪼개 보냄 → 모두 Read 시킴.
        const note = tmpImagePaths.length === 1
          ? `먼저 Read 도구로 이 파일을 보고 반영해 답하세요: ${tmpImagePaths[0]}`
          : `이미지가 커서 ${tmpImagePaths.length}장으로 나뉘었습니다(위→아래·행→열 순, 경계 약간 겹침). `
            + `${tmpImagePaths.length}장을 **모두** Read 로 열어 하나로 이어 붙여 보고 반영하세요:\n`
            + tmpImagePaths.map((p, i) => `  ${i + 1}. ${p}`).join('\n');
        userPrompt = `[학생이 이미지를 첨부했습니다. ${note}]\n\n${userPrompt}`;
      }
    } catch (e) {
      console.error('[chat] temp image write failed:', e);
    }
  }

  // problem 페이지 이미지 dir 또는 사용자 첨부 이미지가 있으면 Read 도구 활성.
  // 보안: --add-dir 로 해당 디렉토리만 한정 → 다른 파일은 못 봄.
  const enableRead = allowedDirs.length > 0;

  const args: string[] = [
    '-p',
    '--model', model,
    // Read 도구 활성화면 LLM 이 turn 을 더 쓸 수 있어야 안전:
    //   1) Read 호출 → 2) 결과 process → 3) python 코드 emit → 4) 답변
    // 부족하면 LLM 이 mid-response 에서 exit code 1 로 빠진다.
    '--max-turns', enableRead ? String(Math.min(40, 15 + tmpImagePaths.length * 2)) : '2',
    '--output-format', 'stream-json',
    '--include-partial-messages',
    '--verbose',
    '--no-session-persistence',
  ];
  if (enableRead) {
    args.push('--allowedTools', 'Read');
    // Haiku 가 system prompt 의 "sympy 자동 실행" 안내를 무시하고 Bash 로
    // python 직접 실행하려 들면 권한 거부 → 재시도 반복 → max_turns 초과로
    // exit 1. 명시적으로 Bash·Edit·Write 등 금지.
    args.push('--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch');
    for (const d of allowedDirs!) {
      args.push('--add-dir', d);
    }
  } else {
    // Hard-disable every tool. injection 차단.
    args.push('--tools', '');
  }
  args.push(
    '--system-prompt', systemPrompt,
    // `--` forces everything after it to be treated as a positional arg.
    '--',
    userPrompt,
  );

  const state = { closed: false, child: null as ReturnType<typeof spawn> | null };
  const cleanup = () => { while (tmpImagePaths.length) { const p = tmpImagePaths.pop()!; try { unlinkSync(p); } catch { /* */ } } };
  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      const child = spawn('claude', args, {
        env: safeChildEnv(),
        stdio: ['ignore', 'pipe', 'pipe'],
      });
      state.child = child;

      const encoder = new TextEncoder();
      const sendEvent = (event: string, data: unknown) => {
        if (state.closed) return;
        try {
          controller.enqueue(encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`));
        } catch {
          state.closed = true;
        }
      };

      let buf = '';
      const recentLines: string[] = []; // 디버깅 위해 마지막 10줄 보관
      // Streaming decoder: a multibyte (Korean) char can straddle a stdout
      // chunk boundary. Per-chunk Buffer.toString('utf-8') would corrupt it;
      // a single TextDecoder with {stream:true} carries the partial bytes.
      const stdoutDecoder = new TextDecoder();
      child.stdout.on('data', (chunk: Buffer) => {
        buf += stdoutDecoder.decode(chunk, { stream: true });
        let nl;
        while ((nl = buf.indexOf('\n')) !== -1) {
          const line = buf.slice(0, nl).trim();
          buf = buf.slice(nl + 1);
          if (!line) continue;
          recentLines.push(line.slice(0, 300));
          if (recentLines.length > 12) recentLines.shift();
          try {
            const obj = JSON.parse(line);
            // stream_event with content_block_delta type=text_delta carries the text
            if (obj.type === 'stream_event' && obj.event?.type === 'content_block_delta') {
              const delta = obj.event.delta;
              if (delta?.type === 'text_delta' && typeof delta.text === 'string') {
                sendEvent('delta', { text: delta.text });
              }
              // We intentionally drop thinking_delta — keep the UX clean.
            } else if (obj.type === 'system' && obj.subtype === 'post_turn_summary') {
              sendEvent('done', { status: obj.status_category });
            } else if (obj.type === 'rate_limit_event') {
              sendEvent('rate_limit', obj.rate_limit_info ?? {});
            }
          } catch {
            // ignore non-JSON lines
          }
        }
      });

      // Never forward raw stderr to the client — it may contain absolute
      // paths, env-derived strings, or stack traces from the CLI. Log
      // server-side instead, surface a generic error to the browser.
      let stderrBuf = '';
      const stderrDecoder = new TextDecoder();
      child.stderr.on('data', (chunk: Buffer) => {
        stderrBuf += stderrDecoder.decode(chunk, { stream: true });
        if (stderrBuf.length > 8192) stderrBuf = stderrBuf.slice(-8192);
      });

      child.on('close', (code) => {
        if (code !== 0) {
          console.error(`[chat] claude exited code=${code} stderr=${stderrBuf.slice(-2000)}`);
          console.error(`[chat] last stdout lines:`, recentLines);
          sendEvent('error', { message: 'tutor backend error' });
        }
        sendEvent('end', {});
        if (!state.closed) { state.closed = true; try { controller.close(); } catch { /* already closed */ } }
        cleanup();
      });

      child.on('error', (err) => {
        console.error('[chat] spawn error:', err);
        sendEvent('error', { message: 'tutor backend unavailable' });
        if (!state.closed) { state.closed = true; try { controller.close(); } catch { /* already closed */ } }
        cleanup();
      });
    },
    cancel() {
      // client disconnect — mark closed + kill child so stdout events stop arriving.
      state.closed = true;
      try { state.child?.kill('SIGTERM'); } catch { /* already exited */ }
      cleanup();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    },
  });
};
