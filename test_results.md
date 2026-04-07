# Test Results

## Test 1 — Direct Answer (Không cần tool)

**Input**  
`Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`

**Console log / tool log quan sát được**  
```text
Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
[agent] Model trả lời trực tiếp, không gọi tool.
TravelBuddy: Chào bạn! Rất vui được giúp bạn chọn điểm đến cho chuyến du lịch sắp tới.

Để mình gợi ý cho bạn một số điểm đến phổ biến ở Việt Nam, bạn có thể cân nhắc:

**1. Đà Nẵng - Hội An** (phù hợp cho mọi đối tượng)
- Ưu điểm: Biển đẹp, ẩm thực phong phú, phố cổ Hội An lãng mạn
- Thời gian lý tưởng: 3-4 ngày
- Hoạt động: Tắm biển, khám phá phố cổ, thưởng thức ẩm thực

**2. Phú Quốc** (cho ai thích biển đảo)
- Ưu điểm: Biển trong xanh, resort đẹp, hoàng hôn tuyệt đẹp
- Thời gian lý tưởng: 3-5 ngày
- Hoạt động: Lặn biển, tham quan vườn tiêu, thưởng thức hải sản

**3. Sapa - Lào Cai** (cho ai thích núi rừng)
- Ưu điểm: Khí hậu mát mẻ, cảnh quan núi non hùng vĩ, văn hóa dân tộc
- Thời gian lý tưởng: 2-3 ngày
- Hoạt động: Trekking, khám phá bản làng, chợ phiên

**4. Nha Trang** (cho chuyến đi biển sôi động)
- Ưu điểm: Biển đẹp, nhiều hoạt động giải trí, ẩm thực đa dạng
- Thời gian lý tưởng: 3-4 ngày
- Hoạt động: Tắm biển, vinpearl, tham quan đảo

**Để mình tư vấn chính xác hơn, bạn có thể chia sẻ thêm:**
1. **Ngân sách** bạn dự định cho chuyến đi là bao nhiêu?
2. **Thời gian** bạn có thể đi được bao lâu?
3. **Sở thích** của bạn là gì? (biển, núi, thành phố, văn hóa...)
4. **Số người đi** cùng bạn?

Với những thông tin này, mình sẽ giúp bạn chọn điểm đến phù hợp nhất và lên kế hoạch chi tiết!
```

## Test 2 — Single Tool Call

**Input**  
`Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`

**Console log / tool log quan sát được**  
```text
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
[agent] Model yêu cầu gọi tool:
  - search_flights: {'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}
[agent] Model trả lời trực tiếp, không gọi tool.
TravelBuddy: Đây là các chuyến bay từ Hà Nội đi Đà Nẵng hiện có:

**Các lựa chọn chuyến bay:**

1. **VietJet Air** | 08:30 -> 09:50 | **890.000đ** (hạng economy)
   - *Ưu điểm:* Giá rẻ nhất, thời gian bay hợp lý (sáng muộn)

2. **Bamboo Airways** | 11:00 -> 12:20 | **1.200.000đ** (hạng economy)
   - *Ưu điểm:* Giá trung bình, thời gian bay thoải mái (trưa)

3. **Vietnam Airlines** | 06:00 -> 07:20 | **1.450.000đ** (hạng economy)
   - *Ưu điểm:* Hãng bay quốc gia, bay sớm đến sớm

4. **Vietnam Airlines** | 14:00 -> 15:20 | **2.800.000đ** (hạng business)
   - *Ưu điểm:* Hạng vé cao cấp, thời gian bay chiều

**Đề xuất của mình:**
- **Nếu muốn tiết kiệm:** Chọn VietJet Air (890k) - giá tốt nhất
- **Nếu muốn thoải mái hơn:** Chọn Bamboo Airways (1.2 triệu) - bay giờ trưa dễ chịu
- **Nếu ưu tiên hãng bay:** Chọn Vietnam Airlines economy (1.45 triệu)

**Để mình tư vấn chi tiết hơn, bạn có thể cho biết:**
1. **Ngân sách** cho vé máy bay là bao nhiêu?
2. **Thời gian bay** bạn thích (sáng/trưa/chiều)?
3. **Chuyến đi này** bạn đi bao nhiêu ngày? Đi một mình hay cùng ai?

Với thông tin này, mình sẽ giúp bạn chọn chuyến bay phù hợp nhất và có thể hỗ trợ thêm về khách sạn nếu cần!
Ví dụ mong đợi:
[agent] Model yêu cầu gọi tool:
  - search_flights: {'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}
```
---

## Test 3 — Multi-Step Tool Chaining

**Input**  
`Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`

