import logging
from pathlib import Path


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Path(__file__).parent.parent / 'utils/bot.log'),
            logging.StreamHandler()
        ]
    )