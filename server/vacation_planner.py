from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="HR Policy Blackout Days")


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

if __name__ == "__main__":
    mcp.run(transport="streamable-http")