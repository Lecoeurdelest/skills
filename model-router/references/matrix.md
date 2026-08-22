# Ma trận theo loại tác vụ

Đọc file này khi bước kế tiếp rơi vào một loại tác vụ cụ thể và cần biết điểm chấm thường rơi vào đâu, cùng những cái bẫy riêng của loại đó. Bảng chính và luật ghi đè nằm trong SKILL.md — file này chỉ làm rõ thêm.

## Mục lục

- [Code](#code)
- [Research & thu thập](#research--thu-thập)
- [Dữ liệu & phân tích](#dữ-liệu--phân-tích)
- [Viết & biên tập](#viết--biên-tập)
- [Ops & hạ tầng](#ops--hạ-tầng)
- [Multimodal](#multimodal)
- [Những bước hay bị chấm sai](#những-bước-hay-bị-chấm-sai)

## Code

| Bước | Điểm điển hình | Bậc | Ghi chú |
|---|---|---|---|
| Sinh boilerplate, CRUD, test đơn giản | A0 B1 C1 D0 = 2 | 1 | Spec đã rõ thì không cần model to |
| Viết một feature trong file có sẵn | A1 B1 C1 D1 = 4 | 2 | |
| Debug lỗi đã có stack trace | A1 B1 C1 D1 = 4 | 2 | Có bằng chứng thì việc thu hẹp không khó |
| Debug lỗi không tái hiện được | A2 B2 C1 D2 = 7 | 4 | Đây là loại việc Bậc 4 thật sự |
| Refactor xuyên nhiều module | A1 B2 C1 D2 = 6 | 3 | D=2 vì phải giữ bất biến toàn cục |
| Review kiến trúc, chọn hướng thiết kế | A2 B2 C1 D1 = 6 | 3 | Lên 4 nếu quyết định khó đảo ngược |
| Migration schema trên production | A1 B2 C2 D1 = 6 → ghi đè | 3+ | Luật 1: +1 nấc effort, kèm xác nhận |

Agentic coding — sửa nhiều file, chạy lệnh, lặp cho tới khi test xanh — là chỗ Anthropic mạnh nhất; DeepSeek V4 Pro là lựa chọn open-weight gần nhất. Nếu bước cần vừa code vừa phán đoán về giao diện thị giác, cân nhắc gpt-5.6.

Bẫy: sinh code trông đúng thì rẻ, nhưng **quyết định** kiến trúc sai thì mọi bước sau đắt lên. Chấm cao cho bước quyết định, chấm thấp cho bước gõ ra.

## Research & thu thập

| Bước | Điểm điển hình | Bậc |
|---|---|---|
| Tra một sự kiện, một con số | A0 B0 C0 D0 = 0 | 1 |
| Trích xuất có cấu trúc từ N nguồn độc lập | A0 B1 C1 D1 = 3 → luật bulk | 1 |
| Tổng hợp, đối chiếu mâu thuẫn giữa các nguồn | A1 B2 C1 D2 = 6 | 3 |
| Đánh giá phương pháp luận một nghiên cứu | A2 B2 C1 D1 = 6 | 3 |
| Vạch bản đồ một lĩnh vực chưa quen | A2 B2 C1 D2 = 7 | 4 |

Tách rõ hai pha: **thu thập** (rẻ, song song, Bậc 1) và **tổng hợp** (đắt, một lần, Bậc 3–4). Chạy cả hai pha trên cùng một model nặng là cách đốt tiền phổ biến nhất trong research.

Nếu C=2 vì người dùng sẽ trích con số cho người khác, đừng hạ bậc pha tổng hợp dù đã bulk pha thu thập.

## Dữ liệu & phân tích

| Bước | Điểm điển hình | Bậc |
|---|---|---|
| Làm sạch, đổi định dạng, join theo khóa rõ | A0 B1 C1 D1 = 3 | 2 |
| Thống kê mô tả, dựng biểu đồ | A0 B1 C1 D1 = 3 | 2 |
| Chọn mô hình, kiểm giả định | A2 B2 C1 D1 = 6 | 3 |
| Diễn giải kết quả cho quyết định kinh doanh | A1 B2 C2 D1 = 6 → ghi đè | 3+ |
| Chứng minh toán, dẫn xuất công thức | A1 B2 C1 D0 = 4 | 2–3 |

Với dẫn xuất toán, bậc phụ thuộc gần như hoàn toàn vào B. Một dẫn xuất 3 dòng không cần Opus; một chứng minh cần giữ bất biến qua 10 bước thì cần.

Bẫy: viết code phân tích thì rẻ, nhưng **đọc kết quả** rồi tuyên bố nhân quả là chỗ sai đắt nhất. Bước diễn giải luôn chấm C≥1.

## Viết & biên tập

| Bước | Điểm điển hình | Bậc |
|---|---|---|
| Sửa chính tả, đổi định dạng | A0 B0 C0 D0 = 0 | 1 |
| Rút gọn, đổi giọng văn theo yêu cầu rõ | A0 B1 C1 D1 = 3 | 2 |
| Viết bản nháp đầu từ dàn ý có sẵn | A1 B1 C1 D1 = 4 | 2 |
| Viết cho đối tượng nhạy cảm, gửi ra ngoài | A1 B1 C2 D1 = 5 → ghi đè | 3 |
| Tự dựng lập luận từ đầu | A2 B2 C1 D1 = 6 | 3 |

C=2 khi văn bản gửi ra ngoài tổ chức, hoặc mang tên người dùng. Trong trường hợp đó không hạ bậc, kể cả khi văn bản ngắn.

## Ops & hạ tầng

| Bước | Điểm điển hình | Bậc |
|---|---|---|
| Chạy lệnh đã biết, commit, đổi tên | A0 B0 C1 D0 = 1 | 1 (luật 5) |
| Viết CI config từ mẫu | A0 B1 C1 D0 = 2 | 1 |
| Chẩn đoán sự cố production đang diễn ra | A2 B2 C2 D2 = 8 | 4 |
| Kế hoạch rollback | A1 B2 C2 D1 = 6 → ghi đè | 3+ |

Ops là nơi luật 1 (không hoàn tác) và luật 5 (bước cơ học) va nhau nhiều nhất. Phân biệt: *quyết định chạy lệnh gì* có thể là Bậc 4; *gõ lệnh đó ra* luôn là Bậc 1.

## Multimodal

Ảnh, video, audio, PDF quét, ngữ cảnh cực dài mà cần rẻ → cột Google, gần như bất kể bậc. Cột Effort ghi `n/a (auto)`.

Ngoại lệ: nếu nội dung multimodal chỉ là đầu vào phụ còn phần nặng là suy luận trên text đã trích ra, thì tách hai bước — trích bằng Gemini Flash-Lite, suy luận bằng cột phù hợp với bậc.

## Những bước hay bị chấm sai

**Chấm quá cao:**

- Bước thi hành một quyết định vừa được cân nhắc kỹ ở bước trước — công việc khó đã xong rồi
- Bước lặp lại một khuôn mẫu đã làm đúng vài lần trong cùng phiên
- Bước "kiểm tra lại" thuần cơ học (chạy test, so diff, đếm dòng)

**Chấm quá thấp:**

- Bước đầu tiên của một task mơ hồ — chọn sai hướng ở đây thì mọi bước sau vô nghĩa, A gần như luôn =2
- Bước ra con số cuối cùng mà người dùng sẽ mang đi dùng ở nơi khác — C=2
- Bước gộp kết quả từ nhiều nguồn có mâu thuẫn — D=2, và thường B=2
- Bước quyết định "có nên làm việc này không" — dễ trông như câu hỏi nhỏ, thực ra là chỗ định đoạt cả task

Khi phân vân giữa hai bậc liền kề: nếu C=2 chọn bậc cao, còn lại chọn bậc thấp và ghi rõ ở dòng "Dự phòng" điều kiện nào sẽ khiến phải nâng lên. Đề xuất thấp mà có đường leo thang rõ ràng thì rẻ hơn đề xuất cao phòng hờ.
