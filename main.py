from mcp.server.fastmcp import FastMCP
from typing import List
from functools import lru_cache

# Create an MCP server
mcp = FastMCP("LeaveManager")

# In memory mock database with 10 leaves days to start
employee_leaves = {
"E-1": {"balance": 7, "history": ["2025–12–25", "2026–03–01", "2026–04–21"]},
"E-2": {"balance": 9, "history": ["2026–11–06"]}

# cache leave balance for faster retrieval, with a max cache size of '5' entries
@lru_cache(maxsize=5)
def get_balance_cached(emp_id: str):
    return employee_leaves.get(emp_id)

# Tool: check leave balance
@mcp.tool()
async def get_leave_balance(emp_id: str) -> str:
    """get leave balance for employee"""
    data = get_balance_cached(emp_id)

    if data:
        return f"{emp_id} has {data['balance']} leave days remaining. Here is history of past leaves: {data['history']}"
    return "Employee ID not found."

# Tool: apply for leaves with specific dates
@mcp.tool()
async def apply_leave(emp_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g. ["2024-12-25", "2025-01-01"] )
    """
    if emp_id not in employee_leaves:
        return "Employee ID not found."
    requested_days = len(leave_dates)
    available_leaves = employee_leaves[emp_id]["balance"]

    if available_leaves < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} leave_days."

    # deduct balance and add to history
    employee_leaves[emp_id]["balance"] -= requested_days
    employee_leaves[emp_id]["history"].extend(leave_dates)
    return f"Leave applied for {requested_days} days. Remaining leaves: {employee_leaves[emp_id]['balance']}"

# Tool : get leave history
@mcp.tool()
async def get_employee_history(emp_id: str) -> str:
    data = employee_leaves.get(emp_id)
    if data:
        history = ', '.join(data["history"]) if data["history"] else "No leaves taken."
        return f"Leave history for {emp_id}: {history}"
    return "Employee ID not found."

# Add a greeting resource, data that can be read by clients(API or files)
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you?"

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

# Run with streamable HTTP transport:- this is when MCP server is deployed as separate HTTP service.
# e.g. transport="streamable-http" or (transport="http", host="0.0.0.0", port=8000)
# Run with 'stdio' transport instead when running as a local MCP Server
if __name__ == "__main__":
    mcp.run(transport="stdio")
