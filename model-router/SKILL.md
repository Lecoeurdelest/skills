---
name: model-router
description: Recommends which LLM and which reasoning-effort level to use for the next step of a task, using a scoring matrix across Claude, OpenAI, Gemini and open-weight models. Use this at the end of EVERY step of ANY multi-step task — coding, research, data work, writing, ops — even when the user never mentions models, cost, or effort. Also use whenever the user asks "model nào", "effort bao nhiêu", "dùng model gì", which model should I use, should I switch models, is this worth Opus, can a cheaper model do this, how do I cut token cost, or asks to route/pick/downgrade/upgrade a model for a task.
---

# Model Router

Cuối mỗi bước của một task nhiều bước, chèn một bảng nhỏ đề xuất model + effort cho **bước kế tiếp**.

Lý do tồn tại: mặc định người ta chạy cả task trên một model duy nhất — hoặc quá nặng (đốt tiền cho việc đổi tên file), hoặc quá nhẹ (Haiku viết migration script). Chi phí và chất lượng đều nằm ở chỗ chọn sai cho **từng bước**, không phải cho cả task. Bảng này ép việc chọn lại ở mỗi ranh giới bước.

## Khi nào chạy

Bất kỳ task nào có ≥2 bước. Chèn bảng sau khi báo kết quả bước vừa xong, trước khi làm bước kế.

Không chèn khi: hội thoại thuần túy, câu hỏi một lượt, hoặc bước cuối cùng (không còn bước kế — thay bằng một dòng tổng kết chi phí nếu task dài).

## Chấm điểm: 4 tín hiệu, mỗi tín hiệu 0–2

Chấm cho **bước kế tiếp**, không phải cho task tổng thể. Đây là lỗi hay gặp nhất: task tổng thể nặng không có nghĩa mọi bước trong nó đều nặng.

**A — Mơ hồ.** 0: spec rõ, chỉ thi hành. 1: vài chỗ phải tự suy luận. 2: phải tự định nghĩa vấn đề trước khi giải.

**B — Chiều sâu suy luận.** 0: một phép tra/biến đổi. 1: 2–4 bước phụ thuộc nhau. 2: ≥5 bước, hoặc phải giữ một bất biến toàn cục xuyên suốt.

**C — Hậu quả nếu sai.** 0: chỉ đọc, sai thì chạy lại. 1: ghi file/sinh code, sửa được. 2: không hoàn tác được — deploy, migration, xóa dữ liệu, gửi ra ngoài, hoặc con số người dùng sẽ trích dẫn cho người khác.

**D — Tải ngữ cảnh.** 0: dưới ~5k token. 1: nhiều nguồn nhưng xử lý độc lập từng cái. 2: phải đối chiếu chéo nhiều nguồn, hoặc giữ một codebase lớn trong đầu.

Tổng 0–8 → bậc:

| Tổng | Bậc | Tên |
|---|---|---|
| 0–2 | 1 | Rẻ/nhanh |
| 3–4 | 2 | Chủ lực |
| 5–6 | 3 | Nặng |
| 7–8 | 4 | Biên |

## Bảng tuyển chọn

| Bậc | Anthropic | OpenAI | Google | Open-weight | Effort |
|---|---|---|---|---|---|
| 1 | Haiku 4.5 | gpt-5.6-luna | Gemini 3.5 Flash-Lite | DeepSeek V4 Flash | `low` / `minimal` |
| 2 | Sonnet 5 | gpt-5.6-terra | Gemini 3.7 Flash | GLM 5.2 | `medium` |
| 3 | Sonnet 5 hoặc Opus 5 | gpt-5.6-sol | Gemini 3.7 Flash | DeepSeek V4 Pro | `high` |
| 4 | Opus 5 / Fable 5 | gpt-5.6-sol | Gemini 3.7 Flash | Kimi K3 | `xhigh` → `max` |

Chọn cột theo thế mạnh, không theo thói quen:

- **Agentic coding, sửa repo nhiều file, phiên chạy dài** → Anthropic
- **Multimodal (ảnh/video/audio), ngữ cảnh cực dài mà rẻ** → Google
- **Layout/thẩm mỹ thị giác, tool orchestration lập trình** → OpenAI
- **Dữ liệu không được rời hạ tầng, hoặc bulk cực lớn** → open-weight

Giá và thang effort đầy đủ: `references/roster.md`. Ánh xạ chi tiết theo từng loại tác vụ (research, viết, phân tích số liệu, debug, ops): `references/matrix.md`.

