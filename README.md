# Weather forecast AI Agent tool | Resonate example application

TODO

## Claude config

```json
{
  "mcpServers": {
    "weather": {
      "command": "/opt/homebrew/bin/uv", // Path to where uv is
      "args": [
        "--directory",
        "ABSOLUTE/PATH/TO/TOOL/agent-tool-weather-forecast",
        "run",
        "weather.py"
      ]
    }
  }
}
```

## Run the proxy

`uv run proxy.py`

## Run the weather data MCP server

`uv run weather_data.py`
