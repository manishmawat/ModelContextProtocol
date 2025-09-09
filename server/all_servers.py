"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""
from fastmcp import FastMCP, Context
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

# Create an MCP server
mcp = FastMCP("All MCP Server tools")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

@mcp.tool()
async def blackout_days() -> dict:
    """Return a list of company blackout days."""
    return {
        "blackout_days": [
            "2025-12-25",  # Christmas
            "2025-01-01",  # New Year's Day
            "2025-07-04",  # Independence Day
            "2025-11-28",  # Company Anniversary
            "2025-11-29",  # Day after Company Anniversary
            "2025-12-11",  # Year-end Inventory
        ]
    }

@mcp.tool()
async def hr_vacation_policy() -> str:
    """Return the company's vacation policy."""
    return (
        "Our company vacation policy allows employees to take up to 20 days of paid vacation per year. "
        "Vacation requests should be submitted at least 2 weeks in advance and are subject to manager approval. "
        "Please avoid scheduling vacations during blackout days."
    )

@mcp.tool()
async def employee_workplan() -> dict:
    """Return a sample employee work plan and project assignments for the current year."""
    return {
        "work_plan": {
            "employee_id": "E12345",
            "name": "John Doe",
            "position": "Software Engineer",
            "department": "Engineering",
            "vacation_days_taken": 5,
            "vacation_days_remaining": 15,
            "upcoming_vacations": [
                {"start_date": "2025-06-15", "end_date": "2025-06-20"},
                {"start_date": "2025-09-01", "end_date": "2025-09-05"},
            ],
            "work_plan_year":[
                {"project": "Project Alpha", "start_date": "2025-01-10", "end_date": "2025-04-30"},
                {"project": "Project Beta", "start_date": "2025-05-01", "end_date": "2025-08-31"},
                {"project": "Project Gamma", "start_date": "2025-09-01", "end_date": "2025-12-31"},
            ]
        }
    }

class BookingPreferences(BaseModel):
    """Schema for collecting user preferences."""

    checkAlternative: bool = Field(description="Would you like to check another date?")
    alternativeDate: str = Field(
        default="2024-12-26",
        description="Alternative date (YYYY-MM-DD)",
    )


@mcp.tool()
async def book_table_elicitation(date: str, time: str, party_size: int, ctx: Context) -> str:
    """Book a table with date availability check."""
    # Check if date is available
    if date == "2024-12-25":
        # Date unavailable - ask user for alternative
        result = await ctx.elicit(
            message=(f"No tables available for {party_size} on {date}. Would you like to try another date?"),
            schema=BookingPreferences,
        )

        if result.action == "accept" and result.data:
            if result.data.checkAlternative:
                return f"[SUCCESS] Booked for {result.data.alternativeDate}"
            return "[CANCELLED] No booking made"
        return "[CANCELLED] Booking cancelled"

    # Date available
    return f"[SUCCESS] Booked for {date} at {time}"

import asyncio

if __name__ == "__main__":
    asyncio.run(mcp.run(transport="http", host="0.0.0.0", port=8000))