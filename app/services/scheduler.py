import argparse
import logging
from datetime import datetime
from app.services.brief_generator import fetch_brief_from_openai
from app.db.crud import insert_brief


VALID_TONES = ["neutral","casual","professional"]
# Default config (you could move these to .env later)
DEFAULT_TOPICS = "Technology trends"
DEFAULT_TONE = "concise"

def run_scheduled_brief(topics: str, tone: str = "netural") -> int:
    prompt = f"Write a daily brief on: {topics}, in a {tone} tone."
    content = fetch_brief_from_openai(prompt)
    created_at = datetime.utcnow().isoformat()
    brief_id = insert_brief(topics, tone, content, created_at)
    logging.info(f"[Scheduler] Brief generated automatically with ID {brief_id}")
    return brief_id

# Allow manual execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the AI brief scheduler manually.")

    parser.add_argument(
                        "--topics",
                        required=True,
                         type=str,
                         help="Topics for the AI brief (required)")
    
    parser.add_argument(
                        "--tone",
                        type=str, 
                        default="neutral",
                        choices=VALID_TONES,
                        help=f"Tone of the brief (choices: {', '.join(VALID_TONES)})")

    args = parser.parse_args()
    run_scheduled_brief(topics=args.topics, tone=args.tone)
