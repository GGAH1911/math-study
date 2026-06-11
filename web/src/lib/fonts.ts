// 폰트 프리셋 — 설정에서 사용자가 고르는 본문/제목/손글씨 3종 세트.
// 전부 Google Fonts 의 SIL Open Font License 폰트(상업적 사용·임베드·수정 무료 → 법적 안전).
// 적용 메커니즘: html[data-font="<id>"] 에 global.css 가 --font-sans/serif/hand 를 오버라이드.
// 로딩: BaseLayout 의 프리페인트 스크립트가 선택된 프리셋의 href 만 <link> 주입(FOUC 최소).
//
// 단일 진실원천 — BaseLayout(프리페인트)·/settings(선택 UI)·global.css(CSS 변수) 가 공유.

export type FontPreset = {
  id: string;
  label: string;
  desc: string;
  // 미리보기·설명용 한글 폰트명(본문/제목/손글씨).
  names: { sans: string; serif: string; hand: string };
  // Google Fonts css2 href — 이 프리셋이 쓰는 패밀리만.
  href: string;
};

// css2 family 파라미터 공통 prefix.
const G = 'https://fonts.googleapis.com/css2?';

export const FONT_PRESETS: FontPreset[] = [
  {
    id: 'sketchbook',
    label: '스케치북',
    desc: '모던한 본문에 명조 제목·펜 손글씨 — 깔끔하고 또렷한 기본값.',
    names: { sans: 'IBM Plex Sans KR', serif: 'Gowun Batang', hand: 'Nanum Pen Script' },
    href: G + 'family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Gowun+Batang:wght@400;700&family=Nanum+Pen+Script&display=swap',
  },
  {
    id: 'warm',
    label: '따뜻한 노트',
    desc: '손으로 쓴 듯한 고운돋움 본문 — 가장 인간적이고 부드럽다. 강조는 개구 손글씨.',
    names: { sans: 'Gowun Dodum', serif: 'Gowun Batang', hand: 'Gaegu' },
    href: G + 'family=Gowun+Dodum&family=Gowun+Batang:wght@400;700&family=Gaegu:wght@400;700&display=swap',
  },
  {
    id: 'round',
    label: '동글동글',
    desc: '둥글고 친근한 주아 — 캐주얼하고 말랑한 분위기. 손글씨는 하이멜로디.',
    names: { sans: 'Jua', serif: 'Jua', hand: 'Hi Melody' },
    href: G + 'family=Jua&family=Hi+Melody&display=swap',
  },
  {
    id: 'classic',
    label: '클래식 명조',
    desc: '전통적인 나눔명조 — 차분하고 우아하다. 책을 읽는 듯한 톤.',
    names: { sans: 'Nanum Myeongjo', serif: 'Nanum Myeongjo', hand: 'Nanum Pen Script' },
    href: G + 'family=Nanum+Myeongjo:wght@400;700;800&family=Nanum+Pen+Script&display=swap',
  },
  {
    id: 'clean',
    label: '깔끔 고딕',
    desc: '구글 본고딕(Noto) — 중립적이고 안정적이며 화면에서 가장 읽기 편하다.',
    names: { sans: 'Noto Sans KR', serif: 'Gowun Batang', hand: 'Nanum Pen Script' },
    href: G + 'family=Noto+Sans+KR:wght@400;500;700&family=Gowun+Batang:wght@400;700&family=Nanum+Pen+Script&display=swap',
  },
];

export const DEFAULT_FONT_ID = 'sketchbook';
export const FONT_STORAGE_KEY = 'ms-font';

// 프리페인트 스크립트가 쓰는 { id: href } 매핑(인라인 주입용).
export const FONT_HREFS: Record<string, string> = Object.fromEntries(
  FONT_PRESETS.map((p) => [p.id, p.href]),
);