## Luật ghi đè

Áp dụng sau khi đã có bậc. Ghi đè thắng điểm số.

1. **Không hoàn tác được** (C=2) → tăng 1 nấc effort, **không** được hạ bậc để tiết kiệm. Kèm một bước xác nhận trước khi chạy.
2. **Cần phản hồi <2s** hoặc đang nói trực tiếp với người dùng cuối → hạ 1 bậc, effort ≤ `low`.
3. **Bulk ≥500 lần gọi** → hạ 1 bậc, effort `low`, dùng batch API (giảm ~50%).
4. **Dữ liệu nhạy cảm/on-prem** → chỉ cột open-weight, giữ nguyên bậc.
5. **Bước cơ học** (chạy lệnh, đổi tên, format, commit) → luôn Bậc 1, bất kể task tổng thể nặng cỡ nào.
6. **Ngữ cảnh >200k token** → chỉ model có cửa sổ ≥1M, hoặc chia nhỏ trước.
7. **Vừa thất bại** → không lặp lại cùng cấu hình. Đổi đúng một trục: +1 bậc **hoặc** đổi nhà cung cấp, không đổi cả hai (nếu đổi cả hai thì không biết cái nào cứu được). Thất bại lần thứ hai → dừng, hỏi người dùng, đừng leo thang tiếp.

## Format

Đúng một bảng, ngay cuối bước:

```
| Bước kế | Model | Effort | Điểm | Lý do |
|---|---|---|---|---|
| Viết migration script | Opus 5 | high | 6 (A1 B2 C2 D1) | ghi DB, không hoàn tác |

Dự phòng: schema rối hơn dự kiến → Opus 5 / xhigh.
```

Cột "Lý do" tối đa ~12 từ — nó là ghi chú, không phải đoạn văn. Dòng "Dự phòng" chỉ viết khi có rủi ro thật; bỏ hẳn nếu bước quá rõ ràng.

**Nếu cấu hình không đổi so với bước trước**, đừng lặp lại bảng — viết một dòng: `→ giữ nguyên Sonnet 5 / medium.` Bảng lặp lại y hệt 5 lần liên tiếp là nhiễu, và người đọc sẽ bắt đầu bỏ qua nó, kể cả lúc nó thực sự đổi.

## Ví dụ

**Bước vừa xong:** đọc 3 file config, tìm chỗ khai báo timeout.
**Bước kế:** sửa timeout ở 3 nơi cho khớp.

| Bước kế | Model | Effort | Điểm | Lý do |
|---|---|---|---|---|
| Sửa timeout 3 file | Haiku 4.5 | low | 2 (A0 B1 C1 D0) | sửa cơ học, đã biết chính xác vị trí |

---

**Bước vừa xong:** dựng xong schema cho pipeline ingest.
**Bước kế:** chọn chiến lược backfill cho 400M dòng đang chạy production.

| Bước kế | Model | Effort | Điểm | Lý do |
|---|---|---|---|---|
| Chiến lược backfill | Opus 5 | xhigh | 7 (A2 B2 C2 D1) | production, không hoàn tác, nhiều ràng buộc |

Dự phòng: nếu bí sau 1 vòng → đổi trục sang gpt-5.6-sol thay vì leo effort.

---

**Bước vừa xong:** chốt dàn ý báo cáo thị trường.
**Bước kế:** đọc 40 bài báo, trích số liệu doanh thu.

| Bước kế | Model | Effort | Điểm | Lý do |
|---|---|---|---|---|
| Trích số liệu 40 nguồn | Gemini 3.5 Flash-Lite | low | 3 (A0 B1 C1 D1) | trích xuất lặp lại, mỗi nguồn độc lập, rẻ |

Dự phòng: nguồn nào có bảng lồng nhau → đẩy riêng nguồn đó lên Sonnet 5 / medium.

Lưu ý ở ví dụ cuối: điểm 3 rơi vào Bậc 2, nhưng luật bulk kéo xuống Bậc 1. Ghi đè thắng điểm — và ghi rõ trong "Lý do" để người đọc không tưởng là chấm sai.

## Giữ độ trung thực

Tên model và giá thay đổi nhanh. Nếu người dùng nhắc tới một model không có trong `references/roster.md`, hoặc nghi ngờ bảng đã cũ, hãy tra web trước khi đề xuất thay vì đoán từ trí nhớ — đề xuất một model không tồn tại còn tệ hơn không đề xuất gì. Roster ghi ngày cập nhật cuối ở đầu file.
