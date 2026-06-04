// OpenRouter BYOK relay — 학생 API key 와 함께 OpenRouter chat completions
// 호출, OpenAI 호환 SSE 응답을 우리 ChatPanel 의 SSE 포맷 ('event: delta')으로
// 변환해 streaming 으로 돌려준다.
//
// 학생 데이터는 서버에 저장하지 않음 (transit relay only — 저작권 안전).

import type { APIRoute } from 'astro';
import { buildTutorPrompt, buildCompactTutorPrompt } from '../../lib/chat-context.ts';
import { isVisionDisabled } from '../../lib/vision.ts';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

export const prerender = false;

type ChatMessage = { role: 'user' | 'assistant'; content: string; images?: string[] };

type ChatRequest = {
  slug: string;
  collection?: 'concepts' | 'problems' | 'dashboard';
  messages: ChatMessage[];
  model: string;
  apiKey: string;
  /** default https://openrouter.ai/api/v1, Ollama local 은 http://.../v1 */
  baseURL?: string;
};

const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$|^__nav__$/;
const ALLOWED_COLLECTIONS: ReadonlySet<'concepts' | 'problems' | 'dashboard'> =
  new Set(['concepts', 'problems', 'dashboard']);
const MAX_USER_MESSAGE_CHARS = 4000;
const MAX_ASSISTANT_MESSAGE_CHARS = 12_000;
const MAX_HISTORY_TURNS = 30;
const MAX_TOTAL_HISTORY_CHARS = 60_000;
const MAX_MODEL_LEN = 100;
const MAX_KEY_LEN = 200;

// OpenAI 호환 message content (text or image_url)
type ContentBlock = { type: 'text'; text: string } | { type: 'image_url'; image_url: { url: string } };
type OpenAIMessage = { role: 'system' | 'user' | 'assistant'; content: string | ContentBlock[] };

async function readImageAsDataURL(absPath: string): Promise<string | null> {
  try {
    const buf = await readFile(absPath);
    const ext = path.extname(absPath).slice(1).toLowerCase();
    const mime = ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : ext === 'png' ? 'image/png' : `image/${ext}`;
    return `data:${mime};base64,${buf.toString('base64')}`;
  } catch {
    return null;
  }
}

