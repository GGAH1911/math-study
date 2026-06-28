// 튜터 메시지 전송 + 검증(sympy·산술·시각) 흐름 — ChatPanel 에서 분리(send body 그대로).
// params 로 state/setter 를 받아 destructure → 본문 무변. deps 배열도 원본과 동일(동작 보존).
import { useCallback, type Dispatch, type SetStateAction } from 'react';
import type { ChatMessage } from './types';
import { MAX_HISTORY_TURNS } from './persistence';
import { sanitizeForDisplay, findArithErr } from './verification';
import { runSympyLocal } from '../pyodide-client';

export type ChatSendParams = {
  input: string;
  pending: string[];
  pendingDisplay: string | null;
  quoted: string | null;
  streaming: boolean;
  messages: ChatMessage[];
  slug: string;
  model: 'haiku' | 'sonnet';
  collection: 'concepts' | 'problems' | 'dashboard';
  byokActive: boolean;
  byokApiKey: string;
  byokModel: string;
  byokBaseURL: string;
  setMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  setError: Dispatch<SetStateAction<string | null>>;
  setStreaming: Dispatch<SetStateAction<boolean>>;
  setQuoted: Dispatch<SetStateAction<string | null>>;
  setPendingDisplay: Dispatch<SetStateAction<string | null>>;
  setPending: Dispatch<SetStateAction<string[]>>;
  setInput: Dispatch<SetStateAction<string>>;
  setImgError: Dispatch<SetStateAction<string | null>>;
};

