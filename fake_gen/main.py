from src.fake_generator import fake
from src.event_model import Event
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('./.configs/config.ini')

def main(n: int = 100, n_users: int = 10, n_products: int = 5) -> list[Event]:
    """
    Main function to generate and print a fake event.
    """
    events = []
    for _ in range(n):
        events.append(fake.event(n_users, n_products))
    return events


if __name__ == "__main__":
    print(main(config.getint('variables', 'n'), config.getint('variables', 'n_users'), config.getint('variables', 'n_products')))
