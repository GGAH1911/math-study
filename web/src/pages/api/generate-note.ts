// /api/generate-note — given a page slug + chat history, ask claude CLI
// to produce a compact study-note in markdown. Reuses /api/chat's spawn
// pattern but collects the streamed output into a single { note: string }
// response — the note is a one-shot block, no need for SSE on the client.

import type { APIRoute } from 'astro';
import { spawn } from 'node:child_process';
import { buildNotePrompt } from '../../lib/chat-context.ts';

export const prerender = false;

type ChatMessage = { role: 'user' | 'assistant'; content: string };
type NoteRequest = {
  slug: string;
  collection?: 'concepts' | 'problems' | 'dashboard';
  messages: ChatMessage[];
  model?: 'haiku' | 'sonnet' | 'opus';
};

const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$|^__nav__$/;
const ALLOWED_COLLECTIONS: ReadonlySet<'concepts' | 'problems' | 'dashboard'> =
  new Set(['concepts', 'problems', 'dashboard']);
const ALLOWED_MODELS: ReadonlySet<'haiku' | 'sonnet' | 'opus'> =
  new Set(['haiku', 'sonnet', 'opus']);
const MAX_MESSAGE_CHARS = 4000;
const MAX_HISTORY_TURNS = 50;       // notes need more context than a single turn
const MAX_TOTAL_HISTORY_CHARS = 50_000;
const MIN_MESSAGES_FOR_NOTE = 2;    // need at least one user + one assistant exchange

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

function formatTranscript(messages: ChatMessage[]): string {
  return [
    '--- 이번 대화 기록 ---',
    ...messages.map((m) => `[${m.role === 'user' ? '학생' : '튜터'}]: ${m.content}`),
  ].join('\n');
}

export const POST: APIRoute = async ({ request }) => {
  let body: NoteRequest;
  try { body = (await request.json()) as NoteRequest; }
  catch {
    return json({ error: 'invalid json' }, 400);
  }
  const { slug, collection = 'concepts', messages, model = 'haiku' } = body;

  if (!slug || !SLUG_RE.test(slug)) return json({ error: 'invalid slug' }, 400);
  if (!ALLOWED_COLLECTIONS.has(collection)) return json({ error: 'invalid collection' }, 400);
  if (!ALLOWED_MODELS.has(model)) return json({ error: 'invalid model' }, 400);
  if (!Array.isArray(messages) || messages.length < MIN_MESSAGES_FOR_NOTE) {
    return json({ error: `대화가 너무 짧아요. 최소 ${MIN_MESSAGES_FOR_NOTE}개 메시지 필요.` }, 400);
  }
  if (messages.length > MAX_HISTORY_TURNS) {
    return json({ error: `too many turns (>${MAX_HISTORY_TURNS})` }, 400);
  }
  let totalChars = 0;
  for (const m of messages) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant') || typeof m.content !== 'string') {
      return json({ error: 'invalid message shape' }, 400);
    }
    if (m.content.length > MAX_MESSAGE_CHARS) return json({ error: 'message too long' }, 400);
    totalChars += m.content.length;
  }
  if (totalChars > MAX_TOTAL_HISTORY_CHARS) return json({ error: 'history too long' }, 400);

  const { systemPrompt } = buildNotePrompt(slug, collection);
  const userPrompt = formatTranscript(messages);

  const args = [
    '-p',
    '--model', model,
    '--max-turns', '1',
    '--output-format', 'stream-json',
    '--include-partial-messages',
    '--verbose',
    '--no-session-persistence',
    '--tools', '',
    '--system-prompt', systemPrompt,
    '--',
    userPrompt,
  ];

  // Collect the streamed claude output into a single note string.
  const note: string = await new Promise<string>((resolve, reject) => {
    const child = spawn('claude', args, { env: safeChildEnv(), stdio: ['ignore', 'pipe', 'pipe'] });
    let acc = '';
    let buf = '';
    let stderr = '';
    child.stdout.on('data', (chunk: Buffer) => {
      buf += chunk.toString('utf-8');
      let nl;
      while ((nl = buf.indexOf('\n')) !== -1) {
        const line = buf.slice(0, nl).trim();
        buf = buf.slice(nl + 1);
        if (!line) continue;
        try {
          const obj = JSON.parse(line);
          if (obj.type === 'stream_event' && obj.event?.type === 'content_block_delta') {
            const delta = obj.event.delta;
            if (delta?.type === 'text_delta' && typeof delta.text === 'string') {
              acc += delta.text;
            }
          }
        } catch { /* ignore non-JSON noise */ }
      }
    });
    child.stderr.on('data', (chunk: Buffer) => { stderr += chunk.toString('utf-8'); });
    child.on('error', (e) => reject(e));
    child.on('close', (code) => {
      if (code !== 0 && acc.length === 0) {
        reject(new Error(`claude exit ${code}: ${stderr.slice(0, 500)}`));
      } else {
        resolve(acc.trim());
      }
    });
    // 60-second safety timeout.
    setTimeout(() => {
      try { child.kill('SIGKILL'); } catch { /* ignore */ }
      reject(new Error('note generation timeout (60s)'));
    }, 60_000);
  }).catch((e: Error) => `<!-- note generation failed: ${e.message} -->`);

  return json({ note }, 200);
};

function json(payload: unknown, status: number): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
