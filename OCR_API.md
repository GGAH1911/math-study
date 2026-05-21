# OCR API (DeepSeek-OCR via Ollama, on `macbook-pro`)

A self-hosted DeepSeek-OCR HTTP service for ingesting exam pages (수능 / 모의고사 / 학력평가 등) into this repo's problem database. It returns the page's text in markdown (with LaTeX-formatted equations) **and** pixel-space bounding boxes for figures, graphs, and diagrams — so you can crop them out of the original image and store them alongside each problem.

The model does **not** interpret diagrams semantically; it only locates them. Cropping + storage is your job.

## Connection

- **Endpoint**: `https://macbook-pro.tailf47aa4.ts.net` (this host is already in our tailnet — no extra setup needed)
- **Auth**: Bearer token, value in `.env` as `OCR_API_KEY`
- **Transport**: HTTPS via Tailscale Serve (valid Let's Encrypt cert, auto-renewed)
- **Reachability**: tailnet-only. Will not respond to public DNS / public IPs.

Quick liveness check before a long run:

```bash
curl -s "$OCR_API_URL/health"
# -> {"status":"ok","ollama_reachable":true,"model":"deepseek-ocr"}
```

If `status` is anything other than `ok` or the request hangs, `macbook-pro` is asleep / offline — the OCR host must be awake for any of this to work.

## Endpoint: `POST /ocr`

`multipart/form-data` with these fields:

| field           | required | values                                    | meaning |
|-----------------|----------|-------------------------------------------|---------|
| `file`          | yes      | PNG or JPEG                               | the page image |
| `mode`          | no       | `markdown` (default) / `layout` / `figure` / `free` | prompt preset |
| `include_crops` | no       | `true` / `false` (default `false`)        | if true, server returns each region as a base64 PNG so you skip a re-crop step |

### Mode cheat sheet

- **`markdown`** — full page: text + LaTeX equations + bounding boxes for all detected regions. **Use this for exam problem pages** — it's the only mode that gives you both the body text and figure locations in one shot.
- **`layout`** — emphasizes layout detection over text content. Useful if `markdown` mode misses a region; re-run in layout mode just for bounding boxes.
- **`figure`** — describes the contents of a single figure (chart, table, diagram). No bounding boxes returned. Useful as a **second pass** on a crop you've already cut.
- **`free`** — plain OCR. No structure, no bounding boxes. Mostly useful for plaintext snippets.

## Response shape

```json
{
  "mode": "markdown",
  "image_size": [1240, 1754],
  "raw":  "...<|ref|>figure<|/ref|><|det|>[[145,230,580,720]]<|/det|>...",
  "text": "문제 12. 함수 f(x) = ...\n\\[ f'(x) = 2x \\]\n...",
  "regions": [
    {
      "ref": "figure",
      "bbox_norm":   [145, 230, 580, 720],
      "bbox_pixels": [180, 403, 719, 1263],
      "crop_b64": null
    }
  ]
}
```

- `raw` — what the model literally emitted, including `<|ref|>...<|/ref|><|det|>[[...]]<|/det|>` grounding tags.
- `text` — `raw` with grounding tags stripped. This is what you store as the problem body. Equations come through as LaTeX (`\[ ... \]` or `\( ... \)`).
- `regions[].ref` — the model's label for the region. Observed values include `figure`, `image`, `text`, `equation`, `title`, `paragraph`, `table`, etc. For diagram cropping you usually want `figure` or `image`.
- `regions[].bbox_norm` — the model's native 0–999 normalized grid. **Don't crop with this.**
- `regions[].bbox_pixels` — the same box rescaled to your input image's actual pixel dimensions. **This is what you crop with.**
- `regions[].crop_b64` — only populated when you pass `include_crops=true`. Base64-encoded PNG of the cropped region. Saves you from re-opening the source image.

## Reference client

```python
import base64, os, httpx

URL = os.environ["OCR_API_URL"]   # from .env
KEY = os.environ["OCR_API_KEY"]

def ocr_page(image_path: str, include_crops: bool = True) -> dict:
    with open(image_path, "rb") as f:
        r = httpx.post(
            f"{URL}/ocr",
            headers={"Authorization": f"Bearer {KEY}"},
            files={"file": (os.path.basename(image_path), f, "image/png")},
            data={"mode": "markdown", "include_crops": str(include_crops).lower()},
            timeout=600,   # cold start can be ~60s, large pages can take minutes
        )
    r.raise_for_status()
    return r.json()


def save_figures(result: dict, out_dir: str, stem: str) -> list[str]:
    """Write each figure/image region to disk; return the saved paths."""
    paths = []
    for i, reg in enumerate(result["regions"]):
        if reg["ref"] not in ("figure", "image"):
            continue
        if not reg["crop_b64"]:
            continue
        path = os.path.join(out_dir, f"{stem}_fig{i:02d}.png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(reg["crop_b64"]))
        paths.append(path)
    return paths


if __name__ == "__main__":
    result = ocr_page("page_001.png")
    print(result["text"])
    print(save_figures(result, out_dir="crops", stem="2024_6_math"))
```

`curl` equivalent:

```bash
curl -s -X POST "$OCR_API_URL/ocr" \
  -H "Authorization: Bearer $OCR_API_KEY" \
  -F file=@page.png \
  -F mode=markdown \
  -F include_crops=true \
  | jq '{text, regions: [.regions[] | {ref, bbox_pixels}]}'
```

## Pipeline notes for exam ingestion

1. **One page = one request.** Don't try to send a multi-page PDF; rasterize to PNG (300 DPI is plenty) and send page-by-page.
2. **Pages with no diagrams** still return a `regions` array — usually with `ref: "text"` / `"equation"` / `"title"` boxes. Filter to `ref in {"figure","image"}` (and arguably `"table"`) for cropping.
3. **Multi-column / two-page-spread scans** confuse the model. Split the spread into single pages first.
4. **Cold start**: first call after macbook-pro reboots or after long idle takes ~30–60s while Ollama loads the model onto Metal. Subsequent calls are seconds. Don't lower the client timeout below ~600s for safety.
5. **Equation accuracy is the ceiling on data quality.** If LaTeX comes out wrong for a problem, the database row is poisoned. Spot-check a sample of math output before bulk-ingesting; if accuracy is borderline, consider re-running just the equation crops through a second pass or a paid math OCR (Mathpix) for that subset.
6. **bbox is sometimes slightly tight** — the model can clip 5–10 px inside the figure border. If your downstream uses the crop as-is, pad the box by ~10 px on each side before cutting:

   ```python
   def pad(box, w, h, p=10):
       x1, y1, x2, y2 = box
       return [max(0, x1-p), max(0, y1-p), min(w, x2+p), min(h, y2+p)]
   ```

7. **The model is prompt-sensitive** (upstream docs flag this explicitly — a missing punctuation mark or newline can change output). The server hard-codes the prompts; do not append instructions to `mode`.
8. **Throughput is single-threaded.** Ollama serializes generation; firing 10 concurrent requests doesn't help. Run the ingest pipeline serially or with concurrency=1.

## Failure modes

| symptom                                | likely cause                                                | fix |
|----------------------------------------|-------------------------------------------------------------|-----|
| 401                                    | wrong / missing `OCR_API_KEY`                               | check `.env` |
| 400 "Invalid image"                    | non-image bytes or corrupt PNG                              | re-rasterize page |
| timeout / connection refused           | `macbook-pro` is asleep, or Ollama crashed                  | poke the host owner; `/health` will be unreachable |
| `regions` empty when figures clearly exist | `mode=free` or `mode=figure` (no grounding)              | use `mode=markdown` or `mode=layout` |
| `bbox_pixels` is `null`                | image couldn't be opened on server (very rare)              | resend |
| LaTeX equations look mangled           | model error, not transport. The page is genuinely hard.     | re-render at higher DPI, or accept and flag for manual review |

## Out of scope

- The server does not store anything. Each request is stateless; uploaded images are not retained past the response.
- The server does not OCR PDFs directly. Rasterize first.
- There is no batching endpoint. One image per request.
