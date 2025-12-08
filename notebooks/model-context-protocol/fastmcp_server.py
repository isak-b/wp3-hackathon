from fastmcp import FastMCP

mcp = FastMCP("Demo Server")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two integers."""
    return a * b


@mcp.resource("config://version")
def get_version() -> str:
    """App version."""
    return "1.0.0"


@mcp.resource("data://some_table")
def some_table() -> list[dict]:
    """Some data table."""
    return [
        {"foo": 1, "bar": 10},
        {"foo": 2, "bar": 11},
        {"foo": 3, "bar": 12},
        {"foo": 4, "bar": 13},
        {"foo": 5, "bar": 14},
    ]


@mcp.prompt
def system_prompt(extra_instructions: str | None = None):
    """A basic system prompt. Add extra instructions if you want."""
    prompt = "Du är en hjälpsam assistent. "

    if extra_instructions:
        prompt += extra_instructions

    return prompt


mcp_server = mcp.http_app()
