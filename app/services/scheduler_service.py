from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.scheduler import run_scheduled_brief
from dotenv import load_dotenv
import logging
import os

# Load environment
load_dotenv()

#Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    try:
        topics = os.getenv("SCHEDULED_TOPICS", "daily news")
        tone = os.getenv("SCHEDULED_TONE", "neutral")
        brief_id = run_scheduled_brief(topics=topics, tone=tone)
        logger.info(f"[Scheduler Service] Generated brief with ID {brief_id}")
    except Exception as e:
        logger.error(f"[Scheduler Service] Failed to generate brief: {e}")

def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, "interval", hours=24)
    logger.info("[Scheduler Service] Scheduler started. Job will run every 24 hours.")
    scheduler.start()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Runs every day at 7:00am
    scheduler.add_job(job, CronTrigger(hour=7, minute=0), id="daily_brief_job")
    logger.info("🚀 Scheduler started - job will run daily at 7:00am")
    scheduler.start()
