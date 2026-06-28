// 튜터 채팅 영역 스타일(커스텀 스크롤바·prose-chat·KaTeX·표 등) — ChatPanel 에서 분리.
export const CHAT_STYLES = `
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
`;
