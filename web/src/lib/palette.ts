// Shared color palettes for graphic components.
//
// Previously each component had its own `COLORS`/`PLOT_COLORS` constant with
// the same 6 dark-mode-friendly colors. Centralizing here so the palette
// stays consistent and is one place to tweak.

// 6-color palette assigned by index. Indigo first so the "primary" curve
// reads as our brand color. Designed for dark backgrounds.
export const PLOT_COLORS: readonly string[] = [
  '#a5b4fc',   // indigo-300
  '#fb7185',   // rose-400
  '#34d399',   // emerald-400
  '#fbbf24',   // amber-400
  '#22d3ee',   // cyan-400
  '#c084fc',   // purple-400
];

// Semantic palette aliases (used inline elsewhere; collected here for
// easier auditing). Keep names short — components import what they need.
export const ACCENT = {
  indigo: '#a5b4fc',
  rose:   '#fb7185',
  emerald:'#34d399',
  amber:  '#fbbf24',
  cyan:   '#22d3ee',
  purple: '#c084fc',
} as const;
