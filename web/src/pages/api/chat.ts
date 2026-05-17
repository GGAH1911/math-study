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
  const body = (await request.json()) as ChatRequest;
  const { slug, collection = 'concepts', messages, model = 'haiku' } = body;

  if (!slug || !Array.isArray(messages) || messages.length === 0) {
    return new Response(JSON.stringify({ error: 'slug + messages required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  const lastUser = messages[messages.length - 1];
  if (lastUser.role !== 'user') {
    return new Response(JSON.stringify({ error: 'last message must be user' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { systemPrompt } = buildTutorPrompt(slug, collection);
  const userPrompt = (formatHistory(messages) + '\n' + lastUser.content).trim();

  const args = [
    '-p',
    '--model', model,
    '--max-turns', '1',
    '--output-format', 'stream-json',
    '--include-partial-messages',
    '--verbose',
    '--no-session-persistence',
    '--system-prompt', systemPrompt,
    userPrompt,
  ];

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      const child = spawn('claude', args, {
        env: process.env,
        stdio: ['ignore', 'pipe', 'pipe'],
      });

      const encoder = new TextEncoder();
      const sendEvent = (event: string, data: unknown) => {
        controller.enqueue(encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`));
      };

      let buf = '';
      child.stdout.on('data', (chunk: Buffer) => {
        buf += chunk.toString('utf-8');
        let nl;
        while ((nl = buf.indexOf('\n')) !== -1) {
          const line = buf.slice(0, nl).trim();
          buf = buf.slice(nl + 1);
          if (!line) continue;
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

      child.stderr.on('data', (chunk: Buffer) => {
        sendEvent('error', { message: chunk.toString('utf-8') });
      });

      child.on('close', (code) => {
        if (code !== 0) sendEvent('error', { message: `claude exited with code ${code}` });
        sendEvent('end', {});
        controller.close();
      });

      child.on('error', (err) => {
        sendEvent('error', { message: err.message });
        controller.close();
      });
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
