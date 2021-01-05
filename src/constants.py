from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Telegram Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

MANIFEST_PATH = BASE_DIR / "manifest.json"
