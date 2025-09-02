from mcp.server import FastMCP

from izzy_mcp_tutorials import FlightsDataAccessObject

# Create the Flights MCP server
mcp = FastMCP("Flights MCP Service")
dao = FlightsDataAccessObject()

@mcp.tool()
def get_available_dates():
    """Returns a list of dates available for search"""
    return dao.get_available_dates()


@mcp.resource("passport://passport-owner/{passport_id}")
def get_passport_owner(passport_id: str):
    """Returns details about the passport owner"""
    return dao.get_passport_owner(passport_id=passport_id)


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