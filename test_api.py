import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Lỗi: Không tìm thấy biến môi trường DEEPSEEK_API_KEY.")
        print("Hãy tạo file .env với nội dung: DEEPSEEK_API_KEY=your_key_here")
        sys.exit(1)

    prompt = "Xin chào, hãy trả lời ngắn gọn bằng tiếng Việt."

    try:
        llm = ChatOpenAI(
            model="deepseek-chat",
            api_key=api_key,
            base_url="https://api.deepseek.com",
            temperature=0,
        )
        response = llm.invoke(prompt)
        print("--- Kết quả ---")
        print(response.content)
    except Exception as error:
        print("Lỗi khi gọi model DeepSeek:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
