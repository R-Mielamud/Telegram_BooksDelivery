from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Base

BASE_DIR = Path(__file__).resolve().parent.parent

# Telegram Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

MANIFEST_PATH = BASE_DIR / "manifest.json"

# API

API_BASE_URL = "https://viberbksdlv.tk/api/"

API_KEY = os.environ.get("API_KEY", "abc")
