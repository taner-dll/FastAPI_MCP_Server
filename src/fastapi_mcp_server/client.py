import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main() -> None:
    url = "http://127.0.0.1:8000/mcp/"

    async with streamable_http_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [tool.name for tool in tools.tools])

            result = await session.call_tool(
                "add",
                {"x": 5, "y": 3},
            )
            print("Result:", result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())

