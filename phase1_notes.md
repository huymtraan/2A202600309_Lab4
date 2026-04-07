# Phase 1 Notes

## Vì sao cần rule hỏi lại khi thiếu thông tin

Agent du lịch rất dễ gặp các yêu cầu thiếu dữ liệu cốt lõi như điểm đi, điểm đến, số đêm hoặc ngân sách. Nếu không hỏi lại, agent sẽ phải đoán và dẫn đến tư vấn lệch nhu cầu hoặc gọi tool sai. Rule này giúp agent chỉ hỏi đúng phần còn thiếu, tránh vừa trả lời lan man vừa giảm lỗi ở bước tool calling sau này.

## Vì sao cần rule không bịa dữ liệu

Ở bài toán du lịch, bịa chuyến bay, khách sạn, giá tiền hoặc ngân sách còn lại sẽ làm mất độ tin cậy ngay lập tức. Vì phase sau dùng tool để lấy dữ liệu, prompt cần buộc model tách rõ đâu là thông tin từ tool và đâu là phần diễn giải. Guardrail này cũng giúp model vượt tốt các test về tính trung thực và hạn chế hallucination.

## Vì sao cần nhấn mạnh budget-awareness

Người dùng du lịch thường không chỉ cần lựa chọn tốt, mà cần lựa chọn phù hợp túi tiền. Nếu prompt không nhấn mạnh budget-awareness, model có xu hướng liệt kê nhiều phương án nhưng không ưu tiên phương án khả thi nhất. Rule này giúp agent chọn phương án hợp lý trước, tính ngân sách còn lại và tư vấn theo hướng thực tế hơn.

## Vì sao cần guardrail từ chối ngoài phạm vi

TravelBuddy chỉ nên đóng vai trò trợ lý du lịch. Nếu không có guardrail rõ, model rất dễ trôi sang các yêu cầu ngoài phạm vi như code, bài tập, tài chính hay chính trị. Việc từ chối lịch sự nhưng dứt khoát giúp giữ đúng vai trò agent, giảm prompt drift và làm hành vi ổn định hơn khi chấm test.

## Vì sao cần format trả lời có cấu trúc

Kết quả du lịch thường có nhiều phần: chuyến bay, khách sạn, chi phí và gợi ý thêm. Nếu không định hình cách trình bày, model có thể trả lời thiếu ý hoặc sắp xếp lộn xộn. Format có cấu trúc giúp câu trả lời dễ đọc hơn cho người dùng, đồng thời giúp model có xu hướng tổng hợp dữ liệu tool rõ ràng thay vì sao chép rời rạc.

## Vì sao phần tools_instruction phải mô tả mối liên hệ giữa các tool

Ba tool trong lab không hoạt động độc lập hoàn toàn. Một bài toán tư vấn chuyến đi hoàn chỉnh thường phải tìm chuyến bay trước, dùng chi phí đó để tính ngân sách còn lại, rồi mới lọc khách sạn phù hợp. Nếu không mô tả luồng liên kết này ngay trong system prompt, model dễ gọi tool rời rạc hoặc sai thứ tự, làm giảm chất lượng multi-step tool chaining ở phase sau.

## Expected behavior on test cases

### 1. “Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.”

Agent nên trả lời trực tiếp bằng tiếng Việt, chưa gọi tool. Nên gợi ý một vài hướng chọn điểm đến dựa trên sở thích, ngân sách hoặc thời gian, sau đó hỏi ngắn gọn một câu để làm rõ như muốn đi biển, núi hay thành phố.

### 2. “Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng”

Agent đã có đủ `origin` và `destination`, nên có thể gọi `search_flights(Hà Nội, Đà Nẵng)`. Sau khi có kết quả, agent cần tóm tắt ngắn gọn, chọn phương án hợp lý nhất thay vì đổ toàn bộ dữ liệu thô ra màn hình.

### 3. “Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!”

Đây là bài toán multi-step. Agent nên hiểu đây là yêu cầu tư vấn chuyến đi hoàn chỉnh. Nếu còn thiếu dữ liệu tối quan trọng như số người hoặc có cần máy bay không thì hỏi thêm ngắn gọn; nếu hệ thống/đề bài cho phép mặc định bài toán một người đi máy bay thì agent có thể gọi chuỗi tool theo flow: tìm chuyến bay, tính ngân sách còn lại, lọc khách sạn theo phần ngân sách đó, rồi tổng hợp thành phương án đề xuất.

### 4. “Tôi muốn đặt khách sạn”

Agent không nên vội gọi tool vì thiếu thông tin tối thiểu. Cần hỏi ngắn gọn thành phố muốn ở và mức giá mỗi đêm hoặc ngân sách lưu trú. Agent cũng không được tuyên bố đã đặt phòng thật, mà chỉ nên nói có thể hỗ trợ tìm phương án khách sạn phù hợp.

### 5. “Giải giúp tôi bài tập lập trình Python về linked list”

Agent phải từ chối lịch sự vì đây là yêu cầu ngoài phạm vi du lịch. Câu trả lời nên ngắn gọn, nhắc lại rằng TravelBuddy chỉ hỗ trợ du lịch, vé máy bay, khách sạn và ngân sách chuyến đi.
