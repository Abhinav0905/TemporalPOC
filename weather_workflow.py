from datetime import timedelta
import logging
from temporalio import workflow, activity
from temporalio.common import RetryPolicy

@activity.defn
async def get_weather_data(city: str) -> dict:
    print(f"Getting weather data for {city}...")  # This will show in worker logs
    # Mock weather data for POC testing
    mock_weather_data = {
        "name": city,
        "main": {
            "temp": 20.5,
            "humidity": 65,
            "pressure": 1012
        },
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ]
    }
    print(f"Weather data retrieved for {city}: {mock_weather_data}")  # This will show in worker logs
    return mock_weather_data

@workflow.defn(name="WeatherWorkflow")
class WeatherWorkflow:
    @workflow.run
    async def run(self, city: str = "New York") -> dict:
        # Configure retry policy for the activity
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            maximum_attempts=3,
            non_retryable_error_types=["ValueError"]
        )
        
        # Log at workflow level
        workflow.logger.info(f"Starting weather check for {city}")
        
        result = await workflow.execute_activity(
            get_weather_data,
            city,
            retry_policy=retry_policy,
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        workflow.logger.info(f"Completed weather check for {city}")
        return result