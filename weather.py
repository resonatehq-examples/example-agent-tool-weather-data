from mcp.server.fastmcp import FastMCP
from resonate import Resonate
from datetime import date
import requests

mcp = FastMCP("weather")
resonate = Resonate.remote()

def make_nws_request(_, url):    
    headers = {
        "User-Agent": "weather-app/1.0",
        "Accept": "application/geo+json"
    }
    response = requests.get(url, headers=headers, timeout=30.0)
    response.raise_for_status()
    return response.json()


@resonate.register
def get_forecast_workflow(ctx, latitude, longitude):
    print(f"Fetching forecast for latitude: {latitude}, longitude: {longitude}")
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    points_data = yield ctx.lfc(make_nws_request, points_url)
    print(f"Points data: {points_data}")

    if not points_data:
        return "Unable to fetch forecast data for this location."

    print(f"fetching forecast from: {points_data['properties']['forecast']}")
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = yield ctx.lfc(make_nws_request, forecast_url)
    print(f"Forecast data: {forecast_data}")

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
        {period['name']}:
        Temperature: {period['temperature']}°{period['temperatureUnit']}
        Wind: {period['windSpeed']} {period['windDirection']}
        Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.tool()
def get_forecast(latitude, longitude):
    """Get the weather forecast for a location.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    
    Returns:
        A promise ID that can be used to retrieve the forecast later.
    """

    today = date.today()
    formatted_date = today.isoformat()
    promise_id = f"forecast-{latitude}-{longitude}-{formatted_date}"
    handle = get_forecast_workflow.run(promise_id, latitude, longitude)
    return {"promise_id": promise_id}


@mcp.tool()
def check_if_result_is_ready(promise_id):
    """Check if the result for a tool workflow is ready using a promise ID.
    Args:
        promise_id: The ID of the promise associated with the workflow invocation
    Returns:
        A boolean indicating whether the result is ready.
    """
    handle = resonate.get(promise_id)
    is_ready = handle.ready()
    return {"promise_id": promise_id, "is_ready": is_ready}


@mcp.tool()
def get_result(promise_id):
    """Get the result of a tool workflow invocation using a promise ID.
    
    Args:
        promise_id: The ID of the promise associated with the workflow invocation

    Returns:
        The result of the function associated with the promise ID.
    """
    handle = resonate.get(promise_id)
    result = handle.result()
    return result


if __name__ == "__main__":
    mcp.run(transport='stdio')