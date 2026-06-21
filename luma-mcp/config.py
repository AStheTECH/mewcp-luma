import logging

LUMA_API_BASE = "https://api.lumalabs.ai"
LUMA_API_VERSION = "dream-machine/v1"
API_TIMEOUT = 60


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
