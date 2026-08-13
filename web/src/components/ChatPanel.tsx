import { useState, useRef, useEffect, useCallback } from 'react';
import MathField from './MathField.tsx';
import { prewarmPyodide } from '../lib/pyodide-client';
import { buildNoteUserPrompt, NOTE_FOLLOWUPS, isNoteRequest, type NoteFollowup } from '../lib/note-prompts';
import { prepareImage, imagesFromDataTransfer } from '../lib/image-utils';
import ImageCropper from './ImageCropper.tsx';
import { isVisionDisabled } from '../lib/vision';
import type { ChatMessage } from '../lib/chat/types';
import { STORAGE_PREFIX, loadHistory, saveHistory, loadDbHistory, saveDbHistory } from '../lib/chat/persistence';
import ChatScrollbar from './chat/ChatScrollbar';
import Message, { QuotedChip } from './chat/Message';
import ByokSettings from './chat/ByokSettings';
import { reconstructPastedMath } from '../lib/chat/markdown';
import { CHAT_STYLES } from '../lib/chat/chat-styles';
import { useChatSend } from '../lib/chat/useChatSend';


type Props = {
  slug: string;
  unitTitle: string;
  collection?: 'concepts' | 'problems' | 'dashboard';
  // fill=true → 부모 컨테이너 높이를 꽉 채우는 flex 레이아웃 (메시지 flex-1 스크롤,
  // 입력은 하단 고정). problem 페이지의 고정 채팅 컬럼/하단 dock 용. 기본(false)은
  // 기존 inline 카드 (concepts/dashboard 페이지).
  fill?: boolean;
};



// Split a message body into a list of segments. ```plot``` and ```svg```
// fenced blocks become "graph" segments; everything else stays as a "md"
// (markdown) segment. Order preserved.

// 대화 스크롤바 — 네이티브(특히 모바일 webkit) 스크롤바는 곧 사라지고 터치로 잡을 수
// 없어 사용자가 "손으로 컨트롤이 안 되고 금방 사라지고 너무 작다"고 호소. 그래서 항상
// 보이고, 충분히 굵고, 포인터(마우스/터치/펜)로 드래그 가능한 커스텀 스크롤바를 직접 그린다.
// targetRef 의 scroll 상태에 thumb 의 높이·위치를 동기화하고, thumb/track 드래그로 scrollTop 을 제어.

