// BYOK(내 API 키) 설정 패널 — ChatPanel 에서 분리(동작 무변, JSX·변수명 그대로).
type Props = {
  byokOpen: boolean;
  byokBaseURL: string; setByokBaseURL: (v: string) => void;
  byokApiKey: string; setByokApiKey: (v: string) => void;
  byokModel: string; setByokModel: (v: string) => void;
  isOllamaLike: boolean;
  saveByok: (apiKey: string, model: string, baseURL: string) => void;
  setByokOpen: (v: boolean) => void;
};

export default function ByokSettings({ byokOpen, byokBaseURL, setByokBaseURL, byokApiKey, setByokApiKey, byokModel, setByokModel, isOllamaLike, saveByok, setByokOpen }: Props) {
  if (!byokOpen) return null;
  return (
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
  );
}
