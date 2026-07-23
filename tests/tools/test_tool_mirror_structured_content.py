"""Tests for the mirror_structured_content flag on structured tools.

A tool with an output schema returns its value as structured_content and, by
default, also serialises it into a content text block (the spec's SHOULD). Set
``mirror_structured_content=False`` to send structured_content only, without the
duplicate serialised copy on the wire.
"""

from __future__ import annotations

from pydantic import BaseModel

from fastmcp import FastMCP


class Weather(BaseModel):
    temperature: float
    conditions: str


class TestMirrorStructuredContent:
    async def test_default_mirrors_structured_content_into_content(self):
        """By default a structured result also carries a serialised content copy."""
        mcp = FastMCP()

        @mcp.tool
        def get_weather() -> Weather:
            return Weather(temperature=22.5, conditions="sunny")

        result = await mcp.call_tool("get_weather")
        assert result.structured_content == {
            "temperature": 22.5,
            "conditions": "sunny",
        }
        # The serialised mirror is present.
        assert result.content

    async def test_opt_out_sends_structured_content_only(self):
        """mirror_structured_content=False omits the serialised content copy."""
        mcp = FastMCP()

        @mcp.tool(mirror_structured_content=False)
        def get_weather() -> Weather:
            return Weather(temperature=22.5, conditions="sunny")

        result = await mcp.call_tool("get_weather")
        assert result.structured_content == {
            "temperature": 22.5,
            "conditions": "sunny",
        }
        # No duplicate serialised copy; structured_content is the only payload.
        assert result.content == []