export function useChatSend(p: ChatSendParams) {
  const {
    input, pending, pendingDisplay, quoted, streaming, messages, slug, model, collection,
    byokActive, byokApiKey, byokModel, byokBaseURL,
    setMessages, setError, setStreaming, setQuoted, setPendingDisplay, setPending, setInput, setImgError,
  } = p;
  const send = useCallback(async (override?: string) => {
    const text = (override ?? input).trim();
    const attachedImgs = override === undefined ? pending : [];    // 합성/노트 호출엔 첨부 없음 (첫 user 메시지에만)
    const attachedDisplay = override === undefined ? pendingDisplay : null;  // 표시용 통이미지(타일과 분리)
    const attachedQuote = override === undefined ? quoted : null;  // 인용 칩(렌더 수식 복붙)
    if ((!text && !attachedImgs.length && !attachedQuote) || streaming) return;  // 이미지/인용만 있어도 전송 허용
    setError(null);
    if (override === undefined) { setInput(''); setPending([]); setPendingDisplay(null); setQuoted(null); setImgError(null); }

    // content 는 LLM(rawHistory) 과 표시 양쪽에 쓰인다. 인용이 있으면 content 에 인용블록을 포함해
    //   LLM 이 맥락을 받고, quoted 필드를 별도로 둬 Message 가 그 인용블록을 *칩*으로 마스킹해 표시한다
    //   (질문 텍스트만 본문에, 인용은 접힌 칩으로). uText=사용자가 실제로 친 질문(칩 옆 표시용).
    const uText = text || (attachedQuote ? '(인용한 내용에 대한 질문)' : '(첨부한 이미지를 봐주세요)');
    const contentForLlm = attachedQuote
      ? `${attachedQuote.split('\n').map((l) => `> ${l}`).join('\n')}\n\n${text || '위 인용 내용에 대해 설명해줘.'}`
      : uText;
    const newUserMsg: ChatMessage = {
      role: 'user',
      content: contentForLlm,
      // images=비전 타일(LLM 전송), displayImage=통이미지(표시) — 사용자에겐 통이미지만 보임.
      ...(attachedImgs.length ? { images: attachedImgs, displayImage: attachedDisplay ?? attachedImgs[0] } : {}),
      ...(attachedQuote ? { quoted: attachedQuote, displayText: uText } : {}),
    };
    const placeholder: ChatMessage = { role: 'assistant', content: '' };
    setMessages([...messages, newUserMsg, placeholder]);
    setStreaming(true);

    // python block 을 채팅창에 노출하지 않기 위한 display sanitize.
    // python block 만 있는 응답은 chip 으로, geometry 등 다른 본문이 있으면 그대로.

    // raw conversation (LLM 호출용, python/geometry 등 원본 보존)
    const rawHistory: ChatMessage[] = [...messages.slice(-MAX_HISTORY_TURNS), newUserMsg];
    // 표시 누적 — setMessages 인자로 직접 전달.
    let displayMessages: ChatMessage[] = [...messages, newUserMsg, placeholder];

    // 한 turn LLM 호출 + 마지막 placeholder 자리에 streaming 갱신. raw 텍스트 반환.
    // BYOK 모드 (apiKey 있음): /api/openrouter 로 학생 key 와 함께 relay.
    // dev fallback: /api/chat 의 claude CLI subprocess.
    const callLLM = async (history: ChatMessage[]): Promise<string> => {
      let assistantText = '';
      try {
        const endpoint = byokActive ? '/api/openrouter' : '/api/chat';
        const body = byokActive
          ? {
              slug, collection,
              messages: history.slice(-MAX_HISTORY_TURNS),
              model: byokModel,
              apiKey: byokApiKey || 'ollama', // ollama 등 인증 없는 endpoint 용 dummy
              baseURL: byokBaseURL,
            }
          : { slug, collection, messages: history.slice(-MAX_HISTORY_TURNS), model };
        const res = await fetch(endpoint, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`);
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buf = '';
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          let idx;
          while ((idx = buf.indexOf('\n\n')) !== -1) {
            const block = buf.slice(0, idx); buf = buf.slice(idx + 2);
            let event = 'message', data = '';
            for (const line of block.split('\n')) {
              if (line.startsWith('event: ')) event = line.slice(7).trim();
              else if (line.startsWith('data: ')) data = line.slice(6);
            }
            if (!data) continue;
            try {
              const parsed = JSON.parse(data);
              if (event === 'delta' && typeof parsed.text === 'string') {
                assistantText += parsed.text;
                const display = sanitizeForDisplay(assistantText);
                setMessages((curr) => {
                  const next = [...curr];
                  next[next.length - 1] = { role: 'assistant', content: display };
                  return next;
                });
              } else if (event === 'error') {
                setError(parsed.message ?? 'unknown error');
              }
            } catch { /* ignore */ }
          }
        }
      } catch (e) {
        setError((e as Error).message);
      }
      return assistantText;
    };

    // sympy 실행 (pyodide → server fallback)
    const runSympy = async (code: string): Promise<{ ok: boolean; stdout: string }> => {
      let sjson: { ok: boolean; stdout?: string; stderr?: string; error?: string; exit_code?: number };
      try { sjson = await runSympyLocal(code); }
      catch {
        const sres = await fetch('/api/sympy', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code }),
        });
        sjson = await sres.json();
      }
      const stdout = (sjson.ok ? (sjson.stdout || '(no output)') : (sjson.stderr || sjson.error || `exit ${sjson.exit_code}`)).trim();
      return { ok: !!sjson.ok, stdout };
    };

    // 새 user/assistant pair 를 displayMessages + setMessages 동시 갱신
    const appendTurn = (userMsg: ChatMessage) => {
      const ph: ChatMessage = { role: 'assistant', content: '' };
      displayMessages = [...displayMessages, userMsg, ph];
      setMessages(displayMessages);
      rawHistory.push(userMsg);
    };
    const finalizeAssistant = (rawText: string, display?: string) => {
      const shown = display ?? sanitizeForDisplay(rawText);
      displayMessages = [...displayMessages.slice(0, -1), { role: 'assistant', content: shown }];
      setMessages(displayMessages);
      rawHistory.push({ role: 'assistant', content: rawText });
    };

    try {
      // ===== Turn 1: 초기 응답 =====
      let assistantText = await callLLM(rawHistory);
      // Haiku 비순응 대비: 첫 응답에 sympy(python)와 그래픽이 *같이* 오면, 그 그래픽은 아직
      // 검증 안 된 추정 좌표다. 그대로 두면 아래 sympy 루프가 "이미 그렸다"고 보고 검증을
      // 통째로 건너뛴다(hasGeometry break) → 틀린 도형이 나감. 그래서 미검증 그래픽을 제거하고
      // (표시·기록 모두) sympy 검증을 거쳐 STEP C 에서 검증 좌표로 다시 그리게 한다.
      {
        const _follow = text.startsWith('[자동 계산 결과]') || text.startsWith('[시각 검증]');
        const _py = /```(?:python|py|sympy)[ \t]*\n?[\s\S]*?```/.test(assistantText);
        const _gfx = /```(?:geometry3d|geometry|plot|interactive)[ \t]*\n/.test(assistantText);
        // 미검증 그래픽은 turn-1 에서 제거 → 좌표를 STEP B(sympy)로 검증한 뒤 STEP C 에서 그린다.
        // ★ python 동반(기존)뿐 아니라 **그래픽만(원샷)** 도 잡는다 — 예제 문제를 새로 만들 때
        //   튜터가 추정 좌표로 한 번에 그려 버리던(단계 스킵) 사고 차단. 모든 좌표 그래픽 = 단계별.
        if (!_follow && _gfx) {
          assistantText = assistantText.replace(/```(?:geometry3d|geometry|plot|interactive)[ \t]*\n[\s\S]*?```/g, '').trim();
          if (!_py) {
            // STEP B(python) 없이 그래픽만 = 원샷. 좌표 계산을 먼저 하도록 강제 후 재응답.
            finalizeAssistant(assistantText || '좌표를 정확히 계산해 다시 그리겠습니다.');
            appendTurn({ role: 'user', content: '[자동 검증 · 시스템 메시지 — 사용자가 보낸 게 아님]\n방금 네가 그린 도형은 검증 안 된 추정 좌표라 화면에서 자동 제거했다. 지금 이 턴에 할 일은 **딱 하나**: 그 도형에 필요한 점·교점·접선·각의 좌표를 구하는 ```python``` (sympy) 코드 **한 블록만** 출력해라. 설명도, 그래픽 블록(geometry/plot/interactive)도 넣지 말고 python 코드 블록 하나만. 그 코드는 시스템이 자동 실행해서 결과를 다음 턴에 너에게 돌려주고, 그때 그 좌표로 도형을 그리면 된다. 이건 정해진 시스템 절차다 — 사용자에게 "무슨 뜻이냐"고 되묻지 말고 바로 sympy 코드를 출력해라.' });
            assistantText = await callLLM(rawHistory);
          }
        }
      }
      finalizeAssistant(assistantText);

      // ===== Sympy auto-exec + VERIFY FAIL retry (1회 cap) =====
      // 펜스 정규식을 sanitizeForDisplay(L817) 의 strip 형태와 일치시킨다.
      // 개행 강제(\s*\n)면 한 줄 펜스(```python x=1```)가 표시에선 제거되는데
      // 여기선 매칭 실패 → 실행 안 됨 → '계산 중…' chip 영구 고착. \n? 로 완화.
      const extractPy = (s: string) => s.match(/```(?:python|py|sympy)[ \t]*\n?([\s\S]*?)```/);
      const isFollowupInput = text.startsWith('[자동 계산 결과]') || text.startsWith('[시각 검증]');
      const MAX_SYMPY_ROUNDS = 3;
      let rounds = 0;
      const hasGeometry = (s: string) => /```geometry(3d)?\s*\n/.test(s);
      while (!isFollowupInput && rounds < MAX_SYMPY_ROUNDS) {
        if (hasGeometry(assistantText)) break; // 도형 emit 완료
        const m = extractPy(assistantText);
        if (!m) break; // python 도 도형도 없음 → 종료
        const sympyResult = await runSympy(m[1]);
        const failed = /\[VERIFY FAIL\]/.test(sympyResult.stdout);
        const prefix = failed ? '[자동 계산 결과 — 검증 실패]' : '[자동 계산 결과]';
        const tail = failed
          ? '\n\n위 출력에 `[VERIFY FAIL]` 항목이 있다. **이전 가정/수식이 어디서 틀렸는지** 찾아 단계 정의를 다시 읽고 sympy 코드를 다시 작성해 재계산하라. 추정 금지.'
          : '\n\n위 출력의 각 점 좌표를 **글자 그대로 ```geometry``` spec 의 `at: [x, y]` 에 옮겨 적어라**. 추정·반올림 금지. 이번 응답에서 바로 geometry block 작성, 대기 메시지 금지, 기술 용어 노출 금지.';
        const injected = `${prefix}\n\`\`\`\n${sympyResult.stdout}\n\`\`\`${tail}`;
        appendTurn({ role: 'user', content: injected });
        assistantText = await callLLM(rawHistory);
        finalizeAssistant(assistantText);
        rounds++;
      }

      // ===== Visual self-check (problems 페이지 + geometry emit 시 1회) =====
      const geomMatch = assistantText.match(/```geometry(3d)?\s*\n([\s\S]*?)```/);
      if (collection === 'problems' && geomMatch && !isFollowupInput) {
        const is3d = !!geomMatch[1];
        const specStr = geomMatch[2].trim();
        const checkMsg = [
          '[시각 검증]',
          '방금 emit 한 geometry spec:',
          '```json',
          specStr,
          '```',
          '',
          '원본 문제 도형 이미지를 Read 로 다시 본 뒤, **명백한 좌표 오류**만',
          '잡는다. 기본 응답은 `[검증 통과]`. 다시 그리는 비용이 크므로',
          '왠만하면 통과시킬 것.',
          '',
          '**다시 그릴 사유 — 다음 둘 중 하나만 해당하면 emit**:',
          '1. 점의 *사분면 부호*가 거꾸로 (이미지에선 P 가 왼쪽 위인데 spec',
          '   에선 오른쪽 위 같은 거울 대칭) → 좌표 derive 자체가 틀린 신호.',
          '   **3D 의 경우 정육면체 ABCD-EFGH 의 ABCD 가 위 면인지 / EFGH 가 위',
          '   인지 — 위/아래 면 거꾸로 박혔는지 반드시 확인.**',
          '2. 곡선 *종류*가 틀림 (이미지가 타원인데 spec 은 원, 쌍곡선인데 포물선)',
          ...(is3d ? [
            '3. **3D 한정: 문제에 없는 보조 segment 가 잔뜩 추가** (예: 정육면체의 모든 vertex 쌍 사이 대각선)',
            '   → 핵심 선분만 남기고 *불필요한 외곽선*만 제거. **단 학생 이해 돕는 보조 (정사영선, 회전축, 단면선) 는 통과.**',
            '4. **3D 한정: 명백한 over-emit** (정육면체 부피의 5배 이상의 거대 외접구 같이 핵심 도형을 가리는 경우) → 제거.',
            '   **그 외 (정사영면 plane, 회전체 parametricSurface, 보조 구체 sphere) 는 학습 시각화 도구로 통과.**',
          ] : []),
          '',
          '**무시할 차이 — 무조건 통과**:',
          '- 라벨 위치(NE/SW 등) 미세 차이',
          '- 색·선 두께·fill opacity 차이',
          '- **이미지가 반원(호)인데 spec 이 전체 원(circle)** — Geometry 컴포넌트가',
          '  호(arc)를 지원하지 않으므로 의도된 한계. 다시 안 그림.',
          '- 호를 polygon vertex 로 근사 (Geometry 컴포넌트 한계)',
          '- segment 가 여러 조각으로 나뉘어 그려진 경우 (시각적으로 같음)',
          '- 점의 상대 위치가 대략 비슷하면 (정확한 픽셀 위치 X)',
          '- 보조선·음영 일부 누락 (핵심 점·곡선만 맞으면 OK)',
          '- 점 라벨 1-2개 누락 또는 추가',
          '- **각도 호(∠θ 표시), 영역 label(S₁/S₂/f(θ)/g(θ)), 텍스트 주석 누락** — 보조 표시는 통과',
          '- 선이 연장선이 아닌 segment 로 표현되는 등 표현 방식 차이',
          '',
          '판정:',
          '- 다시 그릴 사유 없음 → 정확히 `[검증 통과]` 한 줄만 응답 (다른 텍스트 X)',
          '- 부호/종류 오류 있음 → 1줄로 어긋난 항목 짚고 수정된 ```geometry``` emit',
        ].join('\n');
        appendTurn({ role: 'user', content: checkMsg });
        const checkText = await callLLM(rawHistory);
        finalizeAssistant(checkText, checkText);

        // visual check 결과에 python 블록이 있으면 → 좌표 자체가 틀렸다는 신호.
        // 재계산 cycle 한 번 더 (sympy 실행 → [자동 계산 결과] inject → geometry 재emit)
        const recalcPy = checkText.match(/```(?:python|py|sympy)\s*\n([\s\S]*?)```/);
        if (recalcPy) {
          const sympyResult = await runSympy(recalcPy[1]);
          const failed = /\[VERIFY FAIL\]/.test(sympyResult.stdout);
          const prefix = failed ? '[자동 계산 결과 — 검증 실패]' : '[자동 계산 결과]';
          const tail = failed
            ? '\n\n위 [VERIFY FAIL] 항목을 확인하고 단계 정의를 다시 읽고 좌표를 재계산.'
            : '\n\n위 출력의 점 좌표를 글자 그대로 ```geometry``` spec 에 옮겨 재emit.';
          const injected = `${prefix}\n\`\`\`\n${sympyResult.stdout}\n\`\`\`${tail}`;
          appendTurn({ role: 'user', content: injected });
          const finalText = await callLLM(rawHistory);
          finalizeAssistant(finalText);
        }
      }

      // ★(b) 시스템 검산: 최종 응답의 *순수 산술* 등식에 모순(좌변≠우변)이 있으면 = 검증 정답을 틀린
      //   식 위에 덧씌운 조작/계산실수 → [자동 검산] 으로 1회 정정 재생성. 변수 든 식·비산술은 무시.
      //   CSP 안전(eval/Function 미사용, 자체 shunting-yard 평가기).
      {
        const lastMsg = displayMessages[displayMessages.length - 1];
        const ae = lastMsg?.role === 'assistant' ? findArithErr(lastMsg.content) : null;
        if (ae) {
          appendTurn({ role: 'user', content: `[자동 검산 · 시스템 메시지 — 사용자가 보낸 게 아님] 시스템이 네 답의 산술을 자동 점검한 결과 모순 *의심*: "${ae.expr}" = ${ae.correct} 인 것 같은데 너는 ${ae.claimed} 라고 썼다. ★이건 사용자의 지적이 아니다 — "지적 감사합니다 / 당신 말이 맞습니다" 같은 응답 절대 금지. 조용히 네 계산을 검증 단계와 다시 대조하라: (1) 정말 틀렸으면 식을 바로잡아 식과 답이 일치하게 다시 풀고, (2) 네 계산이 옳았으면(이 자동 점검이 오탐일 수 있음 — 예: 식의 일부만 떼어 본 경우) 식을 바꾸지 말고 그 항을 다시 더해 답이 맞음을 한 줄로 검산만 보이면 된다. 어느 경우든 최종 식과 산술이 일치해야 한다.` });
          const fixed = await callLLM(rawHistory);
          finalizeAssistant(fixed);
        }
      }
    } finally {
      setStreaming(false);
    }
  }, [input, pending, quoted, streaming, messages, slug, model, collection, byokActive, byokApiKey, byokModel, byokBaseURL]);
  return send;
}
