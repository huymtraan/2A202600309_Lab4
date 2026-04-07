from typing import Any, Union

from langchain_core.tools import tool

FLIGHTS_DB: dict[tuple[str, str], list[dict[str, Any]]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB: dict[str, list[dict[str, Any]]] = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


def _clean_text(value: str) -> str:
    """Normalize user-provided text for stable lookups."""
    return " ".join(value.strip().split())


def _normalize_place(value: str) -> str:
    """Normalize a place name while preserving Vietnamese accents."""
    cleaned = _clean_text(value)
    return cleaned.title() if cleaned else ""


def _format_vnd(amount: Union[int, float]) -> str:
    """Format a number as Vietnamese Dong."""
    rounded = int(round(float(amount)))
    return f"{rounded:,}".replace(",", ".") + "đ"


def _parse_budget_number(value: Union[int, float]) -> int:
    """Safely convert numeric budget inputs to integer VND."""
    amount = float(value)
    if amount <= 0:
        raise ValueError("Giá trị phải lớn hơn 0.")
    return int(round(amount))


def _parse_expenses(expenses: str) -> list[tuple[str, int]]:
    """Parse expense items in the format ten_khoan:sotien."""
    cleaned = _clean_text(expenses)
    if not cleaned:
        raise ValueError("Danh sách khoản chi không được để trống.")

    parsed_items: list[tuple[str, int]] = []
    for raw_item in cleaned.split(","):
        item = raw_item.strip()
        if not item:
            raise ValueError("Có khoản chi rỗng trong danh sách expenses.")
        if item.count(":") != 1:
            raise ValueError(
                f"Khoản chi '{item}' không đúng định dạng. Hãy dùng ten_khoan:sotien."
            )

        name, amount_text = [part.strip() for part in item.split(":", maxsplit=1)]
        if not name:
            raise ValueError(f"Khoản chi '{item}' đang thiếu tên khoản chi.")
        if not amount_text:
            raise ValueError(f"Khoản chi '{item}' đang thiếu số tiền.")

        try:
            amount_value = float(amount_text)
        except ValueError as exc:
            raise ValueError(
                f"Số tiền trong khoản chi '{item}' không hợp lệ."
            ) from exc

        if amount_value < 0:
            raise ValueError(f"Số tiền trong khoản chi '{item}' không được âm.")

        parsed_items.append((name, int(round(amount_value))))

    return parsed_items


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.

    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy chuyến bay, trả về thông báo không có chuyến.
    """
    clean_origin = _normalize_place(origin)
    clean_destination = _normalize_place(destination)

    if not clean_origin:
        return "Lỗi: bạn chưa cung cấp điểm đi."
    if not clean_destination:
        return "Lỗi: bạn chưa cung cấp điểm đến."
    if clean_origin == clean_destination:
        return "Lỗi: điểm đi và điểm đến không hợp lệ vì đang trùng nhau."

    route = (clean_origin, clean_destination)
    reverse_route = (clean_destination, clean_origin)

    flights = FLIGHTS_DB.get(route)
    reverse_lookup = False

    if flights is None:
        flights = FLIGHTS_DB.get(reverse_route)
        reverse_lookup = flights is not None

    if not flights:
        return (
            f"Không tìm thấy chuyến bay phù hợp giữa {clean_origin} và "
            f"{clean_destination} trong mock database."
        )

    lines = [
        f"Kết quả chuyến bay cho tuyến {clean_origin} -> {clean_destination}:"
    ]
    if reverse_lookup:
        lines.append(
            "Lưu ý: không có dữ liệu chiều thuận, dưới đây là kết quả tra theo chiều ngược lại."
        )

    for index, flight in enumerate(flights, start=1):
        lines.append(
            f"{index}. {flight['airline']} | "
            f"{flight['departure']} -> {flight['arrival']} | "
            f"{_format_vnd(flight['price'])} | "
            f"Hạng vé: {flight['class']}"
        )

    return "\n".join(lines)


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    clean_city = _normalize_place(city)

    if not clean_city:
        return "Lỗi: bạn chưa cung cấp thành phố hoặc điểm đến cần tìm khách sạn."

    try:
        max_price = _parse_budget_number(max_price_per_night)
    except (TypeError, ValueError):
        return "Lỗi: max_price_per_night phải là một số lớn hơn 0."

    hotels = HOTELS_DB.get(clean_city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn cho {clean_city} trong mock database."

    filtered_hotels = [
        hotel for hotel in hotels if int(hotel["price_per_night"]) <= max_price
    ]

    if not filtered_hotels:
        return (
            f"Không có khách sạn nào tại {clean_city} trong mức "
            f"{_format_vnd(max_price)}/đêm. Bạn có thể thử tăng ngân sách."
        )

    sorted_hotels = sorted(
        filtered_hotels,
        key=lambda hotel: (-float(hotel["rating"]), int(hotel["price_per_night"])),
    )

    lines = [
        f"Khách sạn tại {clean_city} với ngân sách tối đa {_format_vnd(max_price)}/đêm:"
    ]
    for index, hotel in enumerate(sorted_hotels, start=1):
        lines.append(
            f"{index}. {hotel['name']} | "
            f"{hotel['stars']} sao | "
            f"{_format_vnd(hotel['price_per_night'])}/đêm | "
            f"Khu vực: {hotel['area']} | "
            f"Rating: {hotel['rating']}"
        )

    return "\n".join(lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')

    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        budget = _parse_budget_number(total_budget)
    except (TypeError, ValueError):
        return "Lỗi: total_budget phải là một số lớn hơn 0."

    try:
        parsed_expenses = _parse_expenses(expenses)
    except ValueError as exc:
        return f"Lỗi: {exc}"

    total_expense = sum(amount for _, amount in parsed_expenses)
    remaining = budget - total_expense

    lines = ["Báo cáo ngân sách chuyến đi:"]
    lines.append(f"Tổng ngân sách: {_format_vnd(budget)}")
    lines.append("Danh sách khoản chi:")
    for index, (name, amount) in enumerate(parsed_expenses, start=1):
        display_name = name.replace("_", " ")
        lines.append(f"{index}. {display_name}: {_format_vnd(amount)}")
    lines.append(f"Tổng chi: {_format_vnd(total_expense)}")

    if remaining >= 0:
        lines.append(f"Còn lại: {_format_vnd(remaining)}")
    else:
        lines.append(f"Vượt ngân sách: {_format_vnd(abs(remaining))}")

    return "\n".join(lines)
