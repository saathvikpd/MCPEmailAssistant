from utils import EmailAssistant
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EmailAssistant")

assistant = EmailAssistant()
mcp.add_tool(assistant.get_email_summary)
mcp.add_tool(assistant.get_top_matching_email)

if __name__ == "__main__":
    mcp.run()
