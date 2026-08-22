# skill

Bộ sưu tập Claude skills.

## Danh sách

| Skill | Mô tả |
|---|---|
| [model-router](./model-router/) | Cuối mỗi bước đề xuất model + effort level phù hợp dựa trên ma trận chấm điểm (Claude / OpenAI / Gemini / open-weight) |
| [skill-limit-recovery](./skill-limit-recovery/) | Xử lý các tình huống giới hạn: context window, session limit, weekly quota, provider overload, unsafe interruption |

## Cài skill

Từng skill là một thư mục độc lập. Cài bằng cách copy thư mục vào `~/.claude/skills/`, ví dụ:

```bash
cp -r model-router ~/.claude/skills/
cp -r skill-limit-recovery ~/.claude/skills/
```

Hoặc dùng file `.skill` (zip) nếu có.
