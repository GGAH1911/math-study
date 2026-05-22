import type { APIRoute } from 'astro';
import { spawn } from 'node:child_process';
import { buildTutorPrompt } from '../../lib/chat-context.ts';

export const prerender = false;

type ChatMessage = { role: 'user' | 'assistant'; content: string };

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

export const POST: APIRoute = async ({ request }) => {
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

  const { systemPrompt, allowedDirs } = buildTutorPrompt(slug, collection);
  const userPrompt = (formatHistory(messages) + '\n' + lastUser.content).trim();

  // problem 페이지 + 이미지 dir 있으면 Read 도구로 그 이미지 만 접근 허용.
  // searchable_text 가 도형을 표현 못 하므로 LLM이 직접 PNG를 봐야 정확.
  // 보안: --add-dir 로 해당 회차 images/ 디렉토리 한정 → 다른 파일은 못 봄.
  const enableRead = collection === 'problems' && allowedDirs && allowedDirs.length > 0;

  const args: string[] = [
    '-p',
    '--model', model,
    // Read 도구 활성화면 LLM 이 turn 을 더 쓸 수 있어야 안전:
    //   1) Read 호출 → 2) 결과 process → 3) python 코드 emit → 4) 답변
    // 부족하면 LLM 이 mid-response 에서 exit code 1 로 빠진다.
    '--max-turns', enableRead ? '15' : '2',
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
      child.stdout.on('data', (chunk: Buffer) => {
        buf += chunk.toString('utf-8');
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
      child.stderr.on('data', (chunk: Buffer) => {
        stderrBuf += chunk.toString('utf-8');
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
      });

      child.on('error', (err) => {
        console.error('[chat] spawn error:', err);
        sendEvent('error', { message: 'tutor backend unavailable' });
        if (!state.closed) { state.closed = true; try { controller.close(); } catch { /* already closed */ } }
      });
    },
    cancel() {
      // client disconnect — mark closed + kill child so stdout events stop arriving.
      state.closed = true;
      try { state.child?.kill('SIGTERM'); } catch { /* already exited */ }
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
