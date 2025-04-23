from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from weather_workflow import WeatherWorkflow, get_weather_data
import multiprocessing

async def run_worker(worker_id: int):
    client = await Client.connect("localhost:7233")
    
    async with Worker(
        client,
        task_queue="weather-task-queue",
        workflows=[WeatherWorkflow],
        activities=[get_weather_data],
        identity=f"weather-worker-{worker_id}"
    ):
        print(f"Worker {worker_id} started, ctrl+c to exit")
        await asyncio.Future()  # run forever

async def main():
    # Create multiple workers
    num_workers = 3  # You can adjust this number based on your needs
    worker_tasks = [run_worker(i) for i in range(num_workers)]
    
    # Run all workers concurrently
    await asyncio.gather(*worker_tasks)

if __name__ == "__main__":
    # Set multiprocessing start method
    multiprocessing.set_start_method("spawn")
    asyncio.run(main())