# Phase 3 Notes

## 1. Architecture overview

- `system_prompt.txt`
  Dùng để định nghĩa vai trò, rules, cách dùng tool và guardrails cho TravelBuddy. Prompt được đọc từ file local thay vì hard-code trong Python.
- `tools.py`
  Cung cấp 3 tool nghiệp vụ: tìm chuyến bay, tìm khách sạn, tính ngân sách.
- `agent_node`
  Là node gọi model DeepSeek đã bind tools. Node này quyết định model sẽ trả lời trực tiếp hay tạo tool call.
- `ToolNode`
  Thực thi tool call mà model yêu cầu, rồi đưa kết quả quay lại graph dưới dạng message.
- `tools_condition`
  Dùng để route sau node `agent`: nếu model có tool call thì sang `tools`, nếu không thì kết thúc.

## 2. Vì sao phase này dùng native tool calling thay vì parse text kiểu `Action: ...`

Native tool calling phù hợp hơn với LangChain/LangGraph hiện đại vì model trả về structured tool calls trực tiếp. Cách này giảm lỗi parser, không cần regex mong manh, và bám đúng mục tiêu phase 3 là để model tự quyết định khi nào gọi tool trong một agent loop chuẩn.

## 3. Flow thực thi ví dụ cụ thể

User:
`Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`

Luồng có thể diễn ra như sau:
- `agent_node` gửi lịch sử hội thoại kèm system prompt vào model
- model quyết định gọi `search_flights` để lấy phương án bay Hà Nội -> Phú Quốc
- sau khi có kết quả, model có thể gọi `calculate_budget` để tính phần ngân sách còn lại
- tiếp theo model có thể gọi `search_hotels` với mức giá/đêm phù hợp với phần ngân sách còn lại
- khi đã đủ dữ liệu, model viết câu trả lời cuối có cấu trúc cho người dùng

## 4. Những điểm trong implementation hỗ trợ rubric

- Setup LangGraph đúng flow `START -> agent -> tools -> agent -> END`
- Có logging rõ model đang gọi tool nào và args gì
- Hỗ trợ multi-step tool chaining tự nhiên qua `ToolNode`
- Code giữ gọn, có type hints, có helper nhỏ để đọc prompt, tạo model và lấy câu trả lời cuối

## 5. Quick self-check

1. Điền `DEEPSEEK_API_KEY` vào file `.env`
2. Chạy `python agent.py`
3. Nhập một câu chào chung như `Xin chào`
4. Nhập câu tìm vé như `Tìm chuyến bay từ Hà Nội đi Đà Nẵng`
5. Nhập câu multi-step như `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`
6. Nhập câu thiếu dữ liệu như `Tôi muốn đặt khách sạn`
7. Nhập yêu cầu ngoài phạm vi như `Giải giúp tôi bài Python`
8. Gõ `quit` để thoát