export const POST: APIRoute = async ({ request }) => {
  let body: ChatRequest;
  try { body = (await request.json()) as ChatRequest; }
  catch {
    return new Response(JSON.stringify({ error: 'invalid json' }), {
      status: 400, headers: { 'Content-Type': 'application/json' },
    });
  }
  const { slug, collection = 'concepts', messages, model, apiKey, baseURL: rawBaseURL } = body;
  // baseURL whitelist — SSRF 차단. https / 또는 localhost·tailnet IP 만.
  const baseURL = (rawBaseURL || 'https://openrouter.ai/api/v1').trim();
  if (!/^https:\/\/|^http:\/\/(localhost|127\.0\.0\.1|0\.0\.0\.0|192\.168\.|10\.|100\.[0-9]{1,3}\.|172\.(1[6-9]|2[0-9]|3[01])\.)/.test(baseURL)) {
    console.warn('[openrouter] invalid baseURL:', baseURL);
    return new Response(JSON.stringify({ error: 'baseURL must be https:// or http://(localhost|RFC1918|tailnet)', got: baseURL }), { status: 400 });
  }
  if (baseURL.length > 300) {
    return new Response(JSON.stringify({ error: 'baseURL too long' }), { status: 400 });
  }

  if (!slug || typeof slug !== 'string' || !SLUG_RE.test(slug)) {
    console.warn('[openrouter] invalid slug:', slug);
    return new Response(JSON.stringify({ error: 'invalid slug', got: slug }), { status: 400 });
  }
  if (!ALLOWED_COLLECTIONS.has(collection)) {
    return new Response(JSON.stringify({ error: 'invalid collection' }), { status: 400 });
  }
  if (typeof model !== 'string' || model.length === 0 || model.length > MAX_MODEL_LEN) {
    return new Response(JSON.stringify({ error: 'invalid model' }), { status: 400 });
  }
  // Ollama 등 인증 없는 endpoint 는 짧은 dummy ('ollama') 허용
  if (typeof apiKey !== 'string' || apiKey.length === 0 || apiKey.length > MAX_KEY_LEN) {
    return new Response(JSON.stringify({ error: 'invalid apiKey' }), { status: 400 });
  }
  if (!Array.isArray(messages) || messages.length === 0 || messages.length > MAX_HISTORY_TURNS) {
    return new Response(JSON.stringify({ error: 'invalid messages' }), { status: 400 });
  }
  let totalChars = 0;
  for (const m of messages) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant') || typeof m.content !== 'string') {
      return new Response(JSON.stringify({ error: 'invalid message shape' }), { status: 400 });
    }
    const lim = m.role === 'assistant' ? MAX_ASSISTANT_MESSAGE_CHARS : MAX_USER_MESSAGE_CHARS;
    if (m.content.length > lim) {
      return new Response(JSON.stringify({ error: `${m.role} message too long (>${lim})` }), { status: 400 });
    }
    totalChars += m.content.length;
  }
  if (totalChars > MAX_TOTAL_HISTORY_CHARS) {
    return new Response(JSON.stringify({ error: 'history too long' }), { status: 400 });
  }
  if (messages[messages.length - 1].role !== 'user') {
    return new Response(JSON.stringify({ error: 'last message must be user' }), { status: 400 });
  }
  // 첨부 이미지 검증 — data:image/* base64만 허용(http URL 거부 = SSRF/저작권), 1장, ~5MB.
  for (const m of messages) {
    if (m.images === undefined) continue;
    if (!Array.isArray(m.images) || m.images.length > 6) {   // 자동 타일 최대 6장
      return new Response(JSON.stringify({ error: 'invalid images' }), { status: 400 });
    }
    for (const u of m.images) {
      if (typeof u !== 'string' || !/^data:image\/(png|jpe?g|webp);base64,/.test(u) || u.length > 7_000_000) {
        return new Response(JSON.stringify({ error: 'invalid image dataURL' }), { status: 400 });
      }
    }
  }

  // 작은 모델 (e4b / e2b / 7b 이하 / gemma 2/3) 는 압축 prompt + few-shot.
  // 큰 모델 (haiku/gemini/gpt/qwen-vl-72b 등) 은 full prompt 그대로.
  const isSmallModel = /e[24]b|:1b|:3b|:4b|:7b|gemma[234](?!.*(?:26b|31b|27b))/i.test(model)
    || (/qwen2?\.5/i.test(model) && !/72b|32b/i.test(model));
  const { systemPrompt, allowedDirs, imagePaths } = isSmallModel
    ? buildCompactTutorPrompt(slug, collection)
    : buildTutorPrompt(slug, collection);
  console.log(`[openrouter] model=${model} compact=${isSmallModel} sysprompt=${systemPrompt.length}chars`);

  // OpenAI 호환 messages 조립. 첫 user 메시지에 문제 이미지 base64 첨부 (vision).
  // vision 미지원 패턴: free 모델 다수, 일부 텍스트 전용 모델, 명시적 텍스트 only 모델.
  // 단 gemma3+/4+ / llama3.2-vision / claude / gemini 등은 vision OK.
  const visionDisabled = isVisionDisabled(model);
  const hasUserImage = messages.some((m) => Array.isArray(m.images) && m.images.length > 0);
  const sysPrompt = (hasUserImage && !visionDisabled)
    ? systemPrompt + '\n\n[이미지] 학생이 첨부한 이미지가 user 메시지에 image_url 로 함께 전달됐다 — 먼저 그 이미지를 읽고 반영해 답하라.'
    : systemPrompt;
  const oaiMessages: OpenAIMessage[] = [{ role: 'system', content: sysPrompt }];
  let imageAttached = false;
  for (let i = 0; i < messages.length; i++) {
    const m = messages[i];
    const blocks: ContentBlock[] = [];
    // (1) 서버 문제 이미지 — problems 첫 user. 타일이 있으면 N장 모두 첨부(세로 긴 문제 원해상도).
    if (!visionDisabled && m.role === 'user' && !imageAttached && collection === 'problems' && imagePaths && imagePaths.length > 0) {
      for (const p of imagePaths) {
        const dataUrl = await readImageAsDataURL(p);
        if (dataUrl) blocks.push({ type: 'image_url', image_url: { url: dataUrl } });
      }
      imageAttached = true;
    }
    // (2) 학생이 첨부한 이미지 (해당 user 메시지에 실린 것)
    if (!visionDisabled && m.role === 'user' && Array.isArray(m.images)) {
      for (const u of m.images) blocks.push({ type: 'image_url', image_url: { url: u } });
    }
    if (blocks.length) {
      blocks.push({ type: 'text', text: m.content });
      oaiMessages.push({ role: 'user', content: blocks });
    } else {
      oaiMessages.push({ role: m.role, content: m.content });
    }
  }

  // OpenRouter chat completions (OpenAI 호환). stream:true 로 SSE.
  let orRes: Response;
  try {
    const url = `${baseURL.replace(/\/$/, '')}/chat/completions`;
    orRes = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/GGAH1911/math-study',
        'X-Title': 'math-study',
      },
      body: JSON.stringify({
        model,
        messages: oaiMessages,
        stream: true,
        // OpenRouter free tier 의 credit 한도 (~15K tokens) 안에 맞추기 위해 명시.
        // 다단 sympy + geometry spec 응답에 4K 충분, 큰 모델은 학생이 max_tokens 옵션 따로.
        max_tokens: 4096,
      }),
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: `network: ${(e as Error).message}` }), { status: 502 });
  }

  if (!orRes.ok || !orRes.body) {
    const errText = await orRes.text().catch(() => '');
    return new Response(JSON.stringify({
      error: `OpenRouter ${orRes.status}: ${errText.slice(0, 300)}`,
    }), { status: orRes.status });
  }

  // OpenAI 호환 SSE → 우리 'delta' / 'end' / 'error' 이벤트로 변환
  const encoder = new TextEncoder();
  const reader = orRes.body.getReader();
  const decoder = new TextDecoder();
  const state = { closed: false };

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      let fullResponse = ''; // debug: 전체 응답 로깅
      const send = (event: string, data: unknown) => {
        if (state.closed) return;
        if (event === 'delta' && typeof (data as { text?: string }).text === 'string') {
          fullResponse += (data as { text: string }).text;
        }
        try {
          controller.enqueue(encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`));
        } catch {
          state.closed = true;
        }
      };
      let buf = '';
      try {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          let idx;
          while ((idx = buf.indexOf('\n')) !== -1) {
            const line = buf.slice(0, idx).trim();
            buf = buf.slice(idx + 1);
            if (!line || !line.startsWith('data: ')) continue;
            const data = line.slice(6);
            if (data === '[DONE]') {
              send('end', {});
              continue;
            }
            try {
              const obj = JSON.parse(data);
              const delta = obj.choices?.[0]?.delta?.content;
              if (typeof delta === 'string' && delta) {
                send('delta', { text: delta });
              }
            } catch { /* malformed line — skip */ }
          }
        }
        send('end', {});
        console.log(`[openrouter] full response (${fullResponse.length} chars):\n---\n${fullResponse}\n---`);
      } catch (e) {
        send('error', { message: (e as Error).message });
      } finally {
        if (!state.closed) { state.closed = true; try { controller.close(); } catch { /* */ } }
      }
    },
    cancel() {
      state.closed = true;
      try { reader.cancel(); } catch { /* */ }
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
