// 튜터 백엔드 — Nous Portal(OpenAI 호환) 스트리밍.
//   chat.ts 의 `claude -p` 경로와 **같은 SSE 이벤트**(delta/done/end/error)를 뱉어 프런트가 구분 못 하게 한다.
//
// ★적용 범위 제한: 이 백엔드가 쓰는 DeepSeek V4 Flash 는 `text->text` 전용이라 **이미지를 못 본다**.
//   튜터의 이미지 첨부·문제 이미지 판독은 claude(비전) 경로가 계속 담당해야 한다 — 라우팅은 chat.ts 가 한다.
//
// ★추론 토큰: 이 모델은 reasoning effort 를 끌 수 없고(default high) 추론이 completion 예산을 같이 먹는다.
//   위젯 생성에선 출력의 85-90%가 추론이었다. 채팅은 첫 토큰 지연(TTFT)이 UX 를 지배하므로
//   reasoning 델타는 **화면에 흘리지 않되**(UX 청결), 관측을 위해 길이만 usage 로 회수한다.

export type NousUsage = {
  inputTokens: number;
  outputTokens: number;
  reasoningTokens: number;
  cacheReadTokens: number;
  costUsd: number;
};

export type NousStreamHandlers = {
  onDelta: (text: string) => void;
  onError: (message: string) => void;
  onDone: (usage: NousUsage | null) => void;
};

export type NousStreamOptions = {
  systemPrompt: string;
  userPrompt: string;
  model?: string;
  signal?: AbortSignal;
  /** 유휴(델타 끊김) 상한 ms. 총 시간이 아니라 정체를 기준으로 — 정상 응답도 길 수 있다. */
  idleMs?: number;
  maxTokens?: number;
};

const BASE = process.env.NOUS_BASE || 'https://inference-api.nousresearch.com/v1';
export const NOUS_DEFAULT_MODEL = process.env.NOUS_TUTOR_MODEL || '~deepseek/deepseek-v4-flash-latest';

export function nousConfigured(): boolean {
  return Boolean(process.env.NOUS_API_KEY);
}

export async function streamNousTutor(opts: NousStreamOptions, h: NousStreamHandlers): Promise<void> {
  const key = process.env.NOUS_API_KEY;
  if (!key) { h.onError('tutor backend unavailable'); h.onDone(null); return; }

  const ac = new AbortController();
  const idleMs = opts.idleMs ?? 90_000;
  let lastDelta = Date.now();
  let idleAborted = false;
  const idleTimer = setInterval(() => {
    if (Date.now() - lastDelta > idleMs) { idleAborted = true; ac.abort(); }
  }, 5000);
  const onOuterAbort = () => ac.abort();
  opts.signal?.addEventListener('abort', onOuterAbort);
  const cleanup = () => { clearInterval(idleTimer); opts.signal?.removeEventListener('abort', onOuterAbort); };

  let usage: NousUsage | null = null;
  try {
    const res = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: opts.model || NOUS_DEFAULT_MODEL,
        messages: [
          { role: 'system', content: opts.systemPrompt },
          { role: 'user', content: opts.userPrompt },
        ],
        max_tokens: opts.maxTokens ?? 16000,
        stream: true,
        stream_options: { include_usage: true },
      }),
      signal: ac.signal,
    });
    if (!res.ok || !res.body) {
      // 본문은 서버 로그에만 — 클라엔 일반 메시지(경로·키 누출 방지, claude 경로와 동일 정책).
      console.error('[chat/nous] HTTP', res.status, (await res.text().catch(() => '')).slice(0, 500));
      h.onError('tutor backend error'); cleanup(); h.onDone(null); return;
    }

    let buf = '';
    let reasoningLen = 0;
    const dec = new TextDecoder();
    for await (const chunk of res.body as unknown as AsyncIterable<Uint8Array>) {
      lastDelta = Date.now();
      buf += dec.decode(chunk, { stream: true });
      let nl: number;
      while ((nl = buf.indexOf('\n')) !== -1) {
        const line = buf.slice(0, nl).trim();
        buf = buf.slice(nl + 1);
        if (!line.startsWith('data:')) continue;
        const payload = line.slice(5).trim();
        if (!payload || payload === '[DONE]') continue;
        let j: any;
        try { j = JSON.parse(payload); } catch { continue; }
        if (j.usage) {
          usage = {
            inputTokens: j.usage.prompt_tokens ?? 0,
            outputTokens: j.usage.completion_tokens ?? 0,
            reasoningTokens: j.usage.completion_tokens_details?.reasoning_tokens ?? 0,
            cacheReadTokens: j.usage.prompt_tokens_details?.cached_tokens ?? 0,
            costUsd: j.usage.cost ?? 0,
          };
        }
        const d = j.choices?.[0]?.delta;
        if (!d) continue;
        if (typeof d.reasoning === 'string') reasoningLen += d.reasoning.length;   // 화면엔 안 흘림
        if (typeof d.content === 'string' && d.content) h.onDelta(d.content);
      }
    }
    if (usage && !usage.reasoningTokens && reasoningLen) usage.reasoningTokens = Math.round(reasoningLen / 4);
  } catch (e) {
    const msg = idleAborted ? `유휴 ${Math.round(idleMs / 1000)}s 초과` : String((e as Error)?.message || e);
    // 외부 abort(클라 연결 끊김)는 정상 종료 — 에러 이벤트를 쏘지 않는다.
    if (!opts.signal?.aborted) {
      console.error('[chat/nous] stream aborted:', msg);
      h.onError('tutor backend error');
    }
  }
  cleanup();
  h.onDone(usage);
}
