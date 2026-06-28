import { useState, useRef, useEffect, useCallback } from 'react';
import MathField from './MathField.tsx';
import { runSympyLocal, prewarmPyodide } from '../lib/pyodide-client';
import { buildNoteUserPrompt, NOTE_FOLLOWUPS, isNoteRequest, type NoteFollowup } from '../lib/note-prompts';
import { prepareImage, imagesFromDataTransfer } from '../lib/image-utils';
import ImageCropper from './ImageCropper.tsx';
import { isVisionDisabled } from '../lib/vision';
import type { ChatMessage } from '../lib/chat/types';
import { STORAGE_PREFIX, MAX_HISTORY_TURNS, loadHistory, saveHistory, loadDbHistory, saveDbHistory } from '../lib/chat/persistence';
import ChatScrollbar from './chat/ChatScrollbar';
import Message, { QuotedChip } from './chat/Message';


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
  const [model, setModel] = useState<'haiku' | 'sonnet'>('haiku');
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
  const reconstructPastedMath = (html: string): string | null => {
    try {
      const doc = new DOMParser().parseFromString(html, 'text/html');
      if (!doc.querySelector('.katex')) return null;
      doc.querySelectorAll('.katex').forEach((k) => {
        // ★LaTeX 원본은 MathML 의 <annotation> 에 있다. encoding 속성이 HTML 파싱서 유실될 수 있어
        //   속성 필터 없이 annotation 태그로 찾는다(엄격 셀렉터 실패→textContent 중복폴백이 'x3...x3' 깨짐 원인).
        const tex = (k.querySelector('annotation')?.textContent ?? '').trim();
        if (tex) { k.replaceWith(doc.createTextNode(` $${tex}$ `)); return; }
        // annotation 이 복사 과정에 잘렸으면 보이는 부분(.katex-html)만 — MathML 중복 텍스트 제거.
        const visible = k.querySelector('.katex-html')?.textContent ?? k.textContent ?? '';
        k.replaceWith(doc.createTextNode(visible));
      });
      const text = (doc.body.textContent ?? '')
        .replace(/\u00a0/g, ' ')
        .replace(/[ \t]*\n[ \t]*/g, '\n')
        .replace(/\n{3,}/g, '\n\n')
        .replace(/[ \t]{2,}/g, ' ')
        .trim();
      return text || null;
    } catch { return null; }
  };

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
    const sanitizeForDisplay = (s: string) => {
      // ① 닫힌 python block 제거.
      let stripped = s.replace(/```(?:python|py|sympy)[\s\S]*?```/g, '');
      // ② 스트리밍 중 아직 닫는 ``` 가 안 온 미완성 펜스도 잘라낸다. 안 그러면
      //    여는 펜스부터 끝까지 raw python 이 사용자에게 노출됨.
      let hadOpenPy = false;
      const openIdx = stripped.search(/```(?:python|py|sympy)\b/);
      if (openIdx !== -1) {
        stripped = stripped.slice(0, openIdx);
        hadOpenPy = true;
      }
      stripped = stripped.trim();
      const hadPy = hadOpenPy || stripped !== s.trim();
      if (hadPy && stripped.length < 50) return '⚙ 정확한 좌표 계산 중…';
      return stripped;
    };

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
        const evalArith = (e: string): number | null => {
          const toks = e.match(/\d+\.?\d*|[+\-*/()]/g); if (!toks) return null;
          const out: (number | string)[] = []; const ops: string[] = [];
          const prec: Record<string, number> = { '+': 1, '-': 1, '*': 2, '/': 2 };
          for (const t of toks) {
            if (/\d/.test(t)) out.push(parseFloat(t));
            else if (t === '(') ops.push(t);
            else if (t === ')') { while (ops.length && ops[ops.length - 1] !== '(') out.push(ops.pop()!); ops.pop(); }
            else { while (ops.length && (prec[ops[ops.length - 1]] ?? 0) >= prec[t]) out.push(ops.pop()!); ops.push(t); }
          }
          while (ops.length) out.push(ops.pop()!);
          const st: number[] = [];
          for (const t of out) {
            if (typeof t === 'number') st.push(t);
            else { const b = st.pop(); const a = st.pop(); if (a === undefined || b === undefined) return null; st.push(t === '+' ? a + b : t === '-' ? a - b : t === '*' ? a * b : a / b); }
          }
          return st.length === 1 ? st[0] : null;
        };
        const findArithErr = (text: string): { expr: string; claimed: string; correct: string } | null => {
          const clean = text.replace(/\\boxed\{([^}]*)\}/g, '$1').replace(/\\cdot|\\times/g, '*').replace(/\\div/g, '/').replace(/\\[a-zA-Z]+|[$]/g, ' ');
          // ★체인 "X = <순수산술> = <숫자>" 에서 두 등호 *사이* 전체 산술을 캡처(앞 등호 필수) — 이전엔
          //   부분 매칭이 "8+12-18+9" 의 "8+" 를 앞 매칭에 뺏겨 "12-18+9=11" 오탐(3≠11)했음. 비체인은 패스(오탐<누락).
          const re = /=\s*([0-9][0-9\s+\-*/().]*?)\s*=\s*(-?[0-9]+(?:\.[0-9]+)?)/g;
          let m: RegExpExecArray | null;
          while ((m = re.exec(clean)) !== null) {
            const e = m[1].replace(/\s/g, '');
            if (!/^[0-9+\-*/().]+$/.test(e) || !/[+\-*/]/.test(e)) continue;
            const v = evalArith(e);
            if (v === null || !isFinite(v)) continue;
            if (Math.abs(v - parseFloat(m[2])) > 1e-6) return { expr: m[1].trim(), claimed: m[2], correct: String(Number.isInteger(v) ? v : +v.toFixed(4)) };
          }
          return null;
        };
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
            {subtitle} 대화는 이 브라우저(localStorage)에 저장.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          {/* BYOK 활성 시 학생 모델 표시, dev fallback 모드면 claude select */}
          {byokActive ? (
            <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded px-2 py-1 text-[10px] font-mono"
                  title={byokBaseURL}>
              {isOllamaLike ? '🖥 ' : ''}{byokModel}
            </span>
          ) : (
            <select
              value={model}
              onChange={(e) => setModel(e.target.value as 'haiku' | 'sonnet')}
              className="bg-[color:var(--color-surface)] border border-[color:var(--color-border)] rounded px-2 py-1 text-xs text-zinc-300 focus:outline-none focus:border-indigo-400"
            >
              <option value="haiku">claude-haiku</option>
              <option value="sonnet">claude-sonnet</option>
            </select>
          )}
          <button
            onClick={() => setByokOpen((v) => !v)}
            title="내 API 키 설정"
            className={`text-[10px] tracking-wider px-2 py-1 rounded transition ${
              byokOpen ? 'bg-indigo-500/20 text-indigo-300' : 'text-zinc-500 hover:text-zinc-200'
            }`}
          >
            ⚙ {byokActive ? '내 키' : '설정'}
          </button>
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

      {byokOpen && (
        <div className="mb-3 rounded-lg border border-indigo-500/30 bg-indigo-500/5 p-3 space-y-2 text-xs">
          <div className="flex items-baseline justify-between">
            <p className="font-semibold text-zinc-200">🔑 내 API 키 설정</p>
            <span className="text-[10px] text-zinc-500">이 기기에만 저장</span>
          </div>

          {/* Provider preset 칩 */}
          <div className="flex flex-wrap gap-1">
            <button
              onClick={() => {
                setByokBaseURL('https://openrouter.ai/api/v1');
                setByokModel('anthropic/claude-haiku-4.5');
              }}
              className="text-[10px] px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:bg-indigo-500/20 hover:text-indigo-300"
            >☁ OpenRouter</button>
            <button
              onClick={() => {
                setByokBaseURL('http://localhost:11434/v1');
                setByokModel('gemma4:e4b-it-q4_K_M');
                setByokApiKey('ollama');
              }}
              className="text-[10px] px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:bg-emerald-500/20 hover:text-emerald-300"
            >🖥 Ollama (localhost)</button>
            <button
              onClick={() => {
                const cur = prompt('Tailscale 의 본인 맥북/PC IP 를 입력하세요 (예: 100.79.230.49)', '100.');
                if (cur && /^100\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/.test(cur.trim())) {
                  setByokBaseURL(`http://${cur.trim()}:11434/v1`);
                  setByokModel('gemma4:e4b-it-q4_K_M');
                  setByokApiKey('ollama');
                }
              }}
              className="text-[10px] px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:bg-emerald-500/20 hover:text-emerald-300"
              title="Tailscale IP 입력 후 자동 설정"
            >🖥 Ollama (Tailscale)</button>
          </div>

          {/* base URL */}
          <div className="flex gap-2 items-center">
            <label className="text-[11px] text-zinc-400 shrink-0 w-14">URL</label>
            <input
              type="text"
              value={byokBaseURL}
              onChange={(e) => setByokBaseURL(e.target.value)}
              placeholder="https://openrouter.ai/api/v1"
              className="flex-1 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded px-2 py-1.5 text-xs font-mono text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400"
            />
          </div>

          {/* API key */}
          <div className="flex gap-2 items-center">
            <label className="text-[11px] text-zinc-400 shrink-0 w-14">API key</label>
            <input
              type="password"
              value={byokApiKey}
              onChange={(e) => setByokApiKey(e.target.value)}
              placeholder={isOllamaLike ? '(Ollama 는 불필요)' : 'sk-or-v1-...'}
              className="flex-1 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded px-2 py-1.5 text-xs font-mono text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400"
            />
          </div>

          {/* model */}
          <div className="flex gap-2 items-center">
            <label className="text-[11px] text-zinc-400 shrink-0 w-14">모델</label>
            <input
              type="text"
              value={byokModel}
              onChange={(e) => setByokModel(e.target.value)}
              placeholder="anthropic/claude-haiku-4.5"
              className="flex-1 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded px-2 py-1.5 text-xs font-mono text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400"
            />
          </div>
          <div className="flex flex-wrap gap-1 pt-1">
            <span className="text-[10px] text-zinc-500 self-center mr-1">모델 빠른 선택:</span>
            {(isOllamaLike
              ? ['gemma4:e4b-it-q4_K_M', 'gemma4:e2b', 'gemma4:26b', 'gemma3:4b', 'llama3.2-vision:11b', 'qwen2.5-vl:7b']
              : ['anthropic/claude-haiku-4.5', 'google/gemini-2.5-flash', 'openai/gpt-5-mini', 'openrouter/auto']
            ).map((id) => (
              <button key={id} onClick={() => setByokModel(id)}
                      className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200">
                {id}
              </button>
            ))}
          </div>

          {!isOllamaLike && (
            <p className="text-[10px] text-zinc-500 leading-relaxed pt-1">
              💡 OpenRouter key 는 <a href="https://openrouter.ai/keys" target="_blank" rel="noreferrer"
                                       className="text-indigo-400 hover:text-indigo-300 underline">openrouter.ai/keys</a> 에서 발급
            </p>
          )}
          {isOllamaLike && (
            <p className="text-[10px] text-zinc-500 leading-relaxed pt-1">
              💡 Ollama 사용: 맥북·PC 에 <code className="text-zinc-300">ollama serve</code> 띄우고 모델 pull (예: <code className="text-zinc-300">ollama pull gemma4:e4b-it-q4_K_M</code>).
              Tailscale 로 원격 접속 시 <code className="text-zinc-300">OLLAMA_HOST=0.0.0.0 ollama serve</code> 후 본인 tailnet IP 입력.
            </p>
          )}

          <div className="flex justify-end gap-2 pt-1">
            <button
              onClick={() => { saveByok('', byokModel, 'https://openrouter.ai/api/v1'); setByokOpen(false); }}
              className="text-[11px] text-zinc-500 hover:text-rose-400 px-2"
            >리셋 (dev fallback)</button>
            <button
              onClick={() => { saveByok(byokApiKey, byokModel, byokBaseURL); setByokOpen(false); }}
              disabled={!byokBaseURL.trim() || (!isOllamaLike && !byokApiKey.trim())}
              className="text-[11px] px-3 py-1 rounded bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-500/30 disabled:opacity-40"
            >저장</button>
          </div>
        </div>
      )}

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

      <style>{`
        /* 대화 스크롤 영역 — 네이티브 스크롤바는 모바일에서 곧 사라지고 터치로 못 잡으며 너무
           얇다. 그래서 네이티브는 완전히 숨기고( ↓ ) JS 로 그리는 커스텀 스크롤바(.chat-scrollbar-*)
           를 쓴다: 항상 보이고, 굵고, 손/터치로 드래그 가능. */
        .chat-scroll { overscroll-behavior: contain; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
        .chat-scroll::-webkit-scrollbar { width: 0; height: 0; display: none; }
        /* 드래그 선택을 또렷하게(인용용). 기본 ::selection(연노랑)이 약해 안 보이던 것 → 진한 인디고+흰
           글자로 강제. 불투명색이라 light(베이지)·dark 양쪽서 또렷. KaTeX 의 모든 자식 span 까지 적용. */
        .chat-scroll ::selection { background: #4f46e5 !important; color: #ffffff !important; }
        .chat-scroll *::selection { background: #4f46e5 !important; color: #ffffff !important; }
        .chat-scroll .katex *::selection { background: #4f46e5 !important; color: #ffffff !important; }
        /* 커스텀 스크롤바 트랙 — 영역 우측 가장자리에 떠 있는 굵은 레일(14px). overflow 있을 때만 노출. */
        .chat-scrollbar-track {
          position: absolute;
          top: 4px; bottom: 4px; right: 1px;
          width: 14px;
          border-radius: 8px;
          background: color-mix(in oklab, var(--color-border) 55%, transparent);
          touch-action: none;
          opacity: 0;
          pointer-events: none;
          transition: opacity .18s ease;
          z-index: 6;
          cursor: pointer;
        }
        .chat-scrollbar-track[data-visible="1"] { opacity: 1; pointer-events: auto; }
        /* thumb — 손으로 잡는 손잡이. 최소 40px 보장(JS), 또렷한 잉크색. */
        .chat-scrollbar-thumb {
          position: absolute;
          left: 2px; right: 2px;
          top: 0;
          min-height: 40px;
          border-radius: 7px;
          background: var(--color-border-strong);
          border: 1px solid color-mix(in oklab, var(--color-subtle) 35%, transparent);
          box-shadow: 0 1px 2px rgba(0,0,0,0.08);
          touch-action: none;
          cursor: grab;
          transition: background .15s ease;
        }
        .chat-scrollbar-thumb:hover { background: color-mix(in oklab, var(--color-border-strong) 60%, var(--color-subtle)); }
        .chat-scrollbar-thumb:active { background: var(--color-subtle); cursor: grabbing; }
        .prose-chat p { margin: 0.25rem 0; }
        .prose-chat p:first-child { margin-top: 0; }
        .prose-chat p:last-child { margin-bottom: 0; }
        .prose-chat .chat-md-heading {
          font-weight: 700;
          line-height: 1.3;
          margin: 0.7rem 0 0.3rem;
          color: var(--color-text);
        }
        .prose-chat h4.chat-md-heading { font-size: 1.02em; }
        .prose-chat h5.chat-md-heading { font-size: 0.95em; color: var(--color-muted); }
        .prose-chat .chat-md-heading:first-child { margin-top: 0; }
        .prose-chat code {
          background: rgba(255,255,255,0.08);
          padding: 1px 5px;
          border-radius: 3px;
          font-size: 0.9em;
          font-family: var(--font-mono);
        }
        .prose-chat pre {
          background: rgba(0,0,0,0.4);
          border: 1px solid #27272a;
          border-radius: 6px;
          padding: 0.5rem 0.75rem;
          margin: 0.5rem 0;
          overflow-x: auto;
          font-size: 0.8em;
        }
        .prose-chat pre code { background: none; padding: 0; }
        .prose-chat .katex { color: inherit; }
        /* 좁은 채팅 폭에서 긴 display 수식이 깨지지 않고 가로 스크롤 */
        /* padding 0.35em: 한글 글리프 잉크가 KaTeX 메트릭 박스 위아래로 솟는데
           overflow-y:hidden 이 패딩 경계에서 클립 → 패딩으로 흡수(글자 상단 잘림 방지). */
        .prose-chat .katex-display { margin: 0.5rem 0; overflow-x: auto; overflow-y: hidden; max-width: 100%; padding: 0.35em 0; }
        .prose-chat table {
          border-collapse: collapse;
          margin: 0.6em 0;
          font-size: 0.92em;
          width: auto;
        }
        .prose-chat th, .prose-chat td {
          border: 1px solid var(--color-border);
          padding: 0.3em 0.6em;
          text-align: left;
          vertical-align: top;
        }
        .prose-chat th {
          background: var(--color-surface-2);
          font-weight: 600;
        }
      `}</style>
    </section>
  );
}
