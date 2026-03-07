import logging
import sys
from mcp.server.fastmcp import FastMCP
from tools import register_tools

# Configure logging (stderr only)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)

logger = logging.getLogger("weather-mcp")

# Create MCP server instance
mcp = FastMCP("Weather MCP Server")

logger.info("Registering MCP tools...")
register_tools(mcp)

logger.info("Weather MCP Server starting (STDIO mode)...")

if __name__ == "__main__":
    mcp.run()