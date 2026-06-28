// 튜터 채팅의 핵심 메시지 타입(ChatPanel·Message·persistence 공유). ChatModalState·Props 는
// 컴포넌트 전용(렌더러 타입 의존)이라 ChatPanel.tsx 에 둔다.

export type ChatMessage = {
  role: 'user' | 'assistant';
  content: string;
  promoted?: { path: string };
  images?: string[];   // 비전(LLM)용 타일 dataURL (user 메시지에만). 표시엔 displayImage 사용.
  displayImage?: string; // 사용자 표시용 통이미지 dataURL(작게). 타일과 분리해 "조각" 노출 안 함.
  quoted?: string;     // 렌더된 수식 채팅을 복붙해 삽입한 인용 내용(LaTeX 재구성). 표시엔 칩, LLM 엔 인용블록.
  displayText?: string; // quoted 동반 시 칩 옆에 보일 사용자 실제 질문(content 는 인용블록 포함이라 분리).
};
