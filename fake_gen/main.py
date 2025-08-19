from src.fake_generator import fake
from src.event_model import Event
from configparser import ConfigParser
import logging


# Configure Logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Load configuration
config = ConfigParser()
config.read("./.configs/config.ini")


def main(n: int = 100, n_users: int = 10, n_products: int = 5) -> list[Event]:
    """
    Main function to generate and print a fake event.
    """
    events = []
    for _ in range(n):
        events.append(fake.event(n_users, n_products))
    return events


if __name__ == "__main__":
    try:
        with open(config["variables"]["out_path"], "w") as f:
            n = config.getint("variables", "n")
            n_users = config.getint("variables", "n_users")
            n_products = config.getint("variables", "n_products")
            events = main(n, n_users, n_products)
            for event in events:
                f.write(event.json() + "\n")
            logging.info(
                f"Generated {n} events with {n_users} users and {n_products} products."
            )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
