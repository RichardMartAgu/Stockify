import logging
from logging.handlers import TimedRotatingFileHandler
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Logger configuration
logger = logging.getLogger("stockify")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Daily rotating file handler with date in the filename
daily_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, "stockify"),
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
    utc=False
)

daily_handler.suffix = "%Y-%m-%d.log"

daily_handler.setFormatter(formatter)
daily_handler.setLevel(logging.INFO)

# Console handler to also show logs in the terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# Add both handlers to the logger
logger.addHandler(daily_handler)
logger.addHandler(console_handler)
