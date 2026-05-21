---
sources: []
created: 2026-05-17
updated: 2026-05-17
kind: site
title: DeepSeek-OCR API (self-hosted)
url: https://macbook-pro.tailf47aa4.ts.net
---

# DeepSeek-OCR API (self-hosted, Ollama 기반)

> **site** · 한국 수능 수학 PDF 인제스트용
> **URL**: `https://macbook-pro.tailf47aa4.ts.net` (tailnet only)

## 요약 (왜 유용한가)

수학 시험 PDF 페이지를 markdown + LaTeX로 정확하게 추출. Claude vision보다 **수식 표기 정확도가 압도적**이고, 도형/그래프 영역의 **bounding box까지 동시에 반환**해서 도형 crop을 자동화할 수 있다.

검증 결과 (2024 수능 p15 — Claude vision이 900초 stuck됐던 페이지):
- DeepSeek-OCR: **8.8초**에 27/28번 문제 완벽 추출
- LaTeX: `\frac`, `\sqrt`, `\int`, `\ge` 등 정확
- 객관식 보기 ①②③④⑤ 보존
- 도형/수식 영역 bbox(`bbox_pixels`) 함께 반환

## 활용법

`scripts/ocr_client.py`의 `ocr_page(png_path)`로 호출. `ingest_round.py`의 vision 단계에서 1차 시도 (실패 시 Claude vision fallback).

- **인증**: `.env`의 `OCR_API_KEY` (Bearer 토큰)
- **mode**: 시험 페이지엔 항상 `markdown`
- **동시성**: 단일 스레드 (Ollama 직렬화) — concurrency=1로 호출
- **타임아웃**: 600s (콜드 스타트 ~60s 가능)
- **결과**:
  - `text`: 본문 (LaTeX 포함)
  - `regions[]`: `ref` (figure/image/text/equation) + `bbox_pixels` + 옵션 `crop_b64`
  - figure crop은 `db/raw/<round>/figures/<page>_<i>.png`에 저장 후 문제 markdown에 `<img>` 링크

## 제약

- 단일 페이지만 (PDF는 페이지 단위 PNG로 rasterize 후 전송)
- Multi-column / 두 페이지 spread 스캔은 혼동
- 수식 OCR이 데이터 품질의 천장 — 어려운 페이지는 spot-check 또는 Mathpix 등 2차 OCR 검토
- 단답형 답안표가 도형으로 렌더된 PDF (한국 수능 답안표 일부)는 OCR도 어려움

## 관련 단원

전 단원 (인제스트 파이프라인 도구)
