# Roster model & giá

**Cập nhật: 2026-08-22.** Giá theo USD / 1 triệu token (input / output), giá niêm yết công khai. Nếu hôm nay đã cách xa ngày này, tra lại trước khi trích dẫn con số.

## Mục lục

- [Anthropic](#anthropic)
- [OpenAI](#openai)
- [Google](#google)
- [Open-weight](#open-weight)
- [Thang effort](#thang-effort)
- [Nhân tố chi phí](#nhân-tố-chi-phí)
- [Nguồn](#nguồn)

## Anthropic

| Model | Giá | Ghi chú |
|---|---|---|
| Fable 5 | $10 / $50 | Tier cao nhất |
| Mythos 5 | $10 / $50 | Hạn chế phát hành |
| Opus 5 | $5 / $25 | Suy luận mạnh nhất trong nhóm phổ thông |
| Opus 4.8 / 4.7 / 4.6 / 4.5 | $5 / $25 | Bản cũ, vẫn chạy |
| Sonnet 5 | $2 / $10 | Giá giới thiệu, cố định từ 9/2026 |
| Sonnet 4.6 / 4.5 | $3 / $15 | |
| Haiku 4.5 | $1 / $5 | Nhanh, gọn nhất |

Cửa sổ ngữ cảnh 1M token ở giá tiêu chuẩn. Model từ 4.7 trở lên dùng tokenizer mới — cùng một đoạn văn tốn nhiều hơn ~30% token, nên khi so giá với bản cũ phải nhân vào.

## OpenAI

| Model | Giá | Ghi chú |
|---|---|---|
| gpt-5.6-sol | — | Flagship; alias `gpt-5.6` trỏ vào đây |
| gpt-5.6-terra | — | Cân bằng, rẻ hơn sol |
| gpt-5.6-luna | — | Khối lượng lớn, hiệu suất chi phí |
| GPT-5.5 | $5–10 / $30–45 | Bậc giá đổi ở mốc 272K token |
| GPT-5.4 | $2.50–5 / $15–22.50 | Bậc giá đổi ở mốc 272K token |
| GPT-5 | $1.25 / $10 | |
| GPT-5 Mini | $0.25 / $2 | |
| GPT-5 Nano | $0.05 / $0.40 | Rẻ nhất |
| o3-pro | $20 / $80 | Suy luận chuyên sâu, đắt |
| o3 | $2 / $8 | |
| o4-mini / o3-mini | $1.10 / $4.40 | |

Giá công khai của dòng gpt-5.6 chưa xác nhận được từ trang chính thức tại thời điểm cập nhật — để trống thay vì đoán. Khi cần ước lượng chi phí cho gpt-5.6, dùng GPT-5.5 làm cận trên và nói rõ đó là ước lượng.

Thế mạnh nêu trong tài liệu: suy luận giữ xuyên nhiều lượt, gọi tool theo cách lập trình được, phán đoán về layout và phân cấp thị giác, và đạt hiệu năng cao với ít token output hơn.

## Google

| Model | Giá | Ghi chú |
|---|---|---|
| Gemini 3.7 Flash | $0.75 / $3.75 | Ưu đãi tới 31/12/2026; hướng agentic + multimodal |
| Gemini 3.6 Flash | $0.75 / $3.75 | Ưu đãi tới 31/12/2026 |
| Gemini 3.5 Flash | $1.50 / $9 | Có free tier giới hạn |
| Gemini 3.5 Flash-Lite | $0.30 / $2.50 | Rẻ nhất trong nhóm GA |

Gemini không phơi ra các nấc effort rời rạc như Claude hay OpenAI — token suy nghĩ tính vào giá output và mức suy nghĩ do model tự điều tiết. Nên khi đề xuất Gemini, cột Effort ghi `n/a (auto)` thay vì bịa ra một nấc.

## Open-weight

| Model | Giá tham chiếu | Mạnh ở |
|---|---|---|
| Kimi K3 | — | Toàn diện; suy luận (GPQA Diamond 93.5%), dùng terminal (Terminal-Bench 2.1 88.3%) |
| DeepSeek V4 Pro | — | Agentic coding (SWE-bench 80.6%), ngữ cảnh lớn |
| DeepSeek V4 Flash | $0.14 / $0.28 | Rẻ nhất, suy luận vẫn khá |
| GLM 5.2 | $0.95 / $3 | Nhanh (~347 t/s), cân bằng giá |
| MiniMax M3 | — | Đều tay giữa suy luận, code, thao tác máy |
| Llama 3.3 70B | $0.59 / $0.70 | Rất nhanh (~2500 t/s), hợp bulk đơn giản |

Giá open-weight phụ thuộc nhà cung cấp inference; các con số trên là mức thị trường tham khảo, không phải niêm yết chính thức.

## Thang effort

**Anthropic** — `low` → `medium` → `high` → `xhigh` → `max`. Mặc định `high` trên Opus 5, Opus 4.8/4.7, Sonnet 5, Sonnet 4.6, Fable 5.

- `low`: tiết kiệm token đáng kể
- `medium`: cân bằng
- `high`: mặc định
- `xhigh`: việc dài hơi (30+ phút); có trên Fable 5, Mythos 5, Opus 5/4.8/4.7, Sonnet 5
- `max`: không giới hạn token suy nghĩ; có trên Fable 5, Mythos 5, Opus 5/4.8, Opus 4.7/4.6, Sonnet 5/4.6

Đặt qua `output_config={"effort": "..."}`. Chạy được trên Claude API, AWS/Bedrock, Google Cloud, Microsoft Foundry.

**OpenAI** — `reasoning_effort`: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Giá trị được hỗ trợ tùy model; GPT-5.5 mặc định `medium`. Kiểm tra trang model trước khi dùng nấc cao — không phải model nào cũng nhận đủ 7 nấc.

**Google** — không có tham số nấc rời rạc; xem mục Google ở trên.

Ánh xạ thô khi so sánh chéo nhà cung cấp: Anthropic `low`≈OpenAI `low`, `medium`≈`medium`, `high`≈`high`, `xhigh`≈`xhigh`, `max`≈`max`. Đây là ánh xạ theo tên, không phải theo lượng token suy nghĩ thực tế — đừng dựa vào nó để so chi phí chính xác.

## Nhân tố chi phí

Áp cho Anthropic; các nhà cung cấp khác có cơ chế tương tự nhưng hệ số khác:

- Prompt caching: ghi 1.25× (TTL 5 phút) hoặc 2× (TTL 1 giờ); đọc 0.1×
- Batch API: giảm 50% cả input lẫn output
- Data residency (`inference_geo: "us"`): 1.1×

Cache đọc ở 0.1× là đòn bẩy lớn nhất trong một phiên dài: một context 100k token đọc lại 20 lần tốn bằng đọc mới 2 lần. Nghĩa là trong một phiên đã cache, chi phí thật của việc **giữ nguyên** model thấp hơn nhiều so với chi phí đổi model — đổi model là mất toàn bộ cache. Cân nhắc điều này trước khi đề xuất đổi qua đổi lại giữa các bước ngắn.

## Nguồn

- [Claude Platform — Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude Platform — Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [OpenAI — Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [Gemini API — Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Vellum — Open LLM Leaderboard](https://www.vellum.ai/open-llm-leaderboard)