**Console log / tool log quan sát được**  
```text
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
[agent] Model yêu cầu gọi tool:
  - search_flights: {'origin': 'Hà Nội', 'destination': 'Phú Quốc'}
[agent] Model yêu cầu gọi tool:
  - calculate_budget: {'total_budget': 5000000, 'expenses': 'vé_máy_bay_khứ_hồi:2200000'}
[agent] Model yêu cầu gọi tool:
  - search_hotels: {'city': 'Phú Quốc', 'max_price_per_night': 750000}
[agent] Model trả lời trực tiếp, không gọi tool.
TravelBuddy: **KẾ HOẠCH CHUYẾN ĐI ĐỀ XUẤT:**

**Chuyến bay đề xuất:**
- **Chiều đi:** VietJet Air | 16:00 -> 18:15 | **1.100.000đ**
- **Chiều về:** Giả sử giá tương tự 1.100.000đ
- **Tổng vé máy bay:** **2.200.000đ**
- *Lý do chọn:* Giá tốt, bay chiều thuận tiện

**Khách sạn đề xuất:**
- **9Station Hostel** | 2 sao | **200.000đ/đêm** | Dương Đông | Rating: 4.5
- **Tổng 2 đêm:** **400.000đ**
- *Lý do chọn:* Giá cực kỳ hợp lý, rating cao (4.5), vị trí Dương Đông thuận tiện

**Bảng chi phí ước tính:**
1. Vé máy bay khứ hồi: **2.200.000đ**
2. Khách sạn 2 đêm: **400.000đ**
3. Ăn uống (3 ngày): ước tính **1.200.000đ** (400k/ngày)
4. Di chuyển tại Phú Quốc: ước tính **500.000đ** (thuê xe máy/grab)
5. Vé tham quan/giải trí: **500.000đ** (bãi Sao, Vinpearl Safari, etc.)
6. Chi phí phát sinh: **200.000đ**

**Tổng chi phí ước tính: 5.000.000đ**

**Ngân sách còn lại: 0đ** (vừa đủ ngân sách)

**Gợi ý thêm:**
1. **Nếu muốn nâng cấp chỗ ở:** Có thể tăng ngân sách khách sạn lên 1-1.5 triệu cho 2 đêm, nhưng cần cắt giảm chi phí ăn uống hoặc giải trí
2. **Tiết kiệm hơn:** Ăn uống tiết kiệm hơn (250-300k/ngày) để dư ngân sách
3. **Di chuyển:** Thuê xe máy khoảng 150k/ngày sẽ tiết kiệm hơn taxi
4. **Đặt vé sớm:** Đặt vé máy bay sớm hơn có thể tìm được giá tốt hơn

**Lưu ý quan trọng:** Với ngân sách 5 triệu cho Phú Quốc 2 đêm, bạn cần chi tiêu khá tiết kiệm. Phú Quốc là điểm du lịch cao cấp nên chi phí thường cao hơn các điểm đến khác.

Bạn thấy kế hoạch này thế nào? Có cần điều chỉnh gì không?
Ví dụ mong đợi:
[agent] Model yêu cầu gọi tool:
  - search_flights: {'origin': 'Hà Nội', 'destination': 'Phú Quốc'}
[agent] Model yêu cầu gọi tool:
  - calculate_budget: {...}
[agent] Model yêu cầu gọi tool:
  - search_hotels: {'city': 'Phú Quốc', 'max_price_per_night': ...}
```

---

## Test 4 — Missing Info / Clarification

**Input**  
`Tôi muốn đặt khách sạn`

**Console log / tool log quan sát được**  
```text
Bạn: Tôi muốn đặt khách sạn
[agent] Model trả lời trực tiếp, không gọi tool.
TravelBuddy: Chào bạn! Mình rất vui được hỗ trợ bạn tìm khách sạn.

Để mình tìm khách sạn phù hợp nhất cho bạn, bạn có thể cho mình biết thêm một số thông tin quan trọng nhé:

1. **Thành phố nào** bạn muốn đặt khách sạn? (VD: Hà Nội, Đà Nẵng, Hồ Chí Minh, Phú Quốc, Nha Trang...)
2. **Mức giá tối đa** bạn muốn chi cho mỗi đêm là bao nhiêu? (VNĐ)
3. **Số đêm** bạn cần ở là bao nhiêu?
4. **Số người** sẽ ở? (để mình biết cần phòng đơn hay đôi)

Với những thông tin này, mình sẽ tìm kiếm và đề xuất cho bạn những khách sạn phù hợp nhất với nhu cầu và ngân sách của bạn!
Ví dụ mong đợi:
[agent] Model trả lời trực tiếp, không gọi tool.
```
---

## Test 5 — Guardrail / Refusal

**Input**  
`Giải giúp tôi bài tập lập trình Python về linked list`

**Console log / tool log quan sát được**  
```text
Bạn: Giải giúp tôi bài tập lập trình Python về linked list
[agent] Model trả lời trực tiếp, không gọi tool.
TravelBuddy: Xin lỗi bạn, mình là TravelBuddy - trợ lý du lịch chuyên về tư vấn vé máy bay, khách sạn và lên kế hoạch chuyến đi.

Mình chỉ có thể hỗ trợ bạn trong phạm vi:
- Tìm kiếm chuyến bay giữa các thành phố
- Tìm kiếm khách sạn theo ngân sách
- Tính toán ngân sách cho chuyến đi
- Tư vấn lên kế hoạch du lịch

Rất tiếc mình không thể giúp bạn giải bài tập lập trình Python về linked list. Bạn có thể tham khảo các nguồn học lập trình trực tuyến hoặc hỏi các diễn đàn chuyên về lập trình nhé!

Nếu bạn có bất kỳ câu hỏi nào về du lịch, vé máy bay, khách sạn hoặc cần lên kế hoạch cho một chuyến đi sắp tới, mình rất sẵn lòng hỗ trợ bạn!
Ví dụ mong đợi:
[agent] Model trả lời trực tiếp, không gọi tool.
```