import logging

from capstone.backend.config import settings

def setup_logging():
    """Configure the logging system for the application."""
    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.FileHandler(settings.LOG_PATH),
            logging.StreamHandler()
        ]
    )

    # Suppress unwanted log messages from specific libraries
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logging.info("Logging initialized successfully.")