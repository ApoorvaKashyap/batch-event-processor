from faker import Faker
from faker.providers import BaseProvider, DynamicProvider
from src.event_model import Event

fake = Faker()

# Event Attribute Providers:
EventTypeProvider = DynamicProvider(
    provider_name="event_type",
    elements=[
        "click",
        "signIn",
        "signOut",
        "formSubmit",
        "purchase",
        "addToCart",
        "removeFromCart",
        "videoPlay",
        "videoPause",
        "scroll",
        "search",
        "error",
        "exception",
        "profileUpdate",
        "registration",
        "newsletterSignup",
        "download",
    ],
)


class IDProvider(BaseProvider):
    def id_gen(self, type: str, n: int = 5) -> str:
        """
        Generate a random user ID.

        Returns:
            str: A randomly generated UUID string.
        """
        if type == "user":
            return "user" + "{0:03}".format(fake.random_int(min=1, max=n))
        elif type == "product":
            return "product" + "{0:03}".format(fake.random_int(min=1, max=n))
        else:
            raise ValueError("Invalid type specified. Use 'user' or 'product'.")


fake.add_provider(EventTypeProvider)
fake.add_provider(IDProvider)


class EventProvider(BaseProvider):
    def event(self, n_users, n_products) -> Event:
        """
        Generate a fake event with random attributes.

        Returns:
            Event: An instance of the Event class with randomly generated attributes.
        """
        timestamp = fake.date_time_this_year()
        userId = fake.id_gen("user", n_users)
        eventType = fake.event_type()
        productId = fake.id_gen("product", n_products)
        sessionDuration = fake.random_int(min=30, max=999)

        return Event(
            timestamp=timestamp,
            userId=userId,
            eventType=eventType,
            productId=productId,
            sessionDuration=sessionDuration,
        )


fake.add_provider(EventProvider)
