from fastmcp import FastMCP

# Create a proxy to a remote server
proxy = FastMCP.as_proxy(
    "http://localhost:5001/mcp",  # URL of the remote server
    name="Weather Data Server Proxy"
)


if __name__ == "__main__":
    proxy.run()  # Runs via STDIO for Claude Desktop