from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.runtime import Runtime
import asyncio
from weather_workflow import WeatherWorkflow, get_weather_data

async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Run the worker
    async with Worker(
        client,
        task_queue="weather-task-queue",
        workflows=[WeatherWorkflow],
        activities=[get_weather_data],
    ):
        print("Worker started, ctrl+c to exit")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())