from src.fake_generator import fake
from src.event_model import Event


def main(n: int) -> list[Event]:
    """
    Main function to generate and print a fake event.
    """
    events = []
    for _ in range(n):
        events.append(fake.event())
    return events


if __name__ == "__main__":
    print(main(5))
