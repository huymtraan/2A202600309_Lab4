import os
from typing import Annotated, Any, Optional

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from tools import calculate_budget, search_flights, search_hotels


class AgentState(TypedDict):
    messages: Annotated[list[Any], add_messages]


TOOLS_LIST = [search_flights, search_hotels, calculate_budget]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "system_prompt.txt")
SYSTEM_PROMPT = ""
llm: Optional[ChatOpenAI] = None
llm_with_tools: Any = None
graph: Any = None
INIT_ERROR: Optional[str] = None


def _load_system_prompt(path: str = SYSTEM_PROMPT_PATH) -> str:
    """Load the system prompt from a local text file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file prompt: {path}")

    with open(path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()

    if not prompt:
        raise ValueError(f"File prompt đang rỗng: {path}")

    return prompt


def _create_llm() -> ChatOpenAI:
    """Create the DeepSeek chat model via the OpenAI-compatible interface."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError(
            "Thiếu DEEPSEEK_API_KEY. Hãy thêm DEEPSEEK_API_KEY vào file .env."
        )

    return ChatOpenAI(
        model="deepseek-chat",
        api_key=api_key,
        base_url="https://api.deepseek.com",
        temperature=0,
    )


def _ensure_initialized() -> None:
    """Raise a practical error if the agent failed to initialize."""
    if INIT_ERROR:
        raise RuntimeError(INIT_ERROR)
    if graph is None or llm_with_tools is None or not SYSTEM_PROMPT:
        raise RuntimeError("Agent chưa được khởi tạo đúng cách.")


def _get_messages_with_system_prompt(messages: list[BaseMessage]) -> list[BaseMessage]:
    """Prepend the system prompt only once."""
    has_system_message = any(isinstance(message, SystemMessage) for message in messages)
    if has_system_message:
        return messages
    return [SystemMessage(content=SYSTEM_PROMPT), *messages]


def _get_final_ai_text(messages: list[BaseMessage]) -> str:
    """Extract the latest AI text message for CLI output."""
    for message in reversed(messages):
        if isinstance(message, AIMessage) and message.content:
            if isinstance(message.content, str):
                return message.content
            if isinstance(message.content, list):
                parts = [
                    item.get("text", "")
                    for item in message.content
                    if isinstance(item, dict) and item.get("type") == "text"
                ]
                if parts:
                    return "\n".join(part for part in parts if part)
    return "TravelBuddy chưa tạo được câu trả lời cuối."


def agent_node(state: AgentState) -> dict[str, list[BaseMessage]]:
    """Call the model with native tool calling and log its decision."""
    _ensure_initialized()

    messages = state["messages"]
    prepared_messages = _get_messages_with_system_prompt(messages)

    try:
        response = llm_with_tools.invoke(prepared_messages)
    except Exception as exc:
        raise RuntimeError(f"Lỗi khi gọi model DeepSeek: {exc}") from exc

    tool_calls = getattr(response, "tool_calls", None) or []
    if tool_calls:
        print("[agent] Model yêu cầu gọi tool:")
        for tool_call in tool_calls:
            print(f"  - {tool_call.get('name')}: {tool_call.get('args')}")
    else:
        print("[agent] Model trả lời trực tiếp, không gọi tool.")

    return {"messages": [response]}


def _build_graph() -> Any:
    """Create and compile the LangGraph workflow."""
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(TOOLS_LIST))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    builder.add_edge("tools", "agent")
    return builder.compile()


def _initialize_agent() -> None:
    """Initialize prompt, model, bound tools, and compiled graph."""
    global SYSTEM_PROMPT, llm, llm_with_tools, graph, INIT_ERROR

    load_dotenv()

    try:
        SYSTEM_PROMPT = _load_system_prompt()
        llm = _create_llm()
        llm_with_tools = llm.bind_tools(TOOLS_LIST)
        graph = _build_graph()
        INIT_ERROR = None
    except Exception as exc:
        graph = None
        llm = None
        llm_with_tools = None
        INIT_ERROR = str(exc)


_initialize_agent()


if __name__ == "__main__":
    print("TravelBuddy CLI")
    print("Gõ 'quit', 'exit' hoặc 'q' để thoát.")

    if INIT_ERROR:
        print(f"Lỗi khởi tạo agent: {INIT_ERROR}")
    else:
        print("Agent đã sẵn sàng.")

    conversation_messages: list[BaseMessage] = []

    while True:
        try:
            user_input = input("\nBạn: ").strip()
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            break
        except EOFError:
            print("\nTạm biệt!")
            break

        if not user_input:
            print("Vui lòng nhập nội dung câu hỏi.")
            continue

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Tạm biệt!")
            break

        if INIT_ERROR:
            print(f"Không thể chạy agent: {INIT_ERROR}")
            continue

        try:
            result = graph.invoke(
                {"messages": [*conversation_messages, HumanMessage(content=user_input)]}
            )
            conversation_messages = result["messages"]
            print(f"TravelBuddy: {_get_final_ai_text(conversation_messages)}")
        except Exception as exc:
            print(f"Lỗi khi chạy agent: {exc}")