export default function ChatPanel({ slug, unitTitle, collection = 'concepts', fill = false }: Props) {
  const placeholderHint =
    collection === 'dashboard' ? '예: 삼각함수가 헷갈리는데 어디부터 봐야 해?' :
    collection === 'problems'  ? '예: 이 문제 어떻게 풀어?' :
                                  '예: 근의 공식이 왜 저렇게 생겼어?';
  const subtitle =
    collection === 'dashboard' ? '학습 길잡이 — 무엇을 모르는지 말하면 어디로 가야 할지 알려드립니다.' :
    collection === 'problems'  ? `"${unitTitle}" 문제에 한정한 LLM 튜터.` :
                                  `"${unitTitle}" 단원에 한정한 LLM 튜터.`;
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mathOpen, setMathOpen] = useState(false);
  const [mathLatex, setMathLatex] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  // 이미지 첨부 state
  const [pending, setPending] = useState<string[]>([]);          // 전송 대기 비전 타일들 (원해상도 PNG dataURL N장)
  const [pendingDisplay, setPendingDisplay] = useState<string | null>(null);  // 사용자 표시용 통이미지(타일과 분리)
  const [quoted, setQuoted] = useState<string | null>(null);     // 렌더 수식 복붙 인용(전송 대기). 표시=칩, LLM=인용블록.
  const [cropSrc, setCropSrc] = useState<string | null>(null);   // 크롭 모달 대상 (원본 dataURL)
  const [imgError, setImgError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // BYOK 설정 — 학생 본인 LLM (OpenRouter / Ollama local / 기타). localStorage 영구 보관.
  // baseURL 있으면 BYOK 사용, 없으면 dev fallback (claude CLI)
  const [byokOpen, setByokOpen] = useState(false);
  const [byokApiKey, setByokApiKey] = useState<string>('');
  const [byokModel, setByokModel] = useState<string>('openrouter/auto');
  const [byokBaseURL, setByokBaseURL] = useState<string>('https://openrouter.ai/api/v1');
  useEffect(() => {
    try {
      const k = localStorage.getItem('math-study:byok:apikey');
      const m = localStorage.getItem('math-study:byok:model');
      const b = localStorage.getItem('math-study:byok:baseurl');
      if (k) setByokApiKey(k);
      if (m) setByokModel(m);
      if (b) setByokBaseURL(b);
    } catch { /* localStorage 비활성 */ }
  }, []);
  // BYOK 활성 조건 — OpenRouter 면 apiKey 필수, Ollama (localhost/tailnet) 면 apiKey 없어도 OK
  // 호스트가 스킴(`//`) 직후에 오도록 앵커링 — 앵커 없으면 `https://10.example.com`
  // 같은 공인 도메인이나 경로에 박힌 `//100.` 이 로컬로 오판돼 무인증 더미키로 전송됨.
  const isOllamaLike = /^https?:\/\/(localhost|127\.0\.0\.1|0\.0\.0\.0|100\.\d|10\.\d|192\.168\.)/.test(byokBaseURL.trim());
  const byokActive = byokApiKey.length > 0 || (isOllamaLike && byokBaseURL.length > 0);
  const saveByok = useCallback((apiKey: string, modelId: string, baseURL: string) => {
    setByokApiKey(apiKey);
    setByokModel(modelId);
    setByokBaseURL(baseURL);
    try {
      if (apiKey) localStorage.setItem('math-study:byok:apikey', apiKey);
      else localStorage.removeItem('math-study:byok:apikey');
      localStorage.setItem('math-study:byok:model', modelId);
      localStorage.setItem('math-study:byok:baseurl', baseURL);
    } catch { /* ignore */ }
  }, []);

  // Insert "$...$" at the current cursor position in the textarea
  const insertMath = useCallback((latex: string) => {
    if (!latex.trim()) return;
    const ta = textareaRef.current;
    const wrapped = `$${latex}$`;
    if (!ta) { setInput((prev) => prev + (prev.endsWith(' ') ? '' : ' ') + wrapped); return; }
    const start = ta.selectionStart ?? input.length;
    const end = ta.selectionEnd ?? input.length;
    const before = input.slice(0, start);
    const after = input.slice(end);
    const sep = before && !before.endsWith(' ') ? ' ' : '';
    const next = before + sep + wrapped + after;
    setInput(next);
    setMathLatex('');
    setMathOpen(false);
    // restore focus + cursor after the inserted block
    setTimeout(() => {
      ta.focus();
      const pos = (before + sep + wrapped).length;
      ta.setSelectionRange(pos, pos);
    }, 0);
  }, [input]);

  // 렌더된 KaTeX 를 복사하면 클립보드 text/plain 이 기호마다 줄바꿈돼 입력창에서 세로로 깨진다.
  // 클립보드 HTML 의 .katex LaTeX annotation 을 $...$ 로 재구성 → 깔끔한 LaTeX(메시지에서 수식 렌더 +
  // LLM 도 정상 수신). 수식 외 텍스트는 그대로 두고 복사 잔여 공백/줄바꿈만 정리.

  const storageKey = `${collection}:${slug}`;

  // Interactive 컴포넌트가 '📋 현재 상태 채팅에 첨부' 버튼을 누르면
  // window CustomEvent로 한 줄 메타가 날아온다. textarea 앞에 prepend.
  // 같은 종류의 메타가 이미 있으면 교체 (누적되지 않게).
  useEffect(() => {
    const onInsert = (e: Event) => {
      const detail = (e as CustomEvent<{ text: string }>).detail;
      if (!detail?.text) return;
      setInput((prev) => {
        // 기존 [현재 상태] ... 라인이 맨 앞에 있으면 떼어내고 새 것으로 교체.
        const cleaned = prev.replace(/^\[현재 상태\][^\n]*\n?/, '');
        return `${detail.text}\n${cleaned}`;
      });
      // focus + cursor를 본문 끝으로
      setTimeout(() => {
        const ta = textareaRef.current;
        if (ta) {
          ta.focus();
          const len = ta.value.length;
          ta.setSelectionRange(len, len);
        }
      }, 0);
    };
    window.addEventListener('math-study:chat-insert', onInsert as EventListener);
    return () => window.removeEventListener('math-study:chat-insert', onInsert as EventListener);
  }, []);


  // Load history on mount — localStorage 즉시 표시 후 DB(계정·기기 넘어) 권위로 동기화.
  useEffect(() => {
    const local = loadHistory(storageKey);
    setMessages(local);
    // pyodide worker 선제 로드 — 첫 sympy 호출 시 대기 ↓
    prewarmPyodide();
    let cancelled = false;
    (async () => {
      const db = await loadDbHistory(collection, slug);
      if (cancelled) return;
      if (db && db.length > 0) setMessages(db);            // DB 권위(다른 기기 대화 포함)
      else if (local.length > 0) saveDbHistory(collection, slug, local); // 마이그레이션
    })();
    return () => { cancelled = true; };
  }, [storageKey]);

  // Persist on change — localStorage 캐시 + DB 둘 다 디바운스. 스트리밍 중엔 토큰마다
  // messages 가 바뀌는데, 그때마다 saveHistory(전체 JSON.stringify=O(n))를 동기 실행하면
  // 긴 히스토리에서 O(n²) 누적으로 스크롤이 버벅인다. 중간 토큰 상태 저장은 무의미(응답
  // 미완성)하므로 스트림이 잦아든 뒤(또는 단일 액션 후) 한 번만 저장한다.
  useEffect(() => {
    if (messages.length === 0) return;
    const t = setTimeout(() => {
      saveHistory(storageKey, messages);
      saveDbHistory(collection, slug, messages);
    }, 500);
    return () => clearTimeout(t);
  }, [storageKey, messages, collection, slug]);

  // 스크롤 정책 (ChatGPT 식):
  //  - 새 user 질문이 들어오면 그 질문을 스크롤 영역 '상단'으로 → 이어질 (긴) 답변이
  //    위에서부터 펼쳐져, 첫 줄이 자동 하단스크롤에 가려져 잘려 보이던 문제를 없앤다.
  //  - assistant 스트리밍/갱신은 사용자가 거의 바닥에 있을 때만 추종(near-bottom).
  //    위로 올려 읽는 중이면 끌어내리지 않는다.
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const last = messages[messages.length - 1];
    if (last && last.role === 'user') {
      const node = el.querySelector(`[data-mi="${messages.length - 1}"]`) as HTMLElement | null;
      if (node) {
        // 영역 내 상대 위치만큼 스크롤. ★behavior:'instant' — 컨테이너 scroll-behavior:smooth 가
        //   직접 scrollTop 쓰기를 애니메이션해 스트리밍 중 위아래로 흔들리던 것 차단.
        el.scrollTo({ top: el.scrollTop + (node.getBoundingClientRect().top - el.getBoundingClientRect().top - 8), behavior: 'instant' as ScrollBehavior });
        return;
      }
    }
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 200;
    if (nearBottom) el.scrollTo({ top: el.scrollHeight, behavior: 'instant' as ScrollBehavior }); // #2 흔들림 픽스: instant
  }, [messages]);

  // #3 재진입: 마운트 시 바텀부터(과거 대화는 최신이 아래에 있어야). 비동기 DB 로드·KaTeX 렌더로
  //   높이가 변하므로 짧게 몇 번 바텀 재고정. 마운트 직후라 사용자가 위로 읽는 중일 일 없어 무해.
  useEffect(() => {
    const el = scrollRef.current; if (!el) return;
    const jumps = [50, 250, 600].map((d) => window.setTimeout(() => {
      el.scrollTo({ top: el.scrollHeight, behavior: 'instant' as ScrollBehavior });
    }, d));
    return () => jumps.forEach((j) => clearTimeout(j));
  }, []);

  // `override`: when called from the 학습 노트 buttons (right-side card or
  // action row), we pass the prompt directly instead of routing through the
  // input field. The textarea is left untouched so the user can keep typing
  // their own follow-up while the note request flies off.
  const send = useChatSend({
    input, pending, pendingDisplay, quoted, streaming, messages, slug, collection,
    byokActive, byokApiKey, byokModel, byokBaseURL,
    setMessages, setError, setStreaming, setQuoted, setPendingDisplay, setPending, setInput, setImgError,
  });

  // 이미지 첨부 — prepareImage 후 needsCrop 이면 크롭 모달, 아니면 바로 pending.
  const addFile = useCallback(async (files: File[]) => {
    if (!files.length) return;
    if (byokActive && isVisionDisabled(byokModel)) {
      setImgError('현재 모델은 이미지를 못 읽어요 — 비전 지원 모델(claude/gemini 등)로 바꾸거나 기본 모드를 쓰세요.');
      return;
    }
    if (pending.length) { setImgError('이미지는 한 번에 하나만 첨부할 수 있어요.'); return; }
    if (files.length > 1) setImgError('이미지는 한 장만 첨부돼요 (첫 장만 사용).');
    try {
      const p = await prepareImage(files[0]);
      if (p.kind === 'needsCrop') { setCropSrc(p.rawDataUrl); setImgError(null); }
      else { setPending(p.tiles); setPendingDisplay(p.display); setImgError(null); }   // 타일=전송, display=표시
    } catch (e) {
      setImgError(e instanceof Error ? e.message : '이미지 처리에 실패했어요.');
    }
  }, [byokActive, byokModel, pending]);

  // send() identity changes whenever messages/input/streaming change. The
  // window event handler below would otherwise capture a stale send.
  const sendRef = useRef(send);
  useEffect(() => { sendRef.current = send; }, [send]);

  // promote() 는 클릭 시점의 최신 messages 만 있으면 된다. messages 를 useCallback deps
  // 에 넣으면 스트리밍 토큰마다 promote 정체성이 바뀌고, 그게 모든 <Message> 의 onPromote
  // prop 을 흔들어 memo 를 전 메시지에서 깨뜨린다(긴 채팅 스크롤 버벅임의 회귀 원인 —
  // 3881d211 의 memo 최적화가 스트리밍 경로에서 무력화됨). ref 로 최신값을 읽어 promote 를
  // 안정화 → memo 유지.
  const messagesRef = useRef(messages);
  useEffect(() => { messagesRef.current = messages; }, [messages]);

  // LearningNoteButton (우측 카드) → 학습 노트 작성 요청. 입력창을 거치지 않고
  // 곧장 send() 로 user message 전송 (override 인자 — input 비우지 않음).
  useEffect(() => {
    const onNoteRequest = (e: Event) => {
      const detail = (e as CustomEvent<{ unitTitle?: string }>).detail;
      const title = detail?.unitTitle ?? unitTitle;
      void sendRef.current(buildNoteUserPrompt(title));
    };
    window.addEventListener('math-study:chat-note-request', onNoteRequest as EventListener);
    return () => window.removeEventListener('math-study:chat-note-request', onNoteRequest as EventListener);
  }, [unitTitle]);

  // Followup buttons (📏 더 짧게 등) under a 학습 노트 reply.
  const handleNoteFollowup = useCallback((kind: NoteFollowup) => {
    void sendRef.current(NOTE_FOLLOWUPS[kind]);
  }, []);

  // 메시지에서 드래그 선택 → "인용" → 인용 칩에 누적(여러 번 선택하면 이어붙임). 입력창에 포커스.
  const addQuote = useCallback((latex: string) => {
    if (!latex.trim()) return;
    setQuoted((prev) => (prev ? prev + '\n\n' : '') + latex.trim());
    setTimeout(() => textareaRef.current?.focus(), 0);
  }, []);

  const promote = useCallback(
    async (idx: number) => {
      const msgs = messagesRef.current;
      const assistant = msgs[idx];
      if (!assistant || assistant.role !== 'assistant') return;
      // Find the preceding user question — skip internal protocol messages
      // ([자동 계산 결과], [자동 계산 결과 — 검증 실패], [시각 검증]) that the
      // sympy/visual-verification loop pushes as user messages, so the real
      // student question is captured instead of an internal protocol string.
      let question = '';
      for (let i = idx - 1; i >= 0; i--) {
        if (msgs[i].role === 'user') {
          const c = msgs[i].content;
          if (c.startsWith('[자동 계산 결과') || c.startsWith('[시각 검증]')) continue;
          question = c;
          break;
        }
      }
      // 학습 노트 요청에서 비롯된 promote 면 파일명에 들어갈 title 을
      // 단원 이름 기반으로 깔끔하게 (`[학습 노트 요청] ...` 본문이
      // 그대로 들어가지 않게).
      const isNote = isNoteRequest(question);
      const titleOverride = isNote ? `학습 노트 - ${unitTitle}` : undefined;
      try {
        const res = await fetch('/api/promote', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ slug, question, answer: assistant.content, title: titleOverride }),
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.error ?? `HTTP ${res.status}`);
        setMessages((curr) => {
          const next = [...curr];
          next[idx] = { ...assistant, promoted: { path: json.path } };
          return next;
        });
        // 우측 LearningNoteButton 카드에 "최근 저장: …" 표시용.
        try {
          const recentKey = `math-study:note-last-saved:${collection}:${slug}`;
          const filename = String(json.path).split('/').pop() ?? '';
          window.localStorage.setItem(recentKey, filename);
        } catch { /* ignore */ }
      } catch (e) {
        setError(`저장 실패: ${(e as Error).message}`);
      }
    },
    [slug, unitTitle, collection], // messages 는 messagesRef 로 읽음 — deps 에서 제외해 promote 안정화
  );

  const clearChat = () => {
    if (!confirm('대화를 모두 지울까요?')) return;
    setMessages([]);
    try { window.localStorage.removeItem(STORAGE_PREFIX + storageKey); } catch {}
    saveDbHistory(collection, slug, []); // DB 도 비움
  };

  return (
    <section className={fill ? 'card h-full flex flex-col min-h-0' : 'card mt-6'}>
      <header className="flex items-center justify-between mb-3 shrink-0">
        <div>
          <h3 className="text-sm font-semibold">{collection === 'dashboard' ? '🧭 학습 길잡이' : '🤖 튜터 대화'}</h3>
          <p className="text-xs text-[color:var(--color-muted)]">
            {subtitle} 대화 내용은 이 기기에 저장돼요.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          {/* BYOK 활성 시 학생 모델 표시, dev fallback 모드면 claude select */}
          {/* 모델 선택 UI 제거: 제품 튜터 모델은 **서버가 고정**한다(openai/gpt-5.6-luna).
              학생이 고를 이유가 없고, 프런트가 model 을 명시해 보내면 서버 기본값을 덮어써
              전환이 조용히 무력화된다(실제로 claude-haiku 가 계속 쓰이고 있었다).
              BYOK(학생 본인 키)만 활성 시 표시한다. */}
          {byokActive && (
            <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded px-2 py-1 text-[10px] font-mono"
                  title={byokBaseURL}>
              {isOllamaLike ? '🖥 ' : ''}{byokModel}
            </span>
          )}
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="text-[10px] uppercase tracking-wider text-zinc-500 hover:text-rose-400 transition"
            >
              지우기
            </button>
          )}
        </div>
      </header>

      <ByokSettings byokOpen={byokOpen} byokBaseURL={byokBaseURL} setByokBaseURL={setByokBaseURL} byokApiKey={byokApiKey} setByokApiKey={setByokApiKey} byokModel={byokModel} setByokModel={setByokModel} isOllamaLike={isOllamaLike} saveByok={saveByok} setByokOpen={setByokOpen} />

      <div data-chat-host className={`chat-scroll-wrap relative ${fill ? 'flex-1 min-h-0' : ''} -mx-1 mb-3`}>
      <div
        ref={scrollRef}
        className={`chat-scroll ${fill ? 'h-full' : 'max-h-[420px]'} space-y-3 overflow-y-auto py-2 pl-1 pr-4 scroll-smooth`}
      >
        {messages.length === 0 ? (
          <p className="text-sm text-[color:var(--color-subtle)] py-8 text-center">
            {collection === 'dashboard'
              ? '무엇이 헷갈리는지 / 어디서 막혔는지 알려주세요.'
              : `"${unitTitle}"에 대해 무엇이든 물어보세요.`}
            <br />
            <span className="text-[color:var(--color-accent)]">{placeholderHint}</span>
          </p>
        ) : (
          messages.map((m, i) => {
            // ★A: 검증 과정(자동 검증/계산결과/시각검증 user 턴 + 그 *사이* 중간 assistant 응답=계산중·1차그래프)은
            //   채팅에서 숨긴다. 데이터는 messages(=DB)에 그대로 남아 디버깅·검증 가능 — '표시'만 거른다.
            //   첫 설명(앞이 진짜 user)과 최종 응답(뒤가 검증턴 아님)은 보인다.
            const vU = (x?: ChatMessage) => !!x && x.role === 'user' && /^\[(자동 검증|자동 계산 결과|시각 검증|자동 검산)/.test(x.content);
            if (vU(m)
              || (m.role === 'assistant' && vU(messages[i - 1]) && vU(messages[i + 1]))
              || (m.role === 'assistant' && m.content.trim() === '[검증 통과]')) return null;
            return (
            <Message
              key={i}
              msg={m}
              index={i}
              busy={streaming}
              isStreaming={streaming && i === messages.length - 1}
              isNoteResponse={
                m.role === 'assistant'
                && i > 0
                && messages[i - 1].role === 'user'
                && isNoteRequest(messages[i - 1].content)
              }
              slug={slug}
              collection={collection}
              onPromote={promote}
              onNoteFollowup={handleNoteFollowup}
              onQuote={addQuote}
            />
            );
          })
        )}
        {(() => {
          // 검증 과정 턴을 숨겼으니, 그 동안 "멈춘 듯" 보이지 않게 진행 표시. 최근 메시지에 검증턴이 있으면
          // 검증 중(그래프 작도 문구), 아니면 빈 placeholder 스트리밍이면 일반 문구.
          const last = messages[messages.length - 1];
          const inVerify = messages.slice(-4).some((x) => /^\[(자동 검증|자동 계산 결과|시각 검증|자동 검산)/.test(x.content));
          if (!streaming || (last?.content !== '' && !inVerify)) return null;
          return (
          <div className="flex items-center gap-2 text-xs text-[color:var(--color-muted)] pl-2">
            <span className="inline-block size-1.5 rounded-full bg-[color:var(--color-accent)] animate-pulse"></span>
            <span>{inVerify ? '📐 정확한 좌표로 그래프 검증·작도 중…' : '답변 생성 중…'}</span>
          </div>
          );
        })()}
      </div>
        <ChatScrollbar targetRef={scrollRef} />
      </div>

      {error && (
        <p className="text-xs text-rose-400 mb-2">⚠ {error}</p>
      )}

      {quoted && (
        <div className="mb-2 shrink-0">
          <QuotedChip text={quoted} onRemove={() => setQuoted(null)} />
        </div>
      )}

      {(pending.length > 0 || imgError) && (
        <div className="flex items-center gap-2 mb-2 shrink-0">
          {pending.length > 0 && (
            <div className="relative">
              <img src={pendingDisplay ?? pending[0]} alt="첨부 이미지" className="h-14 w-14 object-cover rounded border border-[color:var(--color-border)]" />
              <button
                type="button"
                onClick={() => { setPending([]); setPendingDisplay(null); setImgError(null); }}
                className="absolute -top-1.5 -right-1.5 size-5 rounded-full bg-zinc-900 border border-zinc-600 text-zinc-300 text-xs grid place-items-center hover:text-white"
                aria-label="첨부 제거"
              >×</button>
            </div>
          )}
          {imgError && <p className="text-xs text-rose-400">⚠ {imgError}</p>}
        </div>
      )}

      <div
        className={`flex gap-2 items-stretch shrink-0 rounded-lg transition ${dragOver ? 'ring-2 ring-indigo-400/60' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => { e.preventDefault(); setDragOver(false); void addFile(imagesFromDataTransfer(e.dataTransfer)); }}
      >
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onPaste={(e) => {
            const imgs = imagesFromDataTransfer(e.clipboardData);
            if (imgs.length) { e.preventDefault(); void addFile(imgs); return; }
            // 렌더된 수식(KaTeX) 채팅을 복사 → 클립보드 HTML 의 LaTeX 로 재구성 후 *인용 칩*으로 마스킹
            //   (입력창에 세로로 쪼개져 들어가는 것 방지). 수식 입력기/타이핑/평문 LaTeX 는 .katex HTML 이
            //   없으므로 이 경로 안 탐 → 기본 인라인 입력. 즉 출처(렌더 화면 복사)로만 칩이 된다.
            const html = e.clipboardData.getData('text/html');
            if (!html || !/katex/i.test(html)) return;
            const tex = reconstructPastedMath(html);
            if (!tex) return;
            e.preventDefault();
            setQuoted((prev) => (prev ? prev + '\n\n' : '') + tex);
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
              e.preventDefault();
              send();
            }
          }}
          placeholder="질문을 입력하세요. (⌘/Ctrl+Enter로 전송 · 이미지 붙여넣기/드래그)"
          rows={2}
          disabled={streaming}
          className="flex-1 min-h-[3.5rem] bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded-lg px-3 py-2 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400 resize-y"
        />
        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp,image/heic,image/heif"
          className="hidden"
          onChange={(e) => { void addFile(Array.from(e.target.files ?? [])); e.target.value = ''; }}
        />
        <div className="flex flex-col gap-1.5 self-start">
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={streaming}
            title="이미지 첨부 (그래프·수식 캡처)"
            className="px-2.5 py-1.5 rounded border text-xs transition bg-[color:var(--color-surface-2)] border-[color:var(--color-border)] text-zinc-400 hover:text-zinc-100"
          >🖼 이미지</button>
          <button
            type="button"
            onClick={() => setMathOpen((v) => !v)}
            disabled={streaming}
            title="수식 입력 (LaTeX)"
            className={`px-2.5 py-1.5 rounded border text-xs transition ${
              mathOpen
                ? 'bg-indigo-500/30 border-indigo-500/50 text-indigo-200'
                : 'bg-[color:var(--color-surface-2)] border-[color:var(--color-border)] text-zinc-400 hover:text-zinc-100'
            }`}
          >∑ 수식</button>
          <button
            type="button"
            onClick={() => send()}
            disabled={streaming || (!input.trim() && !pending.length && !quoted)}
            className="px-4 py-2 rounded-lg bg-indigo-500/20 hover:bg-indigo-500/30 border border-indigo-500/40 text-indigo-300 text-sm font-medium transition disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {streaming ? '전송 중…' : '전송'}
          </button>
        </div>
      </div>

      {cropSrc && (
        <ImageCropper
          src={cropSrc}
          onCrop={(dataUrl) => { setPending([dataUrl]); setPendingDisplay(dataUrl); setCropSrc(null); setImgError(null); }}
          onCancel={() => setCropSrc(null)}
        />
      )}

      {mathOpen && (
        <div className="mt-2 rounded-lg border border-indigo-500/30 bg-indigo-500/5 p-2 space-y-2">
          <p className="text-[11px] text-zinc-400 px-1">
            수식 입력 후 <kbd className="px-1 py-0.5 rounded bg-zinc-800 text-zinc-300 text-[10px]">Enter</kbd>로 메시지에 삽입 ($수식$ 형식). 가상 키보드는 우측 하단 아이콘에서.
          </p>
          <MathField
            value={mathLatex}
            onChange={setMathLatex}
            onSubmit={() => insertMath(mathLatex)}
            placeholder="예: \\frac{1}{2} 또는 \\int_0^1 x^2 dx"
            autoFocus
            rows={2}
          />
          <div className="flex justify-end gap-2">
            <button
              onClick={() => { setMathLatex(''); setMathOpen(false); }}
              className="text-[11px] text-zinc-500 hover:text-zinc-200 px-2 py-1"
            >취소</button>
            <button
              onClick={() => insertMath(mathLatex)}
              disabled={!mathLatex.trim()}
              className="text-[11px] px-2.5 py-1 rounded bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-500/30 disabled:opacity-40"
            >메시지에 삽입</button>
          </div>
        </div>
      )}

      <style>{CHAT_STYLES}</style>
    </section>
  );
}
