# 맥북 Pro gemma 서버 운영 지침

로컬 LLM(gemma, **토큰·쿼터 0**) 서버. 비전 교정(corrector)과 개념 본문 대량 변환이 이 서버에 의존한다. 관리 스크립트: `web/scripts/gemma_server.sh`.

## 무엇 / 어디

- **호스트**: MacBook Pro — Tailscale `macbook-pro` = `100.79.230.49` (ssh 별칭 `macbook`)
- **엔드포인트**: `http://100.79.230.49:8080/v1` (OpenAI 호환 `/chat/completions`, `/models`). 코드의 `GEMMA_URL` 기본값.
- **모델**: `mlx-community/gemma-4-26B-A4B-it-qat-4bit` (26B MoE, 활성 4B, 4bit 양자화). HF 캐시에 다운로드 완료.
- **런타임**: `mlx_vlm.server` (Apple MLX, 비전+텍스트 둘 다). venv: `~/gemma-corrector/.venv` (python3.12). 로그: `~/gemma-corrector/server.log`.

## 기동 명령 (수동 원형)

```bash
ssh macbook 'cd ~/gemma-corrector && nohup .venv/bin/python -m mlx_vlm.server \
  --model mlx-community/gemma-4-26B-A4B-it-qat-4bit --port 8080 --host 0.0.0.0 \
  > server.log 2>&1 & echo started $!'
```
모델 로딩에 수십 초. `--host 0.0.0.0` 라야 Tailscale(100.79.230.49)로 노출됨.

## 관리 스크립트 사용 (권장)

```bash
web/scripts/gemma_server.sh start     # 기동 + 로딩 대기
web/scripts/gemma_server.sh status    # 생사
web/scripts/gemma_server.sh test      # 생성 1회 확인
web/scripts/gemma_server.sh restart   # 재시작
web/scripts/gemma_server.sh watch     # ★watchdog: 60s마다 점검·죽으면 자동 재시작 (긴 배치 중 백그라운드로)
```

## ★알려진 문제 — 장시간/대량 요청 후 크래시

대량 변환(개념 ~1600개 등) 도중 mlx 서버가 **`Connection refused`로 죽는다**(요청 누적 메모리 추정). 2026-06-22 전수 변환에서 ~334건 후 크래시 → 1253건 실패한 사례.

**대응 (루프 엔지니어링):**
1. 배치 스크립트는 연결오류 시 **재시도/서버 대기**를 내장할 것 (예: `/tmp/convert_all.py`의 `wait_server()` + 40회 재시도). 그래야 watchdog이 재기동하는 동안 in-flight가 살아남는다.
2. 긴 배치는 **`gemma_server.sh watch`를 백그라운드로 동반** → 크래시 자동 복구.
3. 배치는 **멱등·재개식**(마커 파일)으로 짜서, 크래시·재시작 후 이어가게.
4. 동시 호출은 **2병렬까지**(사장님 확인). 그 이상은 미검증.

## 의존 코드

- `web/scripts/corrector.mjs` (`gemmaCall`, `GEMMA_URL`) — 비전 교정.
- 개념 본문 변환 배치(`/tmp/convert_all.py` 류) — 텍스트 생성.
- OpenRouter `gemma-4-26b:free`는 **별개 폴백**(현재 키 비활성). 로컬이 우선.
