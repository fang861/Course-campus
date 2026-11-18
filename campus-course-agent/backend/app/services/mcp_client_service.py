import json
from app.common.exceptions import BusinessException
from app.config import settings
from langchain_mcp_adapters.client import MultiServerMCPClient


async def call_get_my_schedules(authorization: str, date: str | None = None) -> dict:
    client = MultiServerMCPClient(
        {
            "campus": {
                "transport": "streamable_http",
                "url": f"http://{settings.MCP_HOST}:{settings.MCP_PORT}{settings.MCP_PATH}",
                "headers": {"Authorization": authorization},
            }
        }
    )
    tools = await client.get_tools(server_name="campus")
    tool = next((t for t in tools if t.name == "get_my_schedules"), None)
    if tool is None:
        raise BusinessException(message="")
    payload = {}
    if date:
        payload["date"] = date
    result = await tool.ainvoke(payload)

    return json.loads(result[0]["text"])
