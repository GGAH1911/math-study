// 제품 튜터 백엔드 — 외부 API(Nous Portal, OpenAI 호환) 스트리밍.
//   chat.ts 의 `claude -p` 경로와 **같은 SSE 이벤트**(delta/done/end/error)를 뱉어 프런트가 구분 못 하게 한다.
//
// ★왜 외부 API 인가: 튜터를 개인 Claude 구독에 묶어두면 **판매가 불가능**하다(약관·다중유저·인증
//   안정성). 개발·측정·채점은 구독으로, 제품 서빙만 이쪽으로 — 두 경로를 섞지 않는다.
//
// ★기본 모델 = openai/gpt-5.6-luna. 40문항 블라인드 A/B(심판 2명) 실측 근거:
//   텍스트 지도 7.97(현행 Haiku 7.74 상회) · 이미지 판독 **10.0/10, 오독 0** · TTFT 1.8s(최속)
//   · 캐시 적중 99.9%(OpenAI 자동) · 학생 100명 월 \$24. "luna 보다 싸고 동시에 좋은" 후보는 없었다
//   (qwen3.7-flash 는 싸지만 7.46, gpt-5-nano 는 추론 강제라 실측 6배 비쌈, gemma4 는 8.25지만 캐싱
//   불가로 월 \$121). [[reference_nous_portal]]
//
// ★비용 구조: 입력이 출력의 27배(시스템 프롬프트 27k자)라 **캐싱이 비용의 거의 전부**를 결정한다.
//   cache_control 을 안 붙이면 8배 더 낸다(Haiku 실측 \$0.02068 → \$0.00263).

import { readFileSync } from 'node:fs';

export type NousUsage = {
  inputTokens: number;
  outputTokens: number;
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
  /** 사용자가 첨부한 이미지(data:image/...;base64,...) — 그대로 실어 보낸다. */
  imageDataUrls?: string[];
  /** 서버 파일시스템의 이미지(문제 도형·타일). 읽어서 base64 로 변환해 보낸다. */
  imageFilePaths?: string[];
  model?: string;
  signal?: AbortSignal;
  /** 유휴(델타 끊김) 상한 ms. 총 시간이 아니라 정체를 기준으로 — 정상 응답도 길 수 있다. */
  idleMs?: number;
  maxTokens?: number;
};

const BASE = process.env.NOUS_BASE || 'https://inference-api.nousresearch.com/v1';
export const NOUS_DEFAULT_MODEL = process.env.NOUS_TUTOR_MODEL || 'openai/gpt-5.6-luna';
/** 이미지 1장당 base64 상한(약 7MB) — 프롬프트 폭주·타임아웃 방지. */
const MAX_IMG_BYTES = 5 * 1024 * 1024;
const MAX_IMAGES = 8;

export function nousConfigured(): boolean {
  return Boolean(process.env.NOUS_API_KEY);
}

/** 파일 경로 → data URL. 읽기 실패·과대 파일은 조용히 건너뛴다(튜터를 막지 않는다). */
function fileToDataUrl(p: string): string | null {
  try {
    const buf = readFileSync(p);
    if (buf.length > MAX_IMG_BYTES) { console.warn(`[chat/nous] 이미지 과대 스킵(${buf.length}B): ${p}`); return null; }
    const ext = /\.jpe?g$/i.test(p) ? 'jpeg' : /\.webp$/i.test(p) ? 'webp' : 'png';
    return `data:image/${ext};base64,${buf.toString('base64')}`;
  } catch (e) {
    console.warn('[chat/nous] 이미지 읽기 실패:', p, (e as Error)?.message);
    return null;
  }
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

  // ── 이미지 조립 ────────────────────────────────────────────────────────────────
  // claude 경로는 임시파일 + Read 도구로 봤지만, 외부 API 엔 그 개념이 없다 → base64 로 직접 싣는다.
  // 사용자 첨부는 이미 data URL 이라 변환 불필요. 문제 도형·타일만 디스크에서 읽는다.
  const images: string[] = [];
  for (const u of opts.imageDataUrls ?? []) { if (images.length < MAX_IMAGES) images.push(u); }
  for (const p of opts.imageFilePaths ?? []) {
    if (images.length >= MAX_IMAGES) break;
    const d = fileToDataUrl(p);
    if (d) images.push(d);
  }

  const userContent: unknown = images.length
    ? [{ type: 'text', text: opts.userPrompt }, ...images.map((url) => ({ type: 'image_url', image_url: { url } }))]
    : opts.userPrompt;

  let usage: NousUsage | null = null;
  try {
    const res = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: opts.model || NOUS_DEFAULT_MODEL,
        messages: [
          // ★cache_control: 시스템 프롬프트는 **같은 페이지의 모든 턴에 byte-identical** 이라 캐시가 산다.
          //   per-user·질문별 동적값은 chat.ts 가 userPrompt 로 빼놨다(캐시 경계 밖) — 그 설계 덕분이다.
          { role: 'system', content: [{ type: 'text', text: opts.systemPrompt, cache_control: { type: 'ephemeral' } }] },
          { role: 'user', content: userContent },
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
            cacheReadTokens: j.usage.prompt_tokens_details?.cached_tokens ?? 0,
            costUsd: j.usage.cost ?? 0,
          };
        }
        const d = j.choices?.[0]?.delta;
        if (d && typeof d.content === 'string' && d.content) h.onDelta(d.content);
        // reasoning 델타는 화면에 흘리지 않는다(UX 청결). luna 는 기본 비추론이라 대개 오지 않는다.
      }
    }
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
