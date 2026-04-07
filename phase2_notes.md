# Phase 2 Notes

## 1. Tools đã dùng mock database như thế nào

`tools.py` dùng 2 mock database nội bộ:
- `FLIGHTS_DB`: tra cứu chuyến bay theo cặp `(origin, destination)`
- `HOTELS_DB`: tra cứu khách sạn theo `city`

Trong workspace hiện tại chưa có template DB sẵn, nên file `tools.py` tự khai báo một mock database nhỏ để các tool chạy được đúng tinh thần lab. Không có API thật, không có truy cập mạng.

## 2. Vì sao không dùng external API trong lab này

Mục tiêu của phase này là học cách thiết kế tool cho agent và kiểm soát logic lookup/filter/format. Dùng external API sẽ làm tăng độ phức tạp, phụ thuộc mạng, khó tái lập kết quả và đi lệch mục tiêu học thuật của lab.

## 3. Logic chính của từng tool

### `search_flights(origin, destination)`

- Làm sạch input bằng cách strip khoảng trắng
- Kiểm tra lỗi cơ bản: thiếu điểm đi, thiếu điểm đến, trùng điểm đi và điểm đến
- Lookup theo chiều thuận trong `FLIGHTS_DB`
- Nếu không có, thử lookup chiều ngược lại
- Trả kết quả dạng chuỗi tiếng Việt, dễ đọc, có format tiền đẹp

### `search_hotels(city, max_price_per_night)`

- Làm sạch tên thành phố
- Kiểm tra input hợp lệ
- Lookup khách sạn theo thành phố trong `HOTELS_DB`
- Lọc theo giá `<= max_price_per_night`
- Sort theo `rating` giảm dần, nếu bằng nhau thì giá tăng dần
- Trả kết quả có cấu trúc, sẵn sàng cho agent tóm tắt tiếp

### `calculate_budget(total_budget, expenses)`

- Kiểm tra `total_budget` hợp lệ
- Parse chuỗi `expenses` theo format `ten_khoan:sotien`
- Báo lỗi rõ nếu có item sai định dạng
- Tính tổng chi, ngân sách còn lại hoặc phần vượt ngân sách
- Trả về báo cáo chi phí bằng tiếng Việt, format tiền Việt Nam rõ ràng

## 4. Các trường hợp lỗi đã được xử lý

- Input rỗng hoặc chỉ có khoảng trắng
- Điểm đi trùng điểm đến
- Thành phố rỗng
- Ngân sách hoặc giá tối đa mỗi đêm không hợp lệ
- Không có dữ liệu trong mock DB
- Có dữ liệu nhưng không có kết quả phù hợp ngân sách
- `expenses` rỗng
- Khoản chi sai định dạng
- Tên khoản chi rỗng
- Số tiền không parse được
- Số tiền âm

## 5. 3 tools liên kết với nhau ra sao trong bài toán du lịch

Flow gợi ý:
- Dùng `search_flights` để tìm phương án bay và lấy chi phí bay tham chiếu
- Dùng `calculate_budget` để trừ chi phí chuyến bay và các khoản đã biết khỏi tổng ngân sách
- Dùng phần ngân sách còn lại để gọi `search_hotels` với mức `max_price_per_night` phù hợp

Chuỗi này giúp agent phase sau có thể tư vấn một chuyến đi trọn gói theo ngân sách thay vì trả lời từng phần rời rạc.

## 6. Ví dụ input/output ngắn cho mỗi tool

| Tool | Input ví dụ | Output kỳ vọng ngắn |
|---|---|---|
| `search_flights` | `("Hà Nội", "Đà Nẵng")` | Danh sách chuyến bay cho tuyến Hà Nội -> Đà Nẵng |
| `search_flights` | `("", "Đà Nẵng")` | Báo lỗi thiếu điểm đi |
| `search_hotels` | `("Phú Quốc", 800000)` | Danh sách khách sạn tại Phú Quốc trong ngân sách |
| `search_hotels` | `("Phú Quốc", 100000)` | Báo không có khách sạn trong mức giá này |
| `calculate_budget` | `(5000000, "vé_máy_bay:1100000,khách_sạn:1600000")` | Tổng chi 2.700.000đ, còn lại 2.300.000đ |
| `calculate_budget` | `(5000000, "vé_máy_bay-1100000")` | Báo lỗi sai định dạng khoản chi |
