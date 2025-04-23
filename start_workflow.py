from temporalio.client import Client, Schedule, ScheduleSpec, ScheduleActionStartWorkflow
from temporalio.common import RetryPolicy
import asyncio
from weather_workflow import WeatherWorkflow
from datetime import timedelta, datetime

async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    schedule_id = "weather-schedule"
    
    # Check if schedule already exists and delete it
    try:
        await client.delete_schedule(schedule_id)
        print(f"Deleted existing schedule: {schedule_id}")
    except:
        pass  # Schedule doesn't exist, which is fine

    # Create the schedule with action and spec using direct interval
    await client.create_schedule(
        schedule_id,
        Schedule(
            action=ScheduleActionStartWorkflow(
                workflow=WeatherWorkflow.run,
                args=["London"],
                task_queue="weather-task-queue",
                id=schedule_id  # Use schedule_id as workflow id for uniqueness
            ),
            spec=ScheduleSpec(
                cron_expressions=["*/1 * * * *"]  # Run every minute using cron expression
            )
        )
    )

    print(f"\nSchedule '{schedule_id}' created successfully!")
    print("Schedule details:")
    print("----------------")
    print(f"Interval: Every 1 minute")
    print(f"Workflow: WeatherWorkflow")
    print(f"City: London")
    print("\nMonitoring schedule executions...")
    print("(Press Ctrl+C to stop)\n")

    try:
        count = 0
        while True:
            await asyncio.sleep(60)
            count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] Schedule has been running for {count} minute(s)")
    except KeyboardInterrupt:
        print("\nShutting down schedule monitoring...")

if __name__ == "__main__":
    asyncio.run(main())